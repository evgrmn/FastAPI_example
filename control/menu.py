import fastapi as _fastapi

import database.models as table
from caching import functions as cache
from models.menu import Menu, Menu_Data, Menu_Delete
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as _sql


async def get_menus(db: AsyncSession):
    res = await db.execute(_sql.select(table.Menu))

    return list(map(Menu.from_orm, res.scalars().all()))


async def create_menu(
    data: Menu_Data,
    db: AsyncSession,
):
    data = table.Menu(**data.dict())
    db.add(data)
    await db.commit()
    data = Menu.from_orm(data)
    await cache.set(f"Menu_{data.id}", data.dict())

    return data


async def delete_menu(
    id: int,
    db: AsyncSession,
):
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
):
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
    key_name = f"Menu_{id}"
    res = await cache.get(key_name)
    if res:
        await cache.set(key_name, res.update(data))

    return data
