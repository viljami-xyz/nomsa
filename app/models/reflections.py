""" This module defines models for reflections."""

import uuid
from datetime import date

from pydantic import BaseModel, Field

from app.models.utils import as_form


@as_form
class ReflectionModel(BaseModel):
    """_summary_: This class defines the model for new reflections."""

    question_id: int = Field(
        ..., title="Question Id", description="Question Id of the day."
    )
    answer: str = Field(..., title="Answer", description="User's answer.")


class ReflectionQuestion(BaseModel):
    """_summary_: This class defines the model for reflections."""

    id: int
    question_text: str
    category: str
    date: date

    class Config:
        orm_mode = True


class ReflectionAnswer(BaseModel):
    """_summary_: This class defines the model for reflections."""

    id: int
    user_id: uuid.UUID
    question_id: int
    response: str
    confirmed: bool

    question: ReflectionQuestion

    class Config:
        orm_mode = True
