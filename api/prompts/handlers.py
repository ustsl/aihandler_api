from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.prompts.actions import (
    _create_new_prompt,
    _delete_prompt,
    _show_prompt,
    _show_prompts,
    _update_prompt,
)
from api.prompts.models import GPTPromptCreate, GPTPromptBase

from api.utils import verify_user_data
from db.session import get_db

prompt_router = APIRouter(dependencies=[Depends(verify_user_data)])


@prompt_router.post("/", response_model=GPTPromptCreate)
async def create_prompt(
    body: GPTPromptBase, db: AsyncSession = Depends(get_db)
) -> GPTPromptCreate:
    return await _create_new_prompt(body, db)


@prompt_router.get("/")
async def get_prompts(db: AsyncSession = Depends(get_db)):
    res = await _show_prompts(db)
    return res


@prompt_router.get("/{prompt_id}")
async def get_prompt(
    telegram_id: str, prompt_id: UUID, db: AsyncSession = Depends(get_db)
):
    prompt = await _show_prompt(prompt_id=prompt_id, telegram_id=telegram_id, db=db)
    return prompt


@prompt_router.put("/{id}")
async def update_prompt(id: UUID, updates: dict, db: AsyncSession = Depends(get_db)):
    res = await _update_prompt(id, updates, db)
    return res


@prompt_router.delete("/{id}")
async def delete_prompt(id: UUID, db: AsyncSession = Depends(get_db)):
    res = await _delete_prompt(id, db)
    return res
