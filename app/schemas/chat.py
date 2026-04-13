from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, example="Расскажи о FastAPI")
    system: Optional[str] = Field(
        None, example="Ты полезный ассистент, отвечай кратко."
    )
    max_history: Optional[int] = Field(10, ge=0, description="Количество последних сообщений из истории")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    answer: str


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}