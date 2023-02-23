from config.cel_config import celery_app
from models.task import Task, Result

    
async def send_task(file_name: str, task_name: str):
    task = celery_app.send_task(
        task_name, args=[file_name]
    )
    response = Task
    response.message = "Task delivered"
    response.task_id = f"{task}"

    return Task.from_orm(response)