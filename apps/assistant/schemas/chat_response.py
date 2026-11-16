from pydantic import BaseModel, Field
from apps.assistant.schemas.article_item import ArticleItem


class ChatResponse(BaseModel):
    """
    Schema for assistant response payload including conversation text and recommended articles.
    """
    reply: str = Field(..., description="Conversational reply in Persian")
    suggested_articles: list[ArticleItem] = Field(
        default_factory=list,
        description="List of articles discovered and recommended by assistant tools"
    )
