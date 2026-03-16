import json
import time

from src.modules.gpt.modules.calc import GptTokenCalculator
from src.modules.gpt.tool_calls import run_chat_with_tools
from src.modules.tools.executor import execute_tool
from src.modules.tools.validator import validate_tool_arguments


def _normalize_content(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
        return "\n".join(part for part in text_parts if part)
    return ""


def _openai_tools_payload(tools: list) -> list:
    result = []
    for tool in tools:
        result.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema or {"type": "object", "properties": {}},
                },
            }
        )
    return result


async def run_prompt_with_tools(params: dict, tools: list, max_steps: int = 5) -> dict:
    if not tools:
        return {"error": "No tools available"}

    messages = [{"role": "system", "content": params.get("prompt", "")}]
    story = params.get("story") or []
    if story:
        messages.extend(story)
    messages.append({"role": "user", "content": params.get("message", "")})

    tools_map = {tool.name: tool for tool in tools}
    openai_tools = _openai_tools_payload(tools)
    total_tokens = 0
    logs = []

    for _ in range(max_steps):
        model_response = await run_chat_with_tools(
            model=params.get("model"),
            messages=messages,
            tools=openai_tools,
        )
        assistant_message = model_response.get("message") or {}
        total_tokens += int(model_response.get("tokens") or 0)

        tool_calls = assistant_message.get("tool_calls") or []
        if not tool_calls:
            content = _normalize_content(assistant_message.get("content"))
            if not content:
                return {"error": "Empty model response", "tool_call_logs": logs}
            calculator = GptTokenCalculator(
                model=params.get("model"),
                value=total_tokens,
            )
            return {
                "result": content,
                "cost": calculator.calc(),
                "tool_call_logs": logs,
            }

        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.get("content"),
                "tool_calls": tool_calls,
            }
        )

        for tool_call in tool_calls:
            function_data = tool_call.get("function") or {}
            tool_name = function_data.get("name")
            tool = tools_map.get(tool_name)
            started_at = time.perf_counter()
            request_payload = {"arguments_raw": function_data.get("arguments")}

            if not tool:
                logs.append(
                    {
                        "tool_id": None,
                        "tool_name": tool_name or "unknown",
                        "status": "validation_error",
                        "duration_ms": int((time.perf_counter() - started_at) * 1000),
                        "request_payload": request_payload,
                        "response_payload": None,
                        "error_text": "Tool is not allowed for this prompt",
                    }
                )
                return {"error": f"Tool '{tool_name}' is not allowed", "tool_call_logs": logs}

            try:
                args = json.loads(function_data.get("arguments") or "{}")
            except json.JSONDecodeError:
                logs.append(
                    {
                        "tool_id": tool.uuid,
                        "tool_name": tool.name,
                        "status": "validation_error",
                        "duration_ms": int((time.perf_counter() - started_at) * 1000),
                        "request_payload": request_payload,
                        "response_payload": None,
                        "error_text": "Invalid tool arguments JSON",
                    }
                )
                return {"error": "Invalid tool arguments JSON", "tool_call_logs": logs}

            validation_error = validate_tool_arguments(args=args, schema=tool.input_schema)
            if validation_error:
                logs.append(
                    {
                        "tool_id": tool.uuid,
                        "tool_name": tool.name,
                        "status": "validation_error",
                        "duration_ms": int((time.perf_counter() - started_at) * 1000),
                        "request_payload": args,
                        "response_payload": None,
                        "error_text": validation_error,
                    }
                )
                return {"error": validation_error, "tool_call_logs": logs}

            execution_result = await execute_tool(tool=tool, args=args)
            duration_ms = int((time.perf_counter() - started_at) * 1000)
            execution_status = execution_result.get("status", "error")
            error_text = execution_result.get("error")
            response_payload = execution_result.get("result")

            logs.append(
                {
                    "tool_id": tool.uuid,
                    "tool_name": tool.name,
                    "status": execution_status if not error_text else "error",
                    "duration_ms": duration_ms,
                    "request_payload": args,
                    "response_payload": response_payload,
                    "error_text": error_text,
                }
            )

            if error_text:
                return {"error": error_text, "tool_call_logs": logs}

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.get("id"),
                    "name": tool.name,
                    "content": json.dumps(response_payload, ensure_ascii=False),
                }
            )

    return {"error": "Tool call limit exceeded", "tool_call_logs": logs}
