# -*- coding: utf-8 -*-
"""
کش سبک برای مسیرِ فایلِ بنرِ پنل (عکس پروفایل + قاب self panel) که سلف
(cl) قبل از زدنِ inline query می‌سازه. بات کمکی (helper_bot) موقعِ جواب
دادن به inline query این مسیر رو از اینجا می‌خونه تا بتونه همون عکس رو
به‌عنوانِ خودِ پیامِ پنل (همراه با دکمه‌ها) بفرسته - یعنی دیگه لازم نیست
عکس جدا و پیامِ دکمه‌دار جدا ارسال بشه.

چون فایل از قبل روی دیسک آماده‌ست (نه این‌که هلپر بات خودش دانلود/تولیدش
کنه)، فقط یک آپلودِ ساده لازمه و مشکلِ قبلیِ تایم‌اوتِ پاسخِ inline query
(که به‌خاطرِ دانلودِ عکسِ پروفایل + آپلودِ دوباره پیش می‌اومد) دیگه وجود نداره.
"""

_banner_paths: dict[int, str] = {}


def set_banner_path(owner_tg_id: int, path: str) -> None:
    _banner_paths[owner_tg_id] = path


def get_banner_path(owner_tg_id: int) -> str | None:
    return _banner_paths.get(owner_tg_id)


def clear_banner_path(owner_tg_id: int) -> None:
    _banner_paths.pop(owner_tg_id, None)
