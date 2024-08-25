import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

# Instantiate settings based on the current environment
settings = Settings()

# Overwrite with production settings if in production
if os.getenv("ENV") == "production":
    settings.Config.env_file = ".env.prod"
    settings = Settings()
