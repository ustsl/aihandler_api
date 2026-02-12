from sqlalchemy.ext.asyncio import AsyncSession


from src.api.queries.actions.prompt_query.post import _create_query
from src.api.scenarios.actions.get import _get_scenario_detail
from src.api.users.actions.base_user_actions import _get_user
from src.api.utils import handle_dal_errors


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
        current_query = query if prompt.independent else previous_result

        query_result = await _create_query(
            user_id=user.uuid,
            prompt_id=prompt.prompt_id,
            query=current_query,
            db=db,
        )

        previous_result = query_result.get("result", "")
        results.append(query_result)

    return results
