""" """
import json
from datetime import date, timedelta

from app.db.models import QuestionOfDay, QuestionPool
from app.db.reflections import (
    create_question_of_day,
    create_question_pool,
    get_active_questions,
    get_question_pool,
)
from app.models.reflections import QuestionDateCard, QuestionPoolCard
from app.services.openai_chat import gpt_question_query


def generate_question():
    """Generate a random question from the database"""
    question_category_list = [
        "Gratitude",
        "Mindfulness",
        "Self-Compassion",
        "Achievements",
        "Connection",
        "Mind-Body Awareness",
        "Joy and Happiness",
        "Letting Go",
        "Intentions",
    ]
    raw_question_list = []
    parsed_question_list = []
    for category in question_category_list:
        raw_questions = gpt_question_query(category)
        raw_question_list.append(raw_questions)
    for raw_question in raw_question_list:
        try:
            question = json.loads(
                raw_question,
            )
            parsed_question_list.append(question)
        except json.decoder.JSONDecodeError as json_error:
            print(raw_question)
            print(json_error)

    for category in parsed_question_list:
        for question in category:
            print(question)
            question_model = QuestionPool(
                question_text=question["question"],
                category=question["category"],
            )
            create_question_pool(question_model)


async def assign_question_of_day():
    """Assign a question of the day to all users"""
    start_date = date.today()
    next_week = date.today() + timedelta(days=7)
    question_pool = await get_question_pool()
    active_questions = await get_active_questions()

    question_pool = [QuestionPoolCard.from_orm(question) for question in question_pool]
    active_questions = [
        QuestionDateCard.from_orm(question) for question in active_questions
    ]
    if active_questions:
        dates_of_active_questions = [q_day.date for q_day in active_questions]
        next_question_date = max(dates_of_active_questions) + timedelta(days=1)
        if next_question_date > next_week:
            return None
        else:
            start_date = next_question_date

    question_pool = [
        question
        for question in question_pool
        if question.id not in [q_day.source_id for q_day in active_questions]
    ]

    nested_question_pool = {}
    for question in question_pool:
        if question.category not in nested_question_pool:
            nested_question_pool[question.category] = []
        nested_question_pool[question.category].append(question)

    for i, questions in enumerate(nested_question_pool.values(), start=0):
        if len(questions) >= 3:
            questions = questions[:3]
            for question in questions:
                question_of_day = QuestionOfDay(
                    source_id=question.id,
                    question_text=question.question_text,
                    category=question.category,
                    date=start_date + timedelta(days=i),
                )
                await create_question_of_day(question_of_day)
