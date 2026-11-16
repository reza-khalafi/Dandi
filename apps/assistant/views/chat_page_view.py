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

        # Optional target conversation query param (?c=123)
        target_conv_id = None
        raw_c = self.request.GET.get('c')
        if raw_c and raw_c.isdigit():
            target_conv_id = int(raw_c)

        # Fetch conversation, up to 50 stored messages, and full user history
        conversation, existing_messages, user_conversations = AssistantService.get_conversation_history(
            user=user,
            conversation_id=target_conv_id
        )

        context['page_title'] = 'دستیار هوشمند دَندی'
        context['conversation'] = conversation
        context['existing_messages'] = existing_messages
        context['user_conversations'] = user_conversations
        context['sample_prompts'] = [
            'یک مقاله الهام‌بخش درباره تمرکز عمیق، فلسفه یا هنر آهستگی پیشنهاد بده.',
            'آیا مقاله‌ای درباره هوش مصنوعی یا کامپیوتر کوانتومی داری؟',
            'درباره معماری نرم‌افزار، مایکروسرویس‌ها یا تفکر سیستمی چه مقالاتی داری؟',
            'جستارهایی درباره روانشناسی تصمیم‌گیری و عادات اتمی به من معرفی کن.',
        ]
        return context
