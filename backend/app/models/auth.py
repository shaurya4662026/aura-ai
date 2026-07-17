from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
    )
    email: str = Field(
        min_length=5,
        max_length=100,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserLogin(BaseModel):
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    name: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic