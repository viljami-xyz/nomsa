""" Database models """


from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for ORM models"""


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model"""

    username = Column(String)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    """Access token model"""
