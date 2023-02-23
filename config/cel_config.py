import asyncio
from celery import Celery
import _models
from config.config import Const
import json

celery_app = Celery(
    "worker",
    broker_url="amqp://guest:guest@rabbit:5672//",
    result_backend="rpc://",
)
celery_app.conf.task_routes = {Const.TASK_CELERY: "test-queue"}
celery_app.conf.update(task_track_started=True)


@celery_app.task(name=Const.TASK_CELERY)
def task_celery(file_name):
    for el in _models.delete_model_dict:
        asyncio.run(_models.delete_table_data(el[1], el[0]))
    with open('config/data.json') as f:
        menu_data = json.loads(f.read())
    for el in menu_data:
        par = _models.model_dict[el["model"]](**el["data"])
        asyncio.run(_models.add_instance(par))

    return file_name
