import pytest

from src.api.queries.modules.story_crop import story_crop_function


@pytest.mark.asyncio
async def test_story_crop_function_limits_by_double_window():
    story = [{"role": "assistant", "content": str(i)} for i in range(12)]
    cropped = await story_crop_function(story=story, window=3)
    assert len(cropped) == 6
    assert cropped[0]["content"] == "6"
    assert cropped[-1]["content"] == "11"


@pytest.mark.asyncio
async def test_story_crop_function_returns_empty_on_bad_window():
    story = [{"role": "assistant", "content": "1"}]
    cropped = await story_crop_function(story=story, window="not-int")
    assert cropped == []
