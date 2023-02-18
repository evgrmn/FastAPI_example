from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    TESTING = os.getenv("TESTING")
    DB_URL = os.getenv("DB_URL")
    REDIS_ADDRESS = os.getenv("REDIS_ADDRESS")
    if TESTING:
        DB_URL = "postgresql://postgres:password@test_postgres:5432/test"
        REDIS_ADDRESS = "test_redis"


class Variables:
    id: str
    title: str
    description: str
    submenu_id: str
    submenu_title: str
    submenu_description: str
    dish_id: str
    dish_title: str
    dish_description: str
    dish_price: str
    submenu_count: int = 0
    dish_count: int = 0
    menu_dish_count: int = 0
