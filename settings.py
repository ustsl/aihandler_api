import os

from dotenv import load_dotenv
from envparse import Env

env = Env()

load_dotenv()

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")


DB_NAME_TEST = os.getenv("DATABASE_NAME")
DB_USER_TEST = os.getenv("DATABASE_USER")
DB_PASSWORD_TEST = os.getenv("DATABASE_PASSWORD")
DB_HOST_TEST = os.getenv("DATABASE_HOST")
DB_PORT_TEST = os.getenv("DATABASE_PORT")

MAIN_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)


TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}",
)
