from sqlalchemy.ext.asyncio import AsyncSession

from src.api.scenarios.schemas.post import ScenarioPostSchema
from src.api.scenarios.schemas.get import ScenarioGetSchema

from src.api.users.actions.account_user_actions import _get_user_account
from src.api.utils import handle_dal_errors


from src.db.scenarios.dals import ScenarioDAL
from src.db.scenarios.models import ScenarioModel


@handle_dal_errors
async def _create_scenario(
    body: ScenarioPostSchema, telegram_id: str, db: AsyncSession
) -> ScenarioGetSchema:
    async with db as session:
        async with session.begin():
            account = await _get_user_account(telegram_id=telegram_id, db=db)
            data_to_create = body.model_dump()
            data_to_create["account_id"] = account.uuid
            obj_dal = ScenarioDAL(session, ScenarioModel)
            result = await obj_dal.create(**data_to_create)

            return ScenarioGetSchema(
                id=result.uuid,
                title=result.title,
                description=result.description,
                time_create=result.time_create,
            )
