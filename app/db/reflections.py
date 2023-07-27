""" Database operations for reflections. """
import uuid
from datetime import datetime

from sqlalchemy.future import select


from app.db.settings import async_session_maker
from app.db.models import UserResponse, ReflectionQuestion
from app.models.reflections import ReflectionModel


async def get_user_reflection(reflection_id: int, user_id: uuid.UUID):
    """Get a reflection from database"""
    async with async_session_maker() as session:
        stmt = (
            select(UserResponse)
            .where(UserResponse.user_id == user_id)
            .where(UserResponse.id == str(reflection_id))
        )
        result = await session.execute(stmt)
        my_reflection = result.scalars().first()
        return my_reflection


async def get_reflection_question(reflection_id: int):
    """Get a reflection from database"""
    async with async_session_maker() as session:
        stmt = select(ReflectionQuestion).where(ReflectionQuestion.id == reflection_id)
        result = await session.execute(stmt)
        my_reflection = result.scalars().first()
        return my_reflection


async def get_all_reflections(user_id: uuid.UUID):
    """Get all reflections from database"""
    async with async_session_maker() as session:
        stmt = select(UserResponse).where(UserResponse.user_id == user_id)
        result = await session.execute(stmt)
        my_reflections = result.scalars().all()
        return my_reflections


async def get_todays_reflections():
    """Get all this days reflections from database"""
    today = datetime.today().strftime("%Y-%m-%d")
    async with async_session_maker() as session:
        stmt = select(ReflectionQuestion).where(ReflectionQuestion.date == today)
        result = await session.execute(stmt)
        my_reflections = [x.__dict__ for x in result.scalars().all()]
        return my_reflections


async def create_reflection(reflection: ReflectionModel, user_id: uuid.UUID):
    """Insert new reflection into database"""
    async with async_session_maker() as session:
        new_reflection = UserResponse(
            question_id=reflection.question_id,
            response=reflection.answer,
            user_id=user_id,
        )
        session.add(new_reflection)
        await session.commit()
        await session.refresh(new_reflection)
    return new_reflection


async def delete_reflection(reflection_id: uuid.UUID, user_id: uuid.UUID):
    """Delete reflection from database"""
    async with async_session_maker() as session:
        stmt = (
            select(UserResponse)
            .where(UserResponse.id == str(reflection_id))
            .where(UserResponse.user_id == str(user_id))
        )
        result = await session.execute(stmt)
        reflection = result.scalars().first()
        await session.delete(reflection)
        await session.commit()
    return reflection


async def update_reflection(
    reflection_update: ReflectionModel, reflection_id: uuid.UUID, user_id: uuid.UUID
):
    """Update reflection status in database"""
    async with async_session_maker() as session:
        stmt = (
            select(UserResponse)
            .where(UserResponse.id == str(reflection_id))
            .where(UserResponse.user_id == str(user_id))
        )
        result = await session.execute(stmt)
        reflection = result.scalars().first()
        reflection.name = reflection_update.name
        reflection.author = reflection_update.author
        await session.commit()
        await session.refresh(reflection)


async def set_reflection_state(
    reflection_id: uuid.UUID, state: str, user_id: uuid.UUID
):
    """Update reflection status in database"""
    async with async_session_maker() as session:
        stmt = (
            select(UserResponse)
            .where(UserResponse.id == str(reflection_id))
            .where(UserResponse.user_id == str(user_id))
        )
        result = await session.execute(stmt)
        reflection = result.scalars().first()
        reflection.confirmed = state
        await session.commit()
        await session.refresh(reflection)
        return reflection
