import pytest

from .conftest import url
from .vars import Variables as var

pytestmark = pytest.mark.asyncio


async def test_19(client):
    payload = {"title": "menu pytest", "description": "menu pytest"}
    r = await client.post(f"{url}menus/", json=payload)
    var.id = r.json()["id"]
    var.title = r.json()["title"]
    var.description = r.json()["description"]
    assert r.status_code == 201, "menu is not created"


async def test_20(client):
    payload = {"title": "submenu pytest", "description": "submenu pytest"}
    r = await client.post(f"{url}menus/{var.id}/submenus", json=payload)
    var.submenu_id = r.json()["id"]
    var.submenu_title = r.json()["title"]
    var.submenu_description = r.json()["description"]
    assert r.status_code == 201, "submenu is not created"


async def test_21(client):
    r = await client.get(f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "dish" must be empty'


async def test_22(client):
    payload = {
        "title": "dish pytest",
        "description": "dish pytest",
        "price": "12.50",
    }
    r = await client.post(
        f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes",
        json=payload,
    )
    var.dish_id = r.json()["id"]
    var.dish_title = r.json()["title"]
    var.dish_description = r.json()["description"]
    var.dish_price = r.json()["price"]
    assert r.status_code == 201, "dish is not created"


async def test_23(client):
    r = await client.get(f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) != 0, 'table "dish" must not be empty'


async def test_24(client):
    r = await client.get(
        f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes/{var.dish_id}",
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
        f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes/{var.dish_id}",
    )
    assert r.status_code == 200, "dish not found"


async def test_26(client):
    r = await client.get(f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "dish" must be empty'


async def test_27(client):
    r = await client.delete(
        f"{url}menus/{var.id}/submenus/{var.submenu_id}/dishes/{var.dish_id}",
    )
    assert r.status_code == 404, "dish must be deleted"


async def test_28(client):
    r = await client.delete(f"{url}menus/{var.id}/submenus/{var.submenu_id}")
    assert r.status_code == 200, "submenu not found"


async def test_29(client):
    r = await client.get(f"{url}menus/{var.id}/submenus")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "submenu" must be empty'


async def test_30(client):
    r = await client.delete(f"{url}menus/{var.id}")
    assert r.status_code == 200, "menu not found"


async def test_31(client):
    r = await client.get(f"{url}menus/")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'
