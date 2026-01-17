from pydantic import BaseModel, Field, ConfigDict, StringConstraints
from datetime import datetime

# Pydantic-модели для валидации данных


class ChatOut(BaseModel):
    """
    Модель для ответа с данными чата
    Используется в модели ChatWithMessage
    """

    id: int = Field(..., description="Уникальный индификатор чата")
    title: str = Field(..., min_length=1, max_length=200, description="Название чата")
    created_at: datetime = Field(default_factory=datetime.now, description="Дата и время создания")
    
    model_config = ConfigDict(from_attributes=True)

class ChatCreate(BaseModel):
    """
    Модель для создания чата
    Используется в POST запросе. (Возможно использование для PUT запроса в будущем)
    """

    title: str = Field(..., min_length=1, max_length=200, description="Название чата, длина до 200 символов")



class MessageOut(BaseModel):
    """
    Модель для данных сообщения
    """

    id: int = Field(description="Уникальный индификатор сообщения")
    chat_id: int = Field(..., description="ID чата")
    text: str = Field(..., max_length=5000, description="Текст сообщения, до 5000 символов")
    created_at: datetime = Field(default_factory=datetime.now, description="Дата и время создания")

    model_config = ConfigDict(from_attributes=True)


class ChatWithMessage(BaseModel):
    """
    Модель для ответа в GET запросе
    """

    chat_data: ChatOut
    list_message: list[MessageOut]

    model_config = ConfigDict(from_attributes=True)
