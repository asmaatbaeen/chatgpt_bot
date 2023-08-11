import os

from dotenv import find_dotenv
from loguru import logger
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # values retrieved from .env
    SLACK_BOT_TOKEN: str = Field(
        description="",
        default=None,
    )

    SLACK_APP_TOKEN: str = Field(
        description="",
        default=None,
    )

    OPENAI_API_KEY: str = Field(
        description="",
        default=None,
    )

    class Config:
        """take environment variables from .env if present,
        .env used for local development"""

        dotenv_filename = ".env"
        environment = os.environ.get("ENVIRONMENT") or "local"
        logger.info(f"Running in environment: {environment}")
        if environment == "test":
            dotenv_filename = "test.env"
        if environment == "prod":
            dotenv_filename = "prod.env"

        logger.info(f"Getting environment config from {dotenv_filename}")
        env_file = find_dotenv(dotenv_filename)


settings = Settings()
