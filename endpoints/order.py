from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import control.order as _control
from control.user import get_current_user
from database.connect import session
from models.order import Order, Order_Delete
from models.user import User

router = APIRouter()


@router.get(
    "/orders",
    response_model=list[Order],
    status_code=200,
    summary="Get a list of user's orders",
)
async def get_order_list(
    db: AsyncSession = Depends(session),
    user: User = Depends(get_current_user),
):
    """
    Get a list of user's orders
    """

    return await _control.get_order_list(db=db, user=user)


@router.post(
    "/new/{dish_id}/{quantity}",
    response_model=Order,
    status_code=201,
    summary="Manage order",
)
async def manage_order(
    dish_id: int,
    quantity: int,
    db: AsyncSession = Depends(session),
    user: User = Depends(get_current_user),
):
    """
    Create a new user order or manage an existing order. Quantity variable
    can be negative. If it returns a quantity less than zero, it means that
    the order has been deleted
    """

    return await _control.manage_order(
        dish_id=dish_id,
        quantity=quantity,
        db=db,
        user=user,
    )


@router.delete(
    "/delete/{order_id}",
    response_model=Order_Delete,
    status_code=200,
    summary="Delete order",
)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(session),
    user: User = Depends(get_current_user),
):
    """
    Delete an existing order
    """

    return await _control.delete_order(
        id=order_id,
        db=db,
        user=user,
    )


@router.get(
    "/order/{dish_id}",
    response_model=Order,
    status_code=200,
    summary="Get order",
)
async def get_order(
    dish_id: int,
    db: AsyncSession = Depends(session),
    user: User = Depends(get_current_user),
):
    """
    Get order by dish_id and user_id
    """

    return await _control.get_order(
        dish_id=dish_id,
        db=db,
        user=user,
    )
