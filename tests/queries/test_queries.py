from tests.conftest import client
from tests.prompts.fixtures import *
from tests.users.fixtures import *


def test_gpt_query(user_data_with_money, prompt_data):

    user_data = user_data_with_money
    print(user_data)

    headers = {"Authorization": user_data.get("token").get("token")}
    query = f"v1/queries/{user_data.get("telegram_id")}"
    response = client.post(
        query,
        json={
            "prompt_id": prompt_data.get("id"),
            "query": "merhaba",
        },
        headers=headers,
    )

    response = client.post(
        query,
        json={
            "prompt_id": prompt_data.get("id"),
            "query": "merhaba",
        },
        headers=headers,
    )

    data = response.json()

    result = data.get("result")
    assert str(result.lower()) == "hello"
    assert response.status_code == 200

    query = f"v1/queries/"
    query = f"v1/users/{user_data.get("telegram_id")}"
    response = client.get(
        query,
        headers=HEADERS,
    )
    balance = response.json().get("accounts").get("balance")
    balance = float(balance)
    assert balance > 0.99
    assert balance < 1000


def test_gpt_query_no_balance(prompt_data, user_data_with_prompt):

    user_data = user_data_with_prompt

    headers = {"Authorization": user_data.get("token").get("token")}
    query = f"v1/queries/{user_data.get("telegram_id")}"

    response = client.post(
        query,
        json={
            "prompt_id": prompt_data.get("id"),
            "query": "merhaba",
        },
        headers=headers,
    )

    assert response.status_code == 403
