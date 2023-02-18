from fastapi import APIRouter

from models.submenu import Data, Delete, SubMenu
import control.submenu as _control

router = APIRouter()


@router.get(
    "/{menu_id}/submenus",
    response_model=list[SubMenu],
    summary="Get submenu list",
)
async def get_submenus(
    menu_id: int,
):
    """
    Получение списка всех подменю, которые входят в состав определенного меню.
    'menu_id' - id меню в таблице 'menu'.
    """

    return await _control.get_submenus(
        menu_id=menu_id,
    )


@router.post(
    "/{menu_id}/submenus",
    response_model=SubMenu,
    status_code=201,
    summary="Create a new submenu",
)
async def create_submenu(
    data: Data,
    menu_id: int,
):
    """
    Создание нового подменю.
    'menu_id' - id меню в таблице 'menu',
    'title' - название подменю, 'description' - описание подменю
    """

    return await _control.create_submenu(data=data, menu_id=menu_id)


@router.delete(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=Delete,
    summary="Delete submenu",
)
async def delete_submenu(
    menu_id: int,
    submenu_id: int,
):
    """
    Удаление определенного подменю.
    'menu_id' - id меню в таблице 'menu',
    'submenu_id' - id подменю в таблице 'submenu'.
    Удаление подменю удалит все его блюда.
    """

    return await _control.delete_submenu(
        menu_id=menu_id,
        id=submenu_id,
    )


@router.get(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=SubMenu,
    summary="Get submenu",
)
async def get_submenu(
    menu_id: int,
    submenu_id: int,
):
    """
    Получение определенного подменю.
    'menu_id' - id меню, с которым связано
    требуемое подменю, в таблице 'menu',
    'submenu_id' - id требуемого подменю в таблице 'submenu'.
    """

    return await _control.get_submenu(
        menu_id=menu_id,
        id=submenu_id,
    )


@router.patch(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=Data,
    summary="Update submenu",
)
async def update_submenu(
    data: Data,
    menu_id: int,
    submenu_id: int,
):
    """
    Обновление определенного подменю.
    'menu_id' - id меню, с которым связано
    требуемое подменю, в таблице 'menu',
    'submenu_id' - id требуемого подменю в таблице 'submenu'.
    'title' - новое название поменю, 'description' - новое описание меню
    """

    return await _control.update_submenu(
        data=data,
        id=submenu_id,
    )
