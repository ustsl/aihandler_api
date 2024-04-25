import asyncio
from typing import AsyncGenerator


import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


from src.db.session import get_db
from src.settings import TEST_DATABASE_URL, SERVICE_TOKEN
from src.db.models import Base


from src.main import app

# DATABASE

metadata = Base.metadata

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test

HEADERS = {"Authorization": SERVICE_TOKEN}


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        yield ac


@pytest.fixture(scope="session")
def user_data_with_prompt():
    # Create a user with a predefined Telegram ID
    user_data_create = client.post(
        "v1/users/",
        json={"telegram_id": "12345"},
        headers=HEADERS,
    )
    assert user_data_create.status_code == 200, "Failed to create user"
    user_data_create_json = user_data_create.json()

    # Retrieve the user data using the Telegram ID
    user_data_response = client.get(
        f'v1/users/{user_data_create_json.get("telegram_id")}',
        headers=HEADERS,
    )
    assert user_data_response.status_code == 200, "Failed to fetch user data"
    user_data_json = user_data_response.json()

    return user_data_json


@pytest.fixture(scope="session")
def user_data_with_money():

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

    return user_data_json


@pytest.fixture(scope="session")
def prompt_data(user_data_with_prompt):

    user_data = user_data_with_prompt

    account_id = user_data.get("accounts").get("account_id")
    telegram_id = user_data.get("telegram_id")
    token = user_data.get("token").get("token")
    headers = {"Authorization": token}

    prompt_result = client.post(
        f"v1/prompts/{telegram_id}",
        json={
            "title": "Translator",
            "description": "Test descr",
            "prompt": "Get word on Turkish, and translate this word to English. Return only the word in English. More - nothing",
            "model": "gpt-3.5-turbo",
            "account_id": account_id,
            "is_open": True,
        },
        headers=headers,
    )

    return prompt_result.json()
