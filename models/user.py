from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Main(BaseModel):
    class Config:
        orm_mode = True


class User(Main):
    id: int
    email: str
    hashed_password: str
    created: datetime
    superuser: bool


class UserCreate(Main):
    email: str
    password: str


class Token(Main):
    access_token: str
    token_type: str


class User_Delete(Main):
    status: bool
    message: str


class User_Data(Main):
    email: str
    hashed_password: str
