from __future__ import annotations

from pydantic import BaseModel
from config.config import Env


class Main(BaseModel):
    class Config:
        orm_mode = True


class Email(Main):
    address_from: str = Env.SMTP_EMAIL_ADDRESS
    address_to: str
    subject: str
    content: str


class Result(Main):
    result: str


class Email_list(Main):
    task_id: str
    status: str
    timestamp: str
    address_from: str
    address_to: str
    subject: str
    content: str
