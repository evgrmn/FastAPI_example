import pytest

from .conftest import url
from .vars import Variables as var

pytestmark = pytest.mark.asyncio


async def test_9(client):
    payload = {"title": "pytest", "description": "pytest"}
    r = await client.post(f"{url}menus/", json=payload)
    var.id = r.json()["id"]
    var.title = r.json()["title"]
    var.description = r.json()["description"]
    assert r.status_code == 201, "menu is not created"


async def test_10(client):
    r = await client.get(f"{url}menus/")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) != 0, 'table "menu" must not be empty'


async def test_11(client):
    payload = {"title": "submenu pytest", "description": "submenu pytest"}
    r = await client.post(f"{url}menus/{var.id}/submenus", json=payload)
    var.submenu_id = r.json()["id"]
    var.submenu_title = r.json()["title"]
    var.submenu_description = r.json()["description"]
    assert r.status_code == 201, "submenu is not created"


async def test_12(client):
    r = await client.get(f"{url}menus/{var.id}/submenus")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) != 0, 'table "submenu" must not be empty'


async def test_13(client):
    r = await client.get(f"{url}menus/{var.id}/submenus/{var.submenu_id}")
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
    r = await client.delete(f"{url}menus/{var.id}/submenus/{var.submenu_id}")
    assert r.status_code == 200, "submenu not found"


async def test_15(client):
    r = await client.get(f"{url}menus/{var.id}/submenus")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "submenu" must be empty'


async def test_16(client):
    r = await client.get(f"{url}menus/{var.id}/submenus/{var.submenu_id}")
    assert r.status_code == 404, "submenu must be deleted"


async def test_17(client):
    r = await client.delete(f"{url}menus/{var.id}")
    assert r.status_code == 200, "menu not found"


async def test_18(client):
    r = await client.get(f"{url}menus/")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "menu" must be empty'