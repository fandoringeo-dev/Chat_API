from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# Pydantic-модели для валидации данных


class Chat(BaseModel):
    """
    Модель для ответа с данными чата
    Используется в GET запросе
    """

    id: int = Field(..., description="Уникальный индификатор чата")
    title: str = Field(..., min_length=1, max_length=200, description="Название чата")
    created_at: datetime = Field(
        ..., default_factory=datetime.now, description="Дата и время создания"
    )

    model_config = ConfigDict(from_attributes=True)


class ChatCreate(BaseModel):
    """
    Модель для создания чата
    Используется в POST запросе. (Возможно использование для PUT запроса в будущем)
    """

    title: str = Field(..., min_length=1, max_length=200, description="Название чата")
    created_at: datetime = Field(
        ..., default_factory=datetime.now, description="Дата и время создания"
    )


class Message(BaseModel):
    """
    Модель для валидации данных сообщения
    """

    id: int = Field(..., description="Уникальный индификатор сообщения")
    сhat_id: int = Field(..., description="ID чата")
    text: str = Field(..., description="Текст сообщения")
    created_at: datetime = Field(
        ..., default_factory=datetime.now, description="Дата и время создания"
    )

    model_config = ConfigDict(from_attributes=True)
