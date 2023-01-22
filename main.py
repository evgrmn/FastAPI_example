from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import schemas as _schemas
import services as _services
import os.path
from fastapi import Path
import description
import models as _models

if os.path.isfile("database.db"):
    pass
else:
    _services._create_database()

app = _fastapi.FastAPI(title="FastAPI Application", description=description.description)

req = _fastapi.Depends(_services.get_db)


@app.get("/api/v1/menus", response_model=List[_schemas.Menu])
async def get_menus(
    db: _orm.Session = req,
):

    return await _services.get_instances(
        model=_models.Menu, schema=_schemas.Menu, db=db
    )


@app.get("/api/v1/menus/{menu_id}", response_model=_schemas.Menu)
async def get_menu(
    menu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.get_instance(
        model=_models.Menu, schema=_schemas.Menu, id=menu_id, db=db
    )


@app.post("/api/v1/menus", response_model=_schemas.Menu, status_code=201)
async def create_menu(
    menu: _schemas.Common,
    db: _orm.Session = req,
):

    return await _services.create_menu(menu=menu, db=db)


@app.patch("/api/v1/menus/{menu_id}", response_model=_schemas.Common)
async def update_menu(
    data: _schemas.Common,
    menu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.update_instance(
        model=_models.Menu, schema=_schemas.Common, data=data, db=db, id=menu_id
    )


@app.delete("/api/v1/menus/{menu_id}", response_model=_schemas.Delete)
async def delete_menu(
    menu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.delete_menu(menu=_schemas.Delete, id=menu_id, db=db)


@app.post(
    "/api/v1/menus/{menu_id}/submenus", response_model=_schemas.SubMenu, status_code=201
)
async def create_submenu(
    submenu: _schemas.Common,
    menu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.create_submenu(submenu=submenu, db=db, menu_id=menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=List[_schemas.SubMenu])
async def get_submenus(
    menu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.get_instances(
        model=_models.SubMenu, schema=_schemas.SubMenu, db=db, menu_id=menu_id
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=_schemas.SubMenu
)
async def get_submenu(
    menu_id: int = Path(),
    submenu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.get_instance(
        model=_models.SubMenu, schema=_schemas.SubMenu, id=submenu_id, db=db
    )


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=_schemas.Common
)
async def update_submenu(
    data: _schemas.Common,
    menu_id: int = Path(),
    submenu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.update_instance(
        model=_models.SubMenu, schema=_schemas.Common, data=data, db=db, id=submenu_id
    )


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=_schemas.Delete
)
async def delete_submenu(
    menu_id: int = Path(),
    submenu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.delete_submenu(
        menu=_schemas.Delete, menu_id=menu_id, id=submenu_id, db=db
    )


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=_schemas.Dish,
    status_code=201,
)
async def create_dish(
    dish: _schemas.HandleDish,
    menu_id: int = Path(),
    submenu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.create_dish(
        dish=dish, db=db, menu_id=menu_id, submenu_id=submenu_id
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[_schemas.Dish],
)
async def get_dishes(
    menu_id: int = Path(),
    submenu_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.get_instances(
        model=_models.Dish, schema=_schemas.Dish, db=db, submenu_id=submenu_id
    )


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=_schemas.Dish,
)
async def get_dish(
    menu_id: int = Path(),
    submenu_id: int = Path(),
    dish_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.get_instance(
        model=_models.Dish, schema=_schemas.Dish, id=dish_id, db=db
    )


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=_schemas.Delete,
)
async def delete_dish(
    menu_id: int = Path(),
    submenu_id: int = Path(),
    dish_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.delete_dish(
        dish=_schemas.Delete, menu_id=menu_id, submenu_id=submenu_id, id=dish_id, db=db
    )


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=_schemas.HandleDish,
)
async def update_dish(
    data: _schemas.HandleDish,
    menu_id: int = Path(),
    submenu_id: int = Path(),
    dish_id: int = Path(),
    db: _orm.Session = req,
):

    return await _services.update_instance(
        model=_models.Dish, schema=_schemas.HandleDish, data=data, db=db, id=dish_id
    )
