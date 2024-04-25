from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.queries.actions import _create_query
from src.api.queries.models import UserQueryBase, UserQueryResult

from src.api.utils import verify_user_data

from src.db.session import get_db


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
