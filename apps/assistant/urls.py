from django.urls import path
from apps.assistant.views.chat_page_view import ChatPageView
from apps.assistant.views.chat_api_view import ChatApiView
from apps.assistant.views.new_chat_api_view import NewChatApiView
from apps.assistant.views.guide_page_view import GuidePageView
from apps.assistant.views.delete_chat_api_view import DeleteChatApiView

app_name = 'assistant'

urlpatterns = [
    path('', ChatPageView.as_view(), name='chat'),
    path('guide/', GuidePageView.as_view(), name='guide'),
    path('api/chat/', ChatApiView.as_view(), name='api_chat'),
    path('api/new-chat/', NewChatApiView.as_view(), name='api_new_chat'),
    path('api/delete-chat/<int:conversation_id>/', DeleteChatApiView.as_view(), name='api_delete_chat'),
]
