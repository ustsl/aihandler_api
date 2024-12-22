import uuid

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users.actions.base_user_actions import _get_user
from src.api.users.schemas import TokenData
from src.api.utils import handle_dal_errors
from src.db.adapter import model_to_dict
from src.db.users.dals.token import UserTokenDal
from src.db.users.dals.user import UsersDAL
from src.db.users.models import UserModel, UserTokenModel


@handle_dal_errors
async def _get_user_token(telegram_id: str, db: AsyncSession) -> TokenData:
    user = await _get_user(telegram_id=telegram_id, db=db)
    return user.token


@handle_dal_errors
async def _update_user_token(telegram_id: str, db: AsyncSession) -> TokenData:
    try:
        token = await _get_user_token(telegram_id=telegram_id, db=db)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    obj_dal = UserTokenDal(db, UserTokenModel)
    await obj_dal.update(uuid=token.uuid, token=str(uuid.uuid4()))
    token = await _get_user_token(telegram_id=telegram_id, db=db)
    result_dict = model_to_dict(token)
    return TokenData(**result_dict)
