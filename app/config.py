from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    database_hostname: str = os.getenv("DATABASE_HOSTNAME")
    database_port: str = (os.getenv("DATABASE_PORT", 5432))
    database_password: str = os.getenv("DATABASE_PASSWORD")
    database_username: str = os.getenv("DATABASE_USERNAME")
    database_name: str = os.getenv("DATABASE_NAME")

    class Config:
        env_file = ".env"


settings = Settings()