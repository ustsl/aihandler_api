from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.prompts.schemas import (
    GPTPromptBase,
    GPTPromptCreate,
    GPTPromptList,
    GPTPromptShow,
    GPTPromptShowFull,
    PromptToolList,
    PromptToolsBindBody,
)
from src.api.users.actions.base_user_actions import _get_user
from src.api.users.actions.account_user_actions import _get_user_account
from src.api.utils import handle_dal_errors
from src.db.prompts.dals import PromptDAL
from src.db.prompts.models import PromptModel
from src.db.tools.dals import PromptToolDAL, ToolDAL
from src.db.tools.models import PromptToolModel, ToolModel


@handle_dal_errors
async def _create_new_prompt(
    body: GPTPromptBase, telegram_id: str, db
) -> GPTPromptCreate:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    data_to_create = body.model_dump()
    data_to_create["account_id"] = account.uuid
    obj_dal = PromptDAL(db, PromptModel)
    result = await obj_dal.create(**data_to_create)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])
    await db.commit()

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
async def _show_prompt(prompt_id: str, user_id: str, db: AsyncSession) -> GPTPromptShow:
    obj_dal = PromptDAL(db, PromptModel)
    prompt = await obj_dal.get(prompt_id)

    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    if prompt.is_open is True or (user_id == prompt.account.user_id):
        return GPTPromptShowFull(
            uuid=prompt.uuid,
            title=prompt.title,
            description=prompt.description,
            model=prompt.model,
            account_id=str(prompt.account_id),
            user_id=prompt.account.user_id,
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

    raise HTTPException(status_code=403, detail="Prompt is private")


@handle_dal_errors
async def _update_prompt(
    prompt_id: UUID, telegram_id: str, updates: dict, db: AsyncSession
) -> GPTPromptShow:
    obj_dal = PromptDAL(db, PromptModel)
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    prompt = await obj_dal.get(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if account.uuid != prompt.account_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return await obj_dal.update(prompt_id, **updates)


@handle_dal_errors
async def _delete_prompt(prompt_id: UUID, telegram_id, db: AsyncSession) -> dict:
    obj_dal = PromptDAL(db, PromptModel)
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    prompt = await obj_dal.get(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if account.uuid != prompt.account_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return await obj_dal.delete(prompt_id)


@handle_dal_errors
async def _set_prompt_tools(
    prompt_id: UUID,
    telegram_id: str,
    body: PromptToolsBindBody,
    db: AsyncSession,
) -> PromptToolList:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    prompt_dal = PromptDAL(db, PromptModel)
    prompt = await prompt_dal.get(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt.account_id != account.uuid:
        raise HTTPException(status_code=403, detail="Permission denied")

    unique_tool_ids = list(dict.fromkeys(body.tool_ids))
    tool_dal = ToolDAL(db, ToolModel)
    for tool_id in unique_tool_ids:
        tool = await tool_dal.get_available(tool_id=tool_id, account_id=account.uuid)
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool {tool_id} not found")

    prompt_tool_dal = PromptToolDAL(db, PromptToolModel)
    if body.replace:
        await prompt_tool_dal.replace_for_prompt(
            prompt_id=prompt_id,
            tool_ids=unique_tool_ids,
        )
    await db.commit()
    return await _get_prompt_tools(prompt_id=prompt_id, telegram_id=telegram_id, db=db)


@handle_dal_errors
async def _get_prompt_tools(
    prompt_id: UUID,
    telegram_id: str,
    db: AsyncSession,
) -> PromptToolList:
    user = await _get_user(telegram_id=telegram_id, db=db)
    await _show_prompt(prompt_id=prompt_id, user_id=user.uuid, db=db)

    prompt_tool_dal = PromptToolDAL(db, PromptToolModel)
    links = await prompt_tool_dal.list_prompt_tools(prompt_id=prompt_id)

    result = []
    for link in links:
        tool = link.tool
        if not tool or tool.is_deleted or not tool.is_active:
            continue
        result.append(
            {
                "uuid": tool.uuid,
                "name": tool.name,
                "description": tool.description,
                "transport": tool.transport,
                "method": tool.method,
                "url": tool.url,
                "is_active": tool.is_active,
            }
        )
    return {"result": result, "total": len(result)}
