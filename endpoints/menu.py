from fastapi import APIRouter

import control.menu as _control
from models.menu import Menu, Menu_Data, Menu_Delete

router = APIRouter()


@router.get(
    "/",
    response_model=list[Menu],
    summary="Get menu list",
)
async def get_menus():
    """
    Getting a menu list.
    """

    return await _control.get_menus()


@router.post(
    "/",
    response_model=Menu,
    status_code=201,
    summary="Create a new menu",
)
async def create_menu(
    data: Menu_Data,
):
    """
    Menu creation. 'title' - menu title, 'description' - menu description.
    """

    return await _control.create_menu(data=data)


@router.delete(
    "/{menu_id}",
    response_model=Menu_Delete,
    summary="Delete menu",
)
async def delete_menu(
    menu_id: int,
):
    """
    Removing a menu. 'menu_id' - id in the 'menu' table.
    Deleting a menu will delete all submenus and dishes associated with it.
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
    Get a specific menu. 'menu_id' - menu id in table 'menu'.
    """

    return await _control.get_menu(
        id=menu_id,
    )


@router.patch(
    "/{menu_id}",
    response_model=Menu_Data,
    summary="Update menu",
)
async def update_menu(
    data: Menu_Data,
    menu_id: int,
):
    """
    Update a specific menu.
    'menu_id' - id in the 'menu' table,
    'title' - menu title, 'description' - menu description.
    """

    return await _control.update_menu(
        data=data,
        id=menu_id,
    )
