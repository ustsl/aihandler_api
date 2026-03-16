from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.tools.actions import (
    _create_tool,
    _delete_tool,
    _get_tool,
    _get_tools,
    _update_tool,
)
from src.api.tools.schemas import (ToolCreateSchema, ToolListSchema,
                                   ToolResponseSchema, ToolUpdateSchema)
from src.api.utils import verify_user_data
from src.db.session import get_db

tools_router = APIRouter(dependencies=[Depends(verify_user_data)])


@tools_router.post("/{telegram_id}", response_model=ToolResponseSchema)
async def create_tool(
    telegram_id: str,
    body: ToolCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    return await _create_tool(body=body, telegram_id=telegram_id, db=db)


@tools_router.get("/{telegram_id}", response_model=ToolListSchema)
async def get_tools(
    telegram_id: str,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    return await _get_tools(telegram_id=telegram_id, db=db, offset=offset)


@tools_router.get("/{telegram_id}/{tool_id}", response_model=ToolResponseSchema)
async def get_tool(
    telegram_id: str,
    tool_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await _get_tool(tool_id=tool_id, telegram_id=telegram_id, db=db)


@tools_router.put("/{telegram_id}/{tool_id}", response_model=ToolResponseSchema)
async def update_tool(
    telegram_id: str,
    tool_id: UUID,
    body: ToolUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    return await _update_tool(tool_id=tool_id, telegram_id=telegram_id, body=body, db=db)


@tools_router.delete("/{telegram_id}/{tool_id}")
async def delete_tool(
    telegram_id: str,
    tool_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await _delete_tool(tool_id=tool_id, telegram_id=telegram_id, db=db)
