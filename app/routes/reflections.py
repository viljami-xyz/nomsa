"""
    _summary_: This file contains the routes for the reflections API.
    _description_: The reflections API allows users to create, read, update, and delete reflections.

    """
from fastapi import routing, Request, Form
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


router = routing.APIRouter(prefix="/reflections", tags=["reflections"])


@router.get("/", operation_id="reflections")
async def reflections(request: Request):
    """reflections page"""
    return templates.TemplateResponse("reflections/index.html", {"request": request})


@router.post("/new")
async def new_reflection(
    request: Request,
    good: str = Form(...),
    smile: str = Form(...),
    other: str = Form(...),
):
    """Insert new reflection into database"""
    print(good, smile, other)
    return {"message": "New reflection created successfully."}
