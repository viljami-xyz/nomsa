""" This module defines models for reflections."""

from datetime import datetime
from pydantic import BaseModel, Field

from app.models.utils import as_form


@as_form
class ReflectionModel(BaseModel):
    """_summary_: This class defines the model for new reflections."""

    question: str = Field(..., title="Question", description="Question of the day.")
    answer: str = Field(..., title="Answer", description="User's answer.")
    timestamp: str = Field(
        datetime.now(), title="Timestamp", description="Timestamp for the reflection."
    )
