import inspect
from functools import wraps

import httpx


class OpenAIAPIError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def _extract_openai_error(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        payload = None

    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict):
            message = error.get("message")
            error_type = error.get("type")
            code = error.get("code")
            details = [part for part in (message, error_type, code) if part]
            if details:
                return " | ".join(str(part) for part in details)
        if payload.get("message"):
            return str(payload["message"])

    text = response.text.strip()
    if text:
        return text[:500]
    return response.reason_phrase or "OpenAI request failed"


def normalize_openai_exception(exc: Exception) -> OpenAIAPIError:
    if isinstance(exc, OpenAIAPIError):
        return exc
    if isinstance(exc, httpx.HTTPStatusError):
        status_code = exc.response.status_code
        detail = _extract_openai_error(exc.response)
        return OpenAIAPIError(
            f"OpenAI API error {status_code}: {detail}",
            status_code=status_code,
        )
    if isinstance(exc, httpx.TimeoutException):
        return OpenAIAPIError("OpenAI API timeout", status_code=504)
    if isinstance(exc, httpx.ConnectError):
        return OpenAIAPIError("OpenAI API connection error", status_code=503)
    if isinstance(exc, httpx.RequestError):
        return OpenAIAPIError(f"OpenAI API request error: {exc}", status_code=503)
    return OpenAIAPIError(f"OpenAI API unexpected error: {exc}", status_code=500)


def handle_exceptions(func):
    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except (
                httpx.HTTPStatusError,
                httpx.TimeoutException,
                httpx.RequestError,
                OpenAIAPIError,
            ) as e:
                raise normalize_openai_exception(e)
            except Exception as e:
                raise OpenAIAPIError(f"OpenAI API unexpected error: {e}", status_code=500)

        return async_wrapper

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            httpx.HTTPStatusError,
            httpx.TimeoutException,
            httpx.RequestError,
            OpenAIAPIError,
        ) as e:
            raise normalize_openai_exception(e)
        except Exception as e:
            raise OpenAIAPIError(f"OpenAI API unexpected error: {e}", status_code=500)

    return sync_wrapper
