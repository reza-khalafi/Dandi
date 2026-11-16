# راهنمای اجرای لوکال پروژه دَندی روی ویندوز (Windows)

این سند راهنمای گام‌به‌گام راه‌اندازی و اجرای محلی سامانه **دَندی (Dandi)** بر روی سیستم‌عامل **ویندوز ۱۰ و ۱۱ (Windows 10/11 64-bit)** به همراه دیتابیس ساده و پیش‌فرض SQLite است.

این راهنما دستورات را برای هر ۳ محیط متداول ویندوز شامل **PowerShell** (پیشنهادی)، **Command Prompt (CMD)** و **Git Bash** پوشش می‌دهد.

---

## 📋 ۱. پیش‌نیازهای اولیه در ویندوز

قبل از شروع مراحل، مطمئن شوید نرم‌افزارهای زیر روی سیستم شما نصب شده‌اند:

1. **نصب پایتون (Python 3.11 یا بالاتر):**
   - به وب‌سایت رسمی پایتون [python.org/downloads](https://www.python.org/downloads/) مراجعه کرده و آخرین نسخه پایدار پایتون را دانلود و نصب کنید.
   - ⚠️ **نکته بسیار حیاتی:** در همان صفحه اول نصاب پایتون، حتماً تیک گزینه **`Add python.exe to PATH`** را فعال کنید!

2. **نصب گیت برای ویندوز (Git for Windows):**
   - از سایت [git-scm.com/download/win](https://git-scm.com/download/win) ابزار Git را دریافت و نصب فرمایید (این ابزار ترمینال مفید Git Bash را نیز اضافه می‌کند).

---

## 🚀 ۲. مراحل گام‌به‌گام راه‌اندازی محلی

### گام اول: کلون کردن سورس پروژه (Git Clone)
ترمینال **PowerShell** یا **Git Bash** را باز کرده و پروژه را در مسیر مورد نظرتان دریافت کنید:
```powershell
cd C:\Projects
git clone https://github.com/reza-khalafi/Dandi.git
cd Dandi
```

---

### گام دوم: ایجاد محیط مجازی پایتون (Virtual Environment)
برای جلوگیری از تداخل بسته‌ها با پایتون عمومی سیستم، یک محیط مجازی به نام `.venv` بسازید:
```powershell
python -m venv .venv
```

---

### گام سوم: فعال‌سازی محیط مجازی (.venv)
بسته به اینکه از کدام شل ویندوز استفاده می‌کنید، دستور متناظر را اجرا فرمایید:

#### الف) در پاورشل (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```
> ⚠️ **اگر با خطای Execution Policy در پاورشل مواجه شدید:**
> اگر خطایی مبنی بر `running scripts is disabled on this system` دریافت کردید، یک‌بار دستور زیر را در همان پنجره پاورشل اجرا کنید تا مجوز اجرای اسکریپت فعال شود:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> و سپس مجدداً `.\.venv\Scripts\Activate.ps1` را بزنید.

#### ب) در محیط سی‌ام‌دی (Command Prompt / cmd.exe):
```cmd
.\.venv\Scripts\activate.bat
```

#### ج) در گیت‌بش (Git Bash):
```bash
source .venv/Scripts/activate
```
*(پس از فعال‌شدن، عبارت `(.venv)` را در ابتدای خط فرمان مشاهده خواهید کرد).*

---

### گام چهارم: ارتقاء pip و نصب وابستگی‌های پروژه
کتابخانه‌های ثبت‌شده در `requirements.txt` را نصب کنید:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### گام پنجم: تنظیم متغیرهای محیطی (.env)
یک کپی از فایل نمونه `.env.example` بسازید:

- **در پاورشل:**
  ```powershell
  Copy-Item .env.example .env
  ```
- **در CMD:**
  ```cmd
  copy .env.example .env
  ```
- **در Git Bash:**
  ```bash
  cp .env.example .env
  ```

سپس فایل `.env` را با ویرایشگر دلخواه خود (Notepad یا VS Code) باز کنید:
```powershell
notepad .env
```
محتوای آن را بررسی و ذخیره کنید:
```env
# تنظیمات اصلی جنگو
DJANGO_SECRET_KEY="یک_کلید_محرمانه_تصادفی"
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

# دسترسی به مدل‌های هوش مصنوعی Groq
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b
PYDANTIC_AI_NO_BANNER=1
```

> 💡 **تولید کلید امن جنگو در ویندوز:**
> می‌توانید با اجرای دستور زیر در ترمینال، یک کلید امن تصادفی تولید کرده و در فایل `.env` قرار دهید:
> ```powershell
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

---

### گام ششم: ساخت جداول دیتابیس (SQLite Migration)
دیتابیس پیش‌فرض پروژه فایل سبک و بدون نیاز به نصب SQLite است:
```powershell
python manage.py migrate
```
این دستور فایل `db.sqlite3` را در ریشه پروژه ایجاد کرده و تمام ساختارها را اعمال می‌کند.

---

### گام هفتم: ایجاد داده‌های نمونه و مقالات غنی (Seed Data)
برای ایجاد خودکار دسته‌بندی‌ها، تگ‌ها، مقالات فارسی جامع و کاربر ادمین پیش‌فرض:
```powershell
python manage.py seed_data
```

---

### گام هشتم: اجرای تست‌های سامانه (اختیاری)
جهت اطمینان از عملکرد بدون خطای تمام قسمت‌ها و ۱۴ متدولوژی آزمون:
```powershell
python manage.py test tests
```
*(تمامی تست‌ها باید با وضعیت `OK` پاس شوند).*

---

### گام نهم: راه‌اندازی وب‌سرور دَندی در ویندوز
سرور توسعه داخلی جنگو را روشن کنید:
```powershell
python manage.py runserver 127.0.0.1:8000
```
> 🔔 اگر فایروال ویندوز (Windows Defender Firewall) پیامی نشان داد، روی گزینه **Allow Access** کلیک کنید.

حال مرورگر خود را باز کرده و وارد سامانه شوید:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 👤 ۳. لینک‌ها و اطلاعات کاربری
- **صفحه اصلی مجله دَندی**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **پنل مدیریت جنگو**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **دستیار هوشمند چت**: [http://127.0.0.1:8000/assistant/](http://127.0.0.1:8000/assistant/)

جهت ایجاد یک کاربر مدیر جدید:
```powershell
python manage.py createsuperuser
```

---

## 🛠️ ۴. رفع اشکال و نکات اختصاصی ویندوز (Troubleshooting)

1. **خطای `'python' is not recognized as an internal or external command`:**
   - علت: پایتون به مسیر متغیرهای سیستمی (PATH) اضافه نشده است.
   - راه‌حل: نصاب پایتون را مجدداً اجرا کرده، گزینه Modify را انتخاب کنید و تیک **Add to PATH** را بزنید، سپس ترمینال را ببندید و مجدداً باز کنید.

2. **خطای خط مشی اجرای اسکریپت در پاورشل (`File cannot be loaded because running scripts is disabled`):**
   - راه‌حل: دستور زیر را یک‌بار در پاورشل با دسترسی کاربر فعلی اجرا کنید:
     ```powershell
     Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
     ```

3. **تداخل پورت ۸۰۰۰:**
   - در صورت اشغال بودن پورت ۸۰۰۰، پروژه را روی یک پورت دیگر ران کنید:
     ```powershell
     python manage.py runserver 127.0.0.1:8080
     ```
