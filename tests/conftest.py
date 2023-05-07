from __future__ import annotations

import asyncio
from typing import Generator

import httpx
import pytest
import pytest_asyncio

from control.user import get_current_user
from database.models import create_tables, drop_tables
from main import app

from .vars import Variables as var


async def override_dependency():
    return {
        "id": var.user_id,
        "email": var.email,
        "hashed_password": "None",
        "created": var.created,
        "superuser": var.superuser,
    }


app.dependency_overrides[get_current_user] = override_dependency

pytestmark = pytest.mark.asyncio


# initialize tables
asyncio.run(drop_tables())
asyncio.run(create_tables())


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client():
    cl = httpx.AsyncClient(app=app)
    yield cl
    await cl.aclose()


url = "http://test/api/v1/"
