from dataclasses import dataclass, field
from apps.assistant.schemas.article_item import ArticleItem


@dataclass
class AssistantContext:
    """
    Context and dependencies injected into the Pydantic AI agent and its tools.
    """
    user_id: int
    username: str
    recommended_articles: list[ArticleItem] = field(default_factory=list)
