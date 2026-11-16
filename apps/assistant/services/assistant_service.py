import logging
from apps.assistant.agents.context import AssistantContext
from apps.assistant.agents.dandi_agent import dandi_agent
from apps.assistant.schemas.chat_response import ChatResponse

logger = logging.getLogger(__name__)


class AssistantService:
    """
    Business service layer managing user interactions with Dandi AI Agent.
    """

    @staticmethod
    def process_chat_message(user_id: int, username: str, user_message: str) -> ChatResponse:
        """
        Executes the agent run cycle with user context and returns structured response.
        """
        ctx = AssistantContext(user_id=user_id, username=username)

        try:
            result = dandi_agent.run_sync(user_message, deps=ctx)
            reply_text = result.output

            return ChatResponse(
                reply=reply_text,
                suggested_articles=ctx.recommended_articles
            )

        except Exception as exc:
            logger.exception("Error executing Dandi Assistant agent: %s", exc)
            fallback_message = (
                "متأسفانه در برقراری ارتباط با دستیار هوشمند خطایی رخ داد. "
                "لطفاً لحظاتی بعد مجدداً تلاش کنید."
            )
            return ChatResponse(
                reply=fallback_message,
                suggested_articles=[]
            )
