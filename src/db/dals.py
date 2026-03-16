import uuid

from sqlalchemy import delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta

from src.db.utils import exception_dal

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class BaseDAL:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model

    def _has_column(self, column_name: str) -> bool:
        return hasattr(self.model, column_name)

    @exception_dal
    async def create(self, **data):
        new_obj = self.model(**data)
        self.db_session.add(new_obj)
        await self.db_session.flush()
        return new_obj

    async def create_safe(self, **data):
        new_obj = self.model(**data)
        self.db_session.add(new_obj)

    @exception_dal
    async def list(self, page_size: int = 30, offset: int = 0, order_param="uuid"):

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
        conditions = [self.model.uuid == id]
        if self._has_column("is_deleted"):
            conditions.append(self.model.is_deleted.is_(False))
        query = select(self.model).where(*conditions)
        db_query_result = await self.db_session.execute(query)
        obj = db_query_result.scalar_one_or_none()
        if obj is None:
            return {"error": "Resource not found", "status": 404}
        return obj

    @exception_dal
    async def update(self, uuid: uuid.UUID, **kwargs):
        update_values = {k: v for k, v in kwargs.items() if v is not None}
        if not update_values:
            return {"success": "Nothing to update"}

        conditions = [self.model.uuid == uuid]
        if self._has_column("is_deleted"):
            conditions.append(self.model.is_deleted.is_(False))

        query = (
            update(self.model)
            .where(*conditions)
            .values(**update_values)
            .execution_options(synchronize_session="fetch")
        )
        db_result = await self.db_session.execute(query)
        if db_result.rowcount == 0:
            await self.db_session.rollback()
            return {"error": "Resource not found", "status": 404}

        await self.db_session.commit()
        return {"success": "Updated successfully"}

    @exception_dal
    async def delete(self, id: uuid.UUID):
        if self._has_column("is_deleted"):
            query = (
                update(self.model).where(self.model.uuid == id).values(is_deleted=True)
            )
        else:
            query = delete(self.model).where(self.model.uuid == id)

        db_result = await self.db_session.execute(query)
        if db_result.rowcount == 0:
            await self.db_session.rollback()
            return {"error": "Resource not found", "status": 404}

        await self.db_session.commit()
        return {"success": "Prompt deleted successfully"}
