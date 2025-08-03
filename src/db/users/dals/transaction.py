import uuid
from decimal import ROUND_UP, Decimal

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta


class MoneyTransactionUserDal:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model

    async def check_balance(self, user_id: uuid.UUID):
        user_account = await self.db_session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        user_account = user_account.scalars().first()
        if user_account is None:
            return {"error": "User not found", "status": 404}
        if user_account.balance < Decimal("0.1"):
            return {"error": "Low balance", "status": 500}
        return {"result": user_account.balance}

    async def decrease_balance(self, user_id, payment):
        user_account = await self.db_session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        user_account = user_account.scalars().first()
        new_user_balance = float(user_account.balance) - payment
        await self.db_session.execute(
            update(self.model)
            .where(self.model.user_id == user_id)
            .values(balance=new_user_balance)
        )
        return {"result": user_account.balance}

    async def cashback_balance(self, user_id: uuid.UUID, payment: Decimal):
        user_account = await self.db_session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        user_account = user_account.scalars().first()
        additional_amount = payment * 0.10
        new_prompt_balance = float(user_account.balance) + additional_amount
        await self.db_session.execute(
            update(self.model)
            .where(self.model.user_id == user_id)
            .values(balance=new_prompt_balance)
        )
        return {"result": user_account.balance}
