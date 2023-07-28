"""_summary_

Returns
-------
_type_
    _description_
"""

from typing import List

import openai

from app.config.settings import Settings

settings = Settings()

openai.api_key = settings.openai_api_key
MODEL = settings.openai_api_model

QUERY = """Give me 1 charities in {COUNTRY}, that focus on {EFFORT}. 

"""
INSTRUCTION = """ Output should be like following:
[
    {
        "name": "Charity Name",
        "description": "Charity Description",
        "website": "Charity Website",
        "image_url": "Charity Image URL",
        "phone_number": "Charity Phone Number"
    },
]"""
CONVERSATION = []


def gpt_charity_lookup(query: dict) -> List[dict]:
    """ChatGPT_conversation

    Parameters
    ----------
    charity_query : str
        The query to be sent to the OpenAI API

    Returns
    -------
    list
        List of dictionaries with keys 'role' and 'content'
    """
    content = QUERY.format(COUNTRY=query.get("country"), EFFORT=query.get("effort"))
    CONVERSATION.append({"role": "system", "content": content + INSTRUCTION})
    response = openai.ChatCompletion.create(model=MODEL, messages=CONVERSATION)
    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    CONVERSATION.append(
        {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content,
        }
    )
