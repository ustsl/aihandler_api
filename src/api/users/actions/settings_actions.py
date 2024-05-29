from sqlalchemy.ext.asyncio import AsyncSession
from src.api.users.actions.base_user_actions import _get_user
from src.api.users.schemas import SettingsGetData
from src.db.users.dals.settings import UserSettingsDal
from src.db.users.models import UserSettingsModel


async def _update_user_settings(
    telegram_id: str, updates: SettingsGetData, db: AsyncSession
):
    user = await _get_user(telegram_id=telegram_id, db=db)
    obj_dal = UserSettingsDal(db, UserSettingsModel)
    updates_dict = updates.dict()
    return await obj_dal.update(uuid=str(user.settings.uuid), **updates_dict)
