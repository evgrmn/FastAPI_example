import fastapi as _fastapi

import database.connect as table
from caching import functions as cache
from database.connect import db
from models.dish import Dish, Dish_Data, Dish_Delete
from models.menu import Menu
from models.submenu import SubMenu


async def get_dishes(submenu_id: int):
    res = db.query(table.Dish).filter_by(submenu_id=submenu_id)
    return list(map(Dish.from_orm, res))


async def create_dish(data: Dish_Data, menu_id: int, submenu_id: int):
    try:
        submenu = db.query(table.SubMenu).filter_by(id=submenu_id).one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"submenu {submenu_id} not found"
        )
    try:
        menu = db.query(table.Menu).filter_by(id=menu_id).one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"menu {menu_id} not found"
        )
    submenu.dishes_count += 1
    menu.dishes_count += 1
    dish = table.Dish(**data.dict())
    dish.submenu_id = submenu_id
    db.add(dish)
    db.commit()
    key_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{dish.id}"
    await cache.set(
        key_name,
        Dish.from_orm(dish).dict(),
    )
    await cache.set(f"Menu_{menu_id}", Menu.from_orm(menu).dict())
    update_data = SubMenu.from_orm(submenu).dict()
    await cache.set(f"Menu_{menu_id}_SubMenu_{submenu_id}", update_data)

    return Dish.from_orm(dish)


async def delete_dish(menu_id: int, submenu_id: int, id: int):
    try:
        dish = db.query(table.Dish).filter_by(id=id).one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"dish {id} not found",
        )
    try:
        submenu = db.query(table.SubMenu).filter_by(id=submenu_id).one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"submenu {submenu_id} not found"
        )
    try:
        menu = db.query(table.Menu).filter_by(id=menu_id).one()
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"menu {menu_id} not found"
        )
    submenu.dishes_count -= 1
    menu.dishes_count -= 1
    db.delete(dish)
    db.commit()
    key_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{dish.id}"
    await cache.delete(key_name)
    await cache.set(f"Menu_{menu_id}", Menu.from_orm(menu).dict())
    update_data = SubMenu.from_orm(submenu).dict()
    await cache.set(f"Menu_{menu_id}_SubMenu_{submenu_id}", update_data)
    response = Dish_Delete
    response.status = True
    response.message = f"The dish {id} has been deleted"

    return Dish_Delete.from_orm(response)


async def get_dish(menu_id: int, submenu_id: int, id: int):
    key_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{id}"
    dish = await cache.get(key_name)
    if dish:
        return dish
    try:
        dish = (
            db.query(table.Dish)
            .join(table.SubMenu)
            .join(table.Menu)
            .filter(
                table.Menu.id == menu_id,
                table.Dish.id == id,
                table.Dish.submenu_id == submenu_id,
            )
            .one()
        )
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="dish not found",
        )
    dish = Dish.from_orm(dish)
    await cache.set(key_name, dish.dict())

    return dish


async def update_dish(data: Dish_Data, menu_id: int, submenu_id: int, id: int):
    data = data.dict(exclude_unset=True)
    res = db.query(table.Dish).filter_by(id=id).update(data)
    db.commit()
    if not res:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"dish {id} not found",
        )
    key_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{id}"
    res = await cache.get(key_name)
    if res:
        res.update(data)
        await cache.set(key_name, res)

    return data
