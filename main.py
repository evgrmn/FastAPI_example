from __future__ import annotations

import fastapi as _fastapi

from config.description import description
from control.user import admin_account
from database.models import create_tables
from endpoints import chat, dish, email, menu, order, submenu, task, user, html


app = _fastapi.FastAPI(
    title="FastAPI Application",
    description=description,
)


@app.on_event("startup")
async def startup_event():
    await create_tables()
    await admin_account()


app.include_router(
    task.router,
    prefix="/api/v1",
    tags=["Get menu as Excel file"],
)
app.include_router(
    email.router,
    prefix="/api/v1",
    tags=["Emails"],
)
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(order.router, prefix="/api/v1/order", tags=["Order"])
app.include_router(menu.router, prefix="/api/v1/menus", tags=["Menus"])
app.include_router(submenu.router, prefix="/api/v1/menus", tags=["Submenus"])
app.include_router(dish.router, prefix="/api/v1/menus", tags=["Dishes"])
app.include_router(chat.router, prefix="", tags=["Chat"])
app.include_router(html.router, prefix="", tags=["HTML"])
