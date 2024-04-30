from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.prompts.actions import (
    _create_new_prompt,
    _delete_prompt,
    _show_prompt,
    _show_prompts,
    _update_prompt,
)
from src.api.prompts.schemas import GPTPromptCreate, GPTPromptBase, GPTPromptList

from src.api.users.actions.base_user_actions import _get_user_account
from src.api.utils import verify_user_data
from src.db.session import get_db

prompt_router = APIRouter(dependencies=[Depends(verify_user_data)])


@prompt_router.post("/{telegram_id}", response_model=GPTPromptCreate)
async def create_prompt(
    body: GPTPromptBase, telegram_id: str, db: AsyncSession = Depends(get_db)
) -> GPTPromptCreate:

    return await _create_new_prompt(body, telegram_id, db)


@prompt_router.get("/{telegram_id}", response_model=GPTPromptList)
async def get_prompts(
    telegram_id: str,
    search_query: str = None,
    offset: int = 0,
    only_yours: bool = True,
    db: AsyncSession = Depends(get_db),
):

    res = await _show_prompts(db, telegram_id, offset, search_query, only_yours)
    return res


@prompt_router.get("/{telegram_id}/{prompt_id}")
async def get_prompt(
    telegram_id: str,
    prompt_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    prompt = await _show_prompt(prompt_id=prompt_id, telegram_id=telegram_id, db=db)
    return prompt


@prompt_router.put("/{telegram_id}/{id}")
async def update_prompt(
    id: UUID, telegram_id: str, updates: dict, db: AsyncSession = Depends(get_db)
):
    res = await _update_prompt(id, telegram_id, updates, db)
    return res


@prompt_router.delete("/{telegram_id}/{id}")
async def delete_prompt(id: UUID, telegram_id, db: AsyncSession = Depends(get_db)):
    res = await _delete_prompt(id, telegram_id, db)
    return res
