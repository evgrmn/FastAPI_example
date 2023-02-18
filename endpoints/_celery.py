import os.path

import fastapi as _fastapi
from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import FileResponse

import config.schemas as _schemas
import _models
from config.cel_config import celery_app

router = APIRouter()


@router.post(
    "/task",
    response_model=_schemas.Task,
    status_code=201,
    summary="Fill database with test data",
)
async def fill_database():
    """
    Выполнение задачи заполнения базы данных тестовыми данными
    """
    file_name = "Menu.xlsx"
    task = celery_app.send_task("celery_worker.task_celery", args=[file_name])

    return {"message": "Task delivered", "task_id": f"{task}"}


@router.get(
    "/result/{task_id}",
    response_model=_schemas.Result,
    status_code=200,
    summary="Get database as excel file",
)
async def task_result(task_id: str):
    """
    Получение результата задачи и запись данных в excel-файл
    """
    task = AsyncResult(task_id)

    # Task not ready
    if not task.ready():
        return {
            "task_id": str(task_id),
            "status": task.status,
            "result": "",
        }

    task_result = task.get()
    await _models.get_xlsx_menu(task_result)
    # Task done
    return {
        "task_id": str(task_id),
        "status": task.status,
        "result": f"ylab:/app/{task_result}",
    }


@router.get(
    "/download-file",
    status_code=200,
    summary="Download file",
)
async def download_file():
    """
    Скачивание excel-файл ресторанного меню
    """
    file_path = "Menu.xlsx"
    if os.path.isfile(file_path):
        return FileResponse(
            path=file_path, filename=file_path, media_type="multipart/form-data"
        )
    else:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="file not found",
        )
