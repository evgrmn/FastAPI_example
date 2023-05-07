import pytest

from caching.functions import delete_cascade, keys

from .conftest import url
from .vars import Variables as var

pytestmark = pytest.mark.asyncio


async def test_1():
    await delete_cascade("*")
    result = await keys("*")
    assert result == [], "Redis database is not empty"


async def test_2(client):
    r = await client.get(f"{url}menus/")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'


async def test_3(client):
    payload = {"title": "menu pytest", "description": "menu pytest"}
    r = await client.post(f"{url}menus/", json=payload)
    var.id = r.json()["id"]
    var.title = r.json()["title"]
    var.description = r.json()["description"]
    assert r.status_code == 201, "menu did not create"


async def test_4(client):
    r = await client.get(f"{url}menus/")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) != 0, "table 'menu' must not be empty"


async def test_5(client):
    r = await client.get(f"{url}menus/{var.id}")
    assert r.status_code == 200, "wrong response"
    assert r.json()["id"] == var.id, "menu id is not valid"
    assert r.json()["title"] == var.title, "menu title is not valid"
    assert (
        r.json()["description"] == var.description
    ), "menu description\
         is not valid"
    assert r.json()["title"] == "menu pytest", "menu title is not valid"
    assert (
        r.json()["description"] == "menu pytest"
    ), "menu description\
         is not valid"


async def test_6(client):
    r = await client.delete(f"{url}menus/{var.id}")
    assert r.status_code == 200, "menu not found"


async def test_7(client):
    r = await client.get(f"{url}menus/")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'


async def test_8(client):
    r = await client.get(f"{url}menus/{var.id}")
    assert r.status_code == 404, "wrong response"
