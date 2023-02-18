import fastapi as _fastapi

import cache_func
import database.connect as table
from database.connect import db
from models.submenu import Data, Delete, SubMenu


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
    key_cach_name = f"Menu_{menu_id}_SubMenu_{submenu.id}"
    await cache_func.cache_create(
        key_cach_name,
        SubMenu.from_orm(submenu).dict(),
    )
    await cache_func.cache_update(
        f"Menu_{menu_id}", {"submenus_count": menu.submenus_count}
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
    await cache_func.cache_delete_cascade(f"*SubMenu_{id}*")
    await cache_func.cache_update(
        f"Menu_{menu_id}",
        {"submenus_count": menu.submenus_count, "dishes_count": menu.dishes_count},
    )
    response = Delete
    response.status = True
    response.message = f"The submenu {id} has been deleted"

    return Delete.from_orm(response)


async def get_submenu(menu_id: int, id: int):
    key_cach_name = f"Menu_{menu_id}_SubMenu_{id}"
    submenu = await cache_func.cache_get(key_cach_name)
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
    await cache_func.cache_create(key_cach_name, submenu.dict())

    return submenu


async def update_submenu(data: Data, id: int):
    req = db.query(table.SubMenu).filter_by(id=id)
    res = req.update(data.dict(exclude_unset=True))
    db.commit()
    if not res:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="submenu {id} not found",
        )
    await cache_func.cache_update(f"SubMenu_{id}", data)

    return Data.from_orm(data)
