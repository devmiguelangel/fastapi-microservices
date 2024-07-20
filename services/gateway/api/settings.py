from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str


settings = Settings()
