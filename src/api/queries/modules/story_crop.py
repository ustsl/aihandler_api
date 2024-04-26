async def story_crop_function(story: list, window: int) -> list:
    if window == 0 or not window:
        return []
    else:
        return story[-int(window) * 2 :]
