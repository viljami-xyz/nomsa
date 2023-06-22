"""
    _summary_: This file contains the routes for the books API.
    _description_: The books API allows users to create, read, update, and delete books.

    """
from fastapi import routing, Request, Depends

from app.db.models import User
from app.services.authentication import current_active_user

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/diary", tags=["diary"])

router.get("/")


@router.get("/", operation_id="diary")
async def diary(request: Request, user: User = Depends(current_active_user)):
    """diary page"""
    return templates.TemplateResponse(
        "diary/index.html", {"request": request, "user": user}
    )
