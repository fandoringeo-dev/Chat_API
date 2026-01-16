from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Text, ForeignKey
from datetime import datetime

from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text(2000), nullable=False)
    created_at: datetime = mapped_column(DateTime)

    chat = Mapped["Chat"] = relationship(back_populates="chats")