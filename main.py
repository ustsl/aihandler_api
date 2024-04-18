from fastapi import Depends, FastAPI
import uvicorn
from fastapi.routing import APIRouter

from api.prompts.handlers import prompt_router
from api.queries.handlers import query_router
from api.users.handlers import user_router

from api.utils import verify_token

from starlette.middleware.cors import CORSMiddleware

#########################
# BLOCK WITH API ROUTES #
#########################

# create instance of the app
app = FastAPI(title="ai_handler")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mc-angio.ru"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# create the instance for the routes
main_api_router = APIRouter(dependencies=[Depends(verify_token)])

# set routes to the app instance
main_api_router.include_router(prompt_router, prefix="/v1/prompts", tags=["prompts"])
main_api_router.include_router(query_router, prefix="/v1/queries", tags=["queries"])
main_api_router.include_router(user_router, prefix="/v1/users", tags=["users"])
app.include_router(main_api_router)
