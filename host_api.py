# host_api.py
"""
API داخلی هاست اصلی — فقط برای مصرف هاست‌های سلف، نه کاربر نهایی.

مسیرها:
  POST /internal/hosts/register
      body: {"host_id": "...", "name": "...", "capacity": 200}
      -> {"secret": "..."}   (فقط بار اول یا اگه هاست از قبل ثبت نشده، ست می‌شه)

  GET  /internal/hosts/<host_id>/assigned_users
      هدر: X-Internal-Secret: <secret>
      -> {"owner_ids": [123, 456, ...]}

  POST /internal/hosts/<host_id>/heartbeat
      هدر: X-Internal-Secret: <secret>
      body: {"running": [123, 456]}   (owner_id هایی که هم‌اکنون روشنن)
      -> {"ok": true}

این بلوپرینت داخل app.py با app.register_blueprint(host_api_bp) وصل می‌شه.
یه INTERNAL_REGISTER_KEY هم توی config هست که فقط برای مرحله‌ی register
اولیه لازمه (تا هرکسی نتونه هاست جعلی معرفی کنه).
"""
from flask import Blueprint, request, jsonify

import config
import host_registry as hr

host_api_bp = Blueprint("host_api", __name__, url_prefix="/internal/hosts")


def _check_register_key():
    key = request.headers.get("X-Register-Key", "")
    return key and key == config.INTERNAL_REGISTER_KEY


def _check_host_secret(host_id: str) -> bool:
    secret = request.headers.get("X-Internal-Secret", "")
    return bool(secret) and hr.verify_host_secret(host_id, secret)


@host_api_bp.route("/register", methods=["POST"])
def register():
    if not _check_register_key():
        return jsonify({"ok": False, "error": "کلید ثبت‌نام هاست نامعتبره"}), 403

    data = request.get_json(force=True, silent=True) or {}
    host_id = data.get("host_id")
    if not host_id:
        return jsonify({"ok": False, "error": "host_id لازمه"}), 400

    secret = hr.register_host(
        host_id=host_id,
        name=data.get("name", ""),
        capacity=int(data.get("capacity", 200)),
        base_url=data.get("base_url", ""),
    )
    return jsonify({"ok": True, "secret": secret})


@host_api_bp.route("/<host_id>/assigned_users", methods=["GET"])
def assigned_users(host_id):
    if not _check_host_secret(host_id):
        return jsonify({"ok": False, "error": "دسترسی غیرمجاز"}), 403

    hr.touch_heartbeat(host_id)
    owner_ids = hr.get_assigned_users(host_id)
    return jsonify({"ok": True, "owner_ids": owner_ids})


@host_api_bp.route("/<host_id>/heartbeat", methods=["POST"])
def heartbeat(host_id):
    if not _check_host_secret(host_id):
        return jsonify({"ok": False, "error": "دسترسی غیرمجاز"}), 403

    hr.touch_heartbeat(host_id)
    return jsonify({"ok": True})
