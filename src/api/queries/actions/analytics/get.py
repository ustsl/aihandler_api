from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users.actions.base_user_actions import _get_user
from src.api.utils import handle_dal_errors
from src.db.queries.dals import QueryDAL
from src.db.queries.models import QueryModel


@handle_dal_errors
async def _show_queries(
    db: AsyncSession,
    telegram_id: str = None,
    offset: int = 0,
):
    if telegram_id:
        user = await _get_user(telegram_id=telegram_id, db=db)
        # TODO: create logic
    obj_dal = QueryDAL(db, QueryModel)
    results = await obj_dal.list(offset=offset, order_param="time_create")
    return results


@handle_dal_errors
async def _show_personal_queries(
    db: AsyncSession,
    prompt_id: str = None,
    offset: int = 0,
):

    obj_dal = QueryDAL(db, QueryModel)
    results = await obj_dal.personal_list(prompt_id=prompt_id, offset=offset)
    return results
