"""
    _summary_: This file contains the routes for the books API.
    _description_: The books API allows users to create, read, update, and delete books.

    """
import uuid

from fastapi import routing, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.models.books import BookModel
from app.db.models import User
from app.services.authentication import current_active_user

from app.db.books import (
    create_book,
    get_books,
    delete_book,
    update_book,
    get_book,
    set_book_state,
)

templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/books", tags=["books"])


@router.get("/")
async def books(request: Request, user: User = Depends(current_active_user)):
    """books page"""
    user_books = await get_books(user.id)
    return templates.TemplateResponse(
        "books/index.html",
        {"request": request, "user": user, "books": user_books},
    )


@router.post("/new")
async def new_book(
    request: Request,
    form: BookModel = Depends(BookModel.as_form),
    user: User = Depends(current_active_user),
):
    """Insert new book into database"""
    await create_book(form, user.id)
    user_books = await get_books(user.id)
    return templates.TemplateResponse(
        "books/bookList.html",
        {
            "request": request,
            "books": user_books,
            "message": {"status": "success", "text": "Book added successfully!"},
        },
    )


@router.get("/{book_id}")
async def open_book_view(
    request: Request, book_id: uuid.UUID, user: User = Depends(current_active_user)
):
    """Get the book that matches the book_id"""
    book_card = await get_book(book_id=book_id, user_id=user.id)
    return templates.TemplateResponse(
        "books/editBook.html", {"request": request, "book": book_card}
    )


@router.delete("/{book_id}")
async def delete_book_from_db(
    request: Request, book_id: uuid.UUID, user: User = Depends(current_active_user)
):
    """Delete book from database"""
    await delete_book(book_id=book_id, user_id=user.id)
    user_books = await get_books(user.id)
    return templates.TemplateResponse(
        "books/bookList.html",
        {"request": request, "books": user_books},
    )


@router.post("/{book_id}/edit")
async def update_book_in_db(
    request: Request,
    book_id: uuid.UUID,
    form: BookModel = Depends(BookModel.as_form),
    user: User = Depends(current_active_user),
):
    """Update book in database"""
    await update_book(form, book_id, user.id)
    user_books = await get_books(user.id)

    return templates.TemplateResponse(
        "books/index.html",
        {"request": request, "books": user_books},
    )


@router.post("/{book_id}/state")
async def update_book_state(
    request: Request,
    book_id: uuid.UUID,
    state: str = Form(..., title="State", description="Reading state of the book."),
    user: User = Depends(current_active_user),
):
    """Update book in database"""
    book = await set_book_state(state=state, book_id=book_id, user_id=user.id)

    return HTMLResponse(f"State: {book.state}", status_code=200)
