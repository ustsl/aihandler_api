from decimal import ROUND_UP, Decimal
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.ext.declarative import DeclarativeMeta


class MoneyTransactionUserDal:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model
        self._user_account_id = None
        self._user_account = None

    async def check_balance(self, user_account_id: uuid.UUID):
        # Check sender
        self._user_account_id = user_account_id
        user_account = await self.db_session.execute(
            select(self.model).where(self.model.account_id == user_account_id)
        )
        self._user_account = user_account.scalars().first()
        if self._user_account is None:
            return {"error": "User not found", "status": 404}
        if self._user_account.balance < Decimal("0.1"):
            return {"error": "Low balance", "status": 500}
        return {"result": True}

    async def decrease_balance(self, money):
        if not self._user_account or not self._user_account_id:
            return {"error": "Prompt account not found", "status": 404}

        new_user_balance = float(self._user_account.balance) - money
        await self.db_session.execute(
            update(self.model)
            .where(self.model.account_id == self._user_account_id)
            .values(balance=new_user_balance)
        )
        return {"result": True}


class MoneyTransactionRecipientDAL:
    def __init__(self, db_session: AsyncSession, model: DeclarativeMeta):
        self.db_session = db_session
        self.model = model

    async def send(self, prompt_account_id: uuid.UUID, money: Decimal):
        # Check recipient
        prompt_account = await self.db_session.execute(
            select(self.model).where(self.model.account_id == prompt_account_id)
        )
        prompt_account = prompt_account.scalars().first()
        if prompt_account is None:
            return {"error": "Prompt account not found", "status": 404}
        # Add +10% balance
        additional_amount = money * 0.10
        new_prompt_balance = float(prompt_account.balance) + additional_amount
        await self.db_session.execute(
            update(self.model)
            .where(self.model.account_id == prompt_account_id)
            .values(balance=new_prompt_balance)
        )
        return {"status": 201}
