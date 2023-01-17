import fastapi as _fastapi
import sqlalchemy.orm as _orm
import database as _database
import models as _models
import schemas as _schemas


def _create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def count_handle(
    db: _orm.Session, menu_id, addition, dishes_number=None, submenu_id=None
):
    try:
        m = db.query(_models.Menu).filter_by(id=menu_id).one()
    except:
        raise _fastapi.HTTPException(status_code=404, detail="menu not found")
    if not submenu_id:
        m.submenus_count += addition
    if dishes_number:
        m.dishes_count -= dishes_number
    if submenu_id:
        try:
            s = (
                db.query(_models.SubMenu)
                .filter_by(id=submenu_id, menu_id=menu_id)
                .one()
            )
        except:
            raise _fastapi.HTTPException(status_code=404, detail="submenu not found")
        m.dishes_count += addition
        s.dishes_count += addition
        db.add(s)
    db.add(m)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_instance(model: _models, schema: _schemas, id: int, db: _orm.Session):
    try:
        substance = db.query(model).filter_by(id=id).one()
    except:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"{str(model.__tablename__)} not found"
        )

    return schema.from_orm(substance)


async def get_instances(model: _models, schema: _schemas, db: _orm.Session, **filter):
    instances = db.query(model).filter_by(**filter)

    return list(map(schema.from_orm, instances))


async def update_instance(
    model: _models, schema: _schemas, data: _schemas.Common, db: _orm.Session, **filter
):
    tmp = db.query(model).filter_by(**filter)
    tmp.update(data.dict(exclude_unset=True))
    if not tmp:
        raise _fastapi.HTTPException(
            status_code=404, detail=f"{str(model.__tablename__)} not found"
        )
    db.commit()

    return schema.from_orm(data)


async def create_menu(db: _orm.Session, menu: _schemas.Common):
    menu = _models.Menu(**menu.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)

    return _schemas.Menu.from_orm(menu)


async def delete_menu(menu: _schemas.Delete, id: int, db: _orm.Session):
    try:
        delete = db.query(_models.Menu).filter_by(id=id).one()
    except:
        raise _fastapi.HTTPException(status_code=404, detail="menu not found")
    db.delete(delete)
    db.commit()
    menu.status = True
    menu.message = "The menu has been deleted"
    return _schemas.Delete.from_orm(menu)


async def create_submenu(db: _orm.Session, submenu: _schemas.Common, **kwargs):
    submenu = _models.SubMenu(**{**submenu.dict(), **kwargs})
    count_handle(db, kwargs["menu_id"], 1)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)

    return _schemas.SubMenu.from_orm(submenu)


async def delete_submenu(
    menu: _schemas.Delete, menu_id: int, id: int, db: _orm.Session
):
    try:
        delete = db.query(_models.SubMenu).filter_by(menu_id=menu_id, id=id).one()
    except:
        raise _fastapi.HTTPException(status_code=404, detail="submenu not found")
    count_handle(db, menu_id, -1, delete.dishes_count)
    db.delete(delete)
    db.commit()
    menu.status = True
    menu.message = "The submenu has been deleted"

    return _schemas.Delete.from_orm(menu)


async def create_dish(db: _orm.Session, dish: _schemas.HandleDish, **kwargs):
    count_handle(db, kwargs["menu_id"], 1, None, kwargs["submenu_id"])
    del kwargs["menu_id"]
    dish = _models.Dish(**{**dish.dict(), **kwargs})
    db.add(dish)
    db.commit()
    db.refresh(dish)

    return _schemas.Dish.from_orm(dish)


async def delete_dish(
    dish: _schemas.Delete, menu_id: int, submenu_id: int, id: int, db: _orm.Session
):
    try:
        delete = db.query(_models.Dish).filter_by(id=id).one()
    except:
        raise _fastapi.HTTPException(status_code=404, detail="submenu not found")
    count_handle(db, menu_id, -1, None, submenu_id)
    db.delete(delete)
    db.commit()
    dish.status = True
    dish.message = "The dish has been deleted"

    return _schemas.Delete.from_orm(dish)
