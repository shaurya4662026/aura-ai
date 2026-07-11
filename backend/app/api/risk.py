from fastapi import APIRouter, HTTPException

from app.models.risk import (
    PositionSizeRequest,
    PositionSizeResponse,
)
from app.services.risk_service import (
    calculate_position_size,
)

router = APIRouter(
    prefix="/risk",
    tags=["Risk Management"],
)

@router.post(
    "/position-size",
    response_model=PositionSizeResponse,
)
def postition_size(
    data: PositionSizeRequest,
) -> PositionSizeResponse:
    try:
        return calculate_position_size(data)
    
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc