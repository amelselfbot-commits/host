# host_server.py
"""
سرورِ HTTP هاست اصلی — فقط API داخلیِ هاست‌های سلف (host_api.py) رو سرو
می‌کنه. main.py این رو توی یه ترد پس‌زمینه اجرا می‌کنه، هم برای اینکه
Render/Railway و مشابهش یه پورتِ باز ببینن (لازمه‌ی Web Service بودن)،
هم برای اینکه هاست‌های سلف واقعاً بتونن بهش وصل بشن.

روی Render، پورت رو از متغیر محیطیِ PORT می‌گیره (همونی که خودِ Render
موقعِ ساختِ سرویس ست می‌کنه) — پس نیازی نیست دستی چیزی براش بذاری.
"""
import os
import threading

from flask import Flask, jsonify

from host_api import host_api_bp


def _create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(host_api_bp)

    @app.route("/")
    def _health():
        # صرفاً برای health-check سرویس‌های هاستینگ (Render و مشابهش)
        return jsonify({"ok": True, "service": "main-host"})

    return app


def run_host_server():
    app = _create_app()
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)


def start_host_server_background():
    t = threading.Thread(target=run_host_server, daemon=True)
    t.start()
    return t
