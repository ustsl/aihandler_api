from fastapi.routing import APIRouter

from src.api.prompts.handlers import prompt_router
from src.api.queries.handlers import query_router
from src.api.users.handlers import user_router
from src.api.scenarios.handlers import scenario_router


# create the instance for the routes
router = APIRouter()

# set routes to the app instance
router.include_router(scenario_router, prefix="/v1/scenarios", tags=["scenarios"])
router.include_router(prompt_router, prefix="/v1/prompts", tags=["prompts"])
router.include_router(query_router, prefix="/v1/queries", tags=["queries"])
router.include_router(user_router, prefix="/v1/users", tags=["users"])
