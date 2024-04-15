from tests.conftest import client


async def test_gpt_query():

    result = client.post(
        "v1/prompts/",
        json={
            "title": "Translator",
            "description": "Test descr",
            "prompt": "Get word on turkish, an translate on engilsh (etmek=>eat). Return only word in english. More - nothing",
            "model": "gpt-3.5-turbo",
        },
    )

    post_data = result.json()
    response = client.post(
        "v1/queries/",
        json={
            "prompt_id": post_data.get("id"),
            "query": "merhaba",
        },
    )

    data = response.json()
    result = data.get("result")
    assert str(result.lower()) == "hello"
    assert response.status_code == 200
