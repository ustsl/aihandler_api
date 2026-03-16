import pytest
from sqlalchemy import select
from uuid import UUID

from src.db.tools.models import ToolCallLogModel
from tests.conftest import async_session_maker, client


def test_bind_and_get_prompt_tools(
    user_data_with_money, create_prompt_for_user, create_tool_for_user
):
    prompt = create_prompt_for_user(
        user_data_with_money,
        title="Prompt with tools",
        prompt="Use tool when needed",
        context_story_window=0,
    )
    tool = create_tool_for_user(user_data_with_money, name="bind_tool_case")

    bind_response = client.put(
        f'v1/prompts/{user_data_with_money["telegram_id"]}/{prompt["id"]}/tools',
        json={"tool_ids": [tool["uuid"]], "replace": True},
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert bind_response.status_code == 200
    assert bind_response.json()["total"] == 1

    get_response = client.get(
        f'v1/prompts/{user_data_with_money["telegram_id"]}/{prompt["id"]}/tools',
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert get_response.status_code == 200
    assert get_response.json()["result"][0]["uuid"] == tool["uuid"]


def test_bind_foreign_tool_to_prompt_fails(
    user_data_with_money,
    user_data_with_prompt,
    create_prompt_for_user,
    create_tool_for_user,
):
    prompt = create_prompt_for_user(
        user_data_with_prompt,
        title="Owner prompt",
        context_story_window=0,
    )
    foreign_tool = create_tool_for_user(
        user_data_with_money,
        name="foreign_bind_tool_case",
    )

    response = client.put(
        f'v1/prompts/{user_data_with_prompt["telegram_id"]}/{prompt["id"]}/tools',
        json={"tool_ids": [foreign_tool["uuid"]], "replace": True},
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_query_with_tools_executes_orchestrator_and_writes_logs(
    user_data_with_money,
    create_prompt_for_user,
    create_tool_for_user,
    monkeypatch,
):
    prompt = create_prompt_for_user(
        user_data_with_money,
        title="Prompt tool execution",
        prompt="You can call tool",
        context_story_window=0,
    )
    tool = create_tool_for_user(user_data_with_money, name="sum_tool_execution")
    prompt_uuid = UUID(prompt["id"])

    bind_response = client.put(
        f'v1/prompts/{user_data_with_money["telegram_id"]}/{prompt["id"]}/tools',
        json={"tool_ids": [tool["uuid"]], "replace": True},
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert bind_response.status_code == 200

    calls = {"count": 0}

    async def fake_run_chat_with_tools(model, messages, tools):
        if calls["count"] == 0:
            calls["count"] += 1
            return {
                "message": {
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_1",
                            "type": "function",
                            "function": {
                                "name": "sum_tool_execution",
                                "arguments": '{"value": 2}',
                            },
                        }
                    ],
                },
                "tokens": 80,
            }
        return {
            "message": {"content": "tool-based answer", "tool_calls": []},
            "tokens": 40,
        }

    async def fake_execute_tool(tool, args):
        return {"status": "success", "result": {"value": args["value"] * 2}}

    monkeypatch.setattr(
        "src.modules.tools.orchestrator.run_chat_with_tools",
        fake_run_chat_with_tools,
    )
    monkeypatch.setattr(
        "src.modules.tools.orchestrator.execute_tool",
        fake_execute_tool,
    )

    query_response = client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}',
        json={"prompt_id": prompt["id"], "query": "calculate"},
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert query_response.status_code == 200
    assert query_response.json()["result"] == "tool-based answer"
    assert query_response.json()["cost"] > 0

    async with async_session_maker() as session:
        db_logs = await session.execute(
            select(ToolCallLogModel).where(
                ToolCallLogModel.prompt_id == prompt_uuid,
                ToolCallLogModel.tool_name == "sum_tool_execution",
            )
        )
        logs = db_logs.scalars().all()
        assert len(logs) >= 1
