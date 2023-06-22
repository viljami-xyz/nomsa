"""
    Routes for login
"""

from fastapi import routing, Request, Response, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

import httpx

from app.db.models import User
from app.services.authentication import current_active_user

templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(tags=["login", "register"])


@router.get("/login")
def login(request: Request):
    """Login a user"""
    return templates.TemplateResponse("authentication/login.html", {"request": request})


@router.get("/register")
def register(request: Request):
    """Register a user page"""
    return templates.TemplateResponse(
        "authentication/register.html", {"request": request}
    )


@router.get("/logging-out")
async def logout(
    request: Request, response: Response, user: User = Depends(current_active_user)
):
    """Logout a user"""
    if user:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                str(request.base_url) + "auth/logout", headers=request.headers
            )
    return RedirectResponse("/login", headers=response.headers)
