from django.urls import path
from apps.assistant.views.chat_page_view import ChatPageView
from apps.assistant.views.chat_api_view import ChatApiView

app_name = 'assistant'

urlpatterns = [
    path('', ChatPageView.as_view(), name='chat'),
    path('api/chat/', ChatApiView.as_view(), name='api_chat'),
]
