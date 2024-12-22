from sqlalchemy import desc, func, select

from src.db.dals import BaseDAL
from src.db.utils import exception_dal

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class QueryDAL(BaseDAL):
    @exception_dal
    async def personal_list(self, prompt_id, page_size: int = 30, offset: int = 0):

        query = (
            select(self.model)
            .where(getattr(self.model, "prompt_id") == prompt_id)
            .order_by(desc(getattr(self.model, "time_create")))
            .limit(page_size)
            .offset(offset)
        )
        db_query_result = await self.db_session.execute(query)
        result = db_query_result.scalars().all()

        total_count_query = (
            select(func.count())
            .select_from(self.model)
            .where(getattr(self.model, "prompt_id") == prompt_id)
        )
        total_count_result = await self.db_session.execute(total_count_query)
        total_count = total_count_result.scalar()

        return {"result": result, "total": total_count}
