from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.prompts.schemas import (GPTPromptBase, GPTPromptCreate,
                                     GPTPromptList, GPTPromptShow)
from src.api.users.actions.account_user_actions import _get_user_account
from src.api.utils import handle_dal_errors
from src.db.prompts.dals import PromptDAL
from src.db.prompts.models import PromptModel


@handle_dal_errors
async def _create_new_prompt(
    body: GPTPromptBase, telegram_id: str, db
) -> GPTPromptCreate:
    async with db as session:
        async with session.begin():
            account = await _get_user_account(telegram_id=telegram_id, db=db)
            data_to_create = body.model_dump()
            data_to_create["account_id"] = account.uuid
            obj_dal = PromptDAL(session, PromptModel)
            result = await obj_dal.create(**data_to_create)
            if isinstance(result, dict) and result.get("error"):
                raise HTTPException(status_code=500, detail=result["error"])
            return GPTPromptCreate(id=result.uuid, time_create=result.time_create)


@handle_dal_errors
async def _show_prompts(
    db: AsyncSession,
    telegram_id: str = None,
    offset: int = 0,
    search_query: str = None,
    only_yours: bool = True,
) -> GPTPromptList:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    obj_dal = PromptDAL(db, PromptModel)
    results = await obj_dal.list(
        account_id=account.uuid,
        offset=offset,
        search_query=search_query,
        only_yours=only_yours,
    )

    return results


@handle_dal_errors
async def _show_prompt(
    prompt_id: str, telegram_id: str, db: AsyncSession
) -> GPTPromptShow:
    obj_dal = PromptDAL(db, PromptModel)
    prompt = await obj_dal.get(prompt_id)

    if prompt:
        if prompt.is_open == True or (telegram_id == prompt.account.user.telegram_id):
            return GPTPromptShow(
                uuid=prompt.uuid,
                title=prompt.title,
                description=prompt.description,
                model=prompt.model,
                account_id=str(prompt.account_id),
                is_deleted=prompt.is_deleted,
                prompt=prompt.prompt,
                is_open=prompt.is_open,
                is_active=prompt.is_active,
                context_story_window=prompt.context_story_window,
                time_create=prompt.time_create.isoformat(),
                time_update=prompt.time_update.isoformat(),
                telegram_id=prompt.account.user.telegram_id,
                tuning=prompt.tuning,
            )
    else:
        raise HTTPException(status_code=404, detail="Prompt not found")


@handle_dal_errors
async def _update_prompt(
    prompt_id: UUID, telegram_id: str, updates: dict, db: AsyncSession
) -> GPTPromptShow:
    obj_dal = PromptDAL(db, PromptModel)
    try:
        account = await _get_user_account(telegram_id=telegram_id, db=db)
        prompt = await obj_dal.get(prompt_id)
        if prompt:
            if account.uuid == prompt.account_id:
                result = await obj_dal.update(prompt_id, **updates)
                return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@handle_dal_errors
async def _delete_prompt(prompt_id: UUID, telegram_id, db: AsyncSession) -> dict:
    obj_dal = PromptDAL(db, PromptModel)
    try:
        account = await _get_user_account(telegram_id=telegram_id, db=db)
        prompt = await obj_dal.get(prompt_id)
        if prompt:
            if account.uuid == prompt.account_id:
                result = await obj_dal.delete(prompt_id)
                return result
        raise HTTPException(status_code=404, detail="Prompt not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
