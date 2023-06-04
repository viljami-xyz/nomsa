"""
    _summary_: This file contains the routes for the reflections API.
    _description_: The reflections API allows users to create, read, update, and delete reflections.

    """
from fastapi import routing, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


router = routing.APIRouter(prefix="/reflections", tags=["reflections"])


@router.get("/", operation_id="reflections")
async def reflections(request: Request):
    """reflections page"""
    return templates.TemplateResponse("reflections/index.html", {"request": request})
