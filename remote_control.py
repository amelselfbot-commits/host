# remote_control.py
"""
طرفِ هاست سلف برای دستورهای start/stop که هاست اصلی توی amel_bot_commands
ثبت می‌کنه، و گزارشِ وضعیت هر سلف توی amel_bot_status.

این ماژول مستقیم به همون Supabase مشترک وصل می‌شه (نه از طریق HTTP) چون
داده‌های سشن/تنظیمات هر کاربر هم از همین‌جا خونده می‌شن؛ فقط «کدوم کاربرها
مال این هاستن» از طریق API داخلی (host_client.py) گرفته می‌شه.
"""
from typing import List, Dict

import database_supabase as db


def fetch_pending_commands(owner_ids: List[int]) -> List[Dict]:
    if not owner_ids:
        return []
    placeholders = ",".join(["%s"] * len(owner_ids))
    rows = db.execute_query(
        f"""SELECT * FROM amel_bot_commands
            WHERE owner_id IN ({placeholders}) AND consumed = FALSE
            ORDER BY created_at ASC""",
        tuple(owner_ids),
        fetch_all=True,
    ) or []
    return [dict(r) for r in rows]


def mark_consumed(command_id: int):
    db.execute_query(
        "UPDATE amel_bot_commands SET consumed = TRUE WHERE id = %s", (command_id,)
    )


def report_status(owner_id: int, host_id: str, running: bool, paused: bool):
    db.execute_query(
        """INSERT INTO amel_bot_status (owner_id, host_id, running, paused, updated_at)
           VALUES (%s, %s, %s, %s, NOW())
           ON CONFLICT (owner_id) DO UPDATE
           SET host_id = EXCLUDED.host_id, running = EXCLUDED.running,
               paused = EXCLUDED.paused, updated_at = EXCLUDED.updated_at""",
        (owner_id, host_id, running, paused),
    )
