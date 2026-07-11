from fastapi import APIRouter, Query

from app.models.scanner import BreakoutSignal
from app.services.scanner_service import scan_breakouts

router = APIRouter(
    prefix="/scanner",
    tags=["Scanner"],
)

@router.get(
    "/breakouts", 
    response_model=list[BreakoutSignal],
)
def breakout_scanner(
    minimum_volume_ratio: float = Query(
        default=1.5,
        ge=1,
        le=10,
    ),
    minimum_change_percent: float = Query(
        default=1.5,
        ge=1,
        le=10,
    ),
) -> list[BreakoutSignal]:
    return scan_breakouts(
        minimum_volume_ratio=minimum_volume_ratio,
        minimum_change_percent=minimum_change_percent,
    )