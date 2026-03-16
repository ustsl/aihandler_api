from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users.actions.account_user_actions import _get_user_account
from src.api.utils import handle_dal_errors
from src.db.tools.dals import ToolDAL
from src.db.tools.models import ToolModel


def _as_tool_dict(tool: ToolModel) -> dict:
    return {
        "uuid": tool.uuid,
        "name": tool.name,
        "description": tool.description,
        "transport": tool.transport,
        "method": tool.method,
        "url": tool.url,
        "input_schema": tool.input_schema or {},
        "headers_template": tool.headers_template,
        "query_template": tool.query_template,
        "body_template": tool.body_template,
        "auth_type": tool.auth_type,
        "auth_secret_ref": tool.auth_secret_ref,
        "timeout_sec": tool.timeout_sec,
        "max_response_bytes": tool.max_response_bytes,
        "is_active": tool.is_active,
        "is_deleted": tool.is_deleted,
        "account_id": tool.account_id,
        "time_create": tool.time_create,
        "time_update": tool.time_update,
    }


async def _ensure_owner_or_raise(
    tool_id: UUID, account_id: UUID, db: AsyncSession
) -> ToolModel:
    tool_dal = ToolDAL(db, ToolModel)
    owner_tool = await tool_dal.get_owner_tool(tool_id=tool_id, account_id=account_id)
    if owner_tool:
        return owner_tool

    visible_tool = await tool_dal.get_available(tool_id=tool_id, account_id=account_id)
    if visible_tool:
        raise HTTPException(status_code=403, detail="Permission denied")
    raise HTTPException(status_code=404, detail="Tool not found")


@handle_dal_errors
async def _create_tool(body, telegram_id: str, db: AsyncSession) -> dict:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    tool_dal = ToolDAL(db, ToolModel)

    data = body.model_dump()
    data["account_id"] = account.uuid
    if data.get("transport") == "http_json" and not data.get("url"):
        raise HTTPException(status_code=422, detail="url is required for http_json")
    if data.get("transport") == "mcp":
        data["url"] = None

    tool = await tool_dal.create(**data)
    await db.commit()
    return _as_tool_dict(tool)


@handle_dal_errors
async def _get_tools(telegram_id: str, db: AsyncSession, offset: int = 0) -> dict:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    tool_dal = ToolDAL(db, ToolModel)
    tools_data = await tool_dal.list_available(account_id=account.uuid, offset=offset)
    return {
        "result": [_as_tool_dict(tool) for tool in tools_data.get("result", [])],
        "total": tools_data.get("total", 0),
    }


@handle_dal_errors
async def _get_tool(tool_id: UUID, telegram_id: str, db: AsyncSession) -> dict:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    tool_dal = ToolDAL(db, ToolModel)
    tool = await tool_dal.get_available(tool_id=tool_id, account_id=account.uuid)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return _as_tool_dict(tool)


@handle_dal_errors
async def _update_tool(tool_id: UUID, telegram_id: str, body, db: AsyncSession) -> dict:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    tool = await _ensure_owner_or_raise(tool_id=tool_id, account_id=account.uuid, db=db)

    updates = body.model_dump(exclude_none=True)
    if "transport" in updates and updates["transport"] == "mcp":
        updates["url"] = None
    if updates.get("transport", tool.transport) == "http_json" and not updates.get(
        "url", tool.url
    ):
        raise HTTPException(status_code=422, detail="url is required for http_json")

    for key, value in updates.items():
        setattr(tool, key, value)
    await db.commit()
    await db.refresh(tool)
    return _as_tool_dict(tool)


@handle_dal_errors
async def _delete_tool(tool_id: UUID, telegram_id: str, db: AsyncSession) -> dict:
    account = await _get_user_account(telegram_id=telegram_id, db=db)
    tool = await _ensure_owner_or_raise(tool_id=tool_id, account_id=account.uuid, db=db)

    tool.is_deleted = True
    await db.commit()
    return {"success": "Tool deleted successfully"}
