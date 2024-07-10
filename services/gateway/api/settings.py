from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH_URL: str


settings = Settings()
