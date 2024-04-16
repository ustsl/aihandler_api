from fastapi import HTTPException
from api.users.models import (
    AccountData,
    TokenData,
    UserDataBase,
    UserDataExtend,
    UserDataWithId,
)
from api.utils import handle_dal_errors
from db.users.dals import UsersDAL
from db.users.models import UserModel
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
