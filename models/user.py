from __future__ import annotations

from pydantic import BaseModel
from datetime import datetime


class Main(BaseModel):
    class Config:
        orm_mode = True


class User(Main):
    id: int
    email: str
    hashed_password: str
    date_created: datetime


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