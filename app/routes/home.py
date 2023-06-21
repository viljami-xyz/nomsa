""" Home page routing """

from fastapi import Request, routing
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/home", tags=["home"])


@router.get("", operation_id="home")
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("home/index.html", {"request": request})
