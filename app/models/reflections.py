""" This module defines models for reflections."""

import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from app.models.utils import as_form


@as_form
class UserResponseForm(BaseModel):
    """_summary_: This class defines the model for new reflections."""

    question_id: int = Field(
        ..., title="Question Id", description="Question Id of the day."
    )
    answer: str = Field(..., title="Answer", description="User's answer.")


class QuestionDateCard(BaseModel):
    """Summary: This class defines the model for reflections.
    Attributes:
    ----------
    id : int
        Question id.
    question_text : str
        Question text.
    category : str
        Category of question.
    date : date
        Date of question.
    """

    id: int
    question_text: str
    category: str
    date: date

    class Config:
        """ORM mode"""

        orm_mode = True


class UserResponseCard(BaseModel):
    """_summary_: This class defines the model for reflections."""

    id: int
    user_id: uuid.UUID
    question_id: int
    response: str
    confirmed: bool

    question: QuestionDateCard

    class Config:
        """ORM mode"""

        orm_mode = True


class QuestionPoolCard(BaseModel):
    """_summary_: This class defines the model for reflections."""

    id: int
    question_text: str
    category: str

    class Config:
        """ORM mode"""

        orm_mode = True
