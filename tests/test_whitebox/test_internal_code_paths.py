from unittest.mock import MagicMock
from django.test import TestCase
from django.contrib.auth.models import User
from pydantic_ai.messages import ModelRequest, ModelResponse
from apps.assistant.services.assistant_service import AssistantService
from apps.assistant.models.chat_message import ChatMessage
from apps.assistant.models.conversation import Conversation
from apps.assistant.repositories.conversation_repository import ConversationRepository
from apps.assistant.agents.context import AssistantContext
from apps.assistant.tools.article_search_tool import search_dandi_articles, MAX_RECOMMENDED_ARTICLES
from apps.articles.models.category import Category
from apps.articles.models.article import Article
from apps.articles.enums.article_status import ArticleStatus


class WhiteBoxTesting(TestCase):
    """
    White-Box Testing: Evaluates internal control flows, branch conditions, and private methods.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='whitebox_user', password='password123')
        self.conv = Conversation.objects.create(user=self.user, title='گفتگوی جدید')

    def test_sanitize_user_input_branches(self):
        # Branch 1: Normal short string
        s1 = AssistantService._sanitize_user_input("  سلام   ")
        self.assertEqual(s1, "سلام")

        # Branch 2: Null byte removal
        s2 = AssistantService._sanitize_user_input("hello\x00world")
        self.assertEqual(s2, "helloworld")

        # Branch 3: String exceeding MAX_MESSAGE_LENGTH (1200 chars)
        long_str = "x" * 1500
        s3 = AssistantService._sanitize_user_input(long_str)
        self.assertEqual(len(s3), AssistantService.MAX_MESSAGE_LENGTH)

    def test_build_model_message_history_branches(self):
        # Create user and assistant records
        msg1 = ChatMessage.objects.create(conversation=self.conv, sender='user', content='سوال کاربر')
        msg2 = ChatMessage.objects.create(conversation=self.conv, sender='assistant', content='پاسخ هوش مصنوعی')
        msg3 = ChatMessage.objects.create(conversation=self.conv, sender='system', content='پیام متفرقه')

        history = AssistantService._build_model_message_history([msg1, msg2, msg3])

        self.assertEqual(len(history), 2)
        self.assertIsInstance(history[0], ModelRequest)
        self.assertIsInstance(history[1], ModelResponse)

    def test_title_auto_generation_on_first_message(self):
        # When title is 'گفتگوی جدید' and user sends message, title is updated
        ConversationRepository.add_message(
            conversation=self.conv,
            sender='user',
            content='چگونه می‌توان در دنیای مدرن به تمرکز عمیق دست یافت؟'
        )
        self.conv.refresh_from_db()
        self.assertIn('چگونه می‌توان در دنیای مدرن', self.conv.title)

        # Subsequent messages should not overwrite the established title
        ConversationRepository.add_message(
            conversation=self.conv,
            sender='user',
            content='سوال دوم کاربر'
        )
        self.conv.refresh_from_db()
        self.assertIn('چگونه می‌توان در دنیای مدرن', self.conv.title)

    def test_tool_enforces_max_recommended_limit(self):
        cat = Category.objects.create(name='تست', slug='test-cat')
        for i in range(6):
            Article.objects.create(
                title=f'مقاله هوش مصنوعی شماره {i}',
                slug=f'ai-article-{i}',
                summary='خلاصه',
                content='متن',
                category=cat,
                author=self.user,
                status=ArticleStatus.PUBLISHED
            )

        ctx = AssistantContext(user_id=self.user.id, username=self.user.username)
        mock_run_ctx = MagicMock()
        mock_run_ctx.deps = ctx

        # Call tool with large limit request
        results = search_dandi_articles(mock_run_ctx, query='هوش مصنوعی', limit=10)

        # Must be capped strictly at MAX_RECOMMENDED_ARTICLES (3)
        self.assertLessEqual(len(results), MAX_RECOMMENDED_ARTICLES)
        self.assertLessEqual(len(ctx.recommended_articles), MAX_RECOMMENDED_ARTICLES)
