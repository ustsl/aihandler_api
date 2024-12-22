from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.queries.dals import QueryDAL
from src.db.queries.models import QueryModel


async def _save_query(
    user_id: UUID, prompt_id: UUID, query: str, result: str, db: AsyncSession
):
    query_dal = QueryDAL(db_session=db, model=QueryModel)
    result = await query_dal.create(
        user_id=user_id, prompt_id=prompt_id, query=query, result=result
    )
