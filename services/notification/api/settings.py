from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    VIDEO_QUEUE: str
    AUDIO_QUEUE: str
    MAILGUN_API_KEY: str

settings = Settings()
