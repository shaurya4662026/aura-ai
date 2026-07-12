from fastapi import APIRouter, Query

from app.models.scanner import (
    BreakoutSignal,
    MomentumSignal,
) 
from app.services.scanner_service import (
    scan_breakouts,
    scan_momentum,
)

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

@router.get(
    "/momentum",
    response_model=list[MomentumSignal],
)
def momentum_scanner(
    minimum_change_percent: float = Query(
        default=1.0,
        ge=0,
        le=20,
    ),
    minimum_volume_ratio: float = Query(
        default=1.2,
        ge=1,
        le=10,
    )
) -> list[MomentumSignal]:
    return scan_momentum(
        minimum_change_percent=minimum_change_percent,
        minimum_volume_ratio=minimum_volume_ratio,
    )