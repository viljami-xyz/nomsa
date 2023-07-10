"""
    Routes for login
"""

from fastapi import routing, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.db.models import User
from app.services.authentication import fastapi_users


templates = Jinja2Templates(directory="templates")

router = routing.APIRouter()
current_active_user = fastapi_users.current_user(optional=True)


@router.get("/login")
def login(request: Request, user: User = Depends(current_active_user)):
    """Login a user"""
    if user:
        return RedirectResponse("/")
    return templates.TemplateResponse("authentication/login.html", {"request": request})


@router.get("/register")
def register(request: Request, user: User = Depends(current_active_user)):
    """Register a user page"""
    if user:
        return RedirectResponse("/")
    return templates.TemplateResponse(
        "authentication/register.html", {"request": request}
    )
