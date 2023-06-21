"""
    Routes for login
"""

from fastapi import routing, Request, Response, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import httpx

from app.db.models import User
from app.services.authentication import current_active_user

templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/sign", tags=["login"])


@router.get("-in")
def login(request: Request, user: User = Depends(current_active_user)):
    """Login a user"""
    if user:
        return RedirectResponse("/home", headers=request.headers)
    return templates.TemplateResponse("authentication/login.html", {"request": request})


@router.get("-up")
def register(request: Request):
    """Register a user page"""
    return templates.TemplateResponse(
        "authentication/register.html", {"request": request}
    )


@router.get("-out")
async def logout(
    request: Request,
    response: Response,
):
    """Logout a user"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            str(request.base_url) + "auth/logout", headers=request.headers
        )
    return RedirectResponse("/sign-in", headers=response.headers)
