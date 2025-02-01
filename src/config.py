from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "sqlite:///src/data/db.sqlite3"


settings = Settings()
