from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.tables.user import UserTable


def get_user_by_email(
    db: Session,
    email: str,
) -> UserTable | None:
    normalized_email = email.lower().strip()

    statement = select(UserTable).where(
        UserTable.email == normalized_email
    )

    return db.scalar(statement)


def get_user_by_id(
    db: Session,
    user_id: int,
) -> UserTable | None:
    statement = select(UserTable).where(
        UserTable.id == user_id
    )

    return db.scalar(statement)


def create_user(
    db: Session,
    name: str,
    email: str,
    hashed_password: str,
) -> UserTable:
    new_user = UserTable(
        name=name.strip(),
        email=email.lower().strip(),
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user