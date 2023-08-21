""" Database settings and connection. """

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import Settings
from app.db.models import Base

settings = Settings()

engine = create_async_engine(settings.testdb)
sync_engine = create_engine(settings.sync_testdb)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
session_maker = sessionmaker(sync_engine, expire_on_commit=False)


def create_db_and_tables():
    """Create database and tables"""
    Base.metadata.create_all(sync_engine)
