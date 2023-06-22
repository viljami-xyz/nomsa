""" This module contains the routes for the application. """

from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

from fastapi.responses import RedirectResponse


templates = Jinja2Templates(directory="templates")


async def http_exception_handler(request, exc):
    """Exception handler for HTTPException with status code 404"""
    print("basic exception handler", exc.status_code)
    if exc.status_code == 401:
        print(request.url)
        return templates.TemplateResponse(
            "authentication/login.html",
            headers=request.headers,
            context={"request": request},
        )
    if exc.status_code == 404:
        return JSONResponse({"error": "Page not found"}, status_code=404)
    # Handle other HTTPExceptions if needed
    return JSONResponse({"error": "Something went wrong"}, status_code=exc.status_code)


async def validation_exception_handler(request, exc):
    """Exception handler for RequestValidationError"""
    print("validation exception handler", exc.status_code)
    return JSONResponse({"error": "Validation error"}, status_code=400)


async def starlette_exception_handler(request, exc):
    """Exception handler for StarletteHTTPException"""
    print("starlette exception handler", exc.status_code)
    if exc.status_code == 401:
        return RedirectResponse(
            url="/sign-in", headers=request.headers, status_code=exc.status_code
        )
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "errors/404.html", {"request": request}, status_code=404
        )
    # Handle other HTTPExceptions if needed
    return JSONResponse({"error": "Something went wrong"}, status_code=500)
