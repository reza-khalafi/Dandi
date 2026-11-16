from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ChatPageView(LoginRequiredMixin, TemplateView):
    """
    Dedicated web interface for logged-in users to converse with Dandi AI Assistant.
    """
    template_name = 'assistant/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'دستیار هوشمند دَندی'
        context['sample_prompts'] = [
            'آیا مقاله‌ای درباره هوش مصنوعی یا کامپیوتر کوانتومی داری؟',
            'یک مقاله الهام‌بخش درباره تمرکز عمیق، فلسفه یا هنر آهستگی پیشنهاد بده.',
            'درباره معماری نرم‌افزار، مایکروسرویس‌ها یا تفکر سیستمی چه مقالاتی داری؟',
            'جستارهایی درباره روانشناسی تصمیم‌گیری و عادات اتمی به من معرفی کن.',
        ]
        return context
