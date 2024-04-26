from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.queries.actions import _create_query, _show_queries
from src.api.queries.schemas import UserQueryBase, UserQueryResult

from src.api.utils import verify_token, verify_user_data

from src.db.session import get_db


query_router = APIRouter()


@query_router.post(
    "/{telegram_id}",
    response_model=UserQueryResult,
    dependencies=[Depends(verify_user_data)],
)
async def create_query(
    telegram_id: str,
    body: UserQueryBase,
    db: AsyncSession = Depends(get_db),
) -> UserQueryResult:

    res = await _create_query(
        prompt_id=body.prompt_id,
        telegram_id=telegram_id,
        query=body.query,
        story=body.story,
        db=db,
    )

    return res


@query_router.get("/", dependencies=[Depends(verify_token)])
async def get_queries(
    telegram_id: str = None,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):

    res = await _show_queries(offset=offset, db=db)

    return res
