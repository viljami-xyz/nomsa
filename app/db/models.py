""" Database models """

import uuid
from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy import Column, String, ForeignKey, Integer, Table, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    """Base class for ORM models"""


reflection_user = Table(
    "reflection_user",
    Base.metadata,
    Column("reflection_id", Integer, ForeignKey("reflections.reflection_id")),
    Column("id", Integer, ForeignKey("user.id")),
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model"""

    username = Column(String)

    reflections = relationship(
        "Reflection", secondary=reflection_user, back_populates="user"
    )


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    """Access token model"""


class Reflection(Base):
    """Reflection model"""

    __tablename__ = "reflections"
    reflection_id = Column(String, primary_key=True, index=True)
    user_id = Column(ForeignKey("user.id"))
    question = Column(String)
    answer = Column(String)
    confirmed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow())

    user = relationship("User", secondary=reflection_user, back_populates="reflections")


class ReflectQuestion(Base):
    """Qeustion model"""

    __tablename__ = "questions"
    id = Column(String, primary_key=True, index=True)
    question = Column(String)
    category = Column(String)
