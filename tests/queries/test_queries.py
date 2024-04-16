from tests.conftest import HEADERS, client


async def test_gpt_query(prompt_data):

    # Execute a query
    response = client.post(
        "v1/queries/",
        json={
            "prompt_id": prompt_data.get("id"),
            "query": "merhaba",
        },
        headers=HEADERS,
    )
    data = response.json()
    result = data.get("result")
    assert str(result.lower()) == "hello"
    assert response.status_code == 200
