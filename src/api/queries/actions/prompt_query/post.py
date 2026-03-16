from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.prompts.actions import _show_prompt
from src.api.queries.actions.analytics.post import _get_last_query, _save_query
from src.api.queries.actions.balance.put import _transfer_balance
from src.api.queries.modules.quality_metrics import build_query_quality_metrics
from src.api.queries.modules.story_crop import story_crop_function
from src.api.utils import handle_dal_errors
from src.db.tools.dals import PromptToolDAL, ToolCallLogDAL
from src.db.tools.models import PromptToolModel, ToolCallLogModel
from src.db.users.dals.transaction import MoneyTransactionUserDal
from src.db.users.models import UserAccountModel
from src.modules.gpt.handler import gpt_handler
from src.modules.tools.orchestrator import run_prompt_with_tools


def _build_query_payload(
    query: str, result: str, cost: float = 0.0, cached: bool = False
) -> dict:
    return {
        "result": result,
        "cost": round(float(cost), 6),
        "quality_metrics": build_query_quality_metrics(
            query=query, result=result, cached=cached
        ),
    }


async def _get_active_prompt_tools(prompt_id: str, db: AsyncSession) -> list:
    prompt_tool_dal = PromptToolDAL(db, PromptToolModel)
    links = await prompt_tool_dal.list_prompt_tools(prompt_id=prompt_id)
    tools = []
    for link in links:
        tool = link.tool
        if tool and not tool.is_deleted and tool.is_active:
            tools.append(tool)
    return tools


async def _persist_tool_call_logs(
    db: AsyncSession,
    prompt_id: str,
    logs: list[dict],
    query_id: str | None = None,
):
    if not logs:
        return
    log_dal = ToolCallLogDAL(db, ToolCallLogModel)
    for log in logs:
        await log_dal.create_safe_log(
            query_id=query_id,
            prompt_id=prompt_id,
            tool_id=log.get("tool_id"),
            tool_name=log.get("tool_name") or "unknown",
            status=log.get("status") or "error",
            duration_ms=log.get("duration_ms"),
            request_payload=log.get("request_payload"),
            response_payload=log.get("response_payload"),
            error_text=log.get("error_text"),
        )


@handle_dal_errors
async def _create_query(
    prompt_id: str,
    user_id: str,
    query: str,
    db: AsyncSession,
    story: Optional[list] = None,
    vision: Optional[bool] = False,
):
    prompt = await _show_prompt(prompt_id=prompt_id, user_id=user_id, db=db)
    prepared_story = story or []

    if prompt.context_story_window > 0:
        prepared_story = await story_crop_function(
            prepared_story, prompt.context_story_window
        )
    else:
        prepared_story = []

    if not prepared_story:
        last_query = await _get_last_query(prompt=prompt, query=query, db=db)
        if last_query and last_query.result:
            return _build_query_payload(
                query=query,
                result=last_query.result,
                cost=0.0,
                cached=True,
            )

    user_obj_dal = MoneyTransactionUserDal(db, UserAccountModel)
    check_balance = await user_obj_dal.check_balance(user_id)
    if not check_balance.get("result"):
        return {"error": "wallet it empty", "status": 403}

    params = {
        "prompt": prompt.prompt,
        "message": query,
        "story": prepared_story,
        "model": prompt.model,
        "tuning": prompt.tuning,
        "vision": vision,
    }

    prompt_tools = await _get_active_prompt_tools(prompt_id=prompt.uuid, db=db)
    if prompt_tools:
        model_response = await run_prompt_with_tools(params=params, tools=prompt_tools)
    else:
        model_response = await gpt_handler(params)

    if model_response.get("error"):
        if model_response.get("tool_call_logs"):
            await _persist_tool_call_logs(
                db=db,
                prompt_id=prompt.uuid,
                logs=model_response.get("tool_call_logs"),
                query_id=None,
            )
            await db.commit()
        return {"error": model_response.get("error"), "status": 500}

    result_text = model_response.get("result")
    if not result_text:
        return {"error": "Empty model response", "status": 500}

    cost = float(model_response.get("cost") or 0)

    if cost > 0:
        await _transfer_balance(
            query_user_id=user_id,
            prompt_user_id=prompt.user_id,
            cost=cost,
            session=db,
        )

    created_query = await _save_query(
        user_id=user_id,
        prompt_id=prompt_id,
        query=query,
        result=result_text,
        db=db,
    )
    if model_response.get("tool_call_logs"):
        await _persist_tool_call_logs(
            db=db,
            prompt_id=prompt.uuid,
            logs=model_response.get("tool_call_logs"),
            query_id=created_query.uuid,
        )
    await db.commit()

    return _build_query_payload(query=query, result=result_text, cost=cost, cached=False)
