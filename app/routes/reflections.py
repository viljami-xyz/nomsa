"""
    _summary_: This file contains the routes for the reflections API.
    _description_: The reflections API allows users to create, read, update, and delete reflections.

    """
from fastapi import routing, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.db.models import User
from app.db.reflections import (
    get_all_reflections,
    get_todays_reflections,
    create_reflection,
    delete_reflection,
    get_user_reflection,
    get_reflection_question,
)
from app.services.authentication import current_active_user
from app.models.reflections import ReflectionModel

templates = Jinja2Templates(directory="templates")


router = routing.APIRouter()


@router.get("/", operation_id="reflections")
async def reflections(request: Request, user: User = Depends(current_active_user)):
    """reflections page"""
    todays_questions = await get_todays_reflections()
    return templates.TemplateResponse(
        "reflections/index.html",
        {"request": request, "user": user, "questions": todays_questions},
    )


@router.get("/question/{question_id}")
async def get_question(
    request: Request,
    question_id: int = 0,
    _user: User = Depends(current_active_user),
):
    """Get a random question from the database"""

    todays_questions = await get_todays_reflections()
    if question_id == 0:
        question = todays_questions[0]
    elif question_id not in [x["id"] for x in todays_questions]:
        question = {"id": "-1", "text": "All done!"}
    else:
        question = [x for x in todays_questions if x["id"] == question_id][0]
    return templates.TemplateResponse(
        "reflections/questionInput.html", {"request": request, "question": question}
    )


@router.post("/question")
async def answer_question(
    request: Request,
    answer: str = Form(...),
    user: User = Depends(current_active_user),
):
    """Insert new reflection into database"""
    reflection = ReflectionModel(question_id=0, answer=answer)
    await create_reflection(reflection, user.id)
    return templates.TemplateResponse(
        "reflections/questionAnswer.html",
        context={"request": request, "answer": answer},
        status_code=200,
    )
