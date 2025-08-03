from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.queries.actions.analytics.get import _show_personal_queries
from src.api.queries.actions.prompt_query.post import _create_query
from src.api.queries.actions.scenario.post import _start_scenario
from src.api.queries.schemas import (
    UserQueryBase,
    UserQueryResult,
    UserQueryScenarioBase,
)
from src.api.users.actions.base_user_actions import _get_user
from src.api.utils import verify_user_data
from src.db.session import get_db

query_router = APIRouter(dependencies=[Depends(verify_user_data)])


@query_router.post("/{telegram_id}", response_model=UserQueryResult)
async def create_query(
    telegram_id: str,
    body: UserQueryBase,
    db: AsyncSession = Depends(get_db),
) -> UserQueryResult:

    user = await _get_user(telegram_id=telegram_id, db=db)

    vision = False
    if body.vision and body.vision == True:
        vision = body.vision

    res = await _create_query(
        prompt_id=body.prompt_id,
        user_id=user.uuid,
        query=body.query,
        story=body.story,
        vision=vision,
        db=db,
    )

    return res


@query_router.post("/{telegram_id}/scenario", response_model=List[UserQueryResult])
async def start_scenario(
    telegram_id: str,
    body: UserQueryScenarioBase,
    db: AsyncSession = Depends(get_db),
):

    result = await _start_scenario(
        telegram_id=telegram_id, scenario_id=body.scenario_id, query=body.query, db=db
    )

    return result


@query_router.get("/{telegram_id}/{prompt_id}")
async def get_prompt_personal_queries(
    prompt_id: str,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):

    res = await _show_personal_queries(offset=offset, prompt_id=prompt_id, db=db)
    return res
