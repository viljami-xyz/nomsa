""" Database settings and connection. """

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.settings import Settings

settings = Settings()

engine = create_async_engine(settings.testdb)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
