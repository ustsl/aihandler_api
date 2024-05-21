import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import desc, select, update, func
from sqlalchemy.ext.declarative import DeclarativeMeta

from src.db.utils import exception_dal

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class BaseDAL:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model

    @exception_dal
    async def create(self, **data):
        try:
            new_prompt = self.model(**data)
            self.db_session.add(new_prompt)
            await self.db_session.flush()
            return new_prompt
        except Exception as e:
            await self.db_session.rollback()
            error_msg = f"Error creating object: {str(e)}"
            return {"error": error_msg}

    @exception_dal
    async def list(self, page_size: int = 10, offset: int = 0, order_param="uuid"):

        query = (
            select(self.model)
            .order_by(desc(getattr(self.model, order_param)))
            .limit(page_size)
            .offset(offset)
        )
        db_query_result = await self.db_session.execute(query)
        result = db_query_result.scalars().all()

        total_count_query = select(func.count()).select_from(self.model)
        total_count_result = await self.db_session.execute(total_count_query)
        total_count = total_count_result.scalar()

        return {"result": result, "total": total_count}

    @exception_dal
    async def get(self, id: uuid.UUID):
        query = select(self.model).where(
            self.model.uuid == id, self.model.is_deleted == False
        )
        db_query_result = await self.db_session.execute(query)
        prompt = db_query_result.scalar_one()
        return prompt

    @exception_dal
    async def update(self, uuid: uuid.UUID, **kwargs):
        try:
            query = (
                update(self.model)
                .where(self.model.uuid == uuid)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
            )
            await self.db_session.execute(query)
            await self.db_session.commit()
            return {"success": "Updated successfully"}
        except Exception as e:
            await self.db_session.rollback()
            return {"error": f"Error updating: {str(e)}"}

    @exception_dal
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
