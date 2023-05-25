from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

TEMPLATES = Jinja2Templates(directory=str("templates"))

router = APIRouter()


@router.get("/")
async def get(request: Request):
    return TEMPLATES.TemplateResponse(
        "drop_menu.html",
        {"request": request},
    )