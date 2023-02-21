from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.getenv("DB_URL")
    REDIS_ADDRESS = os.getenv("REDIS_ADDRESS")

