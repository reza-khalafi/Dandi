from pydantic import BaseModel, ConfigDict
from typing import Optional


class ArticleItem(BaseModel):
    """
    Structured data schema for an article recommended by the AI Assistant.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    summary: str
    reading_time: int
    category_name: str
    author_name: str
    url: str
    cover_image_url: Optional[str] = None
