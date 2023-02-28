import fastapi as _fastapi
from models.task import Task, Result
import os.path
from fastapi.responses import FileResponse
from celery.result import AsyncResult
import json
from queues.task import download_database
from database.connect import db, Menu, SubMenu, Dish
from sqlalchemy.sql import text


async def fill_database():
    model_dict = {"dish": Dish, "submenu": SubMenu, "menu": Menu}
    for table_name, model in model_dict.items():
        db.query(model).delete()
        db.execute(text(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1"))
        db.commit()
    try:
        with open('config/data.json') as f:
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

    return {"result": "Database filled with data"}


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

