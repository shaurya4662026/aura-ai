from fastapi import APIRouter, Depends

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
)
def register(data: UserCreate):
    return register_user(data)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(data: UserLogin):
    return login_user(data)


@router.get(
    "/me",
    response_model=UserPublic,
)
def current_user(
    user: UserPublic = Depends(get_current_user),
):
    return user