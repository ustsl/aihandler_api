from sqlalchemy.ext.asyncio import AsyncSession

from src.api.scenarios.schemas.post import ScenarioPostSchema
from src.api.scenarios.schemas.get import ScenarioGetSchema, ScenariosGetListSchema


from src.api.users.actions.account_user_actions import _get_user_account
from src.api.utils import handle_dal_errors


from src.db.scenarios.dals import ScenarioDAL
from src.db.scenarios.models import ScenarioModel


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
