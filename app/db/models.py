""" Database models """

from datetime import date

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class for ORM models"""


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    """Access token model"""


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model"""

    username = Column(String)


class UserResponse(Base):
    """Reflection model"""

    __tablename__ = "user_response"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("user.id"))
    question_id = Column(Integer, ForeignKey("reflection_question.id"), nullable=False)
    response = Column(String, nullable=True)
    confirmed = Column(Boolean, default=False)

    user = relationship("User", backref="user")
    question = relationship("ReflectionQuestion", backref="question")


class ReflectionQuestion(Base):
    """Qeustion model"""

    __tablename__ = "reflection_question"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(String, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, default=date.today(), nullable=False)
