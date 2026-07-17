from fastapi import APIRouter, Depends

from app.models.auth import UserPublic
from app.models.portfolio import (
    BuyRequest,
    PortfolioSummary,
    SellRequest,
    TransactionResult,
)
from app.services.auth_service import get_current_user
from app.services.portfolio_service import (
    buy_stock,
    get_portfolio,
    sell_stock,
)


router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)


@router.post(
    "/buy",
    response_model=TransactionResult,
)
def buy(
    data: BuyRequest,
    current_user: UserPublic = Depends(get_current_user),
):
    return buy_stock(
        current_user.id,
        data,
    )


@router.post(
    "/sell",
    response_model=TransactionResult,
)
def sell(
    data: SellRequest,
    current_user: UserPublic = Depends(get_current_user),
):
    return sell_stock(
        current_user.id,
        data,
    )


@router.get(
    "/",
    response_model=PortfolioSummary,
)
def portfolio_summary(
    current_user: UserPublic = Depends(get_current_user),
):
    return get_portfolio(
        current_user.id,
    )