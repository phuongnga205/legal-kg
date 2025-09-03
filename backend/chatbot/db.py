# chatbot/db.py
import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL DB — mặc định SQLite (chat.db trong thư mục gốc)
DATABASE_URL = os.getenv("CHAT_DB_URL", "sqlite:///./chat.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Bảng lưu lịch sử chat
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), index=True)   # ID cuộc hội thoại
    role = Column(String(10))                     # "user" hoặc "assistant"
    lang = Column(String(5))                      # VN / EN / JP
    text = Column(Text)                           # nội dung tin nhắn
    meta = Column(Text, nullable=True)            # metadata (JSON string)
    ts = Column(DateTime, default=datetime.datetime.utcnow)  # thời gian

# Khởi tạo bảng
def init_db():
    Base.metadata.create_all(bind=engine)
