from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from pwdlib import PasswordHash

from app.models.auth import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserPublic,
)


SECRET_KEY = "change-this-secret-key-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_hash = PasswordHash.recommended()
bearer_scheme = HTTPBearer()

users: dict[str, dict] = {}
next_user_id = 1


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    user_id: int,
    email: str,
) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def register_user(data: UserCreate) -> UserPublic:
    global next_user_id

    normalized_email = data.email.lower().strip()

    if normalized_email in users:
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists.",
        )

    user = {
        "id": next_user_id,
        "name": data.name.strip(),
        "email": normalized_email,
        "hashed_password": hash_password(data.password),
    }

    users[normalized_email] = user
    next_user_id += 1

    return UserPublic(
        id=user["id"],
        name=user["name"],
        email=user["email"],
    )


def login_user(data: UserLogin) -> TokenResponse:
    normalized_email = data.email.lower().strip()
    user = users.get(normalized_email)

    if user is None or not verify_password(
        data.password,
        user["hashed_password"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    token = create_access_token(
        user_id=user["id"],
        email=user["email"],
    )

    return TokenResponse(
        access_token=token,
        user=UserPublic(
            id=user["id"],
            name=user["name"],
            email=user["email"],
        ),
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
) -> UserPublic:
    token = credentials.credentials

    authentication_error = HTTPException(
        status_code=401,
        detail="Invalid or expired authentication token.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id_value = payload.get("sub")
        email = payload.get("email")

        if user_id_value is None or email is None:
            raise authentication_error

        user_id = int(user_id_value)

    except (
        jwt.InvalidTokenError,
        TypeError,
        ValueError,
    ):
        raise authentication_error

    user = users.get(email)

    if user is None or user["id"] != user_id:
        raise authentication_error

    return UserPublic(
        id=user["id"],
        name=user["name"],
        email=user["email"],
    )