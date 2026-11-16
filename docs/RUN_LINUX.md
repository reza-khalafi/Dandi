# راهنمای اجرای لوکال پروژه دَندی روی گنو/لینوکس (Linux)

این سند مراحل گام‌به‌گام نصب، راه‌اندازی و اجرای نسخه محلی سامانه **دَندی (Dandi)** را بر روی توزیع‌های مختلف گنو/لینوکس (مانند Ubuntu، Debian، Fedora و Arch Linux) به همراه پایگاه‌داده ساده پیش‌فرض (SQLite) تشریح می‌کند.

---

## 📋 ۱. پیش‌نیازهای سیستمی

قبل از شروع، مطمئن شوید بسته‌های پایه‌ای روی توزیع شما نصب شده است:

### اوبونتو / دبیان (Ubuntu / Debian / Linux Mint):
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git build-essential libjpeg-dev zlib1g-dev
```

### فدورا / ردهت (Fedora / RHEL):
```bash
sudo dnf install -y python3 python3-devel git gcc libjpeg-turbo-devel zlib-devel
```

### آرچ لینوکس (Arch Linux / Manjaro):
```bash
sudo pacman -Syu --needed python python-pip git base-devel libjpeg-turbo zlib
```

> **نکته:** نسخه پیشنهادی پایتون برای پروژه دَندی: **Python 3.11** یا بالاتر می‌باشد. با دستور `python3 --version` نسخه فعلی را بررسی کنید.

---

## 🚀 ۲. مراحل گام‌به‌گام راه‌اندازی محلی

### گام اول: کلون کردن پروژه
ابتدا مخزن پروژه را دریافت کرده و وارد پوشه آن شوید:
```bash
git clone git@github.com:reza-khalafi/Dandi.git
cd Dandi
```
*(یا از طریق آدرس HTTPS: `git clone https://github.com/reza-khalafi/Dandi.git`)*

---

### گام دوم: ایجاد و فعال‌سازی محیط مجازی پایتون (Virtualenv)
جهت ایزوله‌سازی بسته‌ها از محیط سیستم‌عامل، یک Virtual Environment بسازید:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
*(پس از فعال‌سازی، پیشوند `(.venv)` را در ابتدای خط فرمان ترمینال مشاهده خواهید کرد.)*

---

### گام سوم: ارتقاء pip و نصب وابستگی‌ها
وابستگی‌های پروژه قفل‌شده در `requirements.txt` را نصب کنید:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### گام چهارم: پیکربندی متغیرهای محیطی (.env)
یک نسخه از فایل نمونه `.env.example` تهیه کرده و نام آن را به `.env` تغییر دهید:
```bash
cp .env.example .env
```

سپس با یک ادیتور متنی مانند `nano` یا `vim` فایل `.env` را باز کنید:
```bash
nano .env
```
مقادیر زیر را در فایل `.env` تنظیم یا بررسی کنید:
```env
# تنظیمات اصلی جنگو
DJANGO_SECRET_KEY="یک_کلید_محرمانه_تصادفی"
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

# کلید هوش مصنوعی Groq (برای بخش دستیار هوشمند دندی)
# می‌توانید کلید رایگان را از https://console.groq.com دریافت کنید
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b
PYDANTIC_AI_NO_BANNER=1
```

> 💡 **تولید کلید تصادفی جنگو در ترمینال لینوکس:**
> برای تولید یک کلید استاندارد و امن می‌توانید دستور زیر را اجرا کرده و خروجی آن را در `DJANGO_SECRET_KEY` قرار دهید:
> ```bash
> python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

---

### گام پنجم: اعمال مایگریشن‌های دیتابیس (SQLite)
دیتابیس ساده، پرسرعت و سبک لوکال پروژه SQLite است و نیازی به نصب سرویس‌های سنگین خارجی ندارد:
```bash
python manage.py migrate
```
این دستور فایل `db.sqlite3` را با تمام جداول کاربران، مقالات، کامنت‌ها و حافظه چت هوش مصنوعی ایجاد می‌کند.

---

### گام ششم: بارگذاری داده‌های اولیه و مقالات نمونه (Seed Data)
برای اینکه سایت خالی نباشد و دسته‌بندی‌ها، تگ‌ها، تصاویر پیش‌فرض، مقالات غنی و یک کاربر ادمین ساخته شوند، دستور اختصاصی زیر را اجرا کنید:
```bash
python manage.py seed_data
```
این دستور اطلاعات پایه تحریریه را همراه با عکس‌های مجله در دیتابیس ثبت می‌کند.

---

### گام هفتم: اجرای تست‌های خودکار (اختیاری ولی پیشنهادی)
جهت اطمینان از صحت کامل محیط لینوکس و پاس شدن تمامی تست‌ها:
```bash
python manage.py test tests
```
*(تمام تست‌های ۱۴ متدولوژی باید وضعیت OK برگردانند).*

---

### گام هشتم: اجرای سرور توسعه محلی (Runserver)
سرور توسعه داخلی جنگو را استارت بزنید:
```bash
python manage.py runserver 127.0.0.1:8000
```

اکنون مرورگر خود را باز کرده و به آدرس زیر مراجعه فرمایید:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 👤 ۳. اطلاعات ورود به سامانه
- **ورود به پنل ادمین جنگو**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **ورود به سایت دَندی**: [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)
- **دسترسی به دستیار هوشمند**: [http://127.0.0.1:8000/assistant/](http://127.0.0.1:8000/assistant/)

اگر تمایل دارید کاربر مدیر اختصاصی خودتان را بسازید:
```bash
python manage.py createsuperuser
```

---

## 🛠️ ۴. رفع خطاهای احتمالی (Troubleshooting)

1. **خطای `No module named venv`:**
   - علت: پکیج محیط مجازی روی توزیع‌های مبتنی بر دبیان به صورت مجزا قرار دارد.
   - راه‌حل: `sudo apt install python3-venv` را اجرا کنید.

2. **خطای پورت اشغال‌شده (`Port 8000 is already in use`):**
   - علت: یک پروسه دیگر قبلاً پورت ۸۰۰۰ را رزرو کرده است.
   - راه‌حل: یا پروسه را ببندید:
     ```bash
     fuser -k 8000/tcp
     ```
     یا سرور را روی یک پورت آزاد دیگر اجرا نمایید:
     ```bash
     python manage.py runserver 127.0.0.1:8080
     ```

3. **خطای مجوز فایل دیتابیس (`Permission denied: 'db.sqlite3'`):**
   - راه‌حل:
     ```bash
     chmod 664 db.sqlite3
     chmod 775 .
     ```
