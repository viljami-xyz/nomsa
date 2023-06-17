""" Database models """


from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import Settings

settings = Settings()


class Base(DeclarativeBase):
    """Base class for ORM models"""


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model"""
