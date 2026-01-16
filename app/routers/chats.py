from fastapi import APIRouter

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("/")
async def read_chat():
    """
    Возвращает чат и последние N сообщений
    """
    pass


@router.post("/")
async def create_chat():
    """
    Создает новый чат
    """
    pass


@router.post("/{chat_id}/messages")
async def create_message():
    """
    Создает сообщение в чат
    """
    pass


@router.delete('/{chat_id}')
async def delete_chat():
    """
    Удаляет чат со всеми его сообщениями
    """