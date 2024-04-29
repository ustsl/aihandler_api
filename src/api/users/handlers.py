from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users.actions import (
    _create_new_user,
    _get_user,
    _get_users,
    _update_user_account_balance,
)
from src.api.utils import verify_token
from src.db.session import get_db

from src.api.users.schemas import (
    UserBalance,
    UserDataBase,
    UserDataExtend,
    UserDataWithId,
)

user_router = APIRouter(dependencies=[Depends(verify_token)])


@user_router.post("/", response_model=UserDataExtend)
async def create_user(body: UserDataBase, db: AsyncSession = Depends(get_db)):
    return await _create_new_user(body, db)


@user_router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    return await _get_users(db)


@user_router.get("/{telegram_id}", response_model=UserDataExtend)
async def get_user(telegram_id: str, db: AsyncSession = Depends(get_db)):
    res = await _get_user(telegram_id, db)
    return res


@user_router.put("/{telegram_id}/balance")
async def update_prompt(
    telegram_id: str, balance: UserBalance, db: AsyncSession = Depends(get_db)
):
    res = await _update_user_account_balance(telegram_id, balance, db)
    return res
