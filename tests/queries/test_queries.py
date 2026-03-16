from tests.conftest import HEADERS, client


def test_gpt_query_uses_cache_and_deducts_balance_once(user_data_with_money, prompt_data):
    headers = {"Authorization": user_data_with_money["token"]["token"]}
    query_url = f'v1/queries/{user_data_with_money["telegram_id"]}'

    first_response = client.post(
        query_url,
        json={
            "prompt_id": prompt_data["id"],
            "query": "merhaba",
        },
        headers=headers,
    )
    second_response = client.post(
        query_url,
        json={
            "prompt_id": prompt_data["id"],
            "query": "merhaba",
        },
        headers=headers,
    )

    first_data = first_response.json()
    second_data = second_response.json()

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_data["result"].lower() == "hello"
    assert second_data["result"].lower() == "hello"
    assert first_data["cost"] > 0
    assert second_data["cost"] == 0
    assert second_data["quality_metrics"]["cached"] is True

    user_response = client.get(
        f'v1/users/{user_data_with_money["telegram_id"]}',
        headers=HEADERS,
    )
    balance = float(user_response.json()["accounts"]["balance"])
    assert 0.49 < balance < 0.5


def test_gpt_query_no_balance(prompt_data, user_data_with_prompt):
    headers = {"Authorization": user_data_with_prompt["token"]["token"]}
    query_url = f'v1/queries/{user_data_with_prompt["telegram_id"]}'

    response = client.post(
        query_url,
        json={
            "prompt_id": prompt_data["id"],
            "query": "merhaba merhaba",
        },
        headers=headers,
    )

    assert response.status_code == 403
