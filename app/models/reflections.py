""" This module defines models for reflections."""

from datetime import datetime
from pydantic import BaseModel, Field

from app.models.utils import as_form


@as_form
class ReflectionModel(BaseModel):
    """_summary_: This class defines the model for new reflections."""

    question_id: int = Field(
        ..., title="Question Id", description="Question Id of the day."
    )
    answer: str = Field(..., title="Answer", description="User's answer.")
