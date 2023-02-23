from __future__ import annotations

from pydantic import BaseModel


class Task(BaseModel):
    message: str
    task_id: str

    class Config:
        orm_mode = True


class Result(BaseModel):
    task_id: str
    status: str
    result: str

    class Config:
        orm_mode = True