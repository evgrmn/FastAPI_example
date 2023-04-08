from __future__ import annotations

import fastapi as _fastapi

import config.description as descr
from endpoints import dish, menu, submenu, task
from database.models import create_tables

app = _fastapi.FastAPI(
    title="FastAPI Application",
    description=descr.description,
)


@app.on_event("startup")
async def startup_event():
    await create_tables()


app.include_router(
    task.router,
    prefix="/api/v1",
    tags=["Fill in the database anddownload the menu"],
)
app.include_router(menu.router, prefix="/api/v1/menus", tags=["Menus"])
app.include_router(submenu.router, prefix="/api/v1/menus", tags=["Submenus"])
app.include_router(dish.router, prefix="/api/v1/menus", tags=["Dishes"])
