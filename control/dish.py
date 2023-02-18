import fastapi as _fastapi

import cache_func
import database.connect as table
from database.connect import db
from models.dish import Data, Delete, Dish


async def get_dishes(submenu_id: int):
    res = db.query(table.Dish).filter_by(submenu_id=submenu_id)
    return list(map(Dish.from_orm, res))


async def create_dish(data: Data, menu_id: int, submenu_id: int):
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
    key_cach_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{dish.id}"
    await cache_func.cache_create(
        key_cach_name,
        Dish.from_orm(dish).dict(),
    )
    await cache_func.cache_update(
        f"Menu_{menu_id}", {"dishes_count": menu.dishes_count}
    )
    update_data = {"dishes_count": submenu.dishes_count}
    await cache_func.cache_update(f"Menu_{menu_id}_SubMenu_{submenu_id}", update_data)

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
    key_cach_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{dish.id}"
    await cache_func.cache_delete(key_cach_name)
    await cache_func.cache_update(
        f"Menu_{menu_id}", {"dishes_count": menu.dishes_count}
    )
    update_data = {"dishes_count": submenu.dishes_count}
    await cache_func.cache_update(f"Menu_{menu_id}_SubMenu_{submenu_id}", update_data)
    response = Delete
    response.status = True
    response.message = f"The dish {id} has been deleted"

    return Delete.from_orm(response)


async def get_dish(menu_id: int, submenu_id: int, id: int):
    key_cach_name = f"Menu_{menu_id}_SubMenu_{submenu_id}_Dish_{id}"
    dish = await cache_func.cache_get(key_cach_name)
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
    await cache_func.cache_create(key_cach_name, dish.dict())

    return dish


async def update_dish(data: Data, id: int):
    req = db.query(table.Dish).filter_by(id=id)
    res = req.update(data.dict(exclude_unset=True))
    db.commit()
    if not res:
        raise _fastapi.HTTPException(
            status_code=404,
            detail=f"dish {id} not found",
        )
    await cache_func.cache_update(f"Dish_{id}", data)

    return Data.from_orm(data)
