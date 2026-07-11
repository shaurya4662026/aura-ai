import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    BREEZE_ENABLED = (
        os.getenv("BREEZE_ENABLED", "false").lower() == "true"
    )
    BREEZE_API_KEY = os.getenv("BREEZE_API_KEY")
    BREEZE_API_SECRET = os.getenv("BREEZE_API_SECRET")
    BREEZE_SESSION_TOKEN = os.getenv("BREEZE_SESSION_TOKEN")

settings = Settings()