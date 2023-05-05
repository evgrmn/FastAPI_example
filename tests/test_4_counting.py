import pytest

from .conftest import url
from .vars import Variables as var

pytestmark = pytest.mark.asyncio


async def test_32(client):
    payload = {"title": "menu pytest", "description": "menu pytest"}
    r = await client.post(f"{url}menus/", json=payload)
    var.id = r.json()["id"]
    var.title = r.json()["title"]
    var.description = r.json()["description"]
    assert r.status_code == 201, "menu is not created"


async def test_33(client):
    payload = {"title": "submenu pytest", "description": "submenu pytest"}
    r = await client.post(f"{url}menus/{var.id}/submenus", json=payload)
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
        f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes",
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
        f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes",
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
    r = await client.get(f"{url}menus/{var.id}")
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
    r = await client.get(f"{url}menus/{var.id}/submenus/{var.submenu_id}")
    assert r.status_code == 200, "wrong response"
    assert r.json()["id"] == var.submenu_id, "submenu id is not valid"
    assert (
        r.json()["dishes_count"] == var.dish_count
    ), "dishes_count\
         is not valid"


async def test_38(client):
    r = await client.delete(f"{url}menus/{var.id}/submenus/{var.submenu_id}")
    var.dish_count -= 2
    var.menu_dish_count -= 2
    var.submenu_count -= 1
    assert r.status_code == 200, "submenu not found"


async def test_39(client):
    r = await client.get(f"{url}menus/{var.id}/submenus")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "submenu" must be empty'


async def test_40(client):
    r = await client.get(f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "dish" must be empty'


async def test_41(client):
    r = await client.get(f"{url}menus/{var.id}")
    assert r.status_code == 200, "wrong response"
    assert r.json()["id"] == var.id, "menu id is not valid"
    assert r.json()["submenus_count"] == 0, "submenus_count is not valid"
    assert r.json()["dishes_count"] == 0, "dishes_count is not valid"


async def test_42(client):
    r = await client.delete(f"{url}menus/{var.id}")
    assert r.status_code == 200, "menu not found"


async def test_43(client):
    r = await client.get(f"{url}menus/")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'