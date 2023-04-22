from celery.result import AsyncResult

from models.email import Email, Result, Email_list
from queues.email import send_email_task
from caching import functions as cache
from datetime import datetime


async def send_email(data: Email):
    data = data.dict()
    task = send_email_task.apply_async([data])
    key_name = f"email_task_{task}"
    data['status'] = 'PENDING'
    data['task_id'] = f'{task}'
    data['timestamp'] = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
    await cache.set(key_name, data)
    response = Result
    response.result = "Email sent!"

    return Result.from_orm(response)


async def email_list():
    key_list = await cache.keys('email_task')
    response = []
    tmp = {}
    for num, key in enumerate(key_list):
        res = await cache.get(key)
        task = AsyncResult(res['task_id'])
        if res['status'] == 'SUCCESS':
            pass
        elif task.status == 'SUCCESS':
            res['status'] = 'SUCCESS'
            key_name = key
            await cache.set(key_name, res)
        tmp[num] = Email_list(**res)
        response.append(tmp[num])

    return list(map(Email_list.from_orm, response))
