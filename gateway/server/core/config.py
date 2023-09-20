from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = Field(default="sqlite:///sql_app.db", env="GATEWAY_DB_URL")


settings = Settings()
