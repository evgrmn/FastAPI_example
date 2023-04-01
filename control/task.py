import json
import os.path

import fastapi as _fastapi
from celery.result import AsyncResult
from fastapi.responses import FileResponse

from database.connect import Dish, Menu, SubMenu, create_tables, db, drop_tables
from models.task import Fill, Result, Task
from queues.task import download_database


async def fill_database():
    db.close()
    drop_tables()
    create_tables()
    model_dict = {"dish": Dish, "submenu": SubMenu, "menu": Menu}
    try:
        with open("config/data.json") as f:
            menu_data = json.loads(f.read())
    except Exception:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="file not found",
        )
    for el in menu_data:
        data = model_dict[el["model"]](**el["data"])
        db.add(data)
        db.commit()
        db.refresh(data)
    db.close()
    response = Fill
    response.result = "Database filled with data"

    return Fill.from_orm(response)


async def send_task():
    task = download_database.apply_async()
    response = Task
    response.message = "Task delivered"
    response.task_id = f"{task}"

    return Task.from_orm(response)


async def task_result(task_id: str):
    task = AsyncResult(task_id)
    result = Result
    result.task_id = task_id
    result.status = task.status

    # Task not ready
    if not task.ready():
        result.result = ""

        return Result.from_orm(result)

    # Task done
    file_name = task.get()
    if os.path.isfile(f"sharefiles/{file_name}"):
        return FileResponse(
            path=f"sharefiles/{file_name}",
            filename=file_name,
            media_type="multipart/form-data",
        )
    else:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="file not found",
        )
