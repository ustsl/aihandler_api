from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users.actions import (
    _create_new_user,
    _get_user,
    _update_user_account_balance,
)
from src.api.utils import verify_token
from src.db.session import get_db

from src.api.users.models import (
    UserBalance,
    UserDataBase,
    UserDataExtend,
    UserDataWithId,
)

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


@user_router.put("/{telegram_id}/balance")
async def update_prompt(
    telegram_id: str, balance: UserBalance, db: AsyncSession = Depends(get_db)
):
    res = await _update_user_account_balance(telegram_id, balance, db)
    return res
