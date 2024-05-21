from fastapi import HTTPException

from src.api.users.schemas import (
    UserDataBase,
    UserDataExtend,
)
from src.api.utils import handle_dal_errors

from src.db.adapter import model_to_dict
from src.db.users.dals.user import UsersDAL
from src.db.users.models import UserModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound


@handle_dal_errors
async def _get_user(telegram_id: str, db: AsyncSession):
    obj_dal = UsersDAL(db, UserModel)
    result = await obj_dal.get(telegram_id)
    return result


@handle_dal_errors
async def _get_users(db: AsyncSession):
    obj_dal = UsersDAL(db, UserModel)
    result = await obj_dal.list()
    result_dict = model_to_dict(result)
    return result_dict


async def _create_new_user(body: UserDataBase, db) -> UserDataExtend:
    async with db as session:
        async with session.begin():
            obj_dal = UsersDAL(session, UserModel)
            create_user_process = await obj_dal.create(telegram_id=body.telegram_id)

    get_user = await obj_dal.get(telegram_id=body.telegram_id)
    if isinstance(get_user, dict) and get_user.get("error"):
        raise HTTPException(status_code=500, detail=create_user_process["error"])
    return get_user


@handle_dal_errors
async def _block_user(
    telegram_id: str, is_active: bool, db: AsyncSession
) -> UserDataExtend:
    try:
        user = await _get_user(telegram_id=telegram_id, db=db)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    obj_dal = UsersDAL(db, UserModel)
    await obj_dal.update(uuid=user.uuid, is_active=is_active)
    return user
