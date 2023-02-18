from __future__ import annotations

from pydantic import BaseModel


class Menu(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class Data(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Delete(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True
