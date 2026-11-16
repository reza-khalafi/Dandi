from django.views import View
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.assistant.services.assistant_service import AssistantService


class DeleteChatApiView(LoginRequiredMixin, View):
    """
    Endpoint to delete a specific conversation owned by the user.
    """

    def post(self, request: HttpRequest, conversation_id: int) -> HttpResponse:
        success = AssistantService.delete_conversation(request.user, conversation_id)
        if success:
            return JsonResponse({'status': 'success', 'message': 'گفتگو با موفقیت حذف شد.'}, status=200)
        return JsonResponse({'error': 'گفتگوی مورد نظر یافت نشد.'}, status=404)
