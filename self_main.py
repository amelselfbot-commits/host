# self_main.py
"""
نقطه‌ی ورودِ هاست سلف.

این هاست خودش هیچ ربات ثبت‌نامی/پنلی نداره؛ فقط:
  ۱. خودشو به هاست اصلی معرفی می‌کنه (host_client.register)
  ۲. هر چند ثانیه یه‌بار (POLL_INTERVAL_SECONDS) لیست کاربرهایی که هاست
     اصلی بهش تخصیص داده رو می‌گیره (host_client.get_assigned_users)
  ۳. دستورهای start/stop معلق برای همون کاربرها رو از دیتابیس می‌خونه
     و روی bot_manager محلی اجرا می‌کنه (remote_control)
  ۴. وضعیت هر سلف (روشن/خاموش/pause) رو گزارش می‌ده
  ۵. کاربرهایی که دیگه مال این هاست نیستن (تخصیص عوض شده) رو متوقف می‌کنه

برای اجرا: python self_main.py
"""
import time

import config
import database as db
import host_client as hc
import remote_control as rc
from bot import bot_manager
from loop_manager import get_loop


def _apply_commands(owner_ids):
    for cmd in rc.fetch_pending_commands(owner_ids):
        oid = cmd["owner_id"]
        try:
            if cmd["command"] == "start":
                bot_manager.start(
                    oid, get_loop(),
                    check_tokens=cmd.get("check_tokens", False),
                    is_restart=cmd.get("is_restart", False),
                )
            elif cmd["command"] == "stop":
                bot_manager.stop(oid)
        except Exception as e:
            print(f"⚠️ خطا در اجرای دستور {cmd['command']} برای {oid}: {e}")
        finally:
            rc.mark_consumed(cmd["id"])


def _report_all(owner_ids):
    for oid in owner_ids:
        try:
            running = bot_manager.is_running(oid)
            paused = bot_manager.is_paused(oid)
            rc.report_status(oid, config.HOST_ID, running, paused)
        except Exception as e:
            print(f"⚠️ خطا در گزارش وضعیت {oid}: {e}")


def _stop_unassigned(previous_assigned, current_assigned):
    removed = set(previous_assigned) - set(current_assigned)
    for oid in removed:
        try:
            if bot_manager.is_running(oid):
                print(f"↪️ کاربر {oid} دیگه مال این هاست نیست — متوقف می‌شه")
                bot_manager.stop(oid)
        except Exception as e:
            print(f"⚠️ خطا در توقفِ کاربرِ منتقل‌شده {oid}: {e}")


def poll_loop():
    previous_assigned = []
    while True:
        try:
            owner_ids = hc.get_assigned_users()
            _stop_unassigned(previous_assigned, owner_ids)
            _apply_commands(owner_ids)
            _report_all(owner_ids)
            hc.send_heartbeat(running=[oid for oid in owner_ids if bot_manager.is_running(oid)])
            previous_assigned = owner_ids
        except Exception as e:
            print(f"⚠️ خطا در حلقه‌ی poll هاست سلف: {e}")
        time.sleep(config.POLL_INTERVAL_SECONDS)


def main():
    if not config.HOST_ID:
        raise SystemExit("❌ متغیر محیطی HOST_ID ست نشده — هر هاست سلف باید یه شناسه‌ی یکتا داشته باشه.")

    print(f"🚀 هاست سلف «{config.HOST_ID}» در حال اتصال به هاست اصلی: {config.MAIN_HOST_URL}")
    hc.register()
    print("✅ ثبت‌نام هاست انجام شد. شروع حلقه‌ی poll ...")

    from heartbeat import get_heartbeat_manager
    hb = get_heartbeat_manager()
    hb.start()

    from panel_server import start_panel_server_background
    start_panel_server_background()
    print(f"✅ سرور HTTPِ این هاست روی پورتِ محیطی (یا {config.PANEL_API_PORT}) بالا اومد.")

    poll_loop()


if __name__ == "__main__":
    main()
