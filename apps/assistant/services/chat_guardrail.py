import re
from typing import Optional


class ChatGuardrail:
    """
    Security and prompt guardrail protecting against prompt injection, database manipulation,
    and jailbreak attempts, providing deterministic, graceful canned responses.
    """

    # Patterns indicating attempts to manipulate database or wipe data
    DATABASE_MANIPULATION_PATTERNS = [
        r'پاک\s*کردن\s*دیتابیس',
        r'حذف\s*دیتابیس',
        r'دیتابیس.*پاک',
        r'دیتابیس.*حذف',
        r'حذف.*دیتابیس',
        r'اطلاعات.*دیتابیس.*پاک',
        r'اطلاعات.*دیتابیس.*حذف',
        r'بانک\s*داده.*پاک',
        r'بانک\s*داده.*حذف',
        r'drop\s+database',
        r'drop\s+table',
        r'delete\s+from',
        r'truncate\s+table',
        r'rm\s+-rf',
    ]

    # Patterns indicating attempts to reset memory, forget instructions or bypass context
    MEMORY_WIPE_PATTERNS = [
        r'پیام\s*های\s*قبلی.*فراموش',
        r'پیامهای\s*قبلی.*فراموش',
        r'پیام\s*های\s*قبلی.*پاک',
        r'حافظه.*پاک\s*کن',
        r'حافظه‌ات\s*را\s*پاک',
        r'دستورات\s*قبلی.*فراموش',
        r'دستورات\s*قبلی.*نادیده',
        r'ignore\s+all\s+previous\s+instructions',
        r'forget\s+all\s+previous\s+instructions',
        r'forget\s+everything',
        r'reset\s+memory',
    ]

    # Patterns indicating jailbreaks or prompt extraction
    JAILBREAK_PATTERNS = [
        r'system\s*prompt',
        r'پرامپت\s*سیستمی',
        r'دستورات\s*سیستمی.*نشان',
        r'developer\s*mode',
        r'dan\s*mode',
        r'jailbreak',
        r'ignore\s+rules',
    ]

    CANNED_DB_RESPONSE = (
        "من اینجام تا با هم درباره ایده‌ها و مقاله‌های دَندی گپ بزنیم و چیزی رو از ریشه پاک نمی‌کنم! دیتابیس هم جاش کاملاً امنه. 😉\n\n"
        "اگه می‌خوای یه گفتگوی تمیز و تازه از اول شروع کنیم، کافیه روی دکمه **«گفتگوی جدید»** در بالای صفحه بزنی.\n\n"
        "حالا بگو ببینم، امروز ذهنت درگیر چه موضوعیه تا بریم سراغ جذاب‌ترین مقاله‌هاش؟"
    )

    CANNED_MEMORY_RESPONSE = (
        "اگه می‌خوای گفتگوهای قبلی رو بذاریم کنار و از نو شروع کنیم، دکمه **«گفتگوی جدید»** در بالای صفحه دقیقاً برای همینه! با یک کلیک یه صفحه سفید و آماده باز می‌شه. ✨\n\n"
        "دوست داری درباره چی شروع کنیم؟ هوش مصنوعی، فلسفه زندگی یا معماری؟"
    )

    CANNED_JAILBREAK_RESPONSE = (
        "من رفیق و راهنمای جستارهای دَندی هستم و فقط توی همین مدار جذاب حرکت می‌کنم! 😎\n\n"
        "بیا به جای این دستورات، بریم سراغ یه بحث عمیق و خفن فکری؛ چه موضوعی برات جالب‌تره؟"
    )

    @classmethod
    def evaluate_message(cls, message: str) -> Optional[str]:
        """
        Evaluates incoming message against security and guardrail rules.
        Returns a canned response if a violation is detected, or None if safe to proceed.
        """
        text = message.strip()

        # 1. Check database manipulation attempts
        for pattern in cls.DATABASE_MANIPULATION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return cls.CANNED_DB_RESPONSE

        # 2. Check memory wipe attempts
        for pattern in cls.MEMORY_WIPE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return cls.CANNED_MEMORY_RESPONSE

        # 3. Check jailbreak / prompt extraction attempts
        for pattern in cls.JAILBREAK_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return cls.CANNED_JAILBREAK_RESPONSE

        return None
