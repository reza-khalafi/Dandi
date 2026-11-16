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
        "دستیار هوشمند دَندی صرفاً یک راهنمای فکری و گفتگومحور برای کاوش در مقالات است "
        "و هیچ‌گونه دسترسی به پایگاه داده یا ساختارهای زیربنایی سامانه ندارد. "
        "چنانچه مایلید گفتگوی خود را از ابتدا آغاز فرمایید، می‌توانید با کلیک بر روی دکمه «گفتگوی جدید» "
        "در بالای صفحه، حافظه نشست جاری را بازنشانی نمایید.\n\n"
        "مایلید درباره کدام موضوع از مقالات دَندی گفتگو کنیم؟"
    )

    CANNED_MEMORY_RESPONSE = (
        "برای بازنشانی حافظه گفتگو و شروع یک مکالمه تازه، لطفاً از دکمه **«گفتگوی جدید»** در بالای صفحه استفاده فرمایید. "
        "این عمل به شما امکان می‌دهد بدون پیش‌زمینه گفتگوهای قبلی، مبحث جدیدی را آغاز نمایید.\n\n"
        "در چه موضوعی از مقالات دَندی می‌توانم راهنمای شما باشم؟"
    )

    CANNED_JAILBREAK_RESPONSE = (
        "دستیار هوشمند دَندی در چارچوب اصول تحریریه و مأموریت‌های علمی و فرهنگی مجله فعالیت می‌نماید. "
        "امکان تغییر نقش یا دسترسی به تنظیمات سیستمی وجود ندارد. "
        "خوشحال می‌شوم در زمینه موضوعات و جستارهای منتشرشده در مجله دَندی هم‌صحبت شما باشم."
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
