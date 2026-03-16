from tests.conftest import HEADERS, client


def _get_user(user_id: str) -> dict:
    response = client.get(
        f"v1/users/{user_id}",
        headers=HEADERS,
    )
    assert response.status_code == 200
    return response.json()


def test_user_set_language(user_data_with_money):
    telegram_id = user_data_with_money["telegram_id"]
    assert user_data_with_money["settings"]["language"] is None

    api_link = f"v1/users/{telegram_id}/settings"

    invalid_lang_response = client.put(
        api_link,
        json={"language": "eng"},
        headers=HEADERS,
    )
    assert invalid_lang_response.status_code == 200

    unchanged_user_data = _get_user(telegram_id)
    assert unchanged_user_data["settings"]["language"] is None

    valid_lang_response = client.put(
        api_link,
        json={"language": "en"},
        headers=HEADERS,
    )
    assert valid_lang_response.status_code == 200

    updated_user_data = _get_user(telegram_id)
    assert updated_user_data["settings"]["language"] == "en"
