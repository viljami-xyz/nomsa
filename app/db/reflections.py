""" Database operations for reflections. """
import uuid
from datetime import date, timedelta
from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.models import QuestionOfDay, QuestionPool, UserResponse
from app.db.settings import async_session_maker, session_maker
from app.models.reflections import (
    QuestionDateCard,
    QuestionPoolCard,
    UserResponseCard,
    UserResponseForm,
)


async def get_user_response(reflection_id: int, user_id: uuid.UUID) -> UserResponse:
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


async def get_user_response_list(
    id_list: List[int], user_id: uuid.UUID
) -> List[UserResponse]:
    """Return answer where question_id is found on id_list"""
    async with async_session_maker() as session:
        stmt = (
            select(UserResponse)
            .where(UserResponse.user_id == user_id)
            .where(UserResponse.question_id.in_(id_list))
        )
        result = await session.execute(stmt)
        my_reflections = result.scalars().all()
    return my_reflections


async def get_reflection_question(reflection_id: int) -> QuestionPoolCard:
    """Get a reflection from database"""
    async with async_session_maker() as session:
        stmt = select(QuestionOfDay).where(QuestionOfDay.id == reflection_id)
        result = await session.execute(stmt)
        my_reflection = result.scalars().first()
    return my_reflection


async def get_all_user_responses(user_id: uuid.UUID) -> List[UserResponse]:
    """Get all reflections from database"""
    async with async_session_maker() as session:
        stmt = select(UserResponse).where(UserResponse.user_id == user_id)
        result = await session.execute(
            stmt.options(selectinload(UserResponse.question))
        )
        my_reflections = result.scalars().all()
    return my_reflections


async def get_todays_reflections() -> List[QuestionDateCard]:
    """Get all this days reflections from database"""
    today = date.today()
    async with async_session_maker() as session:
        stmt = select(QuestionOfDay).where(QuestionOfDay.date == today)
        result = await session.execute(stmt)
        my_reflections = result.scalars().all()

    return my_reflections


async def get_all_reflections() -> List[QuestionDateCard]:
    """Get all this days reflections from database"""
    today = "2023-07-27"  # datetime.today().strftime("%Y-%m-%d")
    async with async_session_maker() as session:
        stmt = select(QuestionOfDay).where(QuestionOfDay.date == today)
        result = await session.execute(stmt)
        my_reflections = result.scalars().all()

    return my_reflections


async def create_user_response(
    reflection: UserResponseForm, user_id: uuid.UUID
) -> UserResponse:
    """Insert new reflection into database"""
    async with async_session_maker() as session:
        new_reflection = UserResponse(
            question_id=reflection.question_id,
            response=reflection.answer,
            user_id=user_id,
            confirmed=False,
        )
        session.add(new_reflection)
        await session.commit()
        await session.refresh(new_reflection)
    return new_reflection


async def delete_user_response(
    reflection_id: uuid.UUID, user_id: uuid.UUID
) -> UserResponse:
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


# async def update_user_response(
#     reflection_update: ReflectionModel, reflection_id: uuid.UUID, user_id: uuid.UUID
# ):
#     """Update reflection status in database"""
#     async with async_session_maker() as session:
#         stmt = (
#             select(UserResponse)
#             .where(UserResponse.id == str(reflection_id))
#             .where(UserResponse.user_id == str(user_id))
#         )
#         result = await session.execute(stmt)
#         reflection = result.scalars().first()
#         reflection.name = reflection_update.name
#         reflection.author = reflection_update.author
#         await session.commit()
#         await session.refresh(reflection)


async def set_user_response_states(
    reflection_id_list: List[int], state: bool, user_id: uuid.UUID
) -> List[UserResponse]:
    """Update reflection status in database"""
    async with async_session_maker() as session:
        stmt = (
            select(UserResponse)
            .where(UserResponse.question_id.in_(reflection_id_list))
            .where(UserResponse.user_id == str(user_id))
        )
        result = await session.execute(stmt)
        reflections = result.scalars().all()
        for reflection in reflections:
            reflection.confirmed = state
        await session.commit()
    return reflections


# SYNC FUNCTIONS


def create_question_pool(question: QuestionPool) -> None:
    """Insert new reflection into database"""
    with session_maker() as session:
        session.add(question)
        session.commit()
        session.refresh(question)
    return None


async def create_question_of_day(question: QuestionOfDay) -> None:
    """Insert new reflection into database"""
    async with async_session_maker() as session:
        session.add(question)
        await session.commit()
        await session.refresh(question)
    return None


async def get_question_pool() -> List[QuestionPool]:
    """Get question pool"""
    async with async_session_maker() as session:
        stmt = select(QuestionPool)
        result = await session.execute(stmt)
        question_pool = result.scalars().all()
    return question_pool


async def get_active_questions() -> List[QuestionOfDay]:
    """Get question pool"""
    last_week = date.today() - timedelta(days=7)
    async with async_session_maker() as session:
        stmt = select(QuestionOfDay).where(QuestionOfDay.date > last_week)
        result = await session.execute(stmt)
        question_pool = result.scalars().all()
    return question_pool
