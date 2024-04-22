from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.users.actions import _create_new_user, _get_user

from api.utils import verify_token
from db.session import get_db

from api.users.models import UserDataBase, UserDataExtend, UserDataWithId

user_router = APIRouter(dependencies=[Depends(verify_token)])


@user_router.post("/", response_model=UserDataWithId)
async def create_user(
    body: UserDataBase, db: AsyncSession = Depends(get_db)
) -> UserDataWithId:
    return await _create_new_user(body, db)


@user_router.get("/", response_model=UserDataExtend)
async def get_user(
    body: UserDataBase, db: AsyncSession = Depends(get_db)
) -> UserDataExtend:
    return await _create_new_user(body, db)


@user_router.get("/{telegram_id}")
async def get_user(telegram_id: str, db: AsyncSession = Depends(get_db)):
    res = await _get_user(telegram_id, db)
    return res
