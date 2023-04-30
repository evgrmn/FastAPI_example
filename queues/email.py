import asyncio
import smtplib
from email.message import EmailMessage

from config.config import Env

from .connect import celery_app

loop = asyncio.get_event_loop()


async def send_email_func(data: dict):
    SMTP_USER = data["address_from"]
    SMTP_PASSWORD = str(Env.SMTP_PASSWORD)
    SMTP_TO = data["address_to"]
    email = EmailMessage()
    email["Subject"] = "This is an auto submit from FastAPI_example"
    email["From"] = SMTP_USER
    email["To"] = SMTP_TO
    email.set_content("Do not reply")
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 465
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)

    return "Email sent!"


@celery_app.task
def send_email_task(data: dict):
    result = loop.run_until_complete(send_email_func(data=data))

    return result
