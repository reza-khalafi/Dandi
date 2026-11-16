import json
from django.views import View
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from pydantic import ValidationError

from apps.assistant.schemas.chat_request import ChatRequest
from apps.assistant.services.assistant_service import (
    AssistantService,
    RateLimitExceededException,
)


class ChatApiView(LoginRequiredMixin, View):
    """
    JSON API endpoint for sending a message to the Dandi AI Assistant and receiving recommendations.
    Enforces authentication, rate limits, and multi-turn context.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            body = json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({'error': 'قالب داده ارسالی نامعتبر است.'}, status=400)

        try:
            chat_request = ChatRequest(**body)
        except ValidationError as err:
            return JsonResponse({'error': err.errors()}, status=422)

        try:
            chat_response = AssistantService.process_chat_message(
                user=request.user,
                raw_message=chat_request.message,
                conversation_id=chat_request.conversation_id,
            )
            return JsonResponse(chat_response.model_dump(), status=200)

        except RateLimitExceededException as rate_err:
            response = JsonResponse({
                'error': f'به دلیل رعایت سقف مصرف مجاز، لطفاً پس از {rate_err.retry_after} ثانیه مجدداً تلاش فرمایید.'
            }, status=429)
            response['Retry-After'] = str(rate_err.retry_after)
            return response
