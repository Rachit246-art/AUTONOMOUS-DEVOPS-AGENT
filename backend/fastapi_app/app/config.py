# Instead of reading .env in every file, we centralize configuration in one place.
# Whenever we need database settings, we can import settings.

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]

load_dotenv(ROOT_DIR / ".env")


class Settings:

    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_DRIVER = os.getenv("DB_DRIVER")
    DB_TRUSTED_CONNECTION = os.getenv(
        "DB_TRUSTED_CONNECTION", "yes"
    )


settings = Settings()
