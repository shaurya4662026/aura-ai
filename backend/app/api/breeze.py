from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.services.breeze_service import create_breeze_client

router = APIRouter(
    prefix="/breeze",
    tags=["Breeze"],
)

@router.get("/status")
def breeze_status() -> dict:
    if not settings.BREEZE_ENABLED:
        return{
            "connected": False,
            "enabled": False,
            "broker": "ICICI Direct Breeze",
            "message": (
                "Breeze integration is disabled until a static IP"
                "and API credentials are available."
            ),
        }
    
    try:
        create_breeze_client()

        return{
            "connected": True,
            "enabled": True,
            "broker": "ICICI Direct Breeze",
            "message": "Breeze authentication succeeded.",
        }
    
    except Exception as exc:
            raise HTTPException(
                 status_code=503,
                 detail=f"Breeze connection failed: {exc}",
            ) from exc
        