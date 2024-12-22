from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.scenarios.actions.delete import _delete_scenario
from src.api.scenarios.actions.get import (_get_scenario_detail,
                                           _get_scenario_list)
from src.api.scenarios.actions.post import _create_scenario
from src.api.scenarios.actions.update import _update_scenario
from src.api.scenarios.schemas.get import (ScenarioGetFullSchema,
                                           ScenarioGetSchema,
                                           ScenariosGetListSchema)
from src.api.scenarios.schemas.post import ScenarioPostSchema
from src.api.scenarios.schemas.put import (ScenarioGetAfterUpdateFullSchema,
                                           ScenarioUpdateBodySchema)
from src.api.utils import verify_user_data
from src.db.session import get_db

scenario_router = APIRouter(dependencies=[Depends(verify_user_data)])


@scenario_router.post("/{telegram_id}", response_model=ScenarioGetSchema)
async def create_scenario(
    body: ScenarioPostSchema, telegram_id: str, db: AsyncSession = Depends(get_db)
):
    result = await _create_scenario(body=body, telegram_id=telegram_id, db=db)
    return result


@scenario_router.get("/{telegram_id}", response_model=ScenariosGetListSchema)
async def get_scenatios(
    telegram_id: str,
    search_query: str = None,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    result = await _get_scenario_list(
        telegram_id=telegram_id, offset=offset, search_query=search_query, db=db
    )
    return result


@scenario_router.get(
    "/{telegram_id}/{scenario_id}", response_model=ScenarioGetFullSchema
)
async def get_prompt(
    telegram_id: str,
    scenario_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await _get_scenario_detail(
        scenario_id=scenario_id, telegram_id=telegram_id, db=db
    )
    return result


@scenario_router.put(
    "/{telegram_id}/{scenario_id}", response_model=ScenarioGetFullSchema
)
async def update_prompt(
    scenario_id: UUID,
    telegram_id: str,
    updates: ScenarioUpdateBodySchema,
    db: AsyncSession = Depends(get_db),
):
    result = await _update_scenario(
        updates=updates, telegram_id=telegram_id, scenario_id=scenario_id, db=db
    )
    return result


@scenario_router.delete("/{telegram_id}/{scenario_id}")
async def delete_prompt(
    scenario_id: UUID, telegram_id, db: AsyncSession = Depends(get_db)
):
    delete = await _delete_scenario(
        scenario_id=scenario_id, telegram_id=telegram_id, db=db
    )
    return delete
