import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users.actions.account_user_actions import _update_user_account_balance
from src.api.users.actions.base_user_actions import (
    _block_user,
    _create_new_user,
    _get_user,
    _get_users,
)

from src.api.users.actions.settings_actions import _update_user_settings_prompt
from src.api.users.actions.token_actions import _update_user_token
from src.api.utils import verify_token
from src.db.session import get_db

from src.api.users.schemas import (
    TokenData,
    UserBalance,
    UserDataBase,
    UserDataExtend,
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
async def set_user_balance(
    telegram_id: str, balance: UserBalance, db: AsyncSession = Depends(get_db)
):
    res = await _update_user_account_balance(telegram_id, balance, db)
    return res


@user_router.put("/{telegram_id}/prompt")
async def set_user_prompt(
    telegram_id: str, updates: dict, db: AsyncSession = Depends(get_db)
):
    # This function may changes user preset prompt, its need for telegram part of app
    res = await _update_user_settings_prompt(
        telegram_id=telegram_id, prompt_id=updates.get("prompt_id"), db=db
    )
    return res


@user_router.put("/{telegram_id}/block")
async def set_block_user(
    telegram_id: str, updates: dict, db: AsyncSession = Depends(get_db)
):
    res = await _block_user(
        telegram_id=telegram_id, is_active=updates.get("is_active"), db=db
    )
    return res


@user_router.put("/{telegram_id}/token", response_model=TokenData)
async def update_token(telegram_id: str, db: AsyncSession = Depends(get_db)):
    res = await _update_user_token(telegram_id=telegram_id, db=db)
    return res
