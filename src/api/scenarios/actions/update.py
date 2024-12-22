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
async def _update_scenario(
    updates: ScenarioUpdateBodySchema,
    telegram_id: str,
    scenario_id: str,
    db: AsyncSession,
):

    account = await _get_user_account(telegram_id=telegram_id, db=db)
    obj_dal = ScenarioDAL(db, ScenarioModel)
    object = await obj_dal.get(scenario_id=scenario_id, account_id=account.uuid)
    if not object:
        raise HTTPException(status_code=404, detail="Not found")

    updates_dict = updates.model_dump()
    updates_dict.pop("prompts", None)
    await obj_dal.update(scenario_id, **updates_dict)

    ps_dal = PromptScenarioDAL(db, ScenarioPromptsModel)
    await ps_dal.delete(scenario_id=scenario_id)

    if updates.prompts and len(updates.prompts) > 0:
        prompts = updates.prompts

        prompt_dal = PromptDAL(db, PromptModel)

        async with db.begin():
            for prompt in prompts:
                prompt_object = await prompt_dal.get(prompt.prompt_id)
                if prompt_object and (
                    prompt_object.is_open
                    or telegram_id == prompt_object.account_telegram_id
                ):
                    data = {
                        "scenario_id": scenario_id,
                        "prompt_id": prompt.prompt_id,
                        "order": prompt.order,
                        "independent": prompt.independent,
                    }

                    await ps_dal.create_safe(**data)
            await db.commit()

    object = await _get_scenario_detail(
        scenario_id=scenario_id, telegram_id=telegram_id, db=db
    )
    return object
