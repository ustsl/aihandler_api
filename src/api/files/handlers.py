import base64
from pathlib import Path
import os
import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import httpx

from src.api.utils import verify_file_size, verify_user_data
from src.modules.file_saver.handler import file_save
from src.modules.path_worker.handler import PathWorker
from src.settings import OPENAI_TOKEN


files_router = APIRouter(dependencies=[Depends(verify_user_data)])


OPENAI_API_KEY = OPENAI_TOKEN
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
PROMPT = "опиши что ты видишь на картинке"


async def send_image_to_openai(image_path: str, prompt: str):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                        },
                    },
                ],
            }
        ],
    }

    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post(OPENAI_API_URL, headers=headers, json=payload)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))

        return response.json()


@files_router.post("/image/{telegram_id}")
async def image_download(
    telegram_id: str, file: UploadFile = Depends(verify_file_size)
):

    save_path = PathWorker.generate_path(
        user_id=str(telegram_id), folder="images", file=file
    )
    await file_save(file=file, save_path=save_path)

    # result = await send_image_to_openai(save_path, PROMPT)
    # print(result)

    check_path = PathWorker.check_path(save_path=save_path)

    # if check_path:
    #     PathWorker.delete_path(save_path=save_path)

    return {"filename": save_path.name, "path": str(save_path)}


@files_router.get("/{telegram_id}")
async def get_file(file_path: str):
    file = Path(file_path)
    if file.exists() and file.is_file():
        return FileResponse(path=file, filename=file.name)
    else:
        raise HTTPException(status_code=404, detail="File not found")
