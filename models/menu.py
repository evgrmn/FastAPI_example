from __future__ import annotations

from pydantic import BaseModel


class Main(BaseModel):
    class Config:
        orm_mode = True


class Menu(Main):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class Data(Main):
    title: str
    description: str


class Delete(Main):
    status: bool
    message: str
