from fastapi import HTTPException
from src.api.users.models import (
    AccountData,
    UserBalance,
    UserDataBase,
    UserDataExtend,
    UserDataWithId,
)
from src.api.utils import handle_dal_errors
from src.db.users.dals.admin import AdminUserAccountDal
from src.db.users.dals.base import UsersDAL
from src.db.users.models import UserAccountModel, UserModel

from sqlalchemy.ext.asyncio import AsyncSession


async def _create_new_user(body: UserDataBase, db) -> UserDataWithId:
    async with db as session:
        async with session.begin():
            obj_dal = UsersDAL(session, UserModel)
            result = await obj_dal.create(telegram_id=body.telegram_id)

            if isinstance(result, dict) and result.get("error"):
                raise HTTPException(status_code=500, detail=result["error"])

            return UserDataWithId(
                id=result.uuid,
                telegram_id=result.telegram_id,
            )


@handle_dal_errors
async def _get_user(telegram_id: str, db: AsyncSession) -> UserDataExtend:
    obj_dal = UsersDAL(db, UserModel)
    result = await obj_dal.get(telegram_id)
    return result


@handle_dal_errors
async def _get_users(db: AsyncSession):
    obj_dal = UsersDAL(db, UserModel)
    result = await obj_dal.list()
    return result


@handle_dal_errors
async def _get_user_account(telegram_id: str, db: AsyncSession) -> AccountData:
    user = await _get_user(telegram_id=telegram_id, db=db)
    return user.accounts


@handle_dal_errors
async def _update_user_account_balance(
    telegram_id: str, balance: UserBalance, db: AsyncSession
) -> UserDataExtend:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    user_admin_dal = AdminUserAccountDal(db, UserAccountModel)
    await user_admin_dal.update_balance(
        user_account_id=account.account_id, money=balance.balance
    )

    return account
