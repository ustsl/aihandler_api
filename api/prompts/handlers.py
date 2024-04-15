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
from api.prompts.models import GPTPromptCreate, GPTPromptShortShow, GPTPromptShow

from db.session import get_db

prompt_router = APIRouter()


@prompt_router.post("/", response_model=GPTPromptShortShow)
async def create_prompt(
    body: GPTPromptCreate, db: AsyncSession = Depends(get_db)
) -> GPTPromptShortShow:
    return await _create_new_prompt(body, db)


@prompt_router.get("/")
async def get_prompts(db: AsyncSession = Depends(get_db)):
    res = await _show_prompts(db)
    return res


@prompt_router.get("/")
async def get_prompts(db: AsyncSession = Depends(get_db)) -> List[GPTPromptShow]:
    res = await _show_prompts(db)
    return res


@prompt_router.get("/{id}")
async def get_prompt(id: UUID, db: AsyncSession = Depends(get_db)):
    res = await _show_prompt(id, db)
    return res


@prompt_router.put("/{id}")
async def update_prompt(id: UUID, updates: dict, db: AsyncSession = Depends(get_db)):
    res = await _update_prompt(id, updates, db)
    return res


@prompt_router.delete("/{id}")
async def delete_prompt(id: UUID, db: AsyncSession = Depends(get_db)):
    res = await _delete_prompt(id, db)
    return res
