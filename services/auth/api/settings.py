from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    jwt_secret: str
    jwt_expires_in: int
    jwt_algorithm: str

settings = Settings()
