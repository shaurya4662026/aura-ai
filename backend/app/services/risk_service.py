from math import floor

from app.models.risk import (
    PositionSizeRequest,
    PositionSizeResponse,
)

def calculate_position_size(
        data: PositionSizeRequest,
) -> PositionSizeResponse:
    risk_per_share = abs(
        data.entry_price - data.stop_loss
    )

    maximum_allowed_risk = (
        data.total_capital
        * data.risk_percent
        / 100
    )

    quantity_by_risk = floor(
        maximum_allowed_risk / risk_per_share
    )

    quantity_by_capital = floor(
        data.max_position_capital
        / data.entry_price
    )

    quantity = min(
        quantity_by_risk,
        quantity_by_capital,
    )

    if quantity < 1:
        raise ValueError(
            "Capital or risk limit is too low for one share."
        )

    if quantity_by_risk < quantity_by_capital:
        limiting_factor = "risk_limit"
    elif quantity_by_capital < quantity_by_risk:
        limiting_factor = "capital_limit"
    else:
        limiting_factor = "both"

    return PositionSizeResponse(
        quantity=quantity,
        entry_price=round(data.entry_price, 2),
        stop_loss=round(data.stop_loss, 2),
        risk_per_share=round(risk_per_share, 2),
        maximum_allowed_risk=round(
            maximum_allowed_risk,
            2,
        ),
        actual_risk=round(
            quantity * risk_per_share,
            2,
        ),
        position_value=round(
            quantity * data.entry_price,
            2,
        ),
        capital_limit=round(
            data.max_position_capital,
            2,
        ),
        limiting_factor=limiting_factor,
    )