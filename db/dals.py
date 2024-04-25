import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import desc, select, update
from sqlalchemy.ext.declarative import DeclarativeMeta

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class BaseDAL:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model

    async def create(self, **data):
        try:
            new_prompt = self.model(**data)
            self.db_session.add(new_prompt)
            await self.db_session.flush()
            return new_prompt
        except Exception as e:
            await self.db_session.rollback()
            error_msg = f"Error creating prompt: {str(e)}"
            return {"error": error_msg}

    async def list(self, page_size: int = 1, offset: int = 0):
        try:
            query = (
                select(self.model)
                .where(self.model.is_active == True, self.model.is_deleted == False)
                .order_by(desc(self.model.time_update))
                .limit(page_size)
                .offset(offset)
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
            query = select(self.model).where(
                self.model.uuid == id, self.model.is_deleted == False
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
                update(self.model)
                .where(self.model.uuid == id)
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
                update(self.model).where(self.model.uuid == id).values(is_deleted=True)
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Prompt deleted successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error deleting prompt: {str(e)}"}
