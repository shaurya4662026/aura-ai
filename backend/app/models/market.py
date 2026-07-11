from pydantic import BaseModel

class MarketIndex(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    open: float
    high: float
    low: float
    previous_close: float
    data_source: str