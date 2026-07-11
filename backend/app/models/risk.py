from pydantic import BaseModel, Field, model_validator

class PositionSizeRequest(BaseModel):
    total_capital: float = Field(gt=0)
    risk_percent: float = Field(gt=0, le=5)
    entry_price: float = Field(gt=0)
    stop_loss: float = Field(gt=0)
    max_position_capital: float = Field(gt=0)

    @model_validator(mode="after")
    def validate_prices(self):
        if self.entry_price == self.stop_loss:
            raise ValueError(
                "Entry price and stop-loss cannot be the same."
            )
        
        return self
    
class PositionSizeResponse(BaseModel):
    quantity: int
    entry_price: float
    stop_loss: float
    risk_per_share: float
    maximum_allowed_risk: float
    actual_risk: float
    position_value: float
    capital_limit: float
    limiting_factor: str