from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.queries.actions import _create_query
from api.queries.models import UserQueryBase, UserQueryResult

from api.utils import verify_token
from db.session import get_db


query_router = APIRouter()


@query_router.post("/", response_model=UserQueryResult)
async def create_query(
    request: Request, body: UserQueryBase, db: AsyncSession = Depends(get_db)
) -> UserQueryResult:
    res = await _create_query(id=body.prompt_id, query=body.query, db=db)
    return res
