import os.path

import fastapi as _fastapi
from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import FileResponse
import control.task as _control

import _models
from config.config import Const
from models.task import Task, Result

router = APIRouter()


@router.post(
    "/task",
    response_model=Task,
    status_code=201,
    summary="Fill database with test data",
)
async def fill_database():
    """
    Выполнение задачи заполнения базы данных тестовыми данными
    """

    return await _control.send_task(file_name=Const.MENU_FILE_NAME, task_name=Const.TASK_CELERY)


@router.get(
    "/result/{task_id}",
    response_model=Result,
    status_code=200,
    summary="Get database as excel file",
)
async def task_result(task_id: str):
    """
    Получение результата задачи и запись данных в excel-файл
    """
    task = AsyncResult(task_id)
    result = Result
    result.task_id = task_id
    result.status = task.status
    # Task not ready
    if not task.ready():
        result.result = ""
        return Result.from_orm(result)

    task_result = task.get()
    await _models.get_xlsx_menu(task_result)
    # Task done
    result.result = f"ylab:/app/{task_result}"
    return Result.from_orm(result)


@router.get(
    "/download-file",
    status_code=200,
    summary="Download file",
)
async def download_file():
    """
    Скачивание excel-файл ресторанного меню
    """
    if os.path.isfile(Const.MENU_FILE_NAME):
        return FileResponse(
            path=Const.MENU_FILE_NAME, 
            filename=Const.MENU_FILE_NAME, 
            media_type="multipart/form-data",
        )
    else:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="file not found",
        )
