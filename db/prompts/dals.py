from sqlalchemy.orm import selectinload
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import desc, func, select, update
from sqlalchemy.ext.declarative import DeclarativeMeta
from db.dals import BaseDAL
from db.prompts.models import PromptModel
from db.users.models import UserAccountModel
from sqlalchemy import or_

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class PromptDAL(BaseDAL):

    async def get(self, id: uuid.UUID):
        try:
            query = (
                select(PromptModel)
                .options(
                    selectinload(PromptModel.account).selectinload(
                        UserAccountModel.user
                    )
                )
                .where(PromptModel.uuid == id, PromptModel.is_deleted == False)
            )
            db_query_result = await self.db_session.execute(query)
            return db_query_result.scalar_one()

        except NoResultFound:
            return {"error": "Prompt not found", "status": 404}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error retrieving prompt: {str(e)}", "status": 500}

    async def list(
        self,
        page_size: int = 5,
        offset: int = 0,
        account_id: uuid.UUID = None,
        search_query: str = None,
    ):
        try:
            conditions = [
                self.model.is_active == True,
                self.model.is_deleted == False,
                or_(self.model.is_open == True, self.model.account_id == account_id),
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
        except Exception as e:
            await self.db_session.rollback()
            error_msg = f"Error listing prompts: {str(e)}"
            return {"error": error_msg}
