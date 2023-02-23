from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Const:
    DB_URL = os.getenv("DB_URL")
    REDIS_ADDRESS = os.getenv("REDIS_ADDRESS")
    MENU_FILE_NAME = os.getenv("MENU_FILE_NAME")
    TASK_CELERY = os.getenv("TASK_CELERY")

