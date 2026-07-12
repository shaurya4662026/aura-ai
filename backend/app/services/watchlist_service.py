from fastapi import HTTPException

from app.models.watchlist import (
    Watchlist,
    WatchlistCreate,
    WatchlistStock,
    WatchlistStockAdd,
)

watchlists: list[Watchlist] = []
next_watchlist_id = 1

def get_watchlists() -> list[Watchlist]:
    return watchlists

def create_watchlist(data: WatchlistCreate) -> Watchlist:
    global next_watchlist_id

    watchlist = Watchlist(
        id=next_watchlist_id,
        name=data.name,
        stocks=[],
    )
    watchlists.append(watchlist)
    next_watchlist_id += 1

    return watchlist

def add_stock(
        watchlist_id: int,
        data: WatchlistStockAdd,
) -> Watchlist:
    for watchlist in watchlists:
        if watchlist.id == watchlist_id:
            normalized_symbol = data.symbol.upper().strip()

            already_exists = any(
                stock.symbol == normalized_symbol
                for stock in watchlist.stocks
            )

            if already_exists:
                raise HTTPException(
                    status_code=400,
                    detail="Stock is already in this watchlist.",
                )
            watchlist.stocks.append(
                WatchlistStock(
                    symbol=normalized_symbol
                )
            )
            return watchlist
        
    raise HTTPException(
        status_code=404,
        detail="Watchlist not found",
    )