from dotenv import find_dotenv, load_dotenv
from os import getenv


DOTENV_PATH = find_dotenv()
load_dotenv(dotenv_path=DOTENV_PATH)

# PostgreSQL Creds #
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = getenv("POSTGRES_HOST")
POSTGRES_PORT = getenv("POSTGRES_PORT")
POSTGRES_DB = getenv("POSTGRES_DB")

# AUTH #
JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
ACCESS_TOKEN_EXP = getenv("ACCESS_TOKEN_EXP", 30)

# Hashing #
HASH_ALGORITHM = getenv("HASH_ALGORITHM")