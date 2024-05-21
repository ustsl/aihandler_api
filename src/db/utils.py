from functools import wraps
from typing import Callable, Any, Awaitable
from sqlalchemy.exc import NoResultFound, SQLAlchemyError


def exception_dal(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            return {"error": "Resource not found", "status": 404}
        except SQLAlchemyError as e:
            return {"error": str(e), "status": 500}
        except Exception as e:
            return {"error": str(e), "status": 500}

    return wrapper
