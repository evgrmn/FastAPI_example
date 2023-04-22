from fastapi import APIRouter

import control.email as _control
from models.email import Email, Result, Email_list


router = APIRouter()


@router.post(
    "/email",
    response_model=Result,
    status_code=201,
    summary="Send an email",
)
async def task_result(data: Email):
    """
    Send an email using Gmail platform. For more information see 'Check Gmail
    through other email platforms'
    https://support.google.com/mail/answer/7126229?hl=en - Get app password -
    https://support.google.com/accounts/answer/185833?hl=en - Change
    SMTP_EMAIL_ADDRESS and SMTP_PASSWORD in .env file to your actual data
    """

    return await _control.send_email(data=data)


@router.get(
    "/email",
    response_model=list[Email_list],
    status_code=200,
    summary="Get a list of sent emails",
)
async def get_email_list():
    """
    The list of sent email messages is stored in the Redis database
    """

    return await _control.email_list()
