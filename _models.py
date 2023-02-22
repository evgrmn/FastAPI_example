from __future__ import annotations

import fastapi as _fastapi
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from sqlalchemy.sql import text
from xlsxwriter import Workbook

from config.config import Config

from database.connect import db, Menu, SubMenu, Dish

'''DATABASE_URL = Config.DB_URL
engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base: _declarative = _declarative.declarative_base()


class Menu(Base):
    __tablename__ = "menu"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    submenus_count = _sql.Column(_sql.Integer, default=0)
    dishes_count = _sql.Column(_sql.Integer, default=0)

    children = _orm.relationship(
        "SubMenu",
        cascade="all,delete",
        backref="parent",
    )


class SubMenu(Base):
    __tablename__ = "submenu"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    menu_id = _sql.Column(_sql.Integer, _sql.ForeignKey("menu.id"))
    dishes_count = _sql.Column(_sql.Integer, default=0)

    children = _orm.relationship(
        "Dish",
        cascade="all,delete",
        backref="parent",
    )


class Dish(Base):
    __tablename__ = "dish"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    submenu_id = _sql.Column(_sql.Integer, _sql.ForeignKey("submenu.id"))
    price = _sql.Column(_sql.String, index=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db = next(get_db())'''


# New functions
model_dict = {"dish": Dish, "submenu": SubMenu, "menu": Menu}
delete_model_dict = [("dish", Dish), ("submenu", SubMenu), ("menu", Menu)]


async def delete_table_data(model, table_name):
    db.query(model).delete()
    db.execute(text(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1"))
    db.commit()


async def get_xlsx_menu(task_result: str):
    query = """SELECT  menu_count,
    menu_title,
    dish_count,
    dish_title,
    dish_description,
    dish_price
    FROM (SELECT menu.id as menu_id,
        '' as menu_title,
        submenu.id as submenu_id,
        dish.id as dish_id,
        dish.title as dish_title,
        dish.description as dish_description,
        '' as menu_count,
        to_char(row_number() OVER (PARTITION BY submenu.id), '9')
            as dish_count,
        dish.price as dish_price
        FROM menu
        JOIN submenu on menu_id = menu.id
        JOIN dish on submenu_id = submenu.id
        UNION
        SELECT id,
            title,
            0,
            0,
            '',
            '',
            to_char(id, '9'),
            description,
            ''
        FROM menu
        UNION
        SELECT menu_id,
            to_char(row_number() OVER (PARTITION BY menu_id), '9'),
            id,
            0,
            description,
            '',
            '',
            title,
            ''
        FROM submenu) as t
    ORDER by menu_id, submenu_id, dish_id"""
    res = db.execute(text(query))
    db.commit()
    res = res.mappings().all()
    wb = Workbook(task_result)
    ws = wb.add_worksheet("Menu")

    ordered_list = [
        "menu_count",
        "menu_title",
        "dish_count",
        "dish_title",
        "dish_description",
        "dish_price",
    ]
    for row, el in enumerate(res):
        for _key, _value in el.items():
            col = ordered_list.index(_key)
            ws.write(row, col, _value)
    wb.close()


async def count_submenu_and_dishes(
    menu_id,
    addition,
    dishes_count=None,
    submenu_id=None,
):
    try:
        menu = await get_instance(model=Menu, filter={"id": menu_id})
    except Exception:
        raise _fastapi.HTTPException(status_code=404, detail="menu not found")
    if not submenu_id:
        menu.submenus_count += addition
    if dishes_count:
        menu.dishes_count -= dishes_count
    submenu = None
    if submenu_id:
        try:
            submenu = await get_instance(
                model=SubMenu,
                filter={"id": submenu_id, "menu_id": menu_id},
            )
        except Exception:
            raise _fastapi.HTTPException(
                status_code=404,
                detail="submenu not found",
            )
        menu.dishes_count += addition
        submenu.dishes_count += addition
        db.add(submenu)
    db.add(menu)


async def get_instance(model, filter):
    return db.query(model).filter_by(**filter).one()


async def get_instances(model, schema, filter):
    return list(map(schema.from_orm, db.query(model).filter_by(**filter)))


async def add_instance(data):
    db.add(data)
    db.commit()
    db.refresh(data)

    return data


async def delete_instance(model, **filter):
    delete = await get_instance(model, **filter)
    db.delete(delete)
    db.commit()

    if "submenu_id" not in filter["filter"]:
        return delete.dishes_count


async def update_instance(model, data, filter):
    tmp = db.query(model).filter_by(**filter)
    res = tmp.update(data.dict(exclude_unset=True))
    db.commit()

    return res


async def rollback():
    db.rollback()


async def commit():
    db.commit()
