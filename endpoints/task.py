from fastapi import APIRouter, Depends

import control.task as _control
from models.task import Fill, Result, Task
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import session

router = APIRouter()


@router.post(
    "/task/fill",
    response_model=Fill,
    status_code=201,
    summary="Fill database with sample data",
)
async def fill_database(
    db: AsyncSession = Depends(session),
):
    """
    Filling the database with sample data from the config/data.json file.
    """

    return await _control.fill_database(db=db)


@router.post(
    "/task/send",
    response_model=Task,
    status_code=201,
    summary="Save database data in Excel file",
)
async def send_task():
    """
    Write data to excel file. The database will be saved in the "sharefiles" folder.
    """

    return await _control.send_task()


@router.get(
    "/task/result/{task_id}",
    response_model=Result,
    status_code=200,
    summary="Get database as excel file",
)
async def task_result(task_id: str):
    """
    Download the database using celery task_id.
    """

    return await _control.task_result(task_id=task_id)
