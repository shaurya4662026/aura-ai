from fastapi import APIRouter

from app.models.watchlist import (
    Watchlist,
    WatchlistCreate,
    WatchlistStockAdd,
)
from app.services.watchlist_service import (
    add_stock,
    create_watchlist,
    get_watchlists,
)

router = APIRouter(
    prefix="/watchlists",
    tags=["Watchlists"],
)

@router.get(
    "/",
    response_model=list[Watchlist],
)
def list_watchlists():
    return get_watchlists()

@router.post(
    "/",
    response_model=Watchlist,
)
def new_watchlist(
    data: WatchlistCreate,
):
    return create_watchlist(data)

@router.post(
    "/{watchlist_id}/stocks",
    response_model=Watchlist,
)
def add_stock_to_watchlist(
    watchlist_id: int,
    data: WatchlistStockAdd,
):
    return add_stock(
        watchlist_id,
        data,
    )