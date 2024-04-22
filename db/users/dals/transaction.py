from decimal import ROUND_UP, Decimal
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.ext.declarative import DeclarativeMeta


class MoneyTransactionDAL:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model
        self.user_account = None
        self.user_account_id = None

    async def check_balance(self, user_account_id: uuid.UUID):
        # Check sender
        user_account = await self.db_session.execute(
            select(self.model).where(self.model.account_id == user_account_id)
        )
        self.user_account = user_account.scalars().first()
        if self.user_account is None:
            return {"error": "User not found", "status": 404}
        if self.user_account.balance < Decimal("0.1"):
            return {"error": "Low balance", "status": 500}
        return {"result": True}

    async def send(
        self, user_account_id: uuid.UUID, prompt_account_id: uuid.UUID, money: Decimal
    ):
        # Shrink balance
        new_user_balance = float(self.user_account.balance) - money
        await self.db_session.execute(
            update(self.model)
            .where(self.model.account_id == user_account_id)
            .values(balance=new_user_balance)
        )

        # Check recipient
        prompt_account = await self.db_session.execute(
            select(self.model).where(self.model.account_id == prompt_account_id)
        )
        prompt_account = prompt_account.scalars().first()
        if prompt_account is None:
            return {"error": "Prompt account not found", "status": 404}

        # Add +15% balance
        additional_amount = money * 0.15
        new_prompt_balance = float(prompt_account.balance) + additional_amount
        await self.db_session.execute(
            update(self.model)
            .where(self.model.account_id == prompt_account_id)
            .values(balance=new_prompt_balance)
        )
        return {"status": 201}
