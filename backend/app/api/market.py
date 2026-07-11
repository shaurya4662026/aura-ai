from fastapi import APIRouter, HTTPException

from app.models.market import MarketIndex
from app.services.market_service import (
    get_market_index,
    get_market_overview,
)

router = APIRouter(
    prefix="/market",
    tags=["Market Data"],
)

@router.get("/overview", response_model=list[MarketIndex])
def market_overview() -> list[MarketIndex]:
    return get_market_overview()

@router.get("/{symbol}", response_model=MarketIndex)
def market_index(symbol: str) -> MarketIndex:
    index = get_market_index(symbol)

    if index is None:
        raise HTTPException(
            status_code=404,
            detail=f"Market index '{symbol}' was not found.",
        )
    
    return index