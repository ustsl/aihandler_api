import httpx

from src.modules.gpt.modules.exception_wrapper import normalize_openai_exception
from src.settings import OPENAI_TOKEN


def _build_headers() -> dict:
    if not OPENAI_TOKEN:
        raise ValueError("OpenAI API key must be defined.")
    return {"Authorization": f"Bearer {OPENAI_TOKEN}"}


async def run_chat_with_tools(
    model: str,
    messages: list,
    tools: list | None = None,
) -> dict:
    payload = {
        "model": model,
        "messages": messages,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    try:
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=_build_headers(),
                json=payload,
            )
            response.raise_for_status()
            completion = response.json()
            usage = completion.get("usage") or {}
            message = (completion.get("choices") or [{}])[0].get("message") or {}
            return {
                "message": message,
                "tokens": int(usage.get("total_tokens") or 0),
            }
    except (
        httpx.HTTPStatusError,
        httpx.TimeoutException,
        httpx.RequestError,
    ) as exc:
        raise normalize_openai_exception(exc)
