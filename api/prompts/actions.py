from uuid import UUID
from typing import List
from fastapi import HTTPException
from api.prompts.models import (
    GPTPromptCreate,
    GPTPromptShortShow,
    GPTPromptShow,
    GPTCreateShow,
)
from db.prompts.dals import PromptDAL
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils import handle_dal_errors
from db.prompts.models import PromptModel


async def _create_new_prompt(body: GPTPromptCreate, db) -> GPTCreateShow:
    async with db as session:
        async with session.begin():
            obj_dal = PromptDAL(session, PromptModel)
            result = await obj_dal.create(**body.model_dump())
            if isinstance(result, dict) and result.get("error"):
                raise HTTPException(status_code=500, detail=result["error"])
            return GPTCreateShow(id=result.uuid, time_create=result.time_create)


@handle_dal_errors
async def _show_prompts(db: AsyncSession) -> List[GPTPromptShortShow]:
    obj_dal = PromptDAL(db, PromptModel)
    results = await obj_dal.list()
    return results


@handle_dal_errors
async def _show_prompt(
    prompt_id: str, telegram_id: str, db: AsyncSession
) -> GPTPromptShow:
    obj_dal = PromptDAL(db, PromptModel)
    prompt = await obj_dal.get(prompt_id)

    if isinstance(prompt, dict):
        return prompt

    if prompt.is_open == True or (telegram_id == prompt.account.user.telegram_id):
        return GPTPromptShow(
            id=prompt.uuid,
            title=prompt.title,
            description=prompt.description,
            model=prompt.model,
            account_id=str(prompt.account_id),
            price_usage=float(prompt.price_usage),
            is_deleted=prompt.is_deleted,
            prompt=prompt.prompt,
            is_open=prompt.is_open,
            is_active=prompt.is_active,
            time_create=prompt.time_create.isoformat(),
            time_update=prompt.time_update.isoformat(),
            telegram_id=prompt.account.user.telegram_id,
        )


@handle_dal_errors
async def _update_prompt(id: UUID, updates: dict, db: AsyncSession) -> GPTPromptShow:
    obj_dal = PromptDAL(db, PromptModel)
    result = await obj_dal.update(id, **updates)
    return result


@handle_dal_errors
async def _delete_prompt(id: UUID, db: AsyncSession) -> dict:
    obj_dal = PromptDAL(db, PromptModel)
    result = await obj_dal.delete(id)
    return result
