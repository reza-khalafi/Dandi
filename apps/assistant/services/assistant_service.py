import logging
from typing import Tuple
from django.contrib.auth.models import User
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, UserPromptPart, TextPart

from apps.assistant.agents.context import AssistantContext
from apps.assistant.agents.dandi_agent import dandi_agent
from apps.assistant.models.chat_message import ChatMessage
from apps.assistant.models.conversation import Conversation
from apps.assistant.repositories.conversation_repository import ConversationRepository
from apps.assistant.schemas.chat_response import ChatResponse
from apps.assistant.services.rate_limiter import ChatRateLimiter
from apps.assistant.services.chat_guardrail import ChatGuardrail

logger = logging.getLogger(__name__)


class RateLimitExceededException(Exception):
    """Raised when user exceeds rate limits."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")


class AssistantService:
    """
    Business service layer managing conversations, rate limits, multi-turn memory, and agent runs.
    """
    MAX_MESSAGE_LENGTH = 1200
    SHORT_TERM_MEMORY_TURNS = 15
    LONG_TERM_DISPLAY_LIMIT = 50

    @classmethod
    def process_chat_message(cls, user: User, raw_message: str) -> ChatResponse:
        """
        Processes a chat message with rate limiting, multi-turn memory injection, and database persistence.
        """
        # 1. Check rate limits (Throttling)
        is_allowed, retry_after = ChatRateLimiter.check_rate_limit(user.id)
        if not is_allowed:
            raise RateLimitExceededException(retry_after)

        # 2. Sanitize and validate input
        clean_message = cls._sanitize_user_input(raw_message)

        # 3. Retrieve or create active conversation
        conversation = ConversationRepository.get_or_create_active_conversation(user)

        # 4. Build short-term memory (last 15 messages) for LLM context continuity
        history_records = ConversationRepository.get_short_term_context(
            conversation,
            limit=cls.SHORT_TERM_MEMORY_TURNS
        )
        message_history = cls._build_model_message_history(history_records)

        # 5. Persist user's message in database
        ConversationRepository.add_message(
            conversation=conversation,
            sender=ChatMessage.SenderChoices.USER,
            content=clean_message
        )

        # 6. Apply Security Guardrail: Check for manipulation/wipe attempts and return canned response
        guardrail_response = ChatGuardrail.evaluate_message(clean_message)
        if guardrail_response:
            ConversationRepository.add_message(
                conversation=conversation,
                sender=ChatMessage.SenderChoices.ASSISTANT,
                content=guardrail_response,
                suggested_articles_data=[]
            )
            return ChatResponse(
                reply=guardrail_response,
                suggested_articles=[]
            )

        # 7. Execute Pydantic AI agent with multi-turn memory & dependency injection
        ctx = AssistantContext(user_id=user.id, username=user.username)

        try:
            agent_result = dandi_agent.run_sync(
                clean_message,
                message_history=message_history,
                deps=ctx
            )
            reply_text = agent_result.output

        except Exception as exc:
            logger.exception("Error executing Dandi Assistant agent for user %s: %s", user.username, exc)
            reply_text = (
                "متأسفانه در پردازش این پرسش خطایی رخ داد. "
                "لطفاً لحظاتی بعد مجدداً تلاش فرمایید یا پرسش خود را به شکلی دیگر بیان کنید."
            )

        # 7. Persist assistant response & suggested articles data in database (Long-term memory)
        # Cap recommendations strictly to 2-3 articles so user is not overwhelmed
        ctx.recommended_articles = ctx.recommended_articles[:3]
        suggested_articles_dicts = [a.model_dump() for a in ctx.recommended_articles]
        ConversationRepository.add_message(
            conversation=conversation,
            sender=ChatMessage.SenderChoices.ASSISTANT,
            content=reply_text,
            suggested_articles_data=suggested_articles_dicts
        )

        return ChatResponse(
            reply=reply_text,
            suggested_articles=ctx.recommended_articles
        )

    @classmethod
    def get_conversation_history(cls, user: User) -> Tuple[Conversation, list[ChatMessage]]:
        """
        Returns active conversation and up to 50 recent messages for web display.
        """
        conversation = ConversationRepository.get_or_create_active_conversation(user)
        messages = ConversationRepository.get_recent_messages(
            conversation,
            limit=cls.LONG_TERM_DISPLAY_LIMIT
        )
        return conversation, messages

    @classmethod
    def start_new_session(cls, user: User) -> Conversation:
        """
        Archives current conversation and starts a clean conversation session.
        """
        return ConversationRepository.start_new_conversation(user)

    @classmethod
    def _sanitize_user_input(cls, text: str) -> str:
        """
        Cleans user text and enforces length caps to guard against prompt overflow attacks.
        """
        cleaned = text.strip().replace('\x00', '')
        if len(cleaned) > cls.MAX_MESSAGE_LENGTH:
            cleaned = cleaned[:cls.MAX_MESSAGE_LENGTH]
        return cleaned

    @classmethod
    def _build_model_message_history(cls, records: list[ChatMessage]) -> list[ModelMessage]:
        """
        Converts stored Django ChatMessage records into Pydantic AI ModelMessage representations.
        """
        history: list[ModelMessage] = []
        for rec in records:
            if rec.sender == ChatMessage.SenderChoices.USER:
                history.append(ModelRequest(parts=[UserPromptPart(content=rec.content)]))
            elif rec.sender == ChatMessage.SenderChoices.ASSISTANT:
                history.append(ModelResponse(parts=[TextPart(content=rec.content)]))
        return history
