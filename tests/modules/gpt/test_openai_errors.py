import httpx

from src.modules.gpt.handler import factory
from src.modules.gpt.modules.exception_wrapper import (
    OpenAIAPIError,
    normalize_openai_exception,
)


def _http_status_error(status_code: int, payload: dict) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
    response = httpx.Response(status_code, json=payload, request=request)
    return httpx.HTTPStatusError(
        "OpenAI failed",
        request=request,
        response=response,
    )


def test_normalize_openai_status_error_includes_api_detail():
    exc = _http_status_error(
        401,
        {
            "error": {
                "message": "Incorrect API key provided",
                "type": "invalid_request_error",
                "code": "invalid_api_key",
            }
        },
    )

    normalized = normalize_openai_exception(exc)

    assert normalized.status_code == 401
    assert "OpenAI API error 401" in str(normalized)
    assert "Incorrect API key provided" in str(normalized)
    assert "invalid_api_key" in str(normalized)


def test_normalize_openai_timeout():
    request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
    normalized = normalize_openai_exception(httpx.ReadTimeout("timeout", request=request))

    assert normalized.status_code == 504
    assert str(normalized) == "OpenAI API timeout"


async def test_factory_returns_openai_error_status():
    class FailingResponse:
        def __init__(self, params):
            pass

        async def generate(self):
            raise OpenAIAPIError("OpenAI API error 429: rate limit", status_code=429)

        def calc(self):
            pass

        def get_result(self):
            return {}

    result = await factory(FailingResponse, {})

    assert result == {"error": "OpenAI API error 429: rate limit", "status": 429}
