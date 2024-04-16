from tests.conftest import HEADERS, client


async def test_len_data():

    response = client.get(
        "v1/prompts/",
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_found_not_found_prompt_status(prompt_data):
    response = client.get(
        "v1/prompts/b35273d1-e135-43e3-aae5-c9997276479d",
        headers=HEADERS,
    )
    assert response.status_code == 404

    response = client.get(
        f'v1/prompts/{prompt_data.get("id")}',
        headers=HEADERS,
    )
    assert response.status_code == 200
