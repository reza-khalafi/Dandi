import json
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.models import User
from apps.assistant.models.conversation import Conversation
from apps.assistant.models.chat_message import ChatMessage
from apps.assistant.schemas.chat_response import ChatResponse
from apps.assistant.schemas.article_item import ArticleItem


class IntegrationFlowTest(TestCase):
    """
    Integration Testing: Tests end-to-end interactions between views, repositories, and services.
    """

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='integrator', password='StrongPassword123!')
        self.chat_api_url = reverse('assistant:api_chat')
        self.new_chat_url = reverse('assistant:api_new_chat')

    def tearDown(self):
        cache.clear()

    @patch('apps.assistant.agents.dandi_agent.dandi_agent.run_sync')
    def test_full_assistant_dialogue_integration(self, mock_agent_run):
        self.client.login(username='integrator', password='StrongPassword123!')

        # Mock LLM Agent run return
        mock_result = type('AgentResult', (), {'output': 'پاسخ تحلیلی درباره فلسفه و علم.'})()
        mock_agent_run.return_value = mock_result

        # 1. Send first message
        res1 = self.client.post(
            self.chat_api_url,
            data=json.dumps({'message': 'درباره فلسفه رواقی‌گری چه دیدگاهی داری؟'}),
            content_type='application/json'
        )
        self.assertEqual(res1.status_code, 200)

        # Verify database integration: conversation & messages created
        conv = Conversation.objects.filter(user=self.user, is_active=True).first()
        self.assertIsNotNone(conv)
        self.assertEqual(conv.messages.count(), 2)  # 1 User + 1 Assistant
        self.assertEqual(conv.messages.first().sender, ChatMessage.SenderChoices.USER)
        self.assertEqual(conv.messages.last().sender, ChatMessage.SenderChoices.ASSISTANT)

        # 2. Start new chat session via API
        res_new = self.client.post(self.new_chat_url)
        self.assertEqual(res_new.status_code, 200)

        # Verify old conversation is archived (is_active=False) and new one created
        old_conv = Conversation.objects.get(pk=conv.id)
        self.assertFalse(old_conv.is_active)

        active_conv = Conversation.objects.filter(user=self.user, is_active=True).first()
        self.assertIsNotNone(active_conv)
        self.assertNotEqual(old_conv.id, active_conv.id)
