# تقسیم پروژه به «هاست اصلی» و «هاست‌های سلف»

## معماری

```
main-host/            → یک نمونه، فقط این یکی
  main.py             → نقطه‌ی ورود (بدون پنل وب)
  telegram_bot.py      → ربات ثبت‌نام/مدیریت (توکن)
  helper_bot.py        → ربات کمکیِ پنل دکمه‌ای
  app.py, panel_api.py → پنل وب Flask (فعلاً نگه داشته شده، تصمیم بعدی)
  database*.py, db_cache.py, session_db.py → لایه‌ی دیتابیس مرکزی (Supabase)
  host_registry.py     → لیست هاست‌های سلف + تخصیصِ کاربر به هاست
  host_api.py           → API داخلی که هاست‌های سلف باهاش صحبت می‌کنن
  remote_bot_manager.py → جایگزینِ bot_manager قدیمی؛ start/stop رو به‌جای
                          اجرای مستقیم، توی صف دستور می‌ذاره

self-host/             → چند نمونه (self-host-1, self-host-2, ...)
  self_main.py          → نقطه‌ی ورود؛ هر چند ثانیه از هاست اصلی می‌پرسه
                          «کدوم کاربرها مال منن؟» و دستورهای start/stop رو اجرا می‌کنه
  bot.py, bot_manager.py, meowie_game.py, ai_reply.py, ...
                        → همون منطق اجرای واقعیِ سلف‌ها (دست‌نخورده)
  host_client.py        → کلاینت HTTP برای صحبت با هاست اصلی
  remote_control.py     → خوندن دستورهای معلق + گزارشِ وضعیت (مستقیم روی DB مشترک)
  database*.py, session_db.py → همون دیتابیس مرکزی (برای تنظیمات/سشن هر کاربر)
```

## جریان کار

1. کاربر توی ربات ثبت‌نام (روی هاست اصلی) لاگین می‌کنه و سلفشو روشن می‌کنه.
2. `telegram_bot.py` مثل قبل `bot_manager.start(oid, ...)` رو صدا می‌زنه، ولی
   حالا این تابع از `remote_bot_manager` میاد: یه دستور «start» توی جدول
   `amel_bot_commands` ثبت می‌کنه و اگه کاربر هنوز به هیچ هاستی تخصیص داده
   نشده، خودکار به کم‌بارترین هاست سلف تخصیصش می‌ده (`host_registry`).
3. هر هاست سلف (`self_main.py`) هر ۱۵ ثانیه (قابل تنظیم) از API داخلیِ
   هاست اصلی می‌پرسه چه کاربرهایی الان مال اونه، دستورهای معلقِ همون
   کاربرها رو می‌خونه، روی `bot_manager` محلیِ خودش اجرا می‌کنه، و وضعیت
   (روشن/خاموش/پاز) رو برمی‌گردونه.
4. `is_running` / `is_paused` روی هاست اصلی از همین وضعیتِ گزارش‌شده خونده
   می‌شن.

## متغیرهای محیطی جدید

**هاست اصلی:**
- `INTERNAL_REGISTER_KEY` — کلید مشترک برای این‌که فقط هاست‌های سلفِ واقعی
  بتونن خودشونو معرفی کنن.

**هر هاست سلف:**
- `MAIN_HOST_URL` — آدرس هاست اصلی، مثلاً `https://main.example.com`
- `HOST_ID` — شناسه‌ی یکتا، مثلاً `self-host-1`
- `HOST_NAME`, `HOST_CAPACITY` (پیش‌فرض ۲۰۰)
- `INTERNAL_REGISTER_KEY` — همون مقدار روی هاست اصلی
- `POLL_INTERVAL_SECONDS` — پیش‌فرض ۱۵

اجرا: `python self_main.py`

## پنل دکمه‌ای تلگرام (helper_bot) — حل شد ✅

`panel_api.py` رفت روی **self-host** (چون به کلاینتِ زنده نیاز داره) و پشتِ
یه سرورِ Flakس سبک (`panel_server.py`) در دسترسه؛ `self_main.py` خودکار این
سرور رو بالا میاره (فقط اگه `PANEL_API_SECRET` ست شده باشه).

`helper_bot.py` روی main-host دیگه مستقیم از `bot.py` چیزی import نمی‌کنه؛
از طریق `panel_client.py` (HTTP) با هاستِ سلفِ صاحبِ هر کاربر صحبت می‌کنه:
هاستِ درست از `host_registry` (همون تخصیصی که برای start/stop هم استفاده
می‌شه) پیدا می‌شه.

**متغیرهای محیطیِ جدید برای این بخش:**
- روی هاست اصلی و **همه‌ی** هاست‌های سلف: `PANEL_API_SECRET` (یه رشته‌ی
  تصادفیِ مشترک — مثل `INTERNAL_REGISTER_KEY` بسازش، `python3 -c "import secrets; print(secrets.token_hex(32))"`)
- روی هر هاست سلف: `SELF_HOST_PUBLIC_URL` (آدرسی که از بیرون در دسترسه، مثلاً
  `https://self-host-1.example.com`) و اختیاری `PANEL_API_PORT` (پیش‌فرض ۸۰۸۸)

⚠️ نکته‌ی امنیتی: چون `panel_server.py` روی پورت `PANEL_API_PORT` باز می‌شه،
حتماً یا پشتِ HTTPS (ریورس‌پروکسی مثل Nginx/Caddy) بذارش، یا فایروال‌اش کن
که فقط IP هاست اصلی بتونه بهش وصل بشه — چون `PANEL_API_SECRET` تنها
لایه‌ی محافظتشه.

## کارهای باقی‌مونده (دستی)

- **`app.py`**: هنوز مستقیم از `bot.py` (`PANEL_CATEGORIES`,
  `build_category_commands`, `_execute_panel_command`) استفاده می‌کنه.
  چون فعلاً فقط ساختار پایتونی جدا شده و تصمیم نهایی درباره‌ی پنل وب
  عقب افتاده، این فایل رو دست نزدم — قبل از اجرا کردنِ واقعیِ `app.py`
  باید همین مشکلِ import حل بشه (یا با همون الگوی remote command، یا با
  حذف کامل پنل وب).
- **`session_db.py`**: `SESSION_DATABASE_URL` توی `config.py` اصلاً تعریف
  نشده بود (باگ از قبلِ این تقسیم‌بندی) — قبل از دیپلوی روی هر دو هاست
  این متغیر رو یا توی `config.py` تعریف کنید یا با `os.environ.get(...)`
  از env بخونید.
- **جدول‌های جدید** (`amel_hosts`, `amel_host_assignments`,
  `amel_bot_commands`, `amel_bot_status`) با اولین اجرای `main.py` خودکار
  ساخته می‌شن.
