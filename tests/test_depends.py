import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models import Chat 
from app.depends import get_chat

# ====== Тесты для get_chat ======

@pytest.mark.asyncio
async def test_get_chat_exists(async_db: AsyncSession, add_data_to_db):
    """
    Тест: Если чат существует в БД, функция должна вернуть его данные
    """
    # Вызываем функцию для чата id = 2
    result = await get_chat(chat_id=2, db=async_db)
    assert result.title == "Chat 2"
    


@pytest.mark.asyncio
async def test_get_chat_not_found(async_db: AsyncSession):
    """
    Тест: Если чата нет, функция должна выбросить HTTPException 404
    """
    # ACT + ASSERT: Проверяем исключение
    with pytest.raises(HTTPException) as exc_info:
        await get_chat(chat_id=999, db=async_db)
    
    # Проверяем статус код и сообщение
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Chat not found"

