from tests.conftest import HEADERS, client


def test_query_story(user_data_with_money, prompt_data):
    client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}',
        json={
            "prompt_id": prompt_data["id"],
            "query": "merhaba",
        },
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    response = client.get(
        "v1/analytics/queries/",
        headers=HEADERS,
    )
    assert len(response.json().get("result")) > 0
