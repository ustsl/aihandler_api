from tests.conftest import client


def test_create_prompt_invalid_title_returns_422(user_data_with_prompt):
    response = client.post(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}',
        json={
            "title": "Bad@Title!",
            "description": "Test",
            "prompt": "Test",
            "model": "gpt-3.5-turbo",
            "is_open": True,
            "context_story_window": 0,
            "tuning": {},
        },
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 422


def test_create_prompt_invalid_story_window_returns_422(user_data_with_prompt):
    response = client.post(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}',
        json={
            "title": "Valid title",
            "description": "Test",
            "prompt": "Test",
            "model": "gpt-3.5-turbo",
            "is_open": True,
            "context_story_window": 100,
            "tuning": {},
        },
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 422


def test_update_prompt_owner_success(user_data_with_prompt, create_prompt_for_user):
    prompt = create_prompt_for_user(
        user_data_with_prompt,
        title="Owner updatable",
        description="Before",
        prompt="Before body",
    )
    response = client.put(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}/{prompt["id"]}',
        json={"description": "After"},
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 200
    assert response.json()["success"] == "Updated successfully"


def test_update_prompt_foreign_forbidden(
    user_data_with_prompt, user_data_with_money, create_prompt_for_user
):
    foreign_prompt = create_prompt_for_user(
        user_data_with_money,
        title="Foreign private prompt",
        is_open=False,
    )

    response = client.put(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}/{foreign_prompt["id"]}',
        json={"description": "Try update foreign"},
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 403


def test_delete_prompt_foreign_forbidden(
    user_data_with_prompt, user_data_with_money, create_prompt_for_user
):
    foreign_prompt = create_prompt_for_user(
        user_data_with_money,
        title="Foreign deletable prompt",
        is_open=False,
    )

    response = client.delete(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}/{foreign_prompt["id"]}',
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 403


def test_delete_prompt_owner_soft_delete(user_data_with_prompt, create_prompt_for_user):
    prompt = create_prompt_for_user(
        user_data_with_prompt,
        title="Owner deletable prompt",
        is_open=True,
    )
    delete_response = client.delete(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}/{prompt["id"]}',
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert delete_response.status_code == 200

    list_response = client.get(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}',
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert list_response.status_code == 200
    prompt_ids = {item["uuid"] for item in list_response.json()["result"]}
    assert prompt["id"] not in prompt_ids
