from django.views import View
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.assistant.services.assistant_service import AssistantService


class NewChatApiView(LoginRequiredMixin, View):
    """
    Endpoint to archive current chat and initiate a new conversation.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        new_conv = AssistantService.start_new_session(request.user)
        return JsonResponse({
            'status': 'success',
            'conversation_id': new_conv.id,
            'title': new_conv.title,
            'message': 'گفتگوی جدید با موفقیت آغاز شد.'
        }, status=200)
