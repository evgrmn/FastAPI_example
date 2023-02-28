from __future__ import annotations

from pydantic import BaseModel


class Main(BaseModel):
    class Config:
        orm_mode = True


class Dish(Main):
    id: str
    title: str
    description: str
    submenu_id: int
    price: str


class Data(Main):
    title: str
    description: str
    price: str


class Delete(Main):
    status: bool
    message: str
