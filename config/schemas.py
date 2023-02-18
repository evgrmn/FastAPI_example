from __future__ import annotations

from pydantic import BaseModel


class Id(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        orm_mode = True


class Common(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Menu(Id):
    submenus_count: int
    dishes_count: int


class SubMenu(Id):
    dishes_count: int


class Dish(Id):
    price: str


class HandleDish(Common):
    price: str


class Delete(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True


class Task(BaseModel):
    message: str
    task_id: str


class Result(BaseModel):
    task_id: str
    status: str
    result: str
