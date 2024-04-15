from uuid import UUID
from typing import List
from fastapi import HTTPException
from api.prompts.models import GPTPromptCreate, GPTPromptShortShow, GPTPromptShow
from db.prompts.dals import PromptDAL
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils import handle_dal_errors


async def _create_new_prompt(body: GPTPromptCreate, db) -> GPTPromptShortShow:
    async with db as session:
        async with session.begin():
            obj_dal = PromptDAL(session)
            result = await obj_dal.create(**body.model_dump())
            if isinstance(result, dict) and result.get("error"):
                raise HTTPException(status_code=500, detail=result["error"])
            return GPTPromptShortShow(
                id=result.uuid,
                title=result.title,
                description=result.description,
                prompt=result.prompt,
                time_create=result.time_create,
                model=result.model,
            )


@handle_dal_errors
async def _show_prompts(db: AsyncSession) -> List[GPTPromptShow]:
    obj_dal = PromptDAL(db)
    results = await obj_dal.list()
    return results


@handle_dal_errors
async def _show_prompt(id: str, db: AsyncSession) -> GPTPromptShow:
    obj_dal = PromptDAL(db)
    result = await obj_dal.get(id)
    return result


@handle_dal_errors
async def _update_prompt(id: UUID, updates: dict, db: AsyncSession) -> GPTPromptShow:
    obj_dal = PromptDAL(db)
    result = await obj_dal.update(id, **updates)
    return result


@handle_dal_errors
async def _delete_prompt(id: UUID, db: AsyncSession) -> dict:
    obj_dal = PromptDAL(db)
    result = await obj_dal.delete(id)
    return result
