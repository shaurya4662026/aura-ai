from pydantic import BaseModel, Field


class BuyRequest(BaseModel):
    symbol: str = Field(
        min_length=1,
        max_length=20,
    )
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class SellRequest(BaseModel):
    symbol: str = Field(
        min_length=1,
        max_length=20,
    )
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class Holding(BaseModel):
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    invested_value: float
    current_value: float
    profit_loss: float
    profit_loss_percent: float


class PortfolioSummary(BaseModel):
    total_invested: float
    total_current_value: float
    total_profit_loss: float
    total_profit_loss_percent: float
    holdings: list[Holding]


class TransactionResult(BaseModel):
    message: str
    symbol: str
    quantity: int
    price: float