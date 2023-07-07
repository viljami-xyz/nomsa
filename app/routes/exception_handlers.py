""" This module contains the routes for the application. """


from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse


templates = Jinja2Templates(directory="templates")


async def http_exception_handler(request: Request, exc):
    """Exception handler for HTTPException with status code 404"""
    if exc.status_code == 401:
        return templates.TemplateResponse(
            "authentication/login.html",
            context={"request": request},
            status_code=exc.status_code,
            headers={"HX-Redirect": "/login"},
        )
    if exc.status_code == 404:
        return JSONResponse({"error": "Page not found"}, status_code=404)
    # Handle other HTTPExceptions if needed
    return JSONResponse({"error": "Something went wrong"}, status_code=exc.status_code)


async def starlette_exception_handler(request, exc):
    """Exception handler for StarletteHTTPException"""
    if exc.status_code == 401:
        return templates.TemplateResponse(
            "authentication/login.html",
            {"request": request},
            status_code=exc.status_code,
            headers={"HX-Target": "body"},
        )
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "errors/404.html", {"request": request}, status_code=404
        )
    # Handle other HTTPExceptions if needed
    return JSONResponse({"error": "Something went wrong"}, status_code=500)


async def validation_exception_handler(request, exc):
    """Exception handler for RequestValidationError"""
    error_messages = []
    for error in exc.errors():
        error_messages.append({"field": error["loc"][0], "message": error["msg"]})

    return JSONResponse(status_code=400, content={"detail": error_messages})
