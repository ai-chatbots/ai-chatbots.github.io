from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)

# New model for chat messages
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), index=True, nullable=False)
    sender = Column(String(50), nullable=False)  # "user" or "bot"
    message = Column(String(1024), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
