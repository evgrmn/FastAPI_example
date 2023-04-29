from __future__ import annotations

import fastapi as _fastapi

from config.description import description
from endpoints import dish, menu, submenu, task, email, user, order
from database.models import create_tables

app = _fastapi.FastAPI(
    title="FastAPI Application",
    description=description,
)


@app.on_event("startup")
async def startup_event():
    await create_tables()


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
