"""
    _summary_: This file contains the routes for the reflections API.
    _description_: The reflections API allows users to create, read, update, and delete reflections.

    """
from fastapi import routing, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
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


@router.get("/question/{question_id}")
async def get_question(
    request: Request,
    question_id: int = 0,
    _user: User = Depends(current_active_user),
):
    """Get a random question from the database"""
    if question_id > len(QUESTIONS) - 1:
        question = {"id": "-1", "text": "All done!"}
    question = QUESTIONS[int(question_id)]
    return templates.TemplateResponse(
        "reflections/questionInput.html", {"request": request, "question": question}
    )


@router.post("/question")
async def answer_question(
    request: Request,
    answer: str = Form(...),
    _user: User = Depends(current_active_user),
):
    """Insert new reflection into database"""
    return templates.TemplateResponse(
        "reflections/questionAnswer.html",
        context={"request": request, "answer": answer},
        status_code=200,
    )
