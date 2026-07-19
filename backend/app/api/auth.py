from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.auth import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserPublic,
)
from app.services.auth_service import (
    get_current_user,
    login_user,
    register_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=201,
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
) -> UserPublic:
    return register_user(
        data=data,
        db=db,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return login_user(
        data=data,
        db=db,
    )


@router.get(
    "/me",
    response_model=UserPublic,
)
def read_current_user(
    current_user: UserPublic = Depends(get_current_user),
) -> UserPublic:
    return current_user