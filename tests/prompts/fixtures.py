import pytest

from tests.conftest import client


def _create_prompt(
    telegram_id: str,
    token: str,
    *,
    title: str,
    description: str,
    prompt: str,
    is_open: bool,
    context_story_window: int,
) -> dict:
    response = client.post(
        f"v1/prompts/{telegram_id}",
        json={
            "title": title,
            "description": description,
            "prompt": prompt,
            "model": "gpt-3.5-turbo",
            "is_open": is_open,
            "context_story_window": context_story_window,
            "tuning": {},
        },
        headers={"Authorization": token},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture()
def create_prompt_for_user():
    def _factory(
        user_data: dict,
        *,
        title: str = "Prompt",
        description: str = "Desc",
        prompt: str = "Reply with 1",
        is_open: bool = True,
        context_story_window: int = 0,
    ):
        return _create_prompt(
            telegram_id=user_data["telegram_id"],
            token=user_data["token"]["token"],
            title=title,
            description=description,
            prompt=prompt,
            is_open=is_open,
            context_story_window=context_story_window,
        )

    return _factory


@pytest.fixture(scope="session")
def prompt_data(user_data_with_prompt):
    return _create_prompt(
        telegram_id=user_data_with_prompt["telegram_id"],
        token=user_data_with_prompt["token"]["token"],
        title="Translator",
        description="Test descr",
        prompt="Get word on Turkish, and translate this word to English. Return only the word in English. More - nothing",
        is_open=True,
        context_story_window=5,
    )


@pytest.fixture(scope="session")
def foreign_prompts(user_data_with_money):
    telegram_id = user_data_with_money["telegram_id"]
    token = user_data_with_money["token"]["token"]

    public_prompt = _create_prompt(
        telegram_id=telegram_id,
        token=token,
        title="Public prompt",
        description="Visible for others",
        prompt="Answer with public",
        is_open=True,
        context_story_window=0,
    )
    private_prompt = _create_prompt(
        telegram_id=telegram_id,
        token=token,
        title="Private prompt",
        description="Only owner can see it",
        prompt="Answer with private",
        is_open=False,
        context_story_window=0,
    )

    return {"public": public_prompt, "private": private_prompt}
