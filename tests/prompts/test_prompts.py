from tests.conftest import client


def test_clean_prompt_story(fresh_user):
    headers = {"Authorization": fresh_user["token"]["token"]}
    response = client.get(
        f'v1/prompts/{fresh_user["telegram_id"]}',
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()["result"]) == 0


def test_prompt_story_with_prompt(user_data_with_prompt, prompt_data):
    headers = {"Authorization": user_data_with_prompt["token"]["token"]}
    response = client.get(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}',
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()["result"]) >= 1
    assert any(item["uuid"] == prompt_data["id"] for item in response.json()["result"])


def test_found_not_found_prompt_status(prompt_data, user_data_with_prompt):
    headers = {"Authorization": user_data_with_prompt["token"]["token"]}
    not_found_response = client.get(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}/b35273d1-e135-43e3-aae5-c9997276479d',
        headers=headers,
    )
    ok_response = client.get(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}/{prompt_data["id"]}',
        headers=headers,
    )

    assert not_found_response.status_code == 404
    assert ok_response.status_code == 200


def test_create_prompt_to_blocked_user(user_data_with_block):
    headers = {"Authorization": user_data_with_block["token"]["token"]}

    prompt_result = client.post(
        f'v1/prompts/{user_data_with_block["telegram_id"]}',
        json={
            "title": "Translator",
            "description": "Test descr",
            "prompt": "Get word on Turkish, and translate this word to English. Return only the word in English. More - nothing",
            "model": "gpt-3.5-turbo",
            "is_open": True,
            "context_story_window": 5,
            "tuning": {},
        },
        headers=headers,
    )

    assert prompt_result.json()["detail"] == "Blocked"


def test_public_prompt_visible_but_private_hidden(user_data_with_prompt, foreign_prompts):
    headers = {"Authorization": user_data_with_prompt["token"]["token"]}
    response = client.get(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}?only_yours=false',
        headers=headers,
    )

    assert response.status_code == 200
    prompt_ids = {item["uuid"] for item in response.json()["result"]}
    assert foreign_prompts["public"]["id"] in prompt_ids
    assert foreign_prompts["private"]["id"] not in prompt_ids


def test_private_foreign_prompt_returns_403(user_data_with_prompt, foreign_prompts):
    headers = {"Authorization": user_data_with_prompt["token"]["token"]}
    response = client.get(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}/{foreign_prompts["private"]["id"]}',
        headers=headers,
    )

    assert response.status_code == 403
