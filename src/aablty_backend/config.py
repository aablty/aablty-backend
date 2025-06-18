import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: int = int(os.getenv("TELEGRAM_CHAT_ID"))

    # Admin Auth
    ADMIN_TOKEN: str = os.getenv("ADMIN_TOKEN")

    # File upload settings
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE")) # in bytes
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR")

    # CORS settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS").split(",")

    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "aablty Backend"
    VERSION: str = "1.0.0"


settings = Settings()
