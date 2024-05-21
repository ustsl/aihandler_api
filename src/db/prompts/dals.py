from sqlalchemy.orm import selectinload
import uuid

from sqlalchemy.exc import NoResultFound
from sqlalchemy import desc, func, select


from src.db.dals import BaseDAL
from src.db.prompts.models import PromptModel
from src.db.users.models import UserAccountModel

from sqlalchemy import or_

from src.db.utils import exception_dal

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class PromptDAL(BaseDAL):

    @exception_dal
    async def get(self, id: uuid.UUID):
        query = (
            select(PromptModel)
            .options(
                selectinload(PromptModel.account).selectinload(UserAccountModel.user)
            )
            .where(PromptModel.uuid == id, PromptModel.is_deleted == False)
        )
        db_query_result = await self.db_session.execute(query)
        return db_query_result.scalar_one()

    @exception_dal
    async def list(
        self,
        page_size: int = 10,
        offset: int = 0,
        account_id: uuid.UUID = None,
        search_query: str = None,
        only_yours: bool = True,
    ):

        conditions = [
            self.model.is_active == True,
            self.model.is_deleted == False,
        ]
        if search_query:
            conditions.append(self.model.title.ilike(f"%{search_query}%"))
        if only_yours:
            conditions.append(self.model.account_id == account_id)
        else:
            conditions.append(
                or_(self.model.is_open == True, self.model.uuid == account_id)
            )

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
