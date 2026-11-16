import json
from django.views import View
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from pydantic import ValidationError
from apps.assistant.schemas.chat_request import ChatRequest
from apps.assistant.services.assistant_service import AssistantService


class ChatApiView(LoginRequiredMixin, View):
    """
    JSON API endpoint for sending a message to the Dandi AI Assistant and receiving recommendations.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            body = json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)

        try:
            chat_request = ChatRequest(**body)
        except ValidationError as err:
            return JsonResponse({'error': err.errors()}, status=422)

        chat_response = AssistantService.process_chat_message(
            user_id=request.user.id,
            username=request.user.username,
            user_message=chat_request.message,
        )

        return JsonResponse(chat_response.model_dump(), status=200)
