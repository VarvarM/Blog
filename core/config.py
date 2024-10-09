from os import getenv
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')


class DbSettings(BaseSettings):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = False
    pool_size: int = 10


class ApiPrefix(BaseModel):
    prefix: str = '/api'


class Settings(BaseSettings):
    api: ApiPrefix = ApiPrefix()
    db: DbSettings = DbSettings()


settings = Settings()
# print(settings.db_url)
