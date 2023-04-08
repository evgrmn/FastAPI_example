from fastapi import APIRouter, Depends

import control.submenu as _control
from models.submenu import SubMenu, SubMenu_Data, SubMenu_Delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import session

router = APIRouter()


@router.get(
    "/{menu_id}/submenus",
    response_model=list[SubMenu],
    summary="Get submenu list",
)
async def get_submenus(
    menu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Getting a list of all submenus that are part of a specific menu.
    'menu_id' - menu id in the 'menu' table.
    """

    return await _control.get_submenus(
        menu_id=menu_id,
        db=db,
    )


@router.post(
    "/{menu_id}/submenus",
    response_model=SubMenu,
    status_code=201,
    summary="Create a new submenu",
)
async def create_submenu(
    data: SubMenu_Data,
    menu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Create a new submenu.
    'menu_id' - menu id in the 'menu' table,
    'title' - submenu title, 'description' - submenu description.
    """

    return await _control.create_submenu(data=data, menu_id=menu_id, db=db)


@router.delete(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=SubMenu_Delete,
    summary="Delete submenu",
)
async def delete_submenu(
    menu_id: int,
    submenu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Removing a specific submenu.
    'menu_id' - menu id in the 'menu' table,
    'submenu_id' - submenu id in the 'submenu' table.
    Deleting a submenu will delete all of its dishes.
    """

    return await _control.delete_submenu(menu_id=menu_id, id=submenu_id, db=db)


@router.get(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=SubMenu,
    summary="Get submenu",
)
async def get_submenu(
    menu_id: int,
    submenu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Removing a specific submenu.
    'menu_id' - menu id in the 'menu' table,
    'submenu_id' - submenu id in the 'submenu' table.
    Deleting a submenu will delete all of its dishes.
    """

    return await _control.get_submenu(menu_id=menu_id, id=submenu_id, db=db)


@router.patch(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=SubMenu_Data,
    summary="Update submenu",
)
async def update_submenu(
    data: SubMenu_Data,
    menu_id: int,
    submenu_id: int,
    db: AsyncSession = Depends(session),
):
    """
    Update a specific submenu.
    'menu_id' - id of the menu to which it is associated
    the required submenu, in the 'menu' table,
    'submenu_id' - id of the required submenu in the 'submenu' table.
    'title' - new menu title, 'description' - new menu description.
    """

    return await _control.update_submenu(
        data=data, menu_id=menu_id, id=submenu_id, db=db
    )
