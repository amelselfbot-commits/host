# host_registry.py
"""
مدیریت هاست‌های سلف از دیدگاه هاست اصلی.

این ماژول دو چیز رو نگه می‌داره:
  ۱. لیست هاست‌های سلفی که تا حالا خودشونو معرفی (register) کردن
     (جدول amel_hosts)
  ۲. این‌که هر کاربر (owner_id) به کدوم هاست تخصیص داده شده
     (جدول amel_host_assignments)

هاست اصلی هیچ سلفی رو خودش اجرا نمی‌کنه؛ فقط تصمیم می‌گیره هر کاربر
مال کدوم هاست باشه و از طریق API داخلی (host_api.py) این اطلاعات رو
در اختیار هاست‌های سلف می‌ذاره.
"""
import time
import secrets
from typing import Optional, List, Dict

import database_supabase as db


def init_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS amel_hosts (
            host_id TEXT PRIMARY KEY,
            name TEXT DEFAULT '',
            secret TEXT NOT NULL,
            capacity INTEGER DEFAULT 200,
            base_url TEXT DEFAULT '',
            last_heartbeat TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS amel_host_assignments (
            owner_id INTEGER PRIMARY KEY,
            host_id TEXT NOT NULL REFERENCES amel_hosts(host_id) ON DELETE CASCADE,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
    ]
    for q in queries:
        try:
            db.execute_query(q)
        except Exception as e:
            print(f"⚠️ host_registry.init_tables error: {e}")
    print("✅ جداول amel_hosts / amel_host_assignments بررسی/ایجاد شدند")


def register_host(host_id: str, name: str = "", capacity: int = 200, base_url: str = "") -> str:
    """هاست سلف با این تابع خودشو معرفی می‌کنه و یه secret می‌گیره که
    باید توی همه‌ی درخواست‌های بعدیش (هدر X-Internal-Secret) بفرسته."""
    existing = db.execute_query(
        "SELECT secret FROM amel_hosts WHERE host_id = %s", (host_id,), fetch_one=True
    )
    if existing:
        db.execute_query(
            "UPDATE amel_hosts SET name = %s, capacity = %s, base_url = %s, last_heartbeat = NOW() WHERE host_id = %s",
            (name, capacity, base_url, host_id),
        )
        return existing["secret"]

    secret = secrets.token_hex(24)
    db.execute_query(
        """INSERT INTO amel_hosts (host_id, name, secret, capacity, base_url, last_heartbeat)
           VALUES (%s, %s, %s, %s, %s, NOW())""",
        (host_id, name, secret, capacity, base_url),
    )
    return secret


def get_host_url(host_id: str) -> Optional[str]:
    row = db.execute_query(
        "SELECT base_url FROM amel_hosts WHERE host_id = %s", (host_id,), fetch_one=True
    )
    return (row["base_url"] or None) if row else None


def verify_host_secret(host_id: str, secret: str) -> bool:
    row = db.execute_query(
        "SELECT secret FROM amel_hosts WHERE host_id = %s", (host_id,), fetch_one=True
    )
    return bool(row) and row["secret"] == secret


def touch_heartbeat(host_id: str):
    db.execute_query(
        "UPDATE amel_hosts SET last_heartbeat = NOW() WHERE host_id = %s", (host_id,)
    )


def list_hosts() -> List[Dict]:
    rows = db.execute_query("SELECT * FROM amel_hosts", fetch_all=True) or []
    return [dict(r) for r in rows]


def get_host_of_user(owner_id: int) -> Optional[str]:
    row = db.execute_query(
        "SELECT host_id FROM amel_host_assignments WHERE owner_id = %s",
        (owner_id,), fetch_one=True,
    )
    return row["host_id"] if row else None


def get_assigned_users(host_id: str) -> List[int]:
    rows = db.execute_query(
        "SELECT owner_id FROM amel_host_assignments WHERE host_id = %s",
        (host_id,), fetch_all=True,
    ) or []
    return [r["owner_id"] for r in rows]


def _least_loaded_host() -> Optional[str]:
    hosts = list_hosts()
    if not hosts:
        return None
    counts = db.execute_query(
        "SELECT host_id, COUNT(*) AS c FROM amel_host_assignments GROUP BY host_id",
        fetch_all=True,
    ) or []
    load = {row["host_id"]: row["c"] for row in counts}
    hosts.sort(key=lambda h: load.get(h["host_id"], 0))
    for h in hosts:
        if load.get(h["host_id"], 0) < h["capacity"]:
            return h["host_id"]
    return hosts[0]["host_id"] if hosts else None


def assign_user_to_host(owner_id: int, host_id: Optional[str] = None) -> Optional[str]:
    """یه کاربر رو به یه هاست تخصیص می‌ده. اگه host_id ندی، کم‌بارترین
    هاست موجود به‌صورت خودکار انتخاب می‌شه (round-robin ساده بر اساس بار)."""
    target = host_id or _least_loaded_host()
    if not target:
        return None
    db.execute_query(
        """INSERT INTO amel_host_assignments (owner_id, host_id, assigned_at)
           VALUES (%s, %s, NOW())
           ON CONFLICT (owner_id) DO UPDATE SET host_id = EXCLUDED.host_id""",
        (owner_id, target),
    )
    return target


def unassign_user(owner_id: int):
    db.execute_query("DELETE FROM amel_host_assignments WHERE owner_id = %s", (owner_id,))
