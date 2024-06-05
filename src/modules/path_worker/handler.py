import os

from uuid import uuid4

import time
from pathlib import Path

from fastapi import File, UploadFile


class PathWorker:

    def __init__(self):
        pass

    @staticmethod
    def generate_path(user_id: str, folder: str, file: UploadFile = File(...)):
        current_year = time.strftime("%Y")
        save_dir = Path(f"files/{user_id}/{folder}/{current_year}")
        save_dir.mkdir(parents=True, exist_ok=True)
        file_extension = Path(file.filename).suffix
        file_name = f"{int(time.time())}_{uuid4().hex}{file_extension}"
        return save_dir / file_name

    @staticmethod
    def check_path(save_path):
        file_path = str(save_path)
        checked_file = Path(file_path)
        if checked_file.exists():
            return True
        return False

    def delete_path(save_path):
        file_path = str(save_path)
        checked_file = Path(file_path)
        checked_file.unlink()
