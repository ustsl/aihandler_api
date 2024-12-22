import uuid

from sqlalchemy import delete, desc, func, inspect, or_, select, text, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.db.dals import BaseDAL
from src.db.scenarios.models import ScenarioModel, ScenarioPromptsModel
from src.db.users.models import UserAccountModel
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

    async def get(self, scenario_id: uuid.UUID, account_id: uuid.UUID):
        query = select(self.model).where(
            self.model.uuid == scenario_id,
            self.model.account_id == account_id,
            self.model.is_deleted == False,
        )
        db_query_result = await self.db_session.execute(query)
        return db_query_result.scalar_one_or_none()

    @exception_dal
    async def delete(self, scenario_id: str):
        delete_query = delete(self.model).where(self.model.uuid == scenario_id)
        await self.db_session.execute(delete_query)
        await self.db_session.commit()


class PromptScenarioDAL(BaseDAL):

    async def get(self, scenario_id: uuid.UUID, prompt_id: uuid.UUID):
        query = select(self.model).where(
            self.model.scenario_id == scenario_id,
            self.model.prompt == prompt_id,
        )
        db_query_result = await self.db_session.execute(query)
        return db_query_result.scalar_one_or_none()

    @exception_dal
    async def delete(self, scenario_id: str):
        delete_query = delete(self.model).where(self.model.scenario_id == scenario_id)
        await self.db_session.execute(delete_query)
        await self.db_session.commit()

    async def list(self, scenario_id):
        query = text(
            """
        SELECT 
            relations.uuid,
            relations.scenario_id,
            relations.prompt_id,
            relations.independent,
            relations.order,
            prompts.title,
            prompts.description,
            prompts.model
        FROM scenario_prompts_relation AS relations
        JOIN prompts as prompts
        ON relations.prompt_id = prompts.uuid 
        WHERE scenario_id = :scenario_id
        ORDER BY relations.order
            """
        )
        db_query_result = await self.db_session.execute(
            query, {"scenario_id": scenario_id}
        )
        obj = db_query_result.fetchall()
        return obj
