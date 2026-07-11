from app.models.scanner import (
    BreakoutSignal,
    StockSnapshot,
)

def get_demo_stocks() -> list[StockSnapshot]:
    return [
        StockSnapshot(
            symbol="Reliance",
            company_name="Reliance Industries",
            price=3025.00,
            resistance=3000.00,
            change_percent=1.75,
            volume_ratio=1.90,
            data_source="demo",
        ),
        StockSnapshot(
            symbol="TCS",
            company_name="Tata Consultancy Services",
            price=4210.00,
            resistance=4250.00,
            change_percent=0.40,
            volume_ratio=1.90,
            data_source="demo",
        ),
        StockSnapshot(
            symbol="INFY",
            company_name="Infosys",
            price=1840.00,
            resistance=1825.00,
            change_percent=1.45,
            volume_ratio=1.35,
            data_source="demo",
        ),
        StockSnapshot(
            symbol="HDFCBANK",
            company_name="HDFC Bank",
            price=1715.00,
            resistance=1700.00,
            change_percent=1.20,
            volume_ratio=1.65,
            data_source="demo",
        ), 
    ]

def scan_breakouts(
    minimum_volume_ratio: float = 1.5,
    minimum_change_percent: float = 1.0,
) -> list[BreakoutSignal]:
    signals: list[BreakoutSignal] = []

    for stock in get_demo_stocks():
        is_above_resistance = stock.price > stock.resistance
        has_volume_confirmation = (
            stock.volume_ratio >= minimum_volume_ratio
        )
        has_momentum = (
            stock.change_percent >= minimum_change_percent
        )

        if (
            is_above_resistance
            and has_volume_confirmation
            and has_momentum
        ):
            breakout_percent = (
                (stock.price - stock.resistance)
                / stock.resistance
                * 100
            )

            signals_data = {
                    "symbol": stock.symbol,
                    "company_name": stock.company_name,
                    "price": stock.price,
                    "resistance": stock.resistance,
                    "breakout_percent": round(breakout_percent, 2),
                    "change_percent": stock.change_percent,
                    "volume_ratio": stock.volume_ratio,
                    "signal": "breakout_candidate",
                    "data_source": stock.data_source,
                
            }

            signals.append(BreakoutSignal(**signals_data))

    return signals