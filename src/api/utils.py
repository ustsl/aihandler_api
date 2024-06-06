from src.settings import SERVICE_TOKEN

from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import File, Request, HTTPException, UploadFile, status, Depends
from fastapi import HTTPException

from src.db.users.dals.user import UsersDAL
from src.db.users.models import UserModel
from src.db.session import get_db


def handle_dal_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if isinstance(result, dict) and "error" in result:
            status = result.get("status", 500)
            raise HTTPException(status_code=status, detail=result.get("error"))
        return result

    return wrapper


async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if token != SERVICE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )


async def verify_user_data(
    request: Request, telegram_id: str, db: AsyncSession = Depends(get_db)
):
    token = request.headers.get("Authorization")
    async with db as session:
        userDal = UsersDAL(session, UserModel)
        user = await userDal.get(telegram_id=telegram_id)
        if not user or (isinstance(user, dict) and user.get("error")):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if str(user.token.token) != token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token",
            )
        if user.is_active == False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Blocked",
            )


async def verify_file_size(file: UploadFile):
    MAX_FILE_SIZE = 800 * 1024
    content = await file.read()
    file.file.seek(0)
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 800KB limit")
    return file


async def verify_file_format(file: UploadFile):
    allowed_formats = {"image/svg+xml", "image/png", "image/jpeg"}
    if file.content_type not in allowed_formats:
        raise HTTPException(status_code=400, detail="Invalid file format")
    return file


async def verify_file_format(file: UploadFile):
    allowed_formats = {"image/svg+xml", "image/png", "image/jpeg"}
    if file.content_type not in allowed_formats:
        raise HTTPException(status_code=400, detail="Invalid file format")
    return file


async def verify_file(file: UploadFile = File(...)):
    file = await verify_file_format(file)
    file = await verify_file_size(file)
    return file
