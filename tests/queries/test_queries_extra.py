from tests.conftest import client


def test_query_validation_too_long_returns_422(user_data_with_money, prompt_data):
    response = client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}',
        json={
            "prompt_id": prompt_data["id"],
            "query": "a" * 50001,
        },
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert response.status_code == 422


def test_get_personal_queries_returns_created_items(user_data_with_money, prompt_data):
    create_response = client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}',
        json={
            "prompt_id": prompt_data["id"],
            "query": "merhaba-unique-personal-list",
        },
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert create_response.status_code == 200

    list_response = client.get(
        f'v1/queries/{user_data_with_money["telegram_id"]}/{prompt_data["id"]}',
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert list_response.status_code == 200
    assert list_response.json()["total"] >= 1


def test_story_crop_window_applied_to_model_call(
    user_data_with_money, prompt_data, gpt_call_log
):
    story = [{"role": "assistant", "content": f"msg-{i}"} for i in range(15)]

    response = client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}',
        json={
            "prompt_id": prompt_data["id"],
            "query": "story-crop-check",
            "story": story,
        },
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )

    assert response.status_code == 200
    assert len(gpt_call_log) == 1
    sent_story = gpt_call_log[0]["story"]
    assert len(sent_story) == 10
    assert sent_story[0]["content"] == "msg-5"
    assert sent_story[-1]["content"] == "msg-14"


def test_query_private_foreign_prompt_forbidden(
    user_data_with_prompt, user_data_with_money, create_prompt_for_user
):
    private_prompt = create_prompt_for_user(
        user_data_with_money,
        title="Private prompt for query check",
        is_open=False,
    )
    response = client.post(
        f'v1/queries/{user_data_with_prompt["telegram_id"]}',
        json={
            "prompt_id": private_prompt["id"],
            "query": "cannot access",
        },
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 403
