import os

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


ALLOWED_MODELS_WITH_PRICE = {
    "gpt-5": 2,
    "gpt-5-mini": 0.5,
    "gpt-5-nano": 0.05,
    "gpt-4o": 0.08,
    "dall-e-3": 0.15,
    "gpt-4o-mini": 0.02,
    "gpt-4o-mini-audio-preview": 0.04,
    "gpt-4o-audio-preview": 0.07,
}

ALLOWED_MODELS = list(ALLOWED_MODELS_WITH_PRICE.keys())
