from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME = "PocketSmart AI"

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
        ""
    ).strip()

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    ).strip()

    JWT_SECRET = os.getenv(
        "JWT_SECRET",
        "dev-only-change-me"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'data' / 'pocketsmart.db'}"
    )

    CORS_ORIGINS = [
        value.strip()
        for value in os.getenv(
            "CORS_ORIGINS",
            "http://127.0.0.1:8000,http://localhost:8000"
        ).split(",")
        if value.strip()
    ]

    COOKIE_SECURE = (
        os.getenv("COOKIE_SECURE", "false").lower() == "true"
    )

    TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

    MAX_IMAGE_BYTES = 5 * 1024 * 1024


settings = Settings()