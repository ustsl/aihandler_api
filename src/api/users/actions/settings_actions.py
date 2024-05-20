from sqlalchemy.ext.asyncio import AsyncSession
from src.api.prompts.actions import _show_prompt
from src.api.users.actions.base_user_actions import _get_user
from src.api.utils import handle_dal_errors

from src.db.users.dals.settings import UserSettingsDal
from src.db.users.models import UserSettingsModel


@handle_dal_errors
async def _update_user_settings_prompt(
    telegram_id: str, prompt_id: str, db: AsyncSession
):
    prompt = await _show_prompt(telegram_id=telegram_id, prompt_id=prompt_id, db=db)
    if prompt:
        user = await _get_user(telegram_id=telegram_id, db=db)
        if user:
            obj_dal = UserSettingsDal(db, UserSettingsModel)
            result = await obj_dal.update(uuid=user.settings.uuid, prompt_id=prompt_id)
            return result
