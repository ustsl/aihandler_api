from sqlalchemy.orm import selectinload
import uuid

from sqlalchemy.exc import NoResultFound
from sqlalchemy import desc, func, select


from src.db.dals import BaseDAL
from src.db.scenarios.models import ScenarioModel, ScenarioPromptsModel
from src.db.users.models import UserAccountModel

from sqlalchemy import or_

from src.db.utils import exception_dal

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class ScenarioDAL(BaseDAL):
    @exception_dal
    async def list(
        self,
        page_size: int = 30,
        offset: int = 0,
        account_id: uuid.UUID = None,
        search_query: str = None,
    ):

        conditions = [
            self.model.is_active == True,
            self.model.is_deleted == False,
            self.model.account_id == account_id,
        ]
        if search_query:
            conditions.append(self.model.title.ilike(f"%{search_query}%"))

        query = (
            select(self.model)
            .where(*conditions)
            .order_by(desc(self.model.time_update))
            .limit(page_size)
            .offset(offset)
        )
        db_query_result = await self.db_session.execute(query)
        results = db_query_result.scalars().all()

        total_count_query = (
            select(func.count()).where(*conditions).select_from(self.model)
        )
        total_count_result = await self.db_session.execute(total_count_query)
        total_count = total_count_result.scalar()

        return {"result": results, "total": total_count}
