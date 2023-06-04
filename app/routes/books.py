"""
    _summary_: This file contains the routes for the books API.
    _description_: The books API allows users to create, read, update, and delete books.

    """
from typing import Optional, List, Dict, Any

from fastapi import routing, Depends, HTTPException, status, Request, Form, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field

from app.models.books import NewBook

templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/books", tags=["books"])


@router.get("/", operation_id="books")
async def books(request: Request):
    """books page"""
    return templates.TemplateResponse(
        "books/index.html",
        {"request": request},
    )


@router.post("/new")
async def new_book(name: str = Form(...), author: str = Form(...)):
    """Insert new book into database"""
    print(name, author)
    return {"message": "New book created successfully."}
