import fastapi as _fastapi

import database.models as table
from caching import functions as cache
from models.user import User
from models.order import Order, Order_Delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import session
import sqlalchemy as _sql
import json


async def get_order_list(db: AsyncSession, user: User):
    key_name = f"Order_list_User_{user['id']}"
    order_list = await cache.get(key_name)
    if order_list:
        return json.loads(order_list)
    order_list = await db.execute(_sql.select(table.Order).filter_by(user_id=user['id']))
    order_list = list(map(lambda x: Order.from_orm(x).dict(), order_list.scalars().all()))
    await cache.set(key_name, order_list)

    return order_list


async def manage_order(dish_id: int, quantity: int, db: AsyncSession, user: User):
    all_dish_list = await cache.get(f"All_Dish")
    if all_dish_list:
        if dish_id not in all_dish_list:
            raise _fastapi.HTTPException(status_code=404, detail="dish not found")
    else:
        all_dish_list = _sql.select(table.Dish.id)
        all_dish_list = await db.execute(all_dish_list)
        all_dish_list = all_dish_list.fetchall()
        all_dish_list = list(map(lambda x: x[0], all_dish_list))
        await cache.set(f"All_Dish", all_dish_list)
    key_name = f"Order_User_{user['id']}_Dish_{dish_id}"
    order = await db.execute(_sql.select(table.Order).filter_by(user_id=user['id'], dish_id=dish_id))
    order = order.scalars().first()
    if not order:
        if quantity <= 0:
            raise _fastapi.HTTPException(status_code=400, detail="the number of dishes ordered must be greater than zero")
        order = table.Order(dish_id=dish_id, user_id=user['id'], quantity=quantity)
        db.add(order)
        await db.commit()
        await cache.set(key_name, Order.from_orm(order).dict())
    else:
        order.quantity += quantity
        if order.quantity <= 0:            
            try:
                await db.delete(order)
                await db.commit()
            except:
                raise _fastapi.HTTPException(status_code=400, detail="order not found")
            await cache.delete(key_name)
        else:
            await db.commit()
            await cache.set(key_name, Order.from_orm(order).dict())
    await cache.delete(f"Order_list_User_{user['id']}")

    return  order


async def delete_order(id: int, db: AsyncSession, user: User):
    order = await db.execute(_sql.select(table.Order).filter_by(id=id))
    order = order.scalars().first()
    if not order:
        raise _fastapi.HTTPException(status_code=404, detail="order not found")
    await cache.delete(f"Order_User_{user['id']}_Dish_{order.dish_id}")
    await db.delete(order)
    await db.commit()    
    await cache.delete(f"Order_list_User_{user['id']}")
    response = Order_Delete
    response.status = True
    response.message = "Order has been deleted"

    return Order_Delete.from_orm(response)


async def get_order(dish_id: int, db: AsyncSession, user: User):
    key_name = f"Order_User_{user['id']}_Dish_{dish_id}"
    order = await cache.get(key_name)
    if order:
        return order
    req = _sql.select(table.Order).filter_by(dish_id=dish_id, user_id=user['id'])
    order = await db.execute(req)
    order = order.scalars().first()
    if not order:
        raise _fastapi.HTTPException(status_code=404, detail="Order not found")
    order = Order.from_orm(order)
    await cache.set(key_name, order.dict())

    return order
    

    

    
