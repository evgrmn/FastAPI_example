import fastapi as _fastapi
import sqlalchemy as _sql
from sqlalchemy.ext.asyncio import AsyncSession

import database.models as table
from caching import functions as cache
from models.menu import Menu
from models.submenu import SubMenu, SubMenu_Data, SubMenu_Delete


async def get_submenus(
    menu_id: int,
    db: AsyncSession,
):
    key_name = f"SubMenu_list_Menu_{menu_id}"
    submenu_list = await cache.get(key_name)
    if submenu_list:
        return submenu_list
    submenu_list = await db.execute(
        _sql.select(table.SubMenu).filter_by(menu_id=menu_id)
    )
    submenu_list = list(
        map(lambda x: SubMenu.from_orm(x).dict(), submenu_list.scalars().all())
    )

    return submenu_list


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
    await cache.delete(f"SubMenu_list_Menu_id_{menu_id}")

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
    await cache.delete(f"SubMenu_list_Menu_{menu_id}")

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
    submenu_dict = submenu.__dict__
    del submenu_dict["_sa_instance_state"]
    await cache.set(f"Menu_{menu_id}_SubMenu_{id}", submenu_dict)
    await cache.delete(f"SubMenu_list_Menu_{menu_id}")

    return data
