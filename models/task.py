from __future__ import annotations

from pydantic import BaseModel


class Main(BaseModel):
    class Config:
        orm_mode = True


class Task(Main):
    message: str
    task_id: str


class Result(Main):
    task_id: str
    status: str
    result: str


class Fill(Main):
    result: str
