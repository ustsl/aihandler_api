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

MAIN_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/aihandler_db",
)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/aihandler_db_test",
)

ALLOWED_MODELS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0125",
    "gpt-4-turbo",
    "gpt-4-turbo-2024-04-09",
]
