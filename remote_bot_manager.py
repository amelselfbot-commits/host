# remote_bot_manager.py
"""
جایگزینِ bot_manager روی هاست اصلی.

قبلاً main.py / telegram_bot.py / helper_bot.py / panel_api.py مستقیماً
bot.py (که کلاینت واقعی Telethon رو نگه می‌داشت) رو صدا می‌زدن. حالا که
اجرای واقعیِ سلف‌ها رفته روی هاست(های) سلف، این ماژول همون اینترفیس رو
(start/stop/is_running/is_paused/get_owner_by_tg_id) شبیه‌سازی می‌کنه، ولی
به‌جای صدا زدن مستقیم Telethon، توی دیتابیس مشترک یه «دستور» ثبت می‌کنه یا
آخرین «وضعیت» گزارش‌شده از هاست سلف رو می‌خونه.

جریان کار:
  ۱. هاست اصلی start(oid)/stop(oid) صدا می‌زنه → یه ردیف توی amel_bot_commands
     ثبت می‌شه.
  ۲. هاست سلفی که این کاربر بهش تخصیص داده شده (host_registry) هر چند
     ثانیه یه‌بار دستورهای مصرف‌نشده‌ی خودش رو می‌خونه (از طریق API داخلی)
     و روی bot_manager محلیِ خودش اجرا می‌کنه.
  ۳. هاست سلف نتیجه/وضعیت رو توی amel_bot_status می‌نویسه.
  ۴. is_running/is_paused این‌جا همون وضعیتِ گزارش‌شده رو می‌خونن.

⚠️ محدودیت مهم: get_client(owner_id) دیگه نمی‌تونه یه شیء TelegramClient
واقعی برگردونه، چون کلاینت روی یه پردازه/سرور دیگه زنده‌ست. جاهایی از کد
(مثل panel_api.py) که مستقیم از get_client() برای گرفتن پیام/اطلاعات
لحظه‌ای استفاده می‌کردن، باید بعداً به یه اکشن ریموتِ جدید (از طریق API
داخلی، مشابه دستورهای start/stop) تبدیل بشن؛ این تابع فعلاً None برمی‌گردونه
و یه هشدار چاپ می‌کنه تا این نقاط راحت پیدا بشن.
"""
import time
from typing import Optional, Tuple

import database_supabase as db
import host_registry as hr


def init_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS amel_bot_commands (
            id SERIAL PRIMARY KEY,
            owner_id INTEGER NOT NULL,
            command TEXT NOT NULL,          -- 'start' | 'stop'
            check_tokens BOOLEAN DEFAULT FALSE,
            is_restart BOOLEAN DEFAULT FALSE,
            consumed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS amel_bot_status (
            owner_id INTEGER PRIMARY KEY,
            host_id TEXT,
            running BOOLEAN DEFAULT FALSE,
            paused BOOLEAN DEFAULT FALSE,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
    ]
    for q in queries:
        try:
            db.execute_query(q)
        except Exception as e:
            print(f"⚠️ remote_bot_manager.init_tables error: {e}")
    print("✅ جداول amel_bot_commands / amel_bot_status بررسی/ایجاد شدند")


class RemoteBotManager:
    def start(self, owner_id: int, loop=None, check_tokens: bool = False, is_restart: bool = False) -> bool:
        # اگه کاربر هنوز به هیچ هاستی تخصیص داده نشده، الان تخصیص بده
        if not hr.get_host_of_user(owner_id):
            hr.assign_user_to_host(owner_id)

        db.execute_query(
            """INSERT INTO amel_bot_commands (owner_id, command, check_tokens, is_restart)
               VALUES (%s, 'start', %s, %s)""",
            (owner_id, check_tokens, is_restart),
        )
        return True

    def stop(self, owner_id: int) -> None:
        db.execute_query(
            "INSERT INTO amel_bot_commands (owner_id, command) VALUES (%s, 'stop')",
            (owner_id,),
        )

    def is_running(self, owner_id: int) -> bool:
        row = db.execute_query(
            "SELECT running FROM amel_bot_status WHERE owner_id = %s", (owner_id,), fetch_one=True
        )
        return bool(row and row["running"])

    def is_paused(self, owner_id: int) -> bool:
        row = db.execute_query(
            "SELECT paused FROM amel_bot_status WHERE owner_id = %s", (owner_id,), fetch_one=True
        )
        return bool(row and row["paused"])

    def get_client(self, owner_id: int):
        print(f"⚠️ remote_bot_manager.get_client({owner_id}): کلاینت واقعی روی هاست اصلی در دسترس نیست "
              f"— این نقطه از کد باید به یه اکشن ریموت جدید تبدیل بشه.")
        return None

    def get_owner_by_tg_id(self, tg_id: int) -> Tuple[Optional[int], Optional[dict]]:
        account = db.get_account_by_tg_id(tg_id) if hasattr(db, "get_account_by_tg_id") else None
        if not account:
            return None, None
        return account.get("owner_id") or account.get("id"), account


bot_manager = RemoteBotManager()
