import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from db.prompts.models import PromptModel
from sqlalchemy import desc, select, update, delete
from fastapi import status

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class PromptDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, title: str, description: str, prompt: str):
        try:
            new_prompt = PromptModel(
                title=title, description=description, prompt=prompt
            )
            self.db_session.add(new_prompt)
            await self.db_session.flush()
            return new_prompt
        except Exception as e:
            await self.db_session.rollback()
            error_msg = f"Error creating prompt: {str(e)}"
            return {"error": error_msg}

    async def list(self):
        try:
            query = (
                select(PromptModel)
                .where(PromptModel.is_active == True, PromptModel.is_deleted == False)
                .order_by(desc(PromptModel.time_update))
            )
            db_query_result = await self.db_session.execute(query)
            result = db_query_result.scalars().all()
            return result
        except Exception as e:
            await self.db_session.rollback()
            error_msg = f"Error listing prompts: {str(e)}"
            return {"error": error_msg}

    async def get(self, id: uuid.UUID):

        try:
            query = select(PromptModel).where(
                PromptModel.uuid == id, PromptModel.is_deleted == False
            )
            db_query_result = await self.db_session.execute(query)
            prompt = db_query_result.scalar_one()
            return prompt
        except NoResultFound:
            return {"error": "Prompt not found", "status": 404}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error retrieving prompt: {str(e)}", "status": 500}

    async def update(self, id: uuid.UUID, **kwargs):
        try:
            query = (
                update(PromptModel)
                .where(PromptModel.uuid == id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Prompt updated successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error updating prompt: {str(e)}"}

    async def delete(self, id: uuid.UUID):
        try:
            query = (
                update(PromptModel)
                .where(PromptModel.uuid == id)
                .values(is_deleted=True)
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Prompt deleted successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error deleting prompt: {str(e)}"}
