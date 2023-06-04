"""_summary_: This file contains the models for the books API.
_description_: The books API allows users to create, read, update, and delete books.
    """
from typing import List, Optional, Dict, Any
from urllib.parse import parse_qs
from pydantic import BaseModel, Field
from fastapi import Form


class NewBook(BaseModel):
    """_summary_: This class defines the model for new books."""

    author: str = Field(..., title="Author", description="Author of the book.")
    name: str = Field(..., title="Name", description="Name of the book.")
