from api.prompts.actions import _show_prompt
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils import handle_dal_errors
from modules.gpt_core import CreateGPTResponse


@handle_dal_errors
async def _create_query(id: str, query: str, db: AsyncSession):
    prompt = await _show_prompt(id, db)
    gpt = CreateGPTResponse(
        prompt=prompt.prompt,
        message=query,
        model="gpt-3.5-turbo",
    )
    await gpt.generate()
    res = gpt.get_result()
    return res
