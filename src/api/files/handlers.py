from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse


from src.api.utils import verify_file, verify_user_data
from src.modules.file_saver.handler import file_save
from src.modules.path_worker.handler import PathWorker


files_router = APIRouter(dependencies=[Depends(verify_user_data)])


@files_router.post("/image/{telegram_id}")
async def image_download(telegram_id: str, file: UploadFile = Depends(verify_file)):

    save_path = PathWorker.generate_path(
        user_id=str(telegram_id), folder="images", file=file
    )
    await file_save(file=file, save_path=save_path)

    check_path = PathWorker.check_path(save_path=save_path)

    if check_path:
        PathWorker.delete_path(save_path=save_path)

    return {"filename": save_path.name, "path": str(save_path)}


@files_router.get("/{telegram_id}")
async def get_file(file_path: str):
    file = Path(file_path)
    if file.exists() and file.is_file():
        return FileResponse(path=file, filename=file.name)
    else:
        raise HTTPException(status_code=404, detail="File not found")
