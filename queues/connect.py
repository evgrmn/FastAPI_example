from celery import Celery
import os

celery_app = Celery(
    "worker",
    broker="pyamqp://guest:guest@rabbit:5672//",
    backend="rpc://",
    include=["queues.task", "queues.email"],
)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # periodic task every minute
    sender.add_periodic_task(60.0, dump_dbase.s(), name="dump database")


@celery_app.task
def dump_dbase():
    os.system(
        "PGPASSWORD='password' pg_dump -h postgres -p 5432 -U postgres \
            fastapi_database > sharefiles/fastapi_database.dump"
    )
