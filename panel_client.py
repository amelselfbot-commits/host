# panel_client.py
"""
طرفِ هاست اصلی برای صحبت با panel_api.py که روی هاستِ سلفِ صاحبِ هر کاربر
اجرا می‌شه. helper_bot.py از این ماژول استفاده می‌کنه تا دیگه مجبور نباشه
مستقیم از bot.py (که الان روی یه پردازه/سرور دیگه‌ست) چیزی import کنه.

نکته: PANEL_CATEGORIES (ساختار ثابتِ منوها) مستقل از کاربره، پس با
get_categories() از *هر* هاستِ سلفِ آنلاینی گرفته و کش می‌شه — نیازی نیست
بدونیم دقیقاً صاحبِ کدوم کاربره.
"""
from typing import Optional, List, Dict, Tuple

import requests

import config
import host_registry as hr

_categories_cache = None  # {"order": [...], "categories": {...}}


def _headers():
    return {"X-Panel-Secret": config.PANEL_API_SECRET}


def _host_url_for(owner_id: int) -> Optional[str]:
    host_id = hr.get_host_of_user(owner_id)
    if not host_id:
        return None
    return hr.get_host_url(host_id)


def _any_host_url() -> Optional[str]:
    for h in hr.list_hosts():
        if h.get("base_url"):
            return h["base_url"]
    return None


def get_categories(force_refresh: bool = False) -> Optional[Dict]:
    """ساختار PANEL_CATEGORIES + ترتیب رو از یه هاست سلفِ آنلاین می‌گیره و کش می‌کنه."""
    global _categories_cache
    if _categories_cache is not None and not force_refresh:
        return _categories_cache

    base_url = _any_host_url()
    if not base_url:
        return None
    try:
        resp = requests.get(f"{base_url}/internal/panel/categories", headers=_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("ok"):
            _categories_cache = {"order": data["order"], "categories": data["categories"]}
            return _categories_cache
    except Exception as e:
        print(f"⚠️ panel_client.get_categories خطا: {e}")
    return None


def get_category_commands(owner_id: int, category_key: str) -> Optional[List]:
    base_url = _host_url_for(owner_id)
    if not base_url:
        return None
    try:
        resp = requests.post(
            f"{base_url}/internal/panel/category_commands",
            json={"owner_id": owner_id, "category_key": category_key},
            headers=_headers(), timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("items") if data.get("ok") else None
    except Exception as e:
        print(f"⚠️ panel_client.get_category_commands خطا: {e}")
        return None


def execute(owner_id: int, command_text: str) -> bool:
    base_url = _host_url_for(owner_id)
    if not base_url:
        return False
    try:
        resp = requests.post(
            f"{base_url}/internal/panel/execute",
            json={"owner_id": owner_id, "command_text": command_text},
            headers=_headers(), timeout=30,
        )
        resp.raise_for_status()
        return bool(resp.json().get("ok"))
    except Exception as e:
        print(f"⚠️ panel_client.execute خطا: {e}")
        return False


def force_join_info(owner_id: int) -> Tuple[Optional[str], Optional[List]]:
    base_url = _host_url_for(owner_id)
    if not base_url:
        return None, None
    try:
        resp = requests.post(
            f"{base_url}/internal/panel/force_join_info",
            json={"owner_id": owner_id},
            headers=_headers(), timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("ok"):
            return data.get("message"), data.get("channels")
    except Exception as e:
        print(f"⚠️ panel_client.force_join_info خطا: {e}")
    return None, None
