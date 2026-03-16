import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.db.dals import BaseDAL
from src.db.users.models import (UserAccountModel, UserSettingsModel,
                                 UserTokenModel)
from src.db.utils import exception_dal

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################

class UsersDAL(BaseDAL):
    @exception_dal
    async def create(self, **data):
        obj = self.model(**data)
        self.db_session.add(obj)
        await self.db_session.flush()

        new_account = UserAccountModel(user_id=obj.uuid, balance=Decimal("0.50"))
        self.db_session.add(new_account)
        await self.db_session.flush()

        new_token = UserTokenModel(user_id=obj.uuid, token=str(uuid.uuid4()))
        self.db_session.add(new_token)
        await self.db_session.flush()

        new_settings = UserSettingsModel(user_id=obj.uuid)
        self.db_session.add(new_settings)
        await self.db_session.flush()

        return obj

    @exception_dal
    async def get(self, telegram_id: str):
        query = (
            select(self.model)
            .options(
                joinedload(self.model.token),
                joinedload(self.model.accounts),
                joinedload(self.model.settings),
            )
            .where(
                self.model.telegram_id == telegram_id,
                self.model.is_deleted.is_(False),
            )
        )
        db_query_result = await self.db_session.execute(query)
        user = db_query_result.scalar_one_or_none()
        if user is None:
            return {"error": "Resource not found", "status": 404}
        return user
