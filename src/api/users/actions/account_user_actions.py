from fastapi import HTTPException

from src.api.users.actions.base_user_actions import _get_user
from src.api.users.schemas import (
    AccountData,
    UserBalance,
    UserDataExtend,
)
from src.api.utils import handle_dal_errors
from src.db.users.dals.account import UserAccountDal
from src.db.users.models import UserAccountModel

from sqlalchemy.ext.asyncio import AsyncSession


@handle_dal_errors
async def _get_user_account(telegram_id: str, db: AsyncSession) -> AccountData:
    user = await _get_user(telegram_id=telegram_id, db=db)
    return user.accounts


@handle_dal_errors
async def _update_user_account_balance(
    telegram_id: str, balance: UserBalance, db: AsyncSession
) -> UserDataExtend:
    async with db as session:
        async with session.begin():
            account = await _get_user_account(telegram_id=telegram_id, db=session)
            user_admin_dal = UserAccountDal(session, UserAccountModel)
            await user_admin_dal.update_balance(
                user_account_id=account.uuid,
                money=balance.balance + account.balance,
            )
            return account
