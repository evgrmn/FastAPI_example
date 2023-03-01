from fastapi import APIRouter

import control.task as _control
from models.task import Fill, Result, Task

router = APIRouter()


@router.post(
    "/task/fill",
    response_model=Fill,
    status_code=201,
    summary="Fill database with test data",
)
async def fill_database():
    """
    Filling the database with test data from the config/data.json file.
    """

    return await _control.fill_database()


@router.post(
    "/task/send",
    response_model=Task,
    status_code=201,
    summary="Save database data in excel file",
)
async def send_task():
    """
    Write data to excel file. The database will be saved in the "sharefiles" folder.
    """

    return await _control.send_task()


@router.get(
    "/result/task/{task_id}",
    response_model=Result,
    status_code=200,
    summary="Get database as excel file",
)
async def task_result(task_id: str):
    """
    Download the database using celery task_id.
    """

    return await _control.task_result(task_id=task_id)
