import fastapi as _fastapi

import database.connect as table
from database.connect import db
from models.submenu import Data, Delete, SubMenu
from models.menu import Menu
from caching import functions as cache


async def get_submenus(menu_id: int):
    res = db.query(table.SubMenu).filter_by(menu_id=menu_id)
    return list(map(SubMenu.from_orm, res))


async def create_submenu(data: Data, menu_id: int):
    try:
        menu = db.query(table.Menu).filter_by(id=menu_id).one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"menu {menu_id} not found"
        )
    menu.submenus_count += 1
    submenu = table.SubMenu(**data.dict())
    submenu.menu_id = menu_id
    db.add(submenu)
    db.commit()
    key_name = f"Menu_{menu_id}_SubMenu_{submenu.id}"
    await cache.set(
        key_name,
        SubMenu.from_orm(submenu).dict(),
    )
    await cache.set(
        f"Menu_{menu_id}", Menu.from_orm(menu).dict()
    )

    return SubMenu.from_orm(submenu)


async def delete_submenu(menu_id: int, id: int):
    try:
        submenu = db.query(table.SubMenu).filter_by(id=id).one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"submenu {id} not found",
        )
    try:
        menu = db.query(table.Menu).filter_by(id=menu_id).one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"menu {menu_id} not found",
        )
    menu.dishes_count -= submenu.dishes_count
    menu.submenus_count -= 1
    db.delete(submenu)
    db.commit()
    await cache.delete_cascade(f"*SubMenu_{id}*")
    await cache.set(
        f"Menu_{menu_id}",
        Menu.from_orm(menu).dict(),
    )
    response = Delete
    response.status = True
    response.message = f"The submenu {id} has been deleted"

    return Delete.from_orm(response)


async def get_submenu(menu_id: int, id: int):
    key_name = f"Menu_{menu_id}_SubMenu_{id}"
    submenu = await cache.get(key_name)
    if submenu:
        return submenu
    try:
        submenu = (
            db.query(table.SubMenu)
            .join(table.Menu)
            .filter(table.SubMenu.id == id, table.Menu.id == menu_id)
            .one()
        )
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="submenu not found",
        )
    submenu = SubMenu.from_orm(submenu)
    await cache.set(key_name, submenu.dict())

    return submenu


async def update_submenu(data: Data, menu_id: int, id: int):
    data = data.dict(exclude_unset=True)
    res = db.query(table.SubMenu).filter_by(id=id).update(data)
    db.commit()
    if not res:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="submenu {id} not found",
        )
    key_name = f"Menu_{menu_id}_SubMenu_{id}"
    res = await cache.get(key_name)
    if res:
        res.update(data)
        await cache.set(key_name, res)    

    return data
