from tests.conftest import client
from tests.prompts.fixtures import *
from tests.users.fixtures import *

async def test_clean_prompt_story(user_data_with_prompt):

    user_data = user_data_with_prompt

    headers = {"Authorization": user_data.get("token").get("token")}
    query = f"v1/prompts/{user_data.get("telegram_id")}"
    response = client.get(
        query,
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json().get("result")) == 0


async def test_prompt_story_with_prompt(user_data_with_prompt, prompt_data):

    user_data = user_data_with_prompt

    headers = {"Authorization": user_data.get("token").get("token")}
    query = f"v1/prompts/{user_data.get("telegram_id")}"
    response = client.get(
        query,
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json().get("result")) == 1


async def test_found_not_found_prompt_status(prompt_data, user_data_with_prompt):

    user_data = user_data_with_prompt

    headers = {"Authorization": user_data.get("token").get("token")}
    response = client.get(
        f'v1/prompts/{user_data.get("telegram_id")}/b35273d1-e135-43e3-aae5-c9997276479d',
        headers=headers,
    )
    
    assert response.status_code == 404
    response = client.get(
        f'v1/prompts/{user_data.get("telegram_id")}/{prompt_data.get("id")}',
        headers=headers,
    )
    assert response.status_code == 200
