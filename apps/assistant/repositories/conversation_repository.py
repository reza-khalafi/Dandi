from typing import Optional
from django.contrib.auth.models import User
from apps.assistant.models.conversation import Conversation
from apps.assistant.models.chat_message import ChatMessage


class ConversationRepository:
    """
    Database access layer for assistant conversations and messages.
    """

    @staticmethod
    def get_or_create_active_conversation(user: User) -> Conversation:
        """
        Retrieves the user's latest active conversation or creates a new one.
        """
        conversation = (
            Conversation.objects
            .filter(user=user, is_active=True)
            .order_by('-updated_at')
            .first()
        )

        if not conversation:
            conversation = Conversation.objects.create(
                user=user,
                title='گفتگوی جدید',
                is_active=True
            )

        return conversation

    @staticmethod
    def start_new_conversation(user: User) -> Conversation:
        """
        Archives current active conversations and begins a fresh conversation session.
        """
        Conversation.objects.filter(user=user, is_active=True).update(is_active=False)
        return Conversation.objects.create(
            user=user,
            title='گفتگوی جدید',
            is_active=True
        )

    @staticmethod
    def add_message(
        conversation: Conversation,
        sender: str,
        content: str,
        suggested_articles_data: Optional[list] = None
    ) -> ChatMessage:
        """
        Appends a message to the conversation and updates conversation timestamp.
        """
        message = ChatMessage.objects.create(
            conversation=conversation,
            sender=sender,
            content=content,
            suggested_articles_data=suggested_articles_data or []
        )
        conversation.save()  # Auto updates updated_at

        # If it's the first user message, use it to generate a readable title
        if sender == ChatMessage.SenderChoices.USER and conversation.title == 'گفتگوی جدید':
            clean_title = content.strip().replace('\n', ' ')
            conversation.title = clean_title[:45] + ('...' if len(clean_title) > 45 else '')
            conversation.save(update_fields=['title'])

        return message

    @staticmethod
    def get_recent_messages(conversation: Conversation, limit: int = 50) -> list[ChatMessage]:
        """
        Retrieves up to `limit` recent messages for displaying in the chat window.
        """
        # Fetch descending then reverse to preserve chronological reading order
        messages = list(
            ChatMessage.objects
            .filter(conversation=conversation)
            .order_by('-created_at')[:limit]
        )
        messages.reverse()
        return messages

    @staticmethod
    def get_short_term_context(conversation: Conversation, limit: int = 15) -> list[ChatMessage]:
        """
        Retrieves the last `limit` messages to pass as context history to the LLM agent.
        """
        messages = list(
            ChatMessage.objects
            .filter(conversation=conversation)
            .order_by('-created_at')[:limit]
        )
        messages.reverse()
        return messages

    @staticmethod
    def get_user_conversations(user: User, limit: int = 50) -> list[Conversation]:
        """
        Retrieves all past conversations of the user ordered by most recently updated.
        """
        return list(
            Conversation.objects
            .filter(user=user)
            .order_by('-updated_at')[:limit]
        )

    @staticmethod
    def get_conversation_by_id(user: User, conversation_id: int) -> Optional[Conversation]:
        """
        Retrieves a specific conversation owned by the user.
        """
        try:
            return Conversation.objects.get(pk=conversation_id, user=user)
        except Conversation.DoesNotExist:
            return None

    @staticmethod
    def delete_conversation(user: User, conversation_id: int) -> bool:
        """
        Deletes a conversation owned by the user.
        """
        deleted_count, _ = Conversation.objects.filter(pk=conversation_id, user=user).delete()
        return deleted_count > 0
