import pytest
from tests.conftest import client, HEADERS


@pytest.fixture(scope="session")
def user_data_with_prompt():

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

    client.put(
        "v1/users/12345/balance",
        json={"balance": -1},
        headers=HEADERS,
    )

    return user_data_json


@pytest.fixture(scope="session")
def user_data_with_money():

    user_data_create = client.post(
        "v1/users/",
        json={"telegram_id": "4589"},
        headers=HEADERS,
    )

    assert user_data_create.status_code == 200, "Failed to create user"

    user_data_response = client.get(
        f"v1/users/4589",
        headers=HEADERS,
    )
    assert user_data_response.status_code == 200, "Failed to fetch user data"
    user_data_json = user_data_response.json()

    return user_data_json


@pytest.fixture(scope="session")
def user_data_with_block():

    user_data_create = client.post(
        "v1/users/",
        json={"telegram_id": "505050"},
        headers=HEADERS,
    )

    assert user_data_create.status_code == 200, "Failed to create user"

    user_data_change_active = client.put(
        "v1/users/505050/block",
        json={"is_active": False},
        headers=HEADERS,
    )
    assert user_data_change_active.status_code == 200, "Failed to change active status"

    user_data_response = client.get(
        f"v1/users/505050",
        headers=HEADERS,
    )
    assert user_data_response.status_code == 200, "Failed to fetch user data"
    user_data_json = user_data_response.json()

    return user_data_json
