from decimal import ROUND_UP, Decimal
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.ext.declarative import DeclarativeMeta


class UserAccountDal:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model

    async def update_balance(self, user_account_id, money):

        await self.db_session.execute(
            update(self.model)
            .where(self.model.uuid == user_account_id)
            .values(balance=float(money))
        )

        await self.db_session.commit()
        return {"result": True}
