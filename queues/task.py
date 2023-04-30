import asyncio

import sqlalchemy as _sql
from sqlalchemy import String, func
from sqlalchemy.sql.expression import bindparam as new_col
from xlsxwriter import Workbook

import database.models as table
from config.config import Env
from database.connect import async_session

from .connect import celery_app

loop = asyncio.get_event_loop()


async def get_menu():
    async with async_session() as session:
        async with session.begin():
            sub = (
                _sql.select(
                    table.Menu.id.label("menu_id"),
                    table.SubMenu.id.label("submenu_id"),
                    table.Dish.id.label("dish_id"),
                    new_col("c1", "").label("id"),
                    new_col("c2", "").label("title"),
                    new_col("c3", "").label("description"),
                    func.row_number()
                    .over(partition_by=table.Dish.submenu_id)
                    .cast(String)
                    .label("submenu_description"),
                    table.Dish.title.label("dish_title"),
                    table.Dish.description.label("dish_description"),
                    table.Dish.price.label("dish_price"),
                )
                .join(table.SubMenu, table.SubMenu.menu_id == table.Menu.id)
                .join(table.Dish, table.Dish.submenu_id == table.SubMenu.id)
                .union(
                    _sql.select(
                        table.Menu.id,
                        new_col("submenu_id", 0),
                        new_col("dish_id", 0),
                        table.Menu.id.cast(String).label("menu_id"),
                        table.Menu.title,
                        table.Menu.description,
                        new_col("c4", ""),
                        new_col("c5", ""),
                        new_col("c6", ""),
                        new_col("c7", ""),
                    ),
                    _sql.select(
                        table.SubMenu.menu_id,
                        table.SubMenu.id,
                        new_col("dish_id", 0),
                        new_col("c1", ""),
                        func.row_number()
                        .over(partition_by=table.SubMenu.menu_id)
                        .cast(String),
                        table.SubMenu.title,
                        table.SubMenu.description,
                        new_col("c5", ""),
                        new_col("c6", ""),
                        new_col("c7", ""),
                    ),
                )
                .subquery()
            )
            res = _sql.select(
                sub.c.id,
                sub.c.title,
                sub.c.description,
                sub.c.submenu_description,
                sub.c.dish_title,
                sub.c.dish_description,
                sub.c.dish_price,
            ).order_by(sub.c.menu_id, sub.c.submenu_id, sub.c.dish_id)
            restaurant_menu = await session.execute(res)
            restaurant_menu = restaurant_menu.fetchall()

            return restaurant_menu


@celery_app.task
def download_database():
    restaurant_menu = loop.run_until_complete(get_menu())
    wb = Workbook(f"sharefiles/{Env.MENU_FILE_NAME}")
    ws = wb.add_worksheet("Menu")
    for row, el in enumerate(restaurant_menu):
        for col, value in enumerate(el):
            ws.write(row, col, value)
    wb.close()

    return Env.MENU_FILE_NAME
