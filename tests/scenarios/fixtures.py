import pytest

from tests.conftest import *
from tests.users.fixtures import *

prompt_data_cache = {}
scenario_data_cache = {}


@pytest.fixture(scope="session")
def special_prompts_list(user_data_with_prompt):

    user_data = user_data_with_prompt

    account_id = user_data.get("accounts").get("uuid")
    telegram_id = user_data.get("telegram_id")
    token = user_data.get("token").get("token")
    headers = {"Authorization": token}

    data = []

    prompt_result = client.post(
        f"v1/prompts/{telegram_id}",
        json={
            "title": "Calculator",
            "description": "Test descr",
            "prompt": "Если пользователь отправил число (даже если число в виде строки) - умножь его на 2 и напиши полученное число и только его. Если пользователь отправил другое сообщение верни 0",
            "model": "gpt-3.5-turbo",
            "account_id": account_id,
            "is_open": True,
            "context_story_window": 0,
            "tuning": {},
        },
        headers=headers,
    )

    data += [prompt_result.json()]

    prompt_result = client.post(
        f"v1/prompts/{telegram_id}",
        json={
            "title": "Calculator",
            "description": "Test descr",
            "prompt": "Если пользователь отправил число (даже если число в виде строки) - умножь его на 2 и напиши полученное число и только его. Если пользователь отправил другое сообщение верни 0",
            "model": "gpt-3.5-turbo",
            "account_id": account_id,
            "is_open": True,
            "context_story_window": 0,
            "tuning": {},
        },
        headers=headers,
    )

    data += [prompt_result.json()]

    return data


@pytest.fixture(scope="session")
def scenario_prompt_data(user_data_with_prompt):

    if scenario_data_cache.get("result"):
        return scenario_data_cache["result"]

    user_data = user_data_with_prompt

    telegram_id = user_data.get("telegram_id")
    token = user_data.get("token").get("token")
    headers = {"Authorization": token}

    scenario_result = client.post(
        f"v1/scenarios/{telegram_id}",
        json={
            "title": "Scenario1",
            "description": "Test descr",
        },
        headers=headers,
    )
    scenario_data_cache["result"] = scenario_result.json()

    return scenario_result.json()
