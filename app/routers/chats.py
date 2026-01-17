from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy import select, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.schemas import ChatOut, ChatCreate, MessageOut, ChatWithMessage
from app.models.chats import Chat as ChatModel
from app.models.messages import Message as MessageModel
from app.depends import get_async_db, get_chat


router = APIRouter(prefix="/chats", tags=["chats"])


@router.get(
    "/{chat_id}", response_model=ChatWithMessage, status_code=status.HTTP_200_OK
)
async def read_chat(
    chat: ChatModel = Depends(get_chat),
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Возвращает данные чата и последние limit сообщений
    """
    # Достаем limit сообщений к чату и сортируем по created_at
    result = await db.scalars(
        select(MessageModel)
        .where(MessageModel.chat_id == chat.id)
        .order_by(desc(MessageModel.created_at))
        .limit(limit)
    )
    messages = result.all()
    response = ChatWithMessage(chat_data=chat, list_message=messages)
    return response


@router.post("/", response_model=ChatOut, status_code=status.HTTP_201_CREATED)
async def create_chat(title: str, db: AsyncSession = Depends(get_async_db)):
    """
    Создает новый чат
    """
    new_chat = ChatModel(title=title.strip())
    db.add(new_chat)
    await db.commit()
    return new_chat


@router.post(
    "/{chat_id}/messages",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_message(
    text: str,
    chat: ChatModel = Depends(get_chat),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Создает сообщение в чат
    """
    new_message = MessageModel(text=text, chat_id=chat.id)
    db.add(new_message)
    await db.commit()
    return new_message


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat: ChatModel = Depends(get_chat), db: AsyncSession = Depends(get_async_db)
):
    """
    Удаляет чат по ID со всеми его сообщениями
    """
    await db.execute(delete(ChatModel).where(ChatModel.id == chat.id))
    await db.commit()
    return {'status': 'Сhat deleted'}