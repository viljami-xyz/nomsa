"""
    _summary_: This file contains the routes for the books API.
    _description_: The books API allows users to create, read, update, and delete books.

    """

from fastapi import routing, Request
from fastapi.templating import Jinja2Templates

from app.models.books import NewBook

templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/books", tags=["books"])


@router.get("/")
async def books(request: Request):
    """books page"""
    return templates.TemplateResponse(
        "books/index.html",
        {"request": request},
    )


@router.post("/new_book", responses={200: {"model": NewBook}})
async def new_book(request: Request):
    """Insert new book into database"""
    form = await request.form()
    name = form.get("name")
    author = form.get("author")
    if name is None or author is None:
        return {"message": "Invalid form data"}
    return NewBook(author=author, name=name)
