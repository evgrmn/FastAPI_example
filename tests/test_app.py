from __future__ import annotations

import asyncio
from typing import Generator

import httpx
import pytest
import pytest_asyncio
from database.models import create_tables
from main import app

from .vars import Variables as var

pytestmark = pytest.mark.asyncio


# Create tables
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


url = "http://test/api/v1/menus/"


async def test_1(client):
    r = await client.get(url)
    assert r.status_code == 200, "wrong response"


# GRUD for menu


async def test_2(client):
    r = await client.get(url)
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'


async def test_3(client):
    payload = {"title": "menu pytest", "description": "menu pytest"}
    r = await client.post(url, json=payload)
    var.id = r.json()["id"]
    var.title = r.json()["title"]
    var.description = r.json()["description"]
    assert r.status_code == 201, "menu did not create"


async def test_4(client):
    r = await client.get(url)
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) != 0, 'table "table "menu" must not be empty'


async def test_5(client):
    r = await client.get(url + var.id)
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
    r = await client.delete(url + var.id)
    assert r.status_code == 200, "menu not found"


async def test_7(client):
    r = await client.get(url)
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'


async def test_8(client):
    r = await client.get(url + var.id)
    assert r.status_code == 404, "wrong response"


# GRUD for submenu


async def test_9(client):
    payload = {"title": "pytest", "description": "pytest"}
    r = await client.post(url, json=payload)
    var.id = r.json()["id"]
    var.title = r.json()["title"]
    var.description = r.json()["description"]
    assert r.status_code == 201, "menu is not created"


async def test_10(client):
    r = await client.get(url)
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) != 0, 'table "menu" must not be empty'


async def test_11(client):
    payload = {"title": "submenu pytest", "description": "submenu pytest"}
    r = await client.post(url + var.id + "/submenus", json=payload)
    var.submenu_id = r.json()["id"]
    var.submenu_title = r.json()["title"]
    var.submenu_description = r.json()["description"]
    assert r.status_code == 201, "submenu is not created"


async def test_12(client):
    r = await client.get(url + var.id + "/submenus")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) != 0, 'table "submenu" must not be empty'


async def test_13(client):
    r = await client.get(url + var.id + "/submenus/" + var.submenu_id)
    assert r.status_code == 200, "wrong response"
    assert r.json()["id"] == var.submenu_id, "submenu id is not valid"
    assert r.json()["title"] == var.submenu_title, "submenu title`s not valid"
    assert (
        r.json()["description"] == var.submenu_description
    ), "submenu description is not valid"
    assert r.json()["title"] == "submenu pytest", "submenu title is not valid"
    assert (
        r.json()["description"] == "submenu pytest"
    ), "submenu description is not valid"


async def test_14(client):
    r = await client.delete(f"{url}{var.id}/submenus/{var.submenu_id}")
    assert r.status_code == 200, "submenu not found"


async def test_15(client):
    r = await client.get(url + var.id + "/submenus")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "submenu" must be empty'


async def test_16(client):
    r = await client.get(url + var.id + "/submenus/" + var.submenu_id)
    assert r.status_code == 404, "submenu must be deleted"


async def test_17(client):
    r = await client.delete(url + var.id)
    assert r.status_code == 200, "menu not found"


async def test_18(client):
    r = await client.get(url)
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'


# GRUD for dish


async def test_19(client):
    payload = {"title": "menu pytest", "description": "menu pytest"}
    r = await client.post(url, json=payload)
    var.id = r.json()["id"]
    var.title = r.json()["title"]
    var.description = r.json()["description"]
    assert r.status_code == 201, "menu is not created"


async def test_20(client):
    payload = {"title": "submenu pytest", "description": "submenu pytest"}
    r = await client.post(url + var.id + "/submenus", json=payload)
    var.submenu_id = r.json()["id"]
    var.submenu_title = r.json()["title"]
    var.submenu_description = r.json()["description"]
    assert r.status_code == 201, "submenu is not created"


async def test_21(client):
    r = await client.get(f"{url}{var.id}/submenus/{var.submenu_id}/dishes")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "dish" must be empty'


async def test_22(client):
    payload = {
        "title": "dish pytest",
        "description": "dish pytest",
        "price": "12.50",
    }
    r = await client.post(
        url + var.id + "/submenus/" + var.submenu_id + "/dishes",
        json=payload,
    )
    var.dish_id = r.json()["id"]
    var.dish_title = r.json()["title"]
    var.dish_description = r.json()["description"]
    var.dish_price = r.json()["price"]
    assert r.status_code == 201, "dish is not created"


async def test_23(client):
    r = await client.get(f"{url}{var.id}/submenus/{var.submenu_id}/dishes")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) != 0, 'table "dish" must not be empty'


