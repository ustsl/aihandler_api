from fastapi import HTTPException
from functools import wraps


def handle_dal_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if isinstance(result, dict) and "error" in result:
            status = result.get("status", 500)
            raise HTTPException(status_code=status, detail=result["error"])
        return result

    return wrapper
