from pydantic import BaseModel, Field

class WatchlistCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
    )

class WatchlistStockAdd(BaseModel):
    symbol: str = Field(
        min_length=1,
        max_length=20,
    )

class WatchlistStock(BaseModel):
    symbol: str

class Watchlist(BaseModel):
    id: int
    name: str
    stocks: list[WatchlistStock]