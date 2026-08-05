# panel_server.py
"""
یه سرورِ Flask خیلی سبک، فقط برای این‌که panel_api.py (که کارهای پنل دکمه‌ای
رو انجام می‌ده و به کلاینتِ زنده‌ی سلف نیاز داره) از بیرون — یعنی از طرفِ
ربات کمکی روی هاست اصلی — در دسترس باشه.

این سرور جدا از self_main.py توی یه ترد پس‌زمینه اجرا می‌شه تا حلقه‌ی
poll (اتصال به هاست اصلی) رو مسدود نکنه.
"""
import os
import threading

from flask import Flask, jsonify

from panel_api import panel_api_bp
import config


def _create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def _health():
        return jsonify({"ok": True, "service": "self-host", "host_id": config.HOST_ID})

    if config.PANEL_API_SECRET:
        app.register_blueprint(panel_api_bp)
    else:
        print("⚠️ PANEL_API_SECRET ست نشده — مسیرهای پنل (/internal/panel/...) رجیستر نشدن؛ "
              "فقط health-check در دسترسه. برای فعال‌سازیِ پنل دکمه‌ای این متغیر رو ست کن.")

    return app


def run_panel_server():
    app = _create_app()
    # روی Render (و مشابهش) خودِ پلتفرم متغیرِ PORT رو ست می‌کنه و سرویس
    # باید دقیقاً همون پورت رو گوش بده؛ اگه PORT ست نشده بود (مثلاً اجرای
    # محلی)، از PANEL_API_PORT توی config استفاده می‌کنیم.
    port = int(os.environ.get("PORT", config.PANEL_API_PORT))
    # threaded=True چون هر درخواست ممکنه منتظرِ یه کوروتینِ روی event loop
    # اصلی بمونه (از طریق run_coroutine_threadsafe در panel_api._run_coro)
    app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)


def start_panel_server_background():
    t = threading.Thread(target=run_panel_server, daemon=True)
    t.start()
    return t
