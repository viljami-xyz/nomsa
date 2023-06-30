"""_summary_: This file contains the models for the books API.
_description_: The books API allows users to create, read, update, and delete books.
    """


from pydantic import BaseModel, Field

from app.models.utils import as_form


@as_form
class BookModel(BaseModel):
    """_summary_: This class defines the model for new books."""

    author: str = Field(..., title="Author", description="Author of the book.")
    name: str = Field(..., title="Name", description="Name of the book.")
    type_of: str = Field("kindle", title="Type", description="Type of the book.")
    state: str = Field(
        "unread", title="State", description="Reading state of the book."
    )
