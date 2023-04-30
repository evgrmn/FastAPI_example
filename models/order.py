from __future__ import annotations

from pydantic import BaseModel


class Main(BaseModel):
    class Config:
        orm_mode = True


class Order(Main):
    id: int
    user_id: int
    dish_id: int
    quantity: int


class Order_Delete(Main):
    status: bool
    message: str
