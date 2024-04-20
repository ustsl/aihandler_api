from api.prompts.actions import _show_prompt
from sqlalchemy.ext.asyncio import AsyncSession
from api.users.actions import _get_user
from api.utils import handle_dal_errors
from modules.gpt_core import CreateGPTResponse


@handle_dal_errors
async def _create_query(prompt_id: str, telegram_id: str, query: str, db: AsyncSession):
    user = await _get_user(telegram_id=telegram_id, db=db)
    print(float(user.accounts.balance))
    prompt = await _show_prompt(prompt_id, telegram_id, db)
    if prompt:
        gpt = CreateGPTResponse(
            prompt=prompt.prompt,
            message=query,
            model="gpt-3.5-turbo",
        )
        await gpt.generate()
        res = gpt.get_result()
        return res
