from fastapi import FastAPI
from app.routers import chats

#Приложение FastAPI
app = FastAPI(title='FastAPI Чат')

#Подлючение маршрутов для чатов
app.include_router(chats.router)

# Корневой эндпоинт для проверки
@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "API ok"}