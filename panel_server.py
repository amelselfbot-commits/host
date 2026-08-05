# panel_server.py
"""
یه سرورِ Flask خیلی سبک، فقط برای این‌که panel_api.py (که کارهای پنل دکمه‌ای
رو انجام می‌ده و به کلاینتِ زنده‌ی سلف نیاز داره) از بیرون — یعنی از طرفِ
ربات کمکی روی هاست اصلی — در دسترس باشه.

این سرور جدا از self_main.py توی یه ترد پس‌زمینه اجرا می‌شه تا حلقه‌ی
poll (اتصال به هاست اصلی) رو مسدود نکنه.
"""
import threading

from flask import Flask

from panel_api import panel_api_bp
import config


def run_panel_server():
    if not config.PANEL_API_SECRET:
        print("⚠️ PANEL_API_SECRET ست نشده — سرور پنل داخلی بدون این مقدار غیرفعال می‌مونه "
              "و همه‌ی درخواست‌ها 401 می‌گیرن. برای فعال‌سازیِ پنل دکمه‌ای این متغیر رو ست کن.")

    app = Flask(__name__)
    app.register_blueprint(panel_api_bp)
    # threaded=True چون هر درخواست ممکنه منتظرِ یه کوروتینِ روی event loop
    # اصلی بمونه (از طریق run_coroutine_threadsafe در panel_api._run_coro)
    app.run(host="0.0.0.0", port=config.PANEL_API_PORT, threaded=True, use_reloader=False)


def start_panel_server_background():
    t = threading.Thread(target=run_panel_server, daemon=True)
    t.start()
    return t
