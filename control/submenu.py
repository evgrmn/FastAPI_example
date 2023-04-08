import fastapi as _fastapi

import database.models as table
from caching import functions as cache
from models.menu import Menu
from models.submenu import SubMenu, SubMenu_Data, SubMenu_Delete
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as _sql


async def get_submenus(
    menu_id: int,
    db: AsyncSession,
):
    res = await db.execute(_sql.select(table.SubMenu).filter_by(menu_id=menu_id))
    return list(map(SubMenu.from_orm, res.scalars().all()))


async def create_submenu(
    data: SubMenu_Data,
    menu_id: int,
    db: AsyncSession,
):
    try:
        menu = await db.execute(_sql.select(table.Menu).filter_by(id=menu_id))
        menu = menu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"menu {menu_id} not found"
        )
    menu.submenus_count += 1
    submenu = table.SubMenu(**data.dict())
    submenu.menu_id = menu_id
    db.add(submenu)
    await db.commit()
    key_name = f"Menu_{menu_id}_SubMenu_{submenu.id}"
    await cache.set(
        key_name,
        SubMenu.from_orm(submenu).dict(),
    )
    await cache.set(f"Menu_{menu_id}", Menu.from_orm(menu).dict())

    return SubMenu.from_orm(submenu)


async def delete_submenu(
    menu_id: int,
    id: int,
    db: AsyncSession,
):
    try:
        submenu = await db.execute(_sql.select(table.SubMenu).filter_by(id=id))
        submenu = submenu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"submenu {id} not found",
        )
    try:
        menu = await db.execute(_sql.select(table.Menu).filter_by(id=menu_id))
        menu = menu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"menu {menu_id} not found",
        )
    menu.dishes_count -= submenu.dishes_count
    menu.submenus_count -= 1
    await db.delete(submenu)
    await db.commit()
    await cache.delete_cascade(f"*SubMenu_{id}*")
    await cache.set(
        f"Menu_{menu_id}",
        Menu.from_orm(menu).dict(),
    )
    response = SubMenu_Delete
    response.status = True
    response.message = f"The submenu {id} has been deleted"

    return SubMenu_Delete.from_orm(response)


async def get_submenu(
    menu_id: int,
    id: int,
    db: AsyncSession,
):
    key_name = f"Menu_{menu_id}_SubMenu_{id}"
    submenu = await cache.get(key_name)
    if submenu:
        return submenu
    try:
        submenu = await db.execute(
            _sql.select(table.SubMenu)
            .join(table.Menu)
            .filter(
                table.Menu.id == menu_id,
                table.SubMenu.id == id,
            )
        )
        submenu = submenu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="submenu not found",
        )
    submenu = SubMenu.from_orm(submenu)
    await cache.set(key_name, submenu.dict())

    return submenu


async def update_submenu(
    data: SubMenu_Data,
    menu_id: int,
    id: int,
    db: AsyncSession,
):
    data = data.dict(exclude_unset=True)
    submenu = await db.execute(_sql.select(table.SubMenu).filter_by(id=id))
    try:
        submenu = submenu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"submenu {id} not found",
        )
    for key, value in data.items():
        setattr(submenu, key, value)
    await db.commit()
    key_name = f"Menu_{menu_id}_SubMenu_{id}"
    res = await cache.get(key_name)
    if res:
        res.update(data)
        await cache.set(key_name, res)

    return data
