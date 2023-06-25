""" Database models """

import uuid

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy import Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    """Base class for ORM models"""



book_user = Table(

    "book_user",

    Base.metadata,

    Column("book_id", Integer, ForeignKey("books.book_id")),

    Column("id", Integer, ForeignKey("user.id")),

)



class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model"""

    username = Column(String)
    
    books = relationship("Book",secondary=book_user,back_populates="user")


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    """Access token model"""



class Book(Base):
    """Book model"""

    __tablename__ = "books"
    book_id = Column(String, primary_key=True, index=True)
    user_id = Column( ForeignKey("user.id"))
    name = Column(String)
    author = Column(String)

    user = relationship("User",secondary=book_user ,back_populates="books")