async def test_24(client):
    r = await client.get(
        f"{url}{var.id}/submenus/{var.submenu_id}/dishes/{var.dish_id}",
    )
    assert r.status_code == 200, "wrong response"
    assert r.json()["id"] == var.dish_id, "dish id is not valid"
    assert r.json()["title"] == var.dish_title, "dish title is not valid"
    assert (
        r.json()["description"] == var.dish_description
    ), "dish title\
         is not valid"
    assert r.json()["price"] == var.dish_price, "dish price is not valid"
    assert r.json()["title"] == "dish pytest", "dish title is not valid"
    assert r.json()["description"] == "dish pytest", "dish title is not valid"
    assert r.json()["price"] == "12.50", "dish price is not valid"


async def test_25(client):
    r = await client.delete(
        f"{url}{var.id}/submenus/{var.submenu_id}/dishes/{var.dish_id}",
    )
    assert r.status_code == 200, "dish not found"


async def test_26(client):
    r = await client.get(f"{url}{var.id}/submenus/{var.submenu_id}/dishes")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "dish" must be empty'


async def test_27(client):
    r = await client.delete(
        f"{url}{var.id}/submenus/{var.submenu_id}/dishes/{var.dish_id}",
    )
    assert r.status_code == 404, "dish must be deleted"


async def test_28(client):
    r = await client.delete(url + var.id + "/submenus/" + var.submenu_id)
    assert r.status_code == 200, "submenu not found"


async def test_29(client):
    r = await client.get(url + var.id + "/submenus")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "submenu" must be empty'


async def test_30(client):
    r = await client.delete(url + var.id)
    assert r.status_code == 200, "menu not found"


async def test_31(client):
    r = await client.get(url)
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'


# GRUD for counting the number of dishes and submenus


async def test_32(client):
    payload = {"title": "menu pytest", "description": "menu pytest"}
    r = await client.post(url, json=payload)
    var.id = r.json()["id"]
    var.title = r.json()["title"]
    var.description = r.json()["description"]
    assert r.status_code == 201, "menu is not created"


async def test_33(client):
    payload = {"title": "submenu pytest", "description": "submenu pytest"}
    r = await client.post(url + var.id + "/submenus", json=payload)
    var.submenu_id = r.json()["id"]
    var.submenu_title = r.json()["title"]
    var.submenu_description = r.json()["description"]
    var.submenu_count += 1
    assert r.status_code == 201, "submenu is not created"


async def test_34(client):
    payload = {
        "title": "dish pytest 1",
        "description": "dish pytest 1",
        "price": "10.50",
    }
    r = await client.post(
        url + var.id + "/submenus/" + var.submenu_id + "/dishes",
        json=payload,
    )
    var.dish_id = r.json()["id"]
    var.dish_title = r.json()["title"]
    var.dish_description = r.json()["description"]
    var.dish_price = r.json()["price"]
    var.dish_count += 1
    var.menu_dish_count += 1
    assert r.status_code == 201, "dish is not created"


async def test_35(client):
    payload = {
        "title": "dish pytest 2",
        "description": "dish pytest 2",
        "price": "15.00",
    }
    r = await client.post(
        url + var.id + "/submenus/" + var.submenu_id + "/dishes",
        json=payload,
    )
    var.dish_id = r.json()["id"]
    var.dish_title = r.json()["title"]
    var.dish_description = r.json()["description"]
    var.dish_price = r.json()["price"]
    var.dish_count += 1
    var.menu_dish_count += 1
    assert r.status_code == 201, "dish is not created"


async def test_36(client):
    r = await client.get(url + var.id)
    assert r.status_code == 200, "wrong response"
    assert r.json()["id"] == var.id, "menu id is not valid"
    assert (
        r.json()["submenus_count"] == var.submenu_count
    ), "submenus_count is not valid"
    assert (
        r.json()["dishes_count"] == var.menu_dish_count
    ), "dishes_count\
         is not valid"


async def test_37(client):
    r = await client.get(url + var.id + "/submenus/" + var.submenu_id)
    assert r.status_code == 200, "wrong response"
    assert r.json()["id"] == var.submenu_id, "submenu id is not valid"
    assert (
        r.json()["dishes_count"] == var.dish_count
    ), "dishes_count\
         is not valid"


async def test_38(client):
    r = await client.delete(f"{url}{var.id}/submenus/{var.submenu_id}")
    var.dish_count -= 2
    var.menu_dish_count -= 2
    var.submenu_count -= 1
    assert r.status_code == 200, "submenu not found"


async def test_39(client):
    r = await client.get(url + var.id + "/submenus")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "submenu" must be empty'


async def test_40(client):
    r = await client.get(f"{url}{var.id}/submenus/{var.submenu_id}/dishes")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "dish" must be empty'


async def test_41(client):
    r = await client.get(url + var.id)
    assert r.status_code == 200, "wrong response"
    assert r.json()["id"] == var.id, "menu id is not valid"
    assert r.json()["submenus_count"] == 0, "submenus_count is not valid"
    assert r.json()["dishes_count"] == 0, "dishes_count is not valid"


async def test_42(client):
    r = await client.delete(url + var.id)
    assert r.status_code == 200, "menu not found"


async def test_43(client):
    r = await client.get(url)
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'
