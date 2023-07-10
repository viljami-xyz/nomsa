""" Home page routing """

from fastapi import Request, routing, Depends
from fastapi.templating import Jinja2Templates

from app.db.models import User
from app.services.authentication import current_active_user

templates = Jinja2Templates(directory="templates")

router = routing.APIRouter()


@router.get("/", operation_id="home")
async def home(request: Request, user: User = Depends(current_active_user)):
    """Home page"""
    return templates.TemplateResponse(
        "home/index.html", {"request": request, "user": user}
    )
