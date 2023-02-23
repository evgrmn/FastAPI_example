from __future__ import annotations

import fastapi as _fastapi

import config.description as descr
from endpoints import task, dish, menu, submenu

app = _fastapi.FastAPI(
    title="FastAPI Application",
    description=descr.description,
)

app.include_router(task.router, prefix="/api/v1", tags=["Celery task"])
app.include_router(menu.router, prefix="/api/v1/menus", tags=["Menus"])
app.include_router(submenu.router, prefix="/api/v1/menus", tags=["Submenus"])
app.include_router(dish.router, prefix="/api/v1/menus", tags=["Dishes"])
