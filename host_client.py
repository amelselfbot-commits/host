# host_client.py
"""
کلاینتِ سمتِ هاست سلف برای صحبت با API داخلیِ هاست اصلی
(همون host_api.py که سمت هاست اصلیه).

استفاده:
    import host_client as hc
    hc.register()                 # یه‌بار موقع بالا اومدن
    owner_ids = hc.get_assigned_users()
    hc.send_heartbeat(running=[...])
"""
import requests

import config

_secret = None


def register() -> str:
    """این هاست رو به هاست اصلی معرفی می‌کنه و secret اختصاصیش رو می‌گیره."""
    global _secret
    resp = requests.post(
        f"{config.MAIN_HOST_URL}/internal/hosts/register",
        json={
            "host_id": config.HOST_ID,
            "name": config.HOST_NAME,
            "capacity": config.HOST_CAPACITY,
            "base_url": config.SELF_HOST_PUBLIC_URL,
        },
        headers={"X-Register-Key": config.INTERNAL_REGISTER_KEY},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"register failed: {data}")
    _secret = data["secret"]
    return _secret


def _headers():
    if not _secret:
        register()
    return {"X-Internal-Secret": _secret}


def get_assigned_users() -> list:
    resp = requests.get(
        f"{config.MAIN_HOST_URL}/internal/hosts/{config.HOST_ID}/assigned_users",
        headers=_headers(),
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"assigned_users failed: {data}")
    return data["owner_ids"]


def send_heartbeat(running: list) -> None:
    requests.post(
        f"{config.MAIN_HOST_URL}/internal/hosts/{config.HOST_ID}/heartbeat",
        json={"running": running},
        headers=_headers(),
        timeout=15,
    )
