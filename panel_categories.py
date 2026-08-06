# panel_categories.py
# ساختار ثابت منوی پنل — مستقیم اینجا تعریفه، بدون نیاز به HTTP به self-host

PANEL_CATEGORIES = {
    # ─── سطح ۱: منوی اصلی (چیدمانِ شبکه‌ای، مطابق طرح درخواستی) ───────────────
    "text_mode": {
        "title": "حالت متن",
        "menu_style": "primary",
        "toggles": [
            ("text_style_quote_active", "نقل قول", "حالت نقل قول روشن", "حالت نقل قول خاموش"),
            ("text_style_underline_active", "زیر خط", "حالت زیرخط روشن", "حالت زیرخط خاموش"),
            ("text_style_spoiler_active", "اسپویلر", "حالت اسپویلر روشن", "حالت اسپویلر خاموش"),
            ("text_style_gradual_active", "تدریجی", "حالت تدریجی روشن", "حالت تدریجی خاموش"),
            ("text_style_bold_active", "بولد", "حالت بولد روشن", "حالت بولد خاموش"),
            ("text_style_italic_active", "ایتالیک", "حالت ایتالیک روشن", "حالت ایتالیک خاموش"),
            ("text_style_strike_active", "خط خورده", "حالت خط‌خورده روشن", "حالت خط‌خورده خاموش"),
            ("text_style_single_space_active", "تک فاصله", "حالت تک‌فاصله روشن", "حالت تک‌فاصله خاموش"),
            ("text_style_finglish_active", "فینگلیش", "حالت فینگلیش روشن", "حالت فینگلیش خاموش"),
        ],
        "actions": [],
    },
    "clock": {
        "title": "ساعت",
        "menu_style": "primary",
        "toggles": [
            ("clock_name_active", "ساعت نام", "ساعت نام روشن", "ساعت نام خاموش"),
            ("clock_bio_active", "ساعت بیو", "ساعت بیو روشن", "ساعت بیو خاموش"),
            ("clock_premium_active", "ساعت پرمیوم", "ساعت پرمیوم روشن", "ساعت پرمیوم خاموش"),
        ],
        "actions": [],
        "children": [("فونت ساعت", "clock_font")],
    },
    "chat_guard": {
        "title": "نگهبان چت",
        "menu_style": "primary",
        "toggles": [
            ("guard_delete_active", "ذخیره پیام حذف‌شده", "ذخیره پیام حذف‌شده روشن", "ذخیره پیام حذف‌شده خاموش"),
            ("guard_edit_active", "ذخیره پیام ویرایش‌شده", "ذخیره پیام ویرایش‌شده روشن", "ذخیره پیام ویرایش‌شده خاموش"),
            ("guard_view_once_active", "ذخیره عکس تایمی", "ذخیره عکس تایمی روشن", "ذخیره عکس تایمی خاموش"),
        ],
        "actions": [],
    },
    "ping": {
        "title": "پینگ",
        "menu_style": "primary",
        "direct_command": "پینگ",
    },
    "logo": {
        "title": "لوگو",
        "menu_style": "primary",
        "direct_command": "لوگو",
    },
    "locks": {
        "title": "قفل ها",
        "menu_style": "primary",
        "toggles": [
            ("lock_username_active", "قفل یوزرنیم", "قفل یوزرنیم روشن", "قفل یوزرنیم خاموش"),
            ("lock_reply_active", "قفل ریپلای", "قفل ریپلای روشن", "قفل ریپلای خاموش"),
            ("lock_gif_active", "قفل گیف", "قفل گیف روشن", "قفل گیف خاموش"),
            ("private_lock_active", "قفل پیوی", "قفل پیوی روشن", "قفل پیوی خاموش"),
            ("anti_link_active", "قفل لینک", "ضد لینک روشن", "ضد لینک خاموش"),
            ("lock_photo_active", "قفل عکس", "قفل عکس روشن", "قفل عکس خاموش"),
            ("lock_sticker_active", "قفل استیکر", "قفل استیکر روشن", "قفل استیکر خاموش"),
            ("lock_forward_active", "قفل فوروارد", "قفل فوروارد روشن", "قفل فوروارد خاموش"),
            ("anti_delete_active", "قفل ضد حذف", "ضد حذف روشن", "ضد حذف خاموش"),
            ("login_lock_active", "قفل لاگین", "قفل لاگین روشن", "قفل لاگین خاموش"),
        ],
        "actions": [],
    },
    "actions": {
        "title": "اکشن",
        "menu_style": "primary",
        "toggles": [
            ("typing_action_active", "اکشن تایپینگ 24 ساعته", "تایپینگ روشن", "تایپینگ خاموش"),
            ("gaming_action_active", "اکشن گیمینگ 24 ساعته", "گیمینگ روشن", "گیمینگ خاموش"),
            ("voice_action_active", "اکشن ویس 24 ساعته", "ویس روشن", "ویس خاموش"),
            ("video_action_active", "اکشن ارسال ویدیو 24 ساعته", "ارسال ویدیو روشن", "ارسال ویدیو خاموش"),
        ],
        "actions": [],
    },
    "friend_enemy": {
        "title": "دوست و دشمن",
        "menu_style": "success",
        "toggles": [],
        "actions": [],
        "children": [("دوست", "friend_enemy_friend"), ("دشمن", "friend_enemy_enemy")],
    },
    "secretary": {
        "title": "منشی",
        "menu_style": "success",
        "toggles": [
            ("secretary_active", "منشی", "منشی روشن", "منشی خاموش"),
        ],
        "actions": [
            ("نمایش متن دستورات منشی", "INFO::دستورات منشی:\nمنشی روشن / منشی خاموش\nپیام منشی [متن دلخواه]"),
        ],
    },
    "word_filter": {
        "title": "فیلترکلمات",
        "menu_style": "success",
        "toggles": [
            ("word_filter_active", "فیلتر کلمات", "فیلترکلمات روشن", "فیلترکلمات خاموش"),
        ],
        "actions": [
            ("افزودن کلمه", "INFO::برای افزودن تایپ کن: فیلتر کلمه [کلمه]"),
            ("حذف کلمه", "INFO::برای حذف تایپ کن: حذف فیلتر کلمه [کلمه]"),
            ("لیست فیلتر کلمات", "لیست فیلتر کلمات"),
        ],
    },
    "auto_reply": {
        "title": "پاسخ خودکار",
        "menu_style": "success",
        "toggles": [
            ("auto_reply_active", "پاسخ خودکار", "پاسخ خودکار روشن", "پاسخ خودکار خاموش"),
        ],
        "actions": [
            ("تنظیم متن پاسخ", "INFO::برای تنظیم متن تایپ کن: متن پاسخ خودکار [متن دلخواه]"),
            ("افزودن پاسخ کلیدی", "INFO::برای ثبت تایپ کن: پاسخ کلیدی [کلمه] = [پاسخ]\nمثال: پاسخ کلیدی قیمت = قیمت‌ها توی کانال هست."),
            ("حذف پاسخ کلیدی", "INFO::برای حذف تایپ کن: حذف پاسخ کلیدی [کلمه]"),
            ("لیست پاسخ کلیدی", "لیست پاسخ کلیدی"),
            ("پاک کردن همه‌ی پاسخ کلیدی", "پاک کردن پاسخ کلیدی"),
        ],
    },
    "forced_join": {
        "title": "عضویت اجباری پیوی",
        "menu_style": "success",
        "toggles": [
            ("force_join_active", "عضویت اجباری", "جوین اجباری روشن", "جوین اجباری خاموش"),
        ],
        "actions": [
            ("نمایش متن دستورات", "INFO::دستورات عضویت اجباری:\nافزودن کانال [آیدی/یوزرنیم] [لینک]\nحذف کانال [آیدی/یوزرنیم]\nلیست کانال‌های اجباری\nپاک کردن کانال‌های اجباری\nپیام جوین [متن]\nجوین اجباری روشن / جوین اجباری خاموش"),
            ("لیست کانال‌های اجباری", "لیست کانال‌های اجباری"),
            ("پاک کردن کانال‌های اجباری", "پاک کردن کانال‌های اجباری"),
        ],
    },
    "downloader": {
        "title": "دانلودر",
        "menu_style": "primary",
        "direct_command": "INFO::روی یک عکس/ویدیو/فایل ریپلای کن و تایپ کن: تبدیل به گیف (برای ویدیو) یا مستقیم فوروارد کن به پیام‌های ذخیره‌شده",
    },
    "user_react": {
        "title": "ریکت",
        "menu_style": "primary",
        "direct_command": "INFO::روی پیام کاربر ریپلای کن و تایپ کن: تنظیم ری‌اکت [ایموجی] — برای حذف: حذف ری‌اکت",
    },
    "spam": {
        "title": "اسپم",
        "menu_style": "primary",
        "direct_command": "INFO::برای شروع تایپ کن: اسپم [تعداد] [متن] — برای توقف: توقف اسپم — برای تنظیم تأخیر: تاخیر اسپم [ثانیه]",
    },
    "silent_mode": {
        "title": "سایلنت",
        "menu_style": "primary",
        "direct_command": "INFO::سایلنت چت روشن / سایلنت چت خاموش — نادیده‌گرفتن کل این چت\nسایلنت کاربر [آیدی] / لغو سایلنت کاربر [آیدی] — نادیده‌گرفتن یک کاربر خاص",
    },
    "pm_silence": {
        "title": "سکوت",
        "menu_style": "primary",
        "direct_command": "INFO::روی پیام کاربر ریپلای کن و تایپ کن: سکوت — برای لغو: لغو سکوت — برای دیدن لیست: لیست سکوت",
    },
    "user_info": {
        "title": "اطلاعات",
        "menu_style": "primary",
        "direct_command": "وضعیت",
    },
    "tag_all": {
        "title": "تگ",
        "menu_style": "primary",
        "direct_command": "INFO::این دستور فقط توی گروه کار می‌کند. تایپ کن: تگ [متن دلخواه]",
    },
    "block_user": {
        "title": "بلاک",
        "menu_style": "primary",
        "direct_command": "INFO::روی پیام کاربر ریپلای کن و تایپ کن: بلاک کاربر — لیست: لیست بلاک",
    },
    "delete_msg": {
        "title": "حذف",
        "menu_style": "primary",
        "direct_command": "INFO::روی پیامی که می‌خوای حذف شه ریپلای کن و تایپ کن: حذف",
    },
    "ai_assistant": {
        "title": "هوش مصنوعی",
        "menu_style": "success",
        "toggles": [
            ("ai_assistant_active", "دیپ سیک", "دیپ سیک روشن", "دیپ سیک خاموش"),
            ("ai_reply_always_active", "پاسخ به همه پیام‌ها", "هوش مصنوعی پاسخ همه روشن", "هوش مصنوعی پاسخ همه خاموش"),
        ],
        "actions": [
            ("افزودن اطلاعات", "INFO::برای اضافه‌کردن اطلاعات تایپ کن: آموزش هوش مصنوعی [متن] — مثال: آموزش هوش مصنوعی قیمت گوشی X ۱۰ میلیون تومان است"),
            ("نمایش دانش هوش مصنوعی", "نمایش دانش هوش مصنوعی"),
            ("پاک کردن دانش هوش مصنوعی", "پاک کردن دانش هوش مصنوعی"),
        ],
    },
    "translate_tool": {
        "title": "ترجمه",
        "menu_style": "primary",
        "direct_command": "INFO::برای استفاده تایپ کن: ترجمه [متن] — یا روی پیام ریپلای کن و بنویس: ترجمه متن",
    },
    "animation": {
        "title": "انیمیشن",
        "menu_style": "primary",
        "direct_command": "INFO::این بخش هنوز آماده نیست.",
    },
    "cheat": {
        "title": "تقلب",
        "menu_style": "success",
        "direct_command": (
            "INFO::تقلب تاس/دارت/فوتبال/بسکتبال/کازینو — همیشه بهترین نتیجه می‌گیری:\n"
            ".تاس یا .تاس 6\n"
            ".دارت یا .دارت 6\n"
            ".فوتبال یا .فوتبال 5\n"
            ".بسکتبال یا .بسکتبال 5\n"
            ".کازینو انگور  (یا: .کازینو لیمو/هفت)"
        ),
    },
    "calculator": {
        "title": "× ÷",
        "menu_style": "primary",
        "direct_command": "INFO::برای استفاده تایپ کن: محاسبه [عبارت] — مثال: محاسبه 2+2*3",
    },
    "text_to_voice": {
        "title": "تبدیل متن به ویس",
        "menu_style": "primary",
        "direct_command": "INFO::این بخش هنوز آماده نیست.",
    },
    "voice_search": {
        "title": "سرچ ویس آماده",
        "menu_style": "primary",
        "direct_command": "INFO::این بخش هنوز آماده نیست.",
    },
    "music_search": {
        "title": "سرچ آهنگ",
        "menu_style": "primary",
        "direct_command": "INFO::این بخش هنوز آماده نیست.",
    },
    "tabchi": {
        "title": "تبچی",
        "menu_style": "primary",
        "toggles": [
            ("tabchi_active", "تبچی", "تبچی روشن", "تبچی خاموش"),
        ],
        "actions": [
            ("راهنما", "PANELINFO::"
             "تنظیم بنر N  (با ریپلای روی پیام بنر — مقصدش خودِ همین گپ می‌شود)\n"
             "تنظیم بنر N در همه گپ‌ها  (با ریپلای — مقصدش همه‌ی گروه‌هایت می‌شود)\n"
             "حذف بنر N\n"
             "لیست بنر\n"
             "پاکسازی لیست بنر\n"
             "ارسال بنر برای تمام گروه‌ها  (ارسال فوریِ همه‌ی بنرهای فعال)\n"
             "تایم بنر N   (فاصله‌ی ارسال خودکار به دقیقه)\n"
             "N عددی بین ۱ تا ۱۰ است."
             ),
            ("لیست بنر", "لیست بنر"),
            ("پاکسازی لیست بنر", "پاکسازی لیست بنر"),
            ("ارسال بنر برای تمام گروه‌ها", "ارسال بنر برای تمام گروه‌ها"),
        ],
    },
    "profile_snoop": {
        "title": "فضول پروفایل",
        "menu_style": "primary",
        "direct_command": "INFO::این بخش هنوز آماده نیست.",
    },
    "first_comment": {
        "title": "کامنت اول",
        "menu_style": "danger",
        "direct_command": "INFO::این بخش هنوز آماده نیست.",
    },
    "currency": {
        "title": "قیمت ارز",
        "menu_style": "danger",
        "direct_command": "ارز",
    },
    "screen_guard": {
        "title": "اسکرین",
        "menu_style": "danger",
        "direct_command": "INFO::دستورات اسکرین (حتماً باید با نقطه شروع بشه):\nروی یه پیام ریپلای بزن و بنویس: .اسکرین\nپیام به‌صورت استیکر (همراه با پروفایل فرستنده) ساخته می‌شه.\n\nبرای پست‌های کانال:\n.اسکرین [لینک پیام]\nمثال: .اسکرین https://t.me/channel/123\nیا (کانال خصوصی): .اسکرین https://t.me/c/123456789/123",
    },
    "tools": {
        "title": "ابزار بیشتر",
        "menu_style": "primary",
        "toggles": [
            ("auto_seen_active", "سین خودکار", "سین خودکار روشن", "سین خودکار خاموش"),
            ("auto_reaction_active", "ری‌اکشن خودکار", "ری‌اکشن روشن", "ری‌اکشن خاموش"),
            ("auto_save_media", "ذخیره مدیا", "ذخیره مدیا روشن", "ذخیره مدیا خاموش"),
        ],
        "actions": [
            ("آب و هوا", "INFO::برای استفاده تایپ کن: هوا [نام شهر]"),
            ("تنظیم ایموجی ری‌اکشن", "INFO::برای تغییر ایموجیِ ری‌اکشن خودکار تایپ کن: ری‌اکشن [ایموجی] — مثال: ری‌اکشن 👍"),
            ("راهنما", "راهنما"),
            ("پاکسازی لیست بلاک", "پاکسازی لیست بلاک"),
            ("ترک همگانی گروه", "ترک همگانی گروه"),
            ("ترک همگانی کانال", "ترک همگانی کانال"),
            ("تبدیل به گیف", "INFO::روی یک ویدیو ریپلای کن و تایپ کن: تبدیل به گیف"),
            ("توقف سیو کانال", "توقف سیو"),
            ("اطلاعات کاربر (ایدی)", "INFO::توی یه چت یا گروه تایپ کن: ایدی\nاگه روی پیام یه کاربر ریپلای کنی و «ایدی» رو بفرستی، اطلاعات همون کاربر رو نشون می‌ده."),
            ("دانلود پست تلگرام", "INFO::برای استفاده تایپ کن: دانلود [لینک پست]\nمثال: دانلود https://t.me/channel/123\nبرای کانال خصوصی: دانلود https://t.me/c/123456789/123"),
            ("دانلود اینستاگرام", "INFO::برای استفاده تایپ کن: اینستا [لینک پست یا ریل]\nمثال: اینستا https://www.instagram.com/reel/xxxxx/"),
        ],
        "children": [("حذف همگانی پیوی ها", "bulk_delete_pv")],
    },
    "premium_emoji": {
        "title": "ایموجی پرمیوم",
        "menu_style": "danger",
        "toggles": [],
        "actions": [],
        "stub_message": "این بخش هنوز در دسترس نیست",
    },

    "meowie_game": meowie_game.PANEL_CATEGORY,

    # ─── زیرمنوها (توی منوی اصلی نشون داده نمی‌شن، فقط از طریق children) ────
    "clock_font": {
        "title": "فونت ساعت",
        "toggles": [],
        "actions": [(f"فونت {k}", f"فونت ساعت {k}") for k in "0123456789"],
        "parent": "clock",
    },
    "friend_enemy_friend": {
        "title": "دوست",
        "toggles": [],
        "actions": [
            ("نمایش لیست دوست", "نمایش لیست دوست"),
            ("پاک کردن لیست دوست", "پاک کردن لیست دوست"),
        ],
        "parent": "friend_enemy",
    },
    "friend_enemy_enemy": {
        "title": "دشمن",
        "toggles": [
            ("enemy_reply_active", "پاسخ دشمن", "پاسخ دشمن روشن", "پاسخ دشمن خاموش"),
        ],
        "actions": [
            ("نمایش لیست دشمن", "نمایش لیست دشمن"),
            ("پاک کردن لیست دشمن", "پاک کردن لیست دشمن"),
        ],
        "parent": "friend_enemy",
    },
    "bulk_delete_pv": {
        "title": "حذف همگانی پیوی ها",
        "toggles": [],
        "actions": [],
        "children": [
            ("حذف دوطرفه", "bulk_delete_pv_confirm_2way"),
            ("حذف یکطرفه", "bulk_delete_pv_confirm_1way"),
        ],
        "parent": "tools",
    },
    "bulk_delete_pv_confirm_2way": {
        "title": "⚠️ مطمئنی؟ همه‌ی پیوی‌ها برای هر دو طرف حذف می‌شن (برگشت‌ناپذیر)",
        "toggles": [],
        "actions": [
            ("✅ بله، حذف کن", "حذف دوطرفه پیوی ها"),
        ],
        "parent": "bulk_delete_pv",
    },
    "bulk_delete_pv_confirm_1way": {
        "title": "⚠️ مطمئنی؟ همه‌ی پیوی‌ها فقط از سمت خودت حذف می‌شن (برگشت‌ناپذیر)",
        "toggles": [],
        "actions": [
            ("✅ بله، حذف کن", "حذف یکطرفه پیوی ها"),
        ],
        "parent": "bulk_delete_pv",
    },
    "meowie_settings": meowie_game.SETTINGS_PANEL_CATEGORY,
}

PANEL_CATEGORY_ORDER = [
    "text_mode", "clock", "chat_guard",
    "ping", "logo", "locks",
    "actions", "friend_enemy", "secretary",
    "word_filter", "auto_reply", "forced_join",
    "downloader", "user_react", "spam",
    "silent_mode", "pm_silence", "user_info", "tag_all",
    "block_user", "delete_msg", "tools",
    "ai_assistant", "translate_tool", "animation",
    "cheat", "calculator", "text_to_voice",
    "voice_search", "music_search", "tabchi",
    "profile_snoop", "first_comment", "currency",
    "screen_guard", "premium_emoji", "meowie_game",
]
