import fastapi as _fastapi

import database.models as table
from caching import functions as cache
from models.dish import Dish, Dish_Data, Dish_Delete
from models.menu import Menu
from models.submenu import SubMenu
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as _sql


async def get_dishes(
    menu_id: int,
    submenu_id: int,
    db: AsyncSession,
):
    key_name = f"Dish_list_Menu_{menu_id}_SubMenu_{submenu_id}"
    dish_list = await cache.get(key_name)
    if dish_list:
        dish_list = list(map(lambda x: x, dish_list.values()))
        return dish_list
    dish_list = await db.execute(_sql.select(table.Dish).filter_by(submenu_id=submenu_id))
    dish_list = list(map(Dish.from_orm, dish_list.scalars().all()))
    dish_dict = {}
    for n, dish in enumerate(dish_list):
        dish_dict[n] = dish.dict()
    await cache.set(key_name, dish_dict)

    return dish_list


async def create_dish(
    data: Dish_Data,
    menu_id: int,
    submenu_id: int,
    db: AsyncSession,
):
    try:
        submenu = await db.execute(_sql.select(table.SubMenu).filter_by(id=submenu_id))
        submenu = submenu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"submenu {submenu_id} not found"
        )
    try:
        menu = await db.execute(_sql.select(table.Menu).filter_by(id=menu_id))
        menu = menu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"menu {menu_id} not found"
        )
    submenu.dishes_count += 1
    menu.dishes_count += 1
    dish = table.Dish(**data.dict())
    dish.submenu_id = submenu_id
    db.add(dish)
    await db.commit()
    key_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{dish.id}"
    await cache.set(
        key_name,
        Dish.from_orm(dish).dict(),
    )
    await cache.set(f"Menu_{menu_id}", Menu.from_orm(menu).dict())
    update_data = SubMenu.from_orm(submenu).dict()
    await cache.set(f"Menu_{menu_id}_SubMenu_{submenu_id}", update_data)
    await cache.delete(f"Dish_list_Menu_{menu_id}_SubMenu_{submenu_id}")

    return Dish.from_orm(dish)


async def delete_dish(
    menu_id: int,
    submenu_id: int,
    id: int,
    db: AsyncSession,
):
    try:
        dish = await db.execute(_sql.select(table.Dish).filter_by(id=id))
        dish = dish.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"dish {id} not found",
        )
    try:
        submenu = await db.execute(_sql.select(table.SubMenu).filter_by(id=submenu_id))
        submenu = submenu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"submenu {submenu_id} not found"
        )
    try:
        menu = await db.execute(_sql.select(table.Menu).filter_by(id=menu_id))
        menu = menu.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"menu {menu_id} not found"
        )
    submenu.dishes_count -= 1
    menu.dishes_count -= 1
    await db.delete(dish)
    await db.commit()
    key_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{dish.id}"
    await cache.delete(key_name)
    await cache.set(f"Menu_{menu_id}", Menu.from_orm(menu).dict())
    update_data = SubMenu.from_orm(submenu).dict()
    await cache.set(f"Menu_{menu_id}_SubMenu_{submenu_id}", update_data)
    response = Dish_Delete
    response.status = True
    response.message = f"The dish {id} has been deleted"
    await cache.delete(f"Dish_list_Menu_{menu_id}_SubMenu_{submenu_id}")

    return Dish_Delete.from_orm(response)


async def get_dish(
    menu_id: int,
    submenu_id: int,
    id: int,
    db: AsyncSession,
):
    key_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{id}"
    dish = await cache.get(key_name)
    if dish:
        return dish
    try:
        dish = await db.execute(
            _sql.select(table.Dish)
            .join(table.SubMenu)
            .join(table.Menu)
            .filter(
                table.Menu.id == menu_id,
                table.Dish.id == id,
                table.Dish.submenu_id == submenu_id,
            )
        )
        dish = dish.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="dish not found",
        )
    dish = Dish.from_orm(dish)
    await cache.set(key_name, dish.dict())

    return dish


async def update_dish(
    data: Dish_Data,
    menu_id: int,
    submenu_id: int,
    id: int,
    db: AsyncSession,
):
    data = data.dict(exclude_unset=True)
    dish = await db.execute(_sql.select(table.Dish).filter_by(id=id))
    try:
        dish = dish.scalars().one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"dish {id} not found",
        )
    for key, value in data.items():
        setattr(dish, key, value)
    await db.commit()
    key_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{id}"
    res = await cache.get(key_name)
    if res:
        res.update(data)
        await cache.set(key_name, res)
    await cache.delete(f"Dish_list_Menu_{menu_id}_SubMenu_{submenu_id}")

    return data
