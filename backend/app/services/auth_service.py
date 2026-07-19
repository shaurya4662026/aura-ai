from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_id,
)
from app.database.database import get_db
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
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
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


def register_user(
    data: UserCreate,
    db: Session,
) -> UserPublic:
    normalized_email = data.email.lower().strip()

    existing_user = get_user_by_email(
        db=db,
        email=normalized_email,
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists.",
        )

    try:
        user = create_user(
            db=db,
            name=data.name,
            email=normalized_email,
            hashed_password=hash_password(data.password),
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists.",
        )

    return UserPublic(
        id=user.id,
        name=user.name,
        email=user.email,
    )


def login_user(
    data: UserLogin,
    db: Session,
) -> TokenResponse:
    normalized_email = data.email.lower().strip()

    user = get_user_by_email(
        db=db,
        email=normalized_email,
    )

    print("=" * 50)
    print("LOGIN ATTEMPT")
    print("EMAIL:", normalized_email)
    print("USER FOUND:", user is not None)

    if user:
        print("USER ID:", user.id)
        print("DB EMAIL:", user.email)
        print("HASH:", user.hashed_password)
        print("PASSWORD MATCH:",
                verify_password(
                    data.password,
                    user.hashed_password,
                )    
              )
    print("=" * 50)

    if user is None or not verify_password(
        data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    token = create_access_token(
        user_id=user.id,
        email=user.email,
    )

    return TokenResponse(
        access_token=token,
        user=UserPublic(
            id=user.id,
            name=user.name,
            email=user.email,
        ),
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
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

        if user_id_value is None:
            raise authentication_error

        user_id = int(user_id_value)

    except (
        InvalidTokenError,
        TypeError,
        ValueError,
    ):
        raise authentication_error

    user = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise authentication_error

    return UserPublic(
        id=user.id,
        name=user.name,
        email=user.email,
    )