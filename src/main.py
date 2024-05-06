from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routes import main_api_router

#########################
# BLOCK WITH API ROUTES #
#########################

# create instance of the app
app = FastAPI(title="ai_handler")

origins = [
    "http://78.180.37.41",
    "http://78.180.37.41:3000",
    "http://host.docker.internal:3000",
    "http://mc-angio.ru",
    "https://mc-angio.ru",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_api_router)
