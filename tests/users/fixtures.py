import uuid

import pytest

from tests.conftest import HEADERS, client


def _create_and_fetch_user(telegram_id: str) -> dict:
    create_response = client.post(
        "v1/users/",
        json={"telegram_id": telegram_id},
        headers=HEADERS,
    )
    assert create_response.status_code == 200, "Failed to create user"

    fetch_response = client.get(f"v1/users/{telegram_id}", headers=HEADERS)
    assert fetch_response.status_code == 200, "Failed to fetch user data"
    return fetch_response.json()


def _auth_headers(user_data: dict) -> dict:
    return {"Authorization": user_data["token"]["token"]}


@pytest.fixture(scope="session")
def user_data_with_prompt():
    user_data = _create_and_fetch_user("12345")

    balance_response = client.put(
        "v1/users/12345/balance",
        json={"balance": -1},
        headers=HEADERS,
    )
    assert balance_response.status_code == 200, "Failed to adjust user balance"
    return user_data


@pytest.fixture(scope="session")
def user_data_with_money():
    return _create_and_fetch_user("4589")


@pytest.fixture(scope="session")
def user_data_with_block():
    _create_and_fetch_user("505050")

    block_response = client.put(
        "v1/users/505050/block",
        json={"is_active": False},
        headers=HEADERS,
    )
    assert block_response.status_code == 200, "Failed to change active status"

    user_data_response = client.get("v1/users/505050", headers=HEADERS)
    assert user_data_response.status_code == 200, "Failed to fetch user data"
    return user_data_response.json()


@pytest.fixture()
def fresh_user():
    telegram_id = f"test_{uuid.uuid4().hex[:12]}"
    return _create_and_fetch_user(telegram_id)


@pytest.fixture()
def auth_headers():
    return _auth_headers
