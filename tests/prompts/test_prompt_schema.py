import pytest
from pydantic import ValidationError

from src.api.prompts.schemas import GPTPromptBase


def test_prompt_schema_rejects_invalid_title():
    with pytest.raises(ValidationError):
        GPTPromptBase(
            title="Bad@Title!",
            description="desc",
            prompt="body",
            model="gpt-3.5-turbo",
            is_open=True,
            context_story_window=0,
            tuning={},
        )


def test_prompt_schema_rejects_too_large_story_window():
    with pytest.raises(ValidationError):
        GPTPromptBase(
            title="Valid title",
            description="desc",
            prompt="body",
            model="gpt-3.5-turbo",
            is_open=True,
            context_story_window=51,
            tuning={},
        )
