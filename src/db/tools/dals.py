import uuid

from sqlalchemy import and_, delete, desc, func, or_, select
from sqlalchemy.orm import selectinload

from src.db.dals import BaseDAL
from src.db.tools.models import PromptToolModel, ToolCallLogModel, ToolModel
from src.db.utils import exception_dal


class ToolDAL(BaseDAL):
    @exception_dal
    async def list_available(
        self,
        account_id: uuid.UUID,
        offset: int = 0,
        page_size: int = 30,
        include_system: bool = True,
    ):
        conditions = [
            self.model.is_active.is_(True),
            self.model.is_deleted.is_(False),
        ]
        if include_system:
            conditions.append(
                or_(self.model.account_id == account_id, self.model.account_id.is_(None))
            )
        else:
            conditions.append(self.model.account_id == account_id)

        query = (
            select(self.model)
            .where(*conditions)
            .order_by(desc(self.model.time_update))
            .limit(page_size)
            .offset(offset)
        )
        db_query_result = await self.db_session.execute(query)
        result = db_query_result.scalars().all()

        total_query = select(func.count()).select_from(self.model).where(*conditions)
        total_result = await self.db_session.execute(total_query)
        total = total_result.scalar()
        return {"result": result, "total": total}

    @exception_dal
    async def get_available(self, tool_id: uuid.UUID, account_id: uuid.UUID):
        query = select(self.model).where(
            self.model.uuid == tool_id,
            self.model.is_deleted.is_(False),
            or_(self.model.account_id == account_id, self.model.account_id.is_(None)),
        )
        db_query_result = await self.db_session.execute(query)
        return db_query_result.scalar_one_or_none()

    @exception_dal
    async def get_owner_tool(self, tool_id: uuid.UUID, account_id: uuid.UUID):
        query = select(self.model).where(
            self.model.uuid == tool_id,
            self.model.is_deleted.is_(False),
            self.model.account_id == account_id,
        )
        db_query_result = await self.db_session.execute(query)
        return db_query_result.scalar_one_or_none()


class PromptToolDAL(BaseDAL):
    @exception_dal
    async def list_prompt_tools(self, prompt_id: uuid.UUID):
        query = (
            select(PromptToolModel)
            .options(selectinload(PromptToolModel.tool))
            .where(PromptToolModel.prompt_id == prompt_id)
            .order_by(PromptToolModel.sort_order, PromptToolModel.time_create)
        )
        db_query_result = await self.db_session.execute(query)
        return db_query_result.scalars().all()

    @exception_dal
    async def replace_for_prompt(self, prompt_id: uuid.UUID, tool_ids: list[uuid.UUID]):
        delete_query = delete(PromptToolModel).where(PromptToolModel.prompt_id == prompt_id)
        await self.db_session.execute(delete_query)

        for sort_order, tool_id in enumerate(tool_ids):
            await self.create_safe(
                prompt_id=prompt_id,
                tool_id=tool_id,
                sort_order=sort_order,
            )


class ToolCallLogDAL(BaseDAL):
    async def create_safe_log(self, **data):
        await self.create_safe(**data)
