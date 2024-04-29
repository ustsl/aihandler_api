import pytest
from tests.conftest import *
from tests.users.fixtures import *


prompt_data_cache = {}


@pytest.fixture(scope="session")
def prompt_data(user_data_with_prompt):

    if prompt_data_cache.get("result"):
        return prompt_data_cache["result"]

    user_data = user_data_with_prompt

    account_id = user_data.get("accounts").get("account_id")
    telegram_id = user_data.get("telegram_id")
    token = user_data.get("token").get("token")
    headers = {"Authorization": token}

    prompt_result = client.post(
        f"v1/prompts/{telegram_id}",
        json={
            "title": "Translator",
            "description": "Test descr",
            "prompt": "Get word on Turkish, and translate this word to English. Return only the word in English. More - nothing",
            "model": "gpt-3.5-turbo",
            "account_id": account_id,
            "is_open": True,
            "context_story_window": 5,
        },
        headers=headers,
    )
    prompt_data_cache["result"] = prompt_result.json()

    return prompt_result.json()
