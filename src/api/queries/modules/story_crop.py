async def story_crop_function(story: list, window: int) -> list:
    try:
        return story[-int(window) * 2 :]
    except:
        return []
