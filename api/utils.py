from fastapi import HTTPException
from functools import wraps

from fastapi import Request, HTTPException, status, Depends
from settings import SERVICE_TOKEN


def handle_dal_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if isinstance(result, dict) and "error" in result:
            status = result.get("status", 500)
            raise HTTPException(status_code=status, detail=result["error"])
        return result

    return wrapper


async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != SERVICE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )
