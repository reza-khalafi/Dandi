# راهنمای اشتراک‌گذاری آنلاین پروژه لوکال از طریق تانل (Public Tunneling Guide)

این سند راهنمای کامل و گام‌به‌گام نحوه باز کردن دسترسی اینترنت به پروژه محلی **دَندی (Dandi)** است؛ به‌طوری‌که بتوانید بدون نیاز به خرید هاست، سرور ابری (VPS) یا آی‌پی استاتیک (Static IP)، پروژه در حال اجرای خود را در قالب یک لینک عمومی و امن (`https://...`) برای تست روی تلفن همراه، ارائه به کارفرما یا اشتراک با همکاران ارسال فرمایید.

---

## 🧭 ۱. مقایسه روش‌ها: چرا Cloudflare Tunnel به جای Ngrok؟

برای ایجاد تانل امن معکوس (Reverse Tunnel) از کامپیوتر لوکال به شبکه اینترنت، دو ابزار شاخص وجود دارد:

| ویژگی | کلودفلر تانل (Cloudflare Tunnel) | ان‌گروک (Ngrok) |
| :--- | :---: | :---: |
| **نیاز به ثبت‌نام یا اکانت** | ❌ **خیر (کاملاً بی‌نیاز از ثبت‌نام)** | ⚠️ بله (الزام به ثبت‌نام و دریافت Authtoken) |
| **گواهینامه SSL رسمی** | ✅ فعال پیش‌فرض (`https://*.trycloudflare.com`) | ✅ فعال پیش‌فرض |
| **صفحه هشدار و واسط (Interstitial)** | ❌ خیر (مستقیماً سایت دندی را باز می‌کند) | ⚠️ در پلن رایگان صفحه هشدار نشان می‌دهد |
| **پایداری و ترافیک** | ✅ زیرساخت شبکه جهانی Anycast کلودفلر | ✅ پایدار با محدودیت ترافیک در پلن رایگان |

> 💡 **توصیه استاندارد:** در این پروژه ابزار **Cloudflare Tunnel (`cloudflared`)** به دلیل عدم نیاز به اکانت و ارائه تجربه کاربری روان، به عنوان راهکار پیش‌فرض انتخاب شده است. البته نحوه کار با **Ngrok** نیز در این راهنما آموزش داده شده است.

---

## 🛡️ ۲. پیش‌نیاز حیاتی جنگو: تنظیم `CSRF_TRUSTED_ORIGINS`

در نسخه‌های مدرن جنگو (نسخه ۴ به بعد)، برای امنیت در برابر حملات جعل درخواست، هر فرم ارسالی با متد `POST` (شامل فرم ورود، ثبت‌نام و کادر چت با دستیار هوشمند) اعتبارسنجی می‌شود. اگر دامنه تانل در تنظیمات جنگو تعریف نشده باشد، کاربر با خطای **`403 Forbidden - CSRF verification failed`** روبرو خواهد شد.

