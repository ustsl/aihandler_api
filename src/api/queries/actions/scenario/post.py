from sqlalchemy.ext.asyncio import AsyncSession

from src.api.prompts.actions import _show_prompt
from src.api.queries.actions.analytics.post import _save_query
from src.api.queries.actions.balance.put import _transfer_balance
from src.api.queries.actions.prompt_query.post import _create_query, _create_query_safe
from src.api.queries.modules.story_crop import story_crop_function
from src.api.scenarios.actions.get import _get_scenario_detail
from src.api.users.actions.account_user_actions import _get_user_account
from src.api.users.actions.base_user_actions import _get_user
from src.api.utils import handle_dal_errors
from src.db.scenarios.dals import ScenarioDAL
from src.db.scenarios.models import ScenarioModel
from src.db.users.dals.transaction import MoneyTransactionUserDal
from src.db.users.models import UserAccountModel
from src.modules.gpt.handler import gpt_handler


@handle_dal_errors
async def _start_scenario(
    telegram_id: str,
    scenario_id: str,
    query: str,
    db: AsyncSession,
):

    user = await _get_user(telegram_id=telegram_id, db=db)

    scenario_object = await _get_scenario_detail(
        telegram_id=telegram_id, scenario_id=scenario_id, db=db
    )

    results = []

    previous_result = ""

    for prompt in scenario_object.prompts:

        if prompt.independent:
            query = query
        else:
            query = previous_result

        query_result = await _create_query_safe(
            user=user,
            prompt=prompt,
            query=query,
            db=db,
        )

        previous_result = query_result.get("result", "")

        results.append(query_result)

    return results
