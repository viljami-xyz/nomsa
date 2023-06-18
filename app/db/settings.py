""" Database settings and connection. """

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.settings import Settings
from app.db.models import Base

settings = Settings()

engine = create_async_engine(settings.testdb)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    """Create database and tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
