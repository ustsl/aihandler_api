from tests.conftest import client

def test_gpt_query(prompt_data, user_data_with_money):

    user_data = user_data_with_money

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

    data = response.json()
    result = data.get("result")
    assert str(result.lower()) == "hello"
    assert response.status_code == 200
    print(user_data.get("accounts").get("balance"))



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
