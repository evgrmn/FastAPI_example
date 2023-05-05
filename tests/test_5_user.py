import pytest

from .conftest import url
from .vars import Variables as var

pytestmark = pytest.mark.asyncio


async def test_44(client):
    r = await client.get(f"{url}user/all")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "user" must be empty'


async def test_45(client):
    payload = {"email": "user1@gmail.c", "password": "111"}
    r = await client.post(f"{url}user/new", json=payload)
    assert r.status_code == 404, "incorrect email"


async def test_46(client):
    payload = {"email": "@gmail.com", "password": "111"}
    r = await client.post(f"{url}user/new", json=payload)
    assert r.status_code == 404, "incorrect email"


async def test_47(client):
    payload = {"email": "user", "password": "111"}
    r = await client.post(f"{url}user/new", json=payload)
    assert r.status_code == 404, "incorrect email"


async def test_48(client):
    payload = {"email": "user1@gmail.com", "password": "111"}
    r = await client.post(f"{url}user/new", json=payload)
    assert r.status_code == 201, "user is not created"
    var.user_id = r.json()["id"]
    var.email = r.json()["email"]
    var.created = r.json()["created"]
    var.superuser = r.json()["superuser"]
    assert var.superuser is False, "field superuser must be False"


async def test_49(client):
    r = await client.get(f"{url}user/all")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 1, 'table "user" must have 1 record'


async def test_50(client):
    r = await client.get(f"{url}user/me")
    assert r.status_code == 200, "wrong response"


async def test_51(client):
    payload = {"email": "user2@gmail.com", "hashed_password": "222"}
    r = await client.patch(f"{url}user/{var.user_id}", json=payload)
    assert r.status_code == 200, "wrong response"
    var.email = r.json()["email"]


async def test_52(client):
    r = await client.get(f"{url}user/me")
    assert r.status_code == 200, "wrong response"
    assert r.json()["email"] == var.email, "wrong response"


async def test_53(client):
    r = await client.delete(f"{url}user/{var.user_id}")
    assert r.status_code == 200, "user not found"


async def test_54(client):
    r = await client.get(f"{url}user/all")
    assert r.status_code == 200, "wrong response"
    assert len(r.json()) == 0, 'table "user" must be empty'