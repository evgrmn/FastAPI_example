import fastapi as _fastapi

import database.connect as table
from database.connect import db
from models.menu import Data, Delete, Menu
from caching import functions as cache


async def get_menus():
    return list(map(Menu.from_orm, db.query(table.Menu)))


async def create_menu(data: Data):
    data = table.Menu(**data.dict())
    db.add(data)
    db.commit()
    data = Menu.from_orm(data)
    await cache.set(f"Menu_{data.id}", data.dict())

    return data


async def delete_menu(id: int):
    try:
        menu = db.query(table.Menu).filter_by(id=id).one()
        db.delete(menu)
        db.commit()
    except Exception:
        raise _fastapi.HTTPException(status_code=404, detail="menu not found")
    await cache.delete_cascade(f"*Menu_{id}*")
    response = Delete
    response.status = True
    response.message = "The menu has been deleted"

    return Delete.from_orm(response)


async def get_menu(id: int):
    key_name = f"Menu_{id}"
    res = await cache.get(key_name)
    if res:
        return res
    try:
        menu = db.query(table.Menu).filter_by(id=id).one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="menu not found",
        )
    menu = Menu.from_orm(menu)
    await cache.set(key_name, menu.dict())

    return menu


async def update_menu(data, id: int):
    data = data.dict(exclude_unset=True)    
    res = db.query(table.Menu).filter_by(id=id).update(data)
    db.commit()
    if not res:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="menu {id} not found",
        )
    key_name = f"Menu_{id}"
    res = await cache.get(key_name)
    if res:
        await cache.set(key_name, res.update(data))

    return data


