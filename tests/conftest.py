import pytest
import pytest_asyncio
import os
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.database import Base
from app.depends import get_async_db
from app.models.chats import Chat
from app.models.messages import Message


load_dotenv('.test.env', override=True)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "chat_user_test")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_NAME = os.getenv("DB_NAME", "chat_db_test")


DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

@pytest_asyncio.fixture()
async def async_db():
    engine = create_async_engine(
        DATABASE_URL_TEST,
        echo=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async with SessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest_asyncio.fixture()
async def client(async_db: AsyncSession):
    async def override_get_async_db():
        yield async_db  

    app.dependency_overrides[get_async_db] = override_get_async_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest_asyncio.fixture()
async def add_data_to_db(async_db: AsyncSession):
    for i in range(1, 4):
        chat = Chat(title=f'Chat {i}')
        for j in range(1, 4):
            message = Message(chat_id=i, text=f'text {i}.{j}')
            async_db.add(message)           
        async_db.add(chat)  
    await async_db.commit()
