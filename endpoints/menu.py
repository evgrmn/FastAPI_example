from fastapi import APIRouter

import control.menu as _control
from models.menu import Data, Delete, Menu

router = APIRouter()


@router.get(
    "/",
    response_model=list[Menu],
    summary="Get menu list",
)
async def get_menus():
    """
    Получение списка меню.
    """

    return await _control.get_menus()


@router.post(
    "/",
    response_model=Menu,
    status_code=201,
    summary="Create a new menu",
)
async def create_menu(
    data: Data,
):
    """
    Создание меню. 'title' - название меню, 'description' - описание меню
    """

    return await _control.create_menu(data=data)


@router.delete(
    "/{menu_id}",
    response_model=Delete,
    summary="Delete menu",
)
async def delete_menu(
    menu_id: int,
):
    """
    Удаление меню. 'menu_id' - id в таблице 'menu'.
    Удаление меню удалит все связанные с ним подменю и блюда.
    """

    return await _control.delete_menu(id=menu_id)


@router.get(
    "/{menu_id}",
    response_model=Menu,
    summary="Get menu",
)
async def get_menu(
    menu_id: int,
):
    """
    Получение определенного меню. 'menu_id' - id меню в таблице 'menu'
    """

    return await _control.get_menu(
        id=menu_id,
    )


@router.patch(
    "/{menu_id}",
    response_model=Data,
    summary="Update menu",
)
async def update_menu(
    data: Data,
    menu_id: int,
):
    """
    Обновление определенного.
    'menu_id' - id в таблице 'menu',
    'title' - название меню, 'description' - описание меню
    """

    return await _control.update_menu(
        data=data,
        id=menu_id,
    )
