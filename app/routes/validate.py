"""
    Routes for data validation
"""

from fastapi import routing, Request, Form
from fastapi.templating import Jinja2Templates

from pydantic import EmailStr
from pydantic.errors import EmailError

templates = Jinja2Templates(directory="templates")

router = routing.APIRouter()


@router.post("/email")
async def validate_email(
    request: Request, email: str = Form(..., title="Email address")
):
    """Validate user input"""
    try:
        EmailStr.validate(email)
    except EmailError:
        return "Invalid input"
    return "Valid input"


@router.post("/password")
async def validate_password(
    request: Request, password: str = Form(..., title="Password")
):
    """Validate user input"""
    if len(password) < 8:
        return "Password must be at least 8 characters"
    return "Valid input"


@router.post("/password-confirm")
async def validate_password_match(
    request: Request,
    password: str = Form(..., title="Password"),
    password_confirm: str = Form(..., title="Password again"),
):
    """Validate user input"""
    if password != password_confirm:
        return "Passwords do not match"
    return "Valid input"


@router.post("/all")
async def validate_all(request: Request, email: str = Form(..., title="Email address")):
    """Validate user input"""
    try:
        EmailStr.validate(email)
    except EmailError:
        return "Invalid input"
    return "Valid input"
