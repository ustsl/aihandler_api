from tests.conftest import HEADERS, client


def test_users_endpoint_requires_service_token():
    response = client.get("v1/users/")
    assert response.status_code == 401


def test_get_missing_user_returns_404():
    response = client.get("v1/users/does-not-exist", headers=HEADERS)
    assert response.status_code == 404


def test_update_token_changes_value(user_data_with_money):
    telegram_id = user_data_with_money["telegram_id"]
    before_token = user_data_with_money["token"]["token"]

    response = client.put(f"v1/users/{telegram_id}/token", headers=HEADERS)
    assert response.status_code == 200
    new_token = response.json()["token"]
    assert new_token != before_token


def test_deprecated_prompt_settings_alias_works(user_data_with_money):
    telegram_id = user_data_with_money["telegram_id"]
    response = client.put(
        f"v1/users/{telegram_id}/prompt",
        json={"language": "ru"},
        headers=HEADERS,
    )

    assert response.status_code == 200
    user_response = client.get(f"v1/users/{telegram_id}", headers=HEADERS)
    assert user_response.status_code == 200
    assert user_response.json()["settings"]["language"] == "ru"


def test_create_duplicate_user_returns_server_error(fresh_user):
    telegram_id = fresh_user["telegram_id"]
    duplicate_response = client.post(
        "v1/users/",
        json={"telegram_id": telegram_id},
        headers=HEADERS,
    )
    assert duplicate_response.status_code == 500
