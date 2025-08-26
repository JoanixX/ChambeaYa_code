from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

class ChatHistoryModel(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(11), nullable=False)
    message_order = Column(SmallInteger, nullable=False)
    message_role = Column(String(20), nullable=False)
    message = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())