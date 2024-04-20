from sqlalchemy.orm import selectinload
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import desc, select, update
from sqlalchemy.ext.declarative import DeclarativeMeta
from db.dals import BaseDAL
from db.prompts.models import PromptModel
from db.users.models import UserAccountModel

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class PromptDAL(BaseDAL):
    async def get(self, id: uuid.UUID):
        try:
            # Выполняем запрос с необходимыми JOIN'ами
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
