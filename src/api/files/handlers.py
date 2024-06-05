import base64
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
import httpx

from src.api.utils import verify_user_data
from src.modules.file_saver.handler import file_save
from src.modules.path_worker.handler import PathWorker
from src.settings import OPENAI_TOKEN


files_router = APIRouter(dependencies=[Depends(verify_user_data)])


@files_router.post("/image/{telegram_id}")
async def image_download(telegram_id: str, file: UploadFile = File(...)):

    save_path = PathWorker.generate_path(
        user_id=str(telegram_id), folder="mp3", file=file
    )
    await file_save(save_path=save_path, file=file)
    check_path = PathWorker.check_path(save_path=save_path)
    # if check_path:
    #     PathWorker.delete_path(save_path=save_path)

    headers = {
        "Authorization": f"Bearer {OPENAI_TOKEN}",
        "Content-Type": "application/json",
    }

    # Прочитаем содержимое файла и закодируем его в base64
    with open(save_path, "rb") as image_file:
        image_content = base64.b64encode(image_file.read()).decode("utf-8")

    # Подготовим данные для запроса
    data = {
        "image": image_content,  # Отправляем закодированное содержимое файла
        "prompt": "переделай персонажей на картинке в мультяшный вид",
        "num_images": 1,
        "model": "dall-e-3",
    }

    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=data,  # Отправляем данные в формате JSON
        )
        response.raise_for_status()
        completion = response.json()
        result = completion["data"][0]["url"]
        print(result)

    return {"filename": save_path.name, "path": str(save_path)}


@files_router.get("/{telegram_id}")
async def get_file(file_path: str):
    file = Path(file_path)
    if file.exists() and file.is_file():
        return FileResponse(path=file, filename=file.name)
    else:
        raise HTTPException(status_code=404, detail="File not found")
