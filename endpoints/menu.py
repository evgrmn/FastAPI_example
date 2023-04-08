from fastapi import APIRouter, Depends

import control.menu as _control
from models.menu import Menu, Menu_Data, Menu_Delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import session


router = APIRouter()


@router.get(
    "/",
    response_model=list[Menu],
    summary="Get menu list",
)
async def get_menus(
    db: AsyncSession = Depends(session),
):
    """
    Getting a menu list.
    """

    return await _control.get_menus(
        db=db,
    )


@router.post(
    "/",
    response_model=Menu,
    status_code=201,
    summary="Create a new menu",
)
async def create_menu(
    data: Menu_Data,
    db: AsyncSession = Depends(session),
):
    """
    Menu creation. 'title' - menu title, 'description' - menu description.
    """

    return await _control.create_menu(
        data=data,
        db=db,
    )


@router.delete(
    "/{menu_id}",
    response_model=Menu_Delete,
    summary="Delete menu",
)
async def delete_menu(
    menu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Removing a menu. 'menu_id' - id in the 'menu' table.
    Deleting a menu will delete all submenus and dishes associated with it.
    """

    return await _control.delete_menu(
        id=menu_id,
        db=db,
    )


@router.get(
    "/{menu_id}",
    response_model=Menu,
    summary="Get menu",
)
async def get_menu(
    menu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Get a specific menu. 'menu_id' - menu id in table 'menu'.
    """

    return await _control.get_menu(
        id=menu_id,
        db=db,
    )


@router.patch(
    "/{menu_id}",
    response_model=Menu_Data,
    summary="Update menu",
)
async def update_menu(
    data: Menu_Data,
    menu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Update a specific menu.
    'menu_id' - id in the 'menu' table,
    'title' - menu title, 'description' - menu description.
    """

    return await _control.update_menu(data=data, id=menu_id, db=db)
