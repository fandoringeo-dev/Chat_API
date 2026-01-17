from fastapi import HTTPException, Depends
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import async_session_maker

from app.models import Chat as ChatModel


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Предоставляет асинхронную сессию SQLAlchemy для работы с базой данных PostgreSQL.
    """
    async with async_session_maker() as session:
        yield session


async def get_chat(
    chat_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> ChatModel:
    """
    Проверка существования чата
    """
    chat = await db.scalar(select(ChatModel).where(ChatModel.id == chat_id))
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat
