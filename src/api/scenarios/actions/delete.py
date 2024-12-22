from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.scenarios.actions.get import _get_scenario_detail
from src.api.scenarios.schemas.get import ScenarioGetSchema
from src.api.scenarios.schemas.post import ScenarioPostSchema
from src.api.scenarios.schemas.put import ScenarioUpdateBodySchema
from src.api.users.actions.account_user_actions import _get_user_account
from src.api.utils import handle_dal_errors
from src.db.prompts.dals import PromptDAL
from src.db.prompts.models import PromptModel
from src.db.scenarios.dals import PromptScenarioDAL, ScenarioDAL
from src.db.scenarios.models import ScenarioModel, ScenarioPromptsModel


@handle_dal_errors
async def _delete_scenario(
    telegram_id: str,
    scenario_id: str,
    db: AsyncSession,
):

    account = await _get_user_account(telegram_id=telegram_id, db=db)
    obj_dal = ScenarioDAL(db, ScenarioModel)
    object = await obj_dal.get(scenario_id=scenario_id, account_id=account.uuid)
    if not object:
        raise HTTPException(status_code=404, detail="Not found")

    await obj_dal.delete(scenario_id)
    return None
