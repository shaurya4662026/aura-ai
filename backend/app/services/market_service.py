from app.models.market import MarketIndex

def get_market_overview() -> list[MarketIndex]:
    return [
        MarketIndex(
            symbol="NIFTY50",
            name="Nifty50",
            price="25150.40",
            change="125.30",
            change_percent="0.50",
            open="25050.20",
            high="25210.80",
            low="25010.10",
            previous_close="25025.10",
            data_source="demo",
        ),
        MarketIndex(
            symbol="BANKNIFTY",
            name="Nifty Bank",
            price="56820.75",
            change="140.25",
            change_percent="-0.25",
            open="57010.00",
            high="57120.40",
            low="56710.30",
            previous_close="56961.00",
            data_source="demo",
        ),
        MarketIndex(
            symbol="SENSEX",
            name="BSE Sensex",
            price="82140.60",
            change="310.45",
            change_percent="0.38",
            open="81950.20",
            high="81950.80",
            low="81890.50",
            previous_close="81830.15",
            data_source="demo",
        ),

    ]

def get_market_index(symbol: str) -> MarketIndex | None:
    normalised_symbol = symbol.upper()

    for index in get_market_overview():
        if index.symbol == normalised_symbol:
            return index
        
    return None