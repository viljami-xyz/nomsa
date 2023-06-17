"""
Main file to run the application with uvicorn
"""
from typing import AsyncGenerator


from fastapi import Depends
from fastapi.staticfiles import StaticFiles

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase


import uvicorn
from app.config.settings import Settings
from app.routes import authentication, home, books, diary, reflections
from app.db.models import Base, User
from app.db.settings import engine, async_session_maker


settings = Settings()

HOST = settings.host
PORT = int(settings.port)


app = home.app
app.include_router(authentication.router)
# app.include_router(authentication.router)
# app.include_router(books.router)
# app.include_router(diary.router)
# app.include_router(reflections.router)
# app.include_router(users.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def create_db_and_tables():
    """Create database and tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async session"""
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Get user database"""
    yield SQLAlchemyUserDatabase(session, User)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
