"""
    Routes for login
"""

from fastapi import routing, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/sign", tags=["login"])


@router.get("-in")
def login(request: Request):
    """Login a user"""
    return templates.TemplateResponse("authentication/login.html", {"request": request})


@router.get("-up")
def register(request: Request):
    """Register a user page"""
    return templates.TemplateResponse(
        "authentication/register.html", {"request": request}
    )
