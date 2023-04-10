import os
from dotenv import load_dotenv
from enum import Enum
import secrets
from pydantic import BaseSettings


load_dotenv('./.env')


class Environment(Enum):
    LOCAL_DEV = 1
    STAGING = 2
    PRODUCTION = 3
    TESTING = 4


class Settings(BaseSettings):
    API_KEY: str = os.getenv('API_KEY')
    DB_USER: str = os.getenv('USER')
    DB_PASS: str = os.getenv('PASS')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_HOST: str = os.getenv('DB_HOST')
    POSTGRE_URI: str = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'



settings = Settings()