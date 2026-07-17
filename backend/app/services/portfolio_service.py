from fastapi import HTTPException

from app.models.portfolio import (
    BuyRequest,
    Holding,
    PortfolioSummary,
    SellRequest,
    TransactionResult,
)


user_portfolios: dict[int, dict[str, Holding]] = {}


def get_user_portfolio(user_id: int) -> dict[str, Holding]:
    if user_id not in user_portfolios:
        user_portfolios[user_id] = {}

    return user_portfolios[user_id]


def buy_stock(
    user_id: int,
    data: BuyRequest,
) -> TransactionResult:
    portfolio = get_user_portfolio(user_id)
    symbol = data.symbol.upper().strip()

    if symbol in portfolio:
        holding = portfolio[symbol]

        total_cost = (
            holding.average_price * holding.quantity
            + data.price * data.quantity
        )

        total_quantity = holding.quantity + data.quantity

        holding.average_price = round(
            total_cost / total_quantity,
            2,
        )
        holding.quantity = total_quantity
        holding.current_price = data.price

    else:
        portfolio[symbol] = Holding(
            symbol=symbol,
            quantity=data.quantity,
            average_price=data.price,
            current_price=data.price,
            invested_value=0,
            current_value=0,
            profit_loss=0,
            profit_loss_percent=0,
        )

    update_portfolio(portfolio)

    return TransactionResult(
        message="Stock purchased successfully.",
        symbol=symbol,
        quantity=data.quantity,
        price=data.price,
    )


def sell_stock(
    user_id: int,
    data: SellRequest,
) -> TransactionResult:
    portfolio = get_user_portfolio(user_id)
    symbol = data.symbol.upper().strip()

    if symbol not in portfolio:
        raise HTTPException(
            status_code=404,
            detail="Stock not found in portfolio.",
        )

    holding = portfolio[symbol]

    if data.quantity > holding.quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough shares to sell.",
        )

    holding.quantity -= data.quantity
    holding.current_price = data.price

    if holding.quantity == 0:
        del portfolio[symbol]
    else:
        update_portfolio(portfolio)

    return TransactionResult(
        message="Stock sold successfully.",
        symbol=symbol,
        quantity=data.quantity,
        price=data.price,
    )


def get_portfolio(user_id: int) -> PortfolioSummary:
    portfolio = get_user_portfolio(user_id)

    update_portfolio(portfolio)

    invested = sum(
        holding.invested_value
        for holding in portfolio.values()
    )

    current = sum(
        holding.current_value
        for holding in portfolio.values()
    )

    profit = current - invested

    profit_percent = (
        round((profit / invested) * 100, 2)
        if invested > 0
        else 0
    )

    return PortfolioSummary(
        total_invested=round(invested, 2),
        total_current_value=round(current, 2),
        total_profit_loss=round(profit, 2),
        total_profit_loss_percent=profit_percent,
        holdings=list(portfolio.values()),
    )


def update_portfolio(
    portfolio: dict[str, Holding],
) -> None:
    for holding in portfolio.values():
        holding.invested_value = round(
            holding.quantity * holding.average_price,
            2,
        )

        holding.current_value = round(
            holding.quantity * holding.current_price,
            2,
        )

        holding.profit_loss = round(
            holding.current_value - holding.invested_value,
            2,
        )

        holding.profit_loss_percent = (
            round(
                (
                    holding.profit_loss
                    / holding.invested_value
                )
                * 100,
                2,
            )
            if holding.invested_value > 0
            else 0
        )