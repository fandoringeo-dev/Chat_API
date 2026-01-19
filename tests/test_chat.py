import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from httpx import AsyncClient
from sqlalchemy import select

from app.models.chats import Chat
from app.models.messages import Message

@pytest.mark.asyncio
async def test_read_chat(client: AsyncClient, async_db: AsyncSession, add_data_to_db):
    """
    Тест эндпоинта GET
    """
    result = await client.get('/chats/1')
    chat_data: Chat = result.json()['chat_data']
    assert chat_data['id'] == 1
    assert result.status_code == 200
    


@pytest.mark.asyncio
async def test_delete_chat(client: AsyncClient, async_db: AsyncSession, add_data_to_db):
    """
    Тест эндпоинта DELETE c проверкой каскадного удаления сообщений
    """
    # Удаляем первый чат
    result = await client.delete('/chats/1')
    assert result.status_code == 204

    # Делаем запрос на сообщения с текстом "text 1.% и проверяем что он пустой"
    stmt = await async_db.scalars(select(Message).where(Message.text.like('text 1.%')))
    result = stmt.all()
    assert not result 
    
