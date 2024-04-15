from uuid import UUID
from typing import List
from fastapi import HTTPException
from api.prompts.models import GPTPromptCreate, GPTPromptShortShow, GPTPromptShow
from db.prompts.dals import PromptDAL
from sqlalchemy.ext.asyncio import AsyncSession


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
            )


async def _show_prompts(db: AsyncSession) -> List[GPTPromptShow]:
    obj_dal = PromptDAL(db)
    results = await obj_dal.list()
    if isinstance(results, dict) and "error" in results:
        raise HTTPException(status_code=500, detail=results["error"])
    return results


async def _show_prompt(id: str, db: AsyncSession) -> GPTPromptShow:
    obj_dal = PromptDAL(db)
    result = await obj_dal.get(id)
    if isinstance(result, dict) and "error" in result:
        status = 500
        if result.get("status"):
            status = result.get("status")
        raise HTTPException(status_code=status, detail=result["error"])
    return result


async def _update_prompt(id: UUID, updates: dict, db: AsyncSession) -> GPTPromptShow:
    obj_dal = PromptDAL(db)
    result = await obj_dal.update(id, **updates)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


async def _delete_prompt(id: UUID, db: AsyncSession) -> dict:
    obj_dal = PromptDAL(db)
    result = await obj_dal.delete(id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
