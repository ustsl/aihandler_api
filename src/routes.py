from fastapi.routing import APIRouter

from src.api.prompts.handlers import prompt_router
from src.api.queries.handlers import query_router
from src.api.users.handlers import user_router

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(prompt_router, prefix="/v1/prompts", tags=["prompts"])
main_api_router.include_router(query_router, prefix="/v1/queries", tags=["queries"])
main_api_router.include_router(user_router, prefix="/v1/users", tags=["users"])
