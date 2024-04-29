import pytest
from tests.conftest import client, HEADERS


user_cache = {}


@pytest.fixture(scope="session")
def user_data_with_prompt():
    if "12345" in user_cache:
        return user_cache["12345"]
    # Create a user with a predefined Telegram ID
    user_data_create = client.post(
        "v1/users/",
        json={"telegram_id": "12345"},
        headers=HEADERS,
    )
    # assert user_data_create.status_code == 200, "Failed to create user"
    user_data_create_json = user_data_create.json()

    # Retrieve the user data using the Telegram ID
    user_data_response = client.get(
        f'v1/users/{user_data_create_json.get("telegram_id")}',
        headers=HEADERS,
    )
    assert user_data_response.status_code == 200, "Failed to fetch user data"
    user_data_json = user_data_response.json()

    user_cache["12345"] = user_data_json

    return user_data_json


@pytest.fixture(scope="session")
def user_data_with_money():
    if "4589" in user_cache:
        return user_cache["4589"]
    user_data_create = client.post(
        "v1/users/",
        json={"telegram_id": "4589"},
        headers=HEADERS,
    )

    assert user_data_create.status_code == 200, "Failed to create user"

    user_data_change_balance = client.put(
        "v1/users/4589/balance",
        json={"balance": 1000},
        headers=HEADERS,
    )
    assert user_data_change_balance.status_code == 200, "Failed to change balance"

    user_data_response = client.get(
        f"v1/users/4589",
        headers=HEADERS,
    )
    assert user_data_response.status_code == 200, "Failed to fetch user data"
    user_data_json = user_data_response.json()
    user_cache["4589"] = user_data_json
    return user_data_json
