from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import control.dish as _control
from database.connect import session
from models.dish import Dish, Dish_Data, Dish_Delete

router = APIRouter()


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[Dish],
    summary="Get dish list",
)
async def get_dishes(
    menu_id: int,
    submenu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Getting a list of dishes.
    'menu_id' - menu id, taking into account the submenu of this dish,
    'submenu_id' - submenu id of this dish.
    """

    return await _control.get_dishes(menu_id=menu_id, submenu_id=submenu_id, db=db)


@router.post(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=Dish,
    status_code=201,
    summary="Create a new dish",
)
async def create_dish(
    data: Dish_Data,
    menu_id: int,
    submenu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Creating a new dish
    'menu_id' - id of the menu with which the submenu
    of this dish is associated,
    'submenu_id' - submenu id of this dish.
    'title' - the name of the dish,
    'description' - the description of the dish,
    'price' - the price of the dish.
    """

    return await _control.create_dish(
        data=data, menu_id=menu_id, submenu_id=submenu_id, db=db
    )


@router.delete(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Dish_Delete,
    summary="Delete dish",
)
async def delete_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Removing a specific dish.
    'menu_id' - id of the menu with which the submenu of
    the removed dish is associated,
    'submenu_id' - submenu id of the removed dish.
    'dish_id' - id of the dish to be deleted.
    """

    return await _control.delete_dish(
        menu_id=menu_id, submenu_id=submenu_id, id=dish_id, db=db
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
    db: AsyncSession = Depends(session),
):
    """
    Getting a certain meal.
    'menu_id' - id of the menu with which the submenu
    of this dish is associated,
    'submenu_id' - submenu id of this dish.
    'dish_id' - id of the required dish.
    """

    return await _control.get_dish(
        menu_id=menu_id, submenu_id=submenu_id, id=dish_id, db=db
    )


@router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=Dish_Data,
    summary="Update dish",
)
async def update_dish(
    data: Dish_Data,
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Updating a particular dish.
    'menu_id' - id of the menu the dish submenu is associated with,
    'submenu_id' - dish submenu id.
    'dish_id' - dish id.
    'title' - new name of the dish,
    'description' - new description of the dish,
    'price' - the new price of the dish.
    """

    return await _control.update_dish(
        data=data, menu_id=menu_id, submenu_id=submenu_id, id=dish_id, db=db
    )
