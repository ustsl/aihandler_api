import pytest

from tests.conftest import client


def _create_prompt_for_scenario(telegram_id: str, token: str, title: str) -> dict:
    response = client.post(
        f"v1/prompts/{telegram_id}",
        json={
            "title": title,
            "description": "Test descr",
            "prompt": "Если пользователь отправил число (даже если число в виде строки) - умножь его на 2 и напиши полученное число и только его. Если пользователь отправил другое сообщение верни 0",
            "model": "gpt-3.5-turbo",
            "is_open": True,
            "context_story_window": 0,
            "tuning": {},
        },
        headers={"Authorization": token},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="session")
def special_prompts_list(user_data_with_prompt):
    telegram_id = user_data_with_prompt["telegram_id"]
    token = user_data_with_prompt["token"]["token"]

    return [
        _create_prompt_for_scenario(telegram_id, token, "Calculator 1"),
        _create_prompt_for_scenario(telegram_id, token, "Calculator 2"),
    ]


@pytest.fixture(scope="session")
def scenario_prompt_data(user_data_with_prompt):
    telegram_id = user_data_with_prompt["telegram_id"]
    token = user_data_with_prompt["token"]["token"]

    scenario_result = client.post(
        f"v1/scenarios/{telegram_id}",
        json={
            "title": "Scenario1",
            "description": "Test descr",
        },
        headers={"Authorization": token},
    )
    assert scenario_result.status_code == 200
    return scenario_result.json()
