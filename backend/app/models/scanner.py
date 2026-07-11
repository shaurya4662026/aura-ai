from pydantic import BaseModel

class StockSnapshot(BaseModel):
    symbol: str
    company_name: str
    price: float
    resistance: float
    change_percent: float
    volume_ratio: float
    data_source: str

class BreakoutSignal(BaseModel):
    symbol: str
    company_name: str
    price: float
    resistance: float
    breakout_percent: float
    change_percent: float
    volume_ratio: float
    signal: str
    data_source: str
