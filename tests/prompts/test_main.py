from httpx import AsyncClient


async def test_add_data(ac: AsyncClient):

    response = await ac.get("v1/prompts/")

    assert response.status_code == 200
    assert len(response.json()) == 0

    result = await ac.post(
        "v1/prompts/",
        json={
            "title": "Test title",
            "description": "Test descr",
            "prompt": "Test p",
        },
    )
    post_data = result.json()
    await ac.post(
        "v1/prompts/",
        json={
            "title": "Test title",
            "description": "Test descr",
            "prompt": "Test p",
        },
    )

    response = await ac.get("v1/prompts/")
    list_data = response.json()
    assert list_data[0].get("uuid") == post_data.get("id")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_found_not_found_propmpt_status(ac: AsyncClient):
    response = await ac.get("v1/prompts/b35273d1-e135-43e3-aae5-c9997276479d")
    assert response.status_code == 404
    result = await ac.post(
        "v1/prompts/",
        json={
            "title": "Test title 2",
            "description": "Test descr",
            "prompt": "Test p",
        },
    )
    post_data = result.json()
    response = await ac.get(f'v1/prompts/{post_data.get("id")}')
    assert response.status_code == 200
