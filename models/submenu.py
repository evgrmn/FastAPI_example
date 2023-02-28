from __future__ import annotations

from pydantic import BaseModel


class Main(BaseModel):
    class Config:
        orm_mode = True


class SubMenu(Main):
    id: str
    title: str
    description: str
    menu_id: int
    dishes_count: int


class SubMenu_Data(Main):
    title: str
    description: str


class SubMenu_Delete(Main):
    status: bool
    message: str
