"""
    _summary_: This file contains the routes for the reflections API.
    _description_: The reflections API allows users to create, read, update,
    and delete reflections.

    """

from fastapi import Depends, Form, Request, routing
from fastapi.templating import Jinja2Templates

from app.db.models import User
from app.db.reflections import (
    create_user_response,
    get_all_user_responses,
    get_reflection_question,
    get_todays_reflections,
    get_user_response_list,
    set_user_response_states,
)
from app.models.reflections import UserResponseCard, UserResponseForm
from app.services.authentication import current_active_user

templates = Jinja2Templates(directory="templates")
router = routing.APIRouter()


@router.get("/", operation_id="reflections")
async def reflections(request: Request, user: User = Depends(current_active_user)):
    """reflections page"""
    todays_questions = await get_todays_reflections()
    id_list = [question.id for question in todays_questions]
    users_answers = await get_user_response_list(id_list, user.id)
    users_answers = {answer.question_id: answer.response for answer in users_answers}
    not_answered = [
        question.id for question in todays_questions if question.id not in users_answers
    ]
    if not_answered:
        show_id = not_answered[0]
    else:
        show_id = -1
    return templates.TemplateResponse(
        "reflections/index.html",
        {
            "request": request,
            "user": user,
            "questions": todays_questions,
            "answers": users_answers,
            "show_id": show_id,
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
    reflection = UserResponseForm(question_id=question_id, answer=answer)
    await create_user_response(reflection, user.id)

    todays_questions = await get_todays_reflections()
    id_list = [question.id for question in todays_questions]
    users_answers = await get_user_response_list(id_list, user.id)
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


@router.post("/confirm-reflections")
async def confirm_reflections(
    request: Request,
    answer_ids: str = Form(...),
    user: User = Depends(current_active_user),
):
    """Confirm reflections"""
    list_of_ids = [int(x) for x in answer_ids.split(",")]
    reflection_answers = await set_user_response_states(list_of_ids, True, user.id)
    reflection_answers = {
        answer.question_id: answer.response for answer in reflection_answers
    }
    todays_reflections = await get_todays_reflections()
    return templates.TemplateResponse(
        "reflections/reflectionList.html",
        {
            "request": request,
            "user": user,
            "reflections": todays_reflections,
            "answers": reflection_answers,
        },
    )


@router.get("/history")
async def history(
    request: Request,
    user: User = Depends(current_active_user),
):
    """History page"""
    users_answers = await get_all_user_responses(user.id)
    users_answers = [UserResponseCard.from_orm(answer) for answer in users_answers]
    return templates.TemplateResponse(
        "history/index.html",
        {
            "request": request,
            "user": user,
            "history": users_answers,
        },
    )
