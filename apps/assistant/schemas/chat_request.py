from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Schema for validating incoming chat messages from the user.
    """
    message: str = Field(..., min_length=1, max_length=2000, description="User question or prompt")
