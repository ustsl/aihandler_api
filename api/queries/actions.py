from uuid import UUID
from typing import List
from fastapi import HTTPException
from api.prompts.models import GPTPromptCreate, GPTPromptShortShow, GPTPromptShow
from db.prompts.dals import PromptDAL
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils import handle_dal_errors

from modules.gpt_core import CreateGPTResponse
from settings import OPENAI_TOKEN


@handle_dal_errors
async def _create_query(id: str, query: str, db: AsyncSession):
    prompt_dal = PromptDAL(db)
    prompt = await prompt_dal.get(id)

    gpt = CreateGPTResponse(
        prompt=prompt.prompt,
        message=query,
        model="gpt-3.5-turbo",
    )
    await gpt.generate()
    res = gpt.get_result()
    return res
