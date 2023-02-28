from celery import Celery


celery_app = Celery(
    "worker",
    broker="pyamqp://guest:guest@rabbit:5672//",
    backend="rpc://",
    include=['queues.task'],
)

if __name__ == '__main__':
    celery_app.start()