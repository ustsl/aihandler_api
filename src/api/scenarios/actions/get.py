from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.scenarios.schemas.get import (
    ScenarioGetFullSchema,
    ScenarioGetSchema,
    ScenarioPromptsGetBodySchema,
    ScenariosGetListSchema,
)
from src.api.users.actions.account_user_actions import _get_user_account
from src.api.utils import handle_dal_errors
from src.db.scenarios.dals import PromptScenarioDAL, ScenarioDAL
from src.db.scenarios.models import ScenarioModel, ScenarioPromptsModel


@handle_dal_errors
async def _get_scenario_list(
    db: AsyncSession,
    telegram_id: str = None,
    offset: int = 0,
    search_query: str = None,
) -> ScenariosGetListSchema:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    obj_dal = ScenarioDAL(db, ScenarioModel)

    raw_results = await obj_dal.list(
        account_id=account.uuid,
        offset=offset,
        search_query=search_query,
    )

    scenarios = [
        ScenarioGetSchema(
            id=result.uuid,
            title=result.title,
            description=result.description,
            time_create=result.time_create,
        )
        for result in raw_results.get("result")
    ]

    return ScenariosGetListSchema(result=scenarios, total=raw_results.get("total"))


@handle_dal_errors
async def _get_scenario_detail(
    scenario_id: str, telegram_id: str, db: AsyncSession
) -> ScenarioGetFullSchema:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    obj_dal = ScenarioDAL(db, ScenarioModel)
    object = await obj_dal.get(scenario_id=scenario_id, account_id=account.uuid)
    if object:
        ps_dal = PromptScenarioDAL(db, ScenarioPromptsModel)
        prompts = await ps_dal.list(scenario_id=scenario_id)
        return ScenarioGetFullSchema(
            uuid=object.uuid,
            title=object.title,
            description=object.description,
            prompts=[
                ScenarioPromptsGetBodySchema(
                    title=prompt.title,
                    description=prompt.description,
                    prompt_id=prompt.prompt_id,
                    order=prompt.order,
                    independent=prompt.independent,
                    model=prompt.model,
                )
                for prompt in prompts
            ],
            time_create=object.time_create,
        )

    raise HTTPException(status_code=404, detail="Not found")
