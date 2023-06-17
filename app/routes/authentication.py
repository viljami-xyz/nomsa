"""
    Routes for login
"""

from fastapi import routing, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any


templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/login", tags=["login"])


@router.get("")
def login(request: Request):
    """Login a user"""
    return templates.TemplateResponse("authentication/index.html", {"request": request})
