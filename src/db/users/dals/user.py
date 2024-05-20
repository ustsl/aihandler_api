from src.db.dals import BaseDAL

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

import uuid
from decimal import Decimal
from sqlalchemy.orm import joinedload

from src.db.users.models import UserAccountModel, UserTokenModel, UserSettingsModel


class UsersDAL(BaseDAL):

    async def create(self, **data):
        try:
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
        except Exception as e:
            await self.db_session.rollback()
            error_msg = (
                f"Error creating user with associated account and token: {str(e)}"
            )
            return {"error": error_msg}

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
                self.model.is_deleted == False,
            )
        )
        db_query_result = await self.db_session.execute(query)
        return db_query_result.scalar_one()
