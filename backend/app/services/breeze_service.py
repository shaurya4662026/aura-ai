from breeze_connect import BreezeConnect
from app.core.config import settings

def create_breeze_client():
    breeze = BreezeConnect(api_key=settings.BREEZE_API_KEY)

    breeze.generate_session(
        api_secret=settings.BREEZE_API_SECRET,
        session_token=settings.BREEZE_SESSION_TOKEN,
    )

    return breeze