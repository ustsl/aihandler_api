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

from api.queries.actions import _create_query
from api.queries.models import UserQueryBase, UserQueryResult

from db.session import get_db


query_router = APIRouter()


@query_router.post("/", response_model=UserQueryResult)
async def create_query(
    body: UserQueryBase, db: AsyncSession = Depends(get_db)
) -> UserQueryResult:
    res = await _create_query(id=body.prompt_id, query=body.query, db=db)
    return res
