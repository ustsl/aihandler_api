import aiofiles
from fastapi import File, HTTPException, UploadFile


async def file_save(save_path: str, file: UploadFile = File(...)):
    try:
        async with aiofiles.open(save_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
