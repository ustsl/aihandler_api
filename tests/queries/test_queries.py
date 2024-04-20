from tests.conftest import client


async def test_gpt_query(prompt_data, user_data):
    headers = {"Authorization": user_data.get("token").get("token")}
    query = f"v1/queries/{user_data.get("telegram_id")}"
    # Execute a query
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
