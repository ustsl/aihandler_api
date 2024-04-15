from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter

from api.prompts.handlers import prompt_router
from api.queries.handlers import query_router

#########################
# BLOCK WITH API ROUTES #
#########################

# create instance of the app
app = FastAPI(title="ai_handler")

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(prompt_router, prefix="/v1/prompts", tags=["prompts"])
main_api_router.include_router(query_router, prefix="/v1/queries", tags=["queries"])
app.include_router(main_api_router)


# if __name__ == "__main__":
#     # run app on the host and port
#     uvicorn.run(app, host="0.0.0.0", port=8000)
