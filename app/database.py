#Асинхронное подключение к PostgreSQL

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv


# Строка подключения для PostgreSQl
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

async_engine = create_async_engine(DATABASE_URL, echo=True)

#Фабрика сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass