"""
"""


import openai

from app.config.settings import Settings

settings = Settings()

openai.api_key = settings.openai_api_key
MODEL = settings.openai_api_model

CONVERSATION = []


def gpt_question_query(category) -> str:
    """ChatGPT_conversation

    Returns
    -------
    content : str
        The response from the OpenAI API
    """
    query = f"""Give me 3 questions for reflection/meditation purpose
    in the category of {category}.

    """
    instruction = """ Output should be like following:
    [
        {
            "question": "Question text",
            "category": "Theme of the quesetion",
            "writer": "Creator of the question (if applicable)"
        },
    ]"""
    CONVERSATION.append({"role": "system", "content": query + instruction})
    response = openai.ChatCompletion.create(model=MODEL, messages=CONVERSATION)
    CONVERSATION.append(
        {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content,
        }
    )
    return response.choices[0].message.content
