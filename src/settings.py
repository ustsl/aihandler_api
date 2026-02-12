import os
from typing import Literal, TypeAlias, get_args

from dotenv import load_dotenv
from envparse import Env

env = Env()

load_dotenv()

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")

DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")


DB_NAME_TEST = os.getenv("DATABASE_NAME_TEST")
DB_USER_TEST = os.getenv("DATABASE_USER_TEST")
DB_PASSWORD_TEST = os.getenv("DATABASE_PASSWORD_TEST")
DB_HOST_TEST = os.getenv("DATABASE_HOST_TEST")
DB_PORT_TEST = os.getenv("DATABASE_PORT_TEST")


TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/aihandler_db_test",
)


MAIN_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/aihandler_db",
)


GPTModelName: TypeAlias = Literal[
    "gpt-3.5-turbo",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4o-mini-audio-preview",
    "gpt-4o-audio-preview",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "dall-e-3",
]

ALLOWED_MODELS_WITH_PRICE = {
    "gpt-3.5-turbo": 0.045,
    "gpt-4-turbo": 0.075,
    "gpt-4o": 0.12,
    "gpt-4o-mini": 0.03,
    "gpt-4o-mini-audio-preview": 0.06,
    "gpt-4o-audio-preview": 0.105,
    "gpt-5": 3.0,
    "gpt-5-mini": 0.75,
    "gpt-5-nano": 0.075,
    "dall-e-3": 0.225,
}

ALLOWED_MODELS = list(get_args(GPTModelName))
