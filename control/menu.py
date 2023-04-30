import fastapi as _fastapi
import sqlalchemy as _sql
from sqlalchemy.ext.asyncio import AsyncSession

import database.models as table
from caching import functions as cache
from models.menu import Menu, Menu_Data, Menu_Delete
from models.user import User


async def get_menus(
    db: AsyncSession,
):
    key_name = "Menu_list"
    menu_list = await cache.get(key_name)
    if menu_list:
        return menu_list
    menu_list = await db.execute(_sql.select(table.Menu))
    menu_list = menu_list.scalars().all()
    menu_list = list(map(lambda x: Menu.from_orm(x).dict(), menu_list))
    await cache.set(key_name, menu_list)

    return menu_list


async def create_menu(
    data: Menu_Data,
    db: AsyncSession,
    user: User,
):
    if not user["superuser"]:
        raise _fastapi.HTTPException(status_code=400, detail="not properly authorized")
    data = table.Menu(**data.dict())
    db.add(data)
    await db.commit()
    data = Menu.from_orm(data)
    await cache.set(f"Menu_{data.id}", data.dict())
    await cache.delete("Menu_list")

    return data


async def delete_menu(
    id: int,
    db: AsyncSession,
    user: User,
):
    if not user["superuser"]:
        raise _fastapi.HTTPException(status_code=400, detail="not properly authorized")
    try:
        menu = await db.execute(_sql.select(table.Menu).filter_by(id=id))
        await db.delete(menu.scalars().one())
        await db.commit()
    except Exception:
        raise _fastapi.HTTPException(status_code=404, detail="menu not found")
    await cache.delete_cascade(f"*Menu_{id}*")
    response = Menu_Delete
    response.status = True
    response.message = "The menu has been deleted"
    await cache.delete("Menu_list")

    return Menu_Delete.from_orm(response)


async def get_menu(
    id: int,
    db: AsyncSession,
):
    key_name = f"Menu_{id}"
    res = await cache.get(key_name)
    if res:
        return res
    try:
        menu = await db.execute(_sql.select(table.Menu).filter_by(id=id))
        menu = menu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="menu not found",
        )
    menu = Menu.from_orm(menu)
    await cache.set(key_name, menu.dict())

    return menu


async def update_menu(
    data: Menu_Data,
    id: int,
    db: AsyncSession,
    user: User,
):
    if not user["superuser"]:
        raise _fastapi.HTTPException(status_code=400, detail="not properly authorized")
    data = data.dict(exclude_unset=True)
    menu = await db.execute(_sql.select(table.Menu).filter_by(id=id))
    try:
        menu = menu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"menu {id} not found",
        )
    for key, value in data.items():
        setattr(menu, key, value)
    await db.commit()
    menu_dict = menu.__dict__
    del menu_dict["_sa_instance_state"]
    await cache.set(f"Menu_{id}", menu_dict)
    await cache.delete("Menu_list")

    return data
