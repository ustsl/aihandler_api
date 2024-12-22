from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.queries.actions.analytics.get import _show_queries
from src.api.utils import verify_token
from src.db.session import get_db

analytics_router = APIRouter(dependencies=[Depends(verify_token)])


@analytics_router.get("/queries")
async def get_queries(
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    res = await _show_queries(offset=offset, db=db)
    return res