این پیکربندی در فایل [config/settings.py](file:///Users/rezakhalafi/Sites/dandi/config/settings.py) انجام شده است:

```python
# پشتیبانی از دامنه‌های تانل کلودفلر و ان‌گروک
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in os.environ.get(
        'DJANGO_CSRF_TRUSTED_ORIGINS',
        'https://*.trycloudflare.com,https://*.ngrok-free.app,https://*.ngrok.app,http://127.0.0.1:8000'
    ).split(',') if origin.strip()
]
```

همچنین مقدار `ALLOWED_HOSTS = ['*']` در حالت لوکال اجازه عبور هر هاستینگی را صادر می‌کند.

---

## 🚀 ۳. روش اول: اجرای آنی با Cloudflare Tunnel (پیشنهادی)

### گام ۱: دریافت باینری `cloudflared` (یک‌بار برای همیشه)

بسته به سیستم‌عامل خود دستور مربوطه را اجرا کنید:

#### در مک‌اواس (macOS Apple Silicon):
```bash
curl -sL "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz" | tar -xz -C .venv/bin/
chmod +x .venv/bin/cloudflared
```

#### در مک‌اواس (macOS Intel x86_64):
```bash
curl -sL "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz" | tar -xz -C .venv/bin/
chmod +x .venv/bin/cloudflared
```

#### در گنو/لینوکس (Linux x86_64):
```bash
curl -sL "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64" -o .venv/bin/cloudflared
chmod +x .venv/bin/cloudflared
```

#### در ویندوز (Windows PowerShell):
فایل اجرایی `cloudflared-windows-amd64.exe` را از [صفحه رسمی رلیزهای کلودفلر](https://github.com/cloudflare/cloudflared/releases/latest) دانلود کنید و در پوشه پروژه ذخیره نمایید.

---

### گام ۲: روشن کردن سرور جنگو
در پنجره اول ترمینال، وب‌سرور داخلی جنگو را استارت بزنید:
```bash
python manage.py runserver 127.0.0.1:8000
```

---

### گام ۳: ایجاد تانل عمومی
در پنجره دوم ترمینال، دستور زیر را اجرا کنید:

- **در مک یا لینوکس:**
  ```bash
  .venv/bin/cloudflared tunnel --url http://127.0.0.1:8000
  ```
- **در ویندوز:**
  ```powershell
  .\cloudflared.exe tunnel --url http://127.0.0.1:8000
  ```

در خروجی ترمینال، باکسی مشابه شکل زیر ظاهر می‌شود:
```text
+--------------------------------------------------------------------------------------------+
|  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
|  https://xxxx-xxxx-xxxx.trycloudflare.com                                                  |
+--------------------------------------------------------------------------------------------+
```

لینک تولیدشده را کپی کنید؛ پروژه شما اکنون در سراسر اینترنت در دسترس است! 🌍

---

## ⚡ ۴. روش دوم: اجرا با استفاده از Ngrok (در صورت تمایل)

اگر تمایل دارید از Ngrok استفاده فرمایید، مراحل زیر الزامی است:

### گام ۱: دانلود باینری Ngrok
باینری رسمی Ngrok برای مک هم‌اکنون در پوشه `.venv/bin/ngrok` پروژه موجود است. برای سایر سیستم‌عامل‌ها می‌توانید آن را از [ngrok.com/download](https://ngrok.com/download) دریافت کنید.

### گام ۲: دریافت و تنظیم Authtoken رایگان
به دلیل سیاست‌های نسخه ۳ ان‌گروک (`ERR_NGROK_4018`)، ثبت توکن اجباری است:
1. در سایت [dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup) یک حساب رایگان بسازید.
2. توکن اختصاصی خود را از بخش [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken) کپی کنید.
3. در خط فرمان دستور زیر را بزنید:
   ```bash
   .venv/bin/ngrok config add-authtoken <توکن_شما>
   ```

### گام ۳: اجرای تانل Ngrok
```bash
.venv/bin/ngrok http 8000
```
آدرس `https://xxxx.ngrok-free.app` تولید می‌شود و می‌توانید از آن استفاده نمایید.

---

## 🔒 ۵. نکات امنیتی و پایان جلسه دمو (Best Practices)

1. **بستن تانل پس از پایان ارائه:**
   - هر زمان کار شما با کلاینت یا تست به پایان رسید، کافی است در پنجره ترمینال تانل کلیدهای ترکیبی `Ctrl + C` را فشار دهید تا اتصال اینترنت به کامپیوتر محلی بلافاصله مسدود شود.
2. **عدم نمایش اطلاعات حساس:**
   - مطمئن شوید متغیرهای حساس در `.env` روی محیط محلی باقی می‌مانند.
3. **بررسی لاگ‌های زنده‌ی درخواست‌ها:**
   - هنگام کلیک کاربر روی لینک عمومی، لاگ تک‌تک درخواست‌های HTTP را در پنجره `runserver` جنگو به صورت زنده مشاهده خواهید کرد.
