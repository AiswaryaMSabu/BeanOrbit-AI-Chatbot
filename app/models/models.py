# app/models/models.py

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()


class Application(Base):
    """
    Table to store application details and status.
    """
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(String(50), unique=True, index=True, nullable=False)
    student_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)


class UserQuery(Base):
    """
    Table to store user queries (minimum requirement).
    """
    __tablename__ = "user_queries"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class ChatHistory(Base):
    """
    Table to store complete chat history including bot responses.
    Optional but recommended for production readiness.
    """
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
