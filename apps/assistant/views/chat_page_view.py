from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.assistant.services.assistant_service import AssistantService


class ChatPageView(LoginRequiredMixin, TemplateView):
    """
    Dedicated web interface for logged-in users to converse with Dandi AI Assistant.
    Provides persistent conversation history across page refreshes.
    """
    template_name = 'assistant/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetch active conversation and up to 50 stored messages (Long-term memory)
        conversation, existing_messages = AssistantService.get_conversation_history(user)

        context['page_title'] = 'دستیار هوشمند دَندی'
        context['conversation'] = conversation
        context['existing_messages'] = existing_messages
        context['sample_prompts'] = [
            'یک مقاله الهام‌بخش درباره تمرکز عمیق، فلسفه یا هنر آهستگی پیشنهاد بده.',
            'آیا مقاله‌ای درباره هوش مصنوعی یا کامپیوتر کوانتومی داری؟',
            'درباره معماری نرم‌افزار، مایکروسرویس‌ها یا تفکر سیستمی چه مقالاتی داری؟',
            'جستارهایی درباره روانشناسی تصمیم‌گیری و عادات اتمی به من معرفی کن.',
        ]
        return context
