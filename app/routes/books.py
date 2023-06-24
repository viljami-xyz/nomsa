"""
    _summary_: This file contains the routes for the books API.
    _description_: The books API allows users to create, read, update, and delete books.

    """

from fastapi import routing, Request, Depends
from fastapi.templating import Jinja2Templates

from app.models.books import NewBook
from app.models.utils import as_form
from app.db.models import User
from app.services.authentication import current_active_user

templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/books", tags=["books"])


@router.get("/")
async def books(request: Request, user: User = Depends(current_active_user)):
    """books page"""
    return templates.TemplateResponse(
        "books/index.html",
        {"request": request, "user": user},
    )


@router.post("/new", responses={200: {"model": NewBook}})
async def new_book(
    request: Request,
    form: NewBook = Depends(NewBook.as_form),
    user: User = Depends(current_active_user),
):
    """Insert new book into database"""
    name = form.name
    author = form.author
    if name is None or author is None:
        return {"message": "Invalid form data"}
    return NewBook(author=author, name=name)
