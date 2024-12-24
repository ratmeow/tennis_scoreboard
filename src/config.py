from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL = "sqlite+aiosqlite:///data/db.sqlite3"


settings = Settings()
