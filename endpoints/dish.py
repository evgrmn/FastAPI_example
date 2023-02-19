from fastapi import APIRouter

import control.dish as _control
from models.dish import Data, Delete, Dish

router = APIRouter()


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[Dish],
    summary="Get dish list",
)
async def get_dishes(
    menu_id: int,
    submenu_id: int,
):
    """
    Получение списка блюд.
    'menu_id' - id меню, с которым связано подменю данного блюда,
    'submenu_id' - id подменю данного блюда.
    """

    return await _control.get_dishes(
        submenu_id=submenu_id,
    )


@router.post(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=Dish,
    status_code=201,
    summary="Create a new dish",
)
async def create_dish(
    data: Data,
    menu_id: int,
    submenu_id: int,
):
    """
    Создание нового блюда.
    'menu_id' - id меню, с которым связано подменю данного блюда,
    'submenu_id' - id подменю данного блюда.
    'title' - название блюда, 'description' - описание блюда,
    'price' - цена блюда
    """

    return await _control.create_dish(
        data=data,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )


@router.delete(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Delete,
    summary="Delete dish",
)
async def delete_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
):
    """
    Удаление определенного блюда.
    'menu_id' - id меню, с которым связано подменю удаляемого блюда,
    'submenu_id' - id подменю удаляемого блюда.
    'dish_id' - id удаляемого блюда.
    """

    return await _control.delete_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        id=dish_id,
    )


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Dish,
    summary="Get dish",
)
async def get_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
):
    """
    Получение определенного блюда.
    'menu_id' - id меню, с которым связано подменю данного блюда,
    'submenu_id' - id подменю данного блюда.
    'dish_id' - id требуемого блюда.
    """

    return await _control.get_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        id=dish_id,
    )


@router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Data,
    summary="Update dish",
)
async def update_dish(
    data: Data,
    menu_id: int,
    submenu_id: int,
    dish_id: int,
):
    """
    Обновление определенного блюда.
    'menu_id' - id меню, с которым связано подменю блюда,
    'submenu_id' - id подменю блюда.
    'dish_id' - id блюда.
    'title' - новое название блюда, 'description' - новое описание блюда,
    'price' - новая цена блюда
    """

    return await _control.update_dish(
        data=data,
        menu_id=menu_id,
        submenu_id=submenu_id,
        id=dish_id,
    )
