from sqlalchemy.sql import text
from xlsxwriter import Workbook

from config.config import Env
from database.connect import db

from .connect import celery_app


@celery_app.task
def download_database():
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
    wb = Workbook(f"sharefiles/{Env.MENU_FILE_NAME}")
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

    return Env.MENU_FILE_NAME
