"""
    _summary_: This file contains the routes for the reflections API.
    _description_: The reflections API allows users to create, read, update, and delete reflections.

    """
from fastapi import routing, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from app.db.models import User
from app.services.authentication import current_active_user

templates = Jinja2Templates(directory="templates")


router = routing.APIRouter()

QUESTIONS = [
    {"id": "0", "text": "What good happened today?"},
    {"id": "1", "text": "Appreciation moment?"},
    {"id": "2", "text": "What would you change?"},
]


@router.get("/", operation_id="reflections")
async def reflections(request: Request, user: User = Depends(current_active_user)):
    """reflections page"""
    return templates.TemplateResponse(
        "reflections/index.html",
        {"request": request, "user": user, "questions": QUESTIONS},
    )


@router.post("/new")
async def new_reflection(
    request: Request,
    good: str = Form(...),
    smile: str = Form(...),
    other: str = Form(...),
    user: User = Depends(current_active_user),
):
    """Insert new reflection into database"""
    print(good, smile, other)
    return {"message": "New reflection created successfully."}


@router.get("/question/{question_id}")
async def get_question(
    request: Request,
    question_id: int = 0,
    _user: User = Depends(current_active_user),
):
    """Get a random question from the database"""
    question = QUESTIONS[int(question_id)]
    print(question)
    return templates.TemplateResponse(
        "reflections/questionInput.html", {"request": request, "question": question}
    )


@router.post("/question/{question_id}")
async def answer_question(
    request: Request,
    question_id: int = 0,
    answer: str = Form(...),
    _user: User = Depends(current_active_user),
):
    """Insert new reflection into database"""
    print(question_id, answer)
    return {"message": "New reflection created successfully."}
