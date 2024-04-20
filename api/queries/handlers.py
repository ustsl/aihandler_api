from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.queries.actions import _create_query
from api.queries.models import UserQueryBase, UserQueryResult

from api.utils import verify_token, verify_user_data
from db.session import get_db
from db.users.dals import UsersDAL


query_router = APIRouter(dependencies=[Depends(verify_user_data)])


@query_router.post("/", response_model=UserQueryResult)
async def create_query(
    telegram_id: str,
    body: UserQueryBase,
    db: AsyncSession = Depends(get_db),
) -> UserQueryResult:

    res = await _create_query(
        prompt_id=body.prompt_id, telegram_id=telegram_id, query=body.query, db=db
    )
    return res
