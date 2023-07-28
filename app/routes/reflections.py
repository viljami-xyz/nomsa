"""
    _summary_: This file contains the routes for the reflections API.
    _description_: The reflections API allows users to create, read, update,
    and delete reflections.

    """

from fastapi import Depends, Form, Request, routing
from fastapi.templating import Jinja2Templates

from app.db.models import User
from app.db.reflections import (
    create_reflection,
    get_reflection_question,
    get_todays_reflections,
    get_user_reflection_list,
)
from app.models.reflections import ReflectionModel
from app.services.authentication import current_active_user

templates = Jinja2Templates(directory="templates")
router = routing.APIRouter()


@router.get("/", operation_id="reflections")
async def reflections(request: Request, user: User = Depends(current_active_user)):
    """reflections page"""
    todays_questions = await get_todays_reflections()
    id_list = [question.id for question in todays_questions]
    users_answers = await get_user_reflection_list(id_list, user.id)
    users_answers = {answer.question_id: answer.response for answer in users_answers}
    first_question_id = todays_questions[0].id
    return templates.TemplateResponse(
        "reflections/index.html",
        {
            "request": request,
            "user": user,
            "questions": todays_questions,
            "answers": users_answers,
            "show_id": first_question_id,
        },
    )


@router.get("/question/{question_id}")
async def get_question(
    request: Request,
    question_id: int = 0,
    _: User = Depends(current_active_user),
):
    """Get a random question from the database"""

    todays_question_by_id = await get_reflection_question(question_id)
    return templates.TemplateResponse(
        "reflections/questionInput.html",
        {"request": request, "question": todays_question_by_id, "show_id": question_id},
    )


@router.post("/question")
async def answer_question(
    request: Request,
    answer: str = Form(...),
    question_id: int = Form(...),
    user: User = Depends(current_active_user),
):
    """Insert new reflection into database"""
    reflection = ReflectionModel(question_id=question_id, answer=answer)
    await create_reflection(reflection, user.id)

    todays_questions = await get_todays_reflections()
    id_list = [question.id for question in todays_questions]
    users_answers = await get_user_reflection_list(id_list, user.id)
    users_answers = {answer.question_id: answer.response for answer in users_answers}
    not_answered = [
        question.id for question in todays_questions if question.id not in users_answers
    ]
    if not_answered:
        show_id = not_answered[0]
    else:
        show_id = -1

    return templates.TemplateResponse(
        "reflections/reflectionWindow.html",
        {
            "request": request,
            "user": user,
            "questions": todays_questions,
            "answers": users_answers,
            "show_id": show_id,
        },
    )
