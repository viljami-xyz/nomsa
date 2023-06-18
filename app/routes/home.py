""" Home page routing """

from fastapi import Request, routing
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

router = routing.APIRouter(prefix="/home", tags=["home"])


@router.get("", operation_id="home")
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("home/index.html", {"request": request})


# @router.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     """Exception handler for HTTPException with status code 404"""
#     if exc.status_code == 404:
#         return templates.TemplateResponse(
#             "errors/404.html", {"request": request}, status_code=404
#         )
#     # Handle other HTTPExceptions if needed
#     if exc.status_code == 307:
#         return templates.TemplateResponse("home/index.html", {"request": request})
#     return JSONResponse({"error": "Something went wrong"}, status_code=exc.status_code)


# @router.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     """Exception handler for RequestValidationError"""
#     return JSONResponse({"error": "Validation error"}, status_code=400)


# @router.exception_handler(StarletteHTTPException)
# async def starlette_exception_handler(request, exc):
#     """Exception handler for StarletteHTTPException"""
#     print(exc.status_code)
#     if exc.status_code == 404:
#         return templates.TemplateResponse(
#             "errors/404.html", {"request": request}, status_code=404
#         )
#     # Handle other HTTPExceptions if needed
#     return JSONResponse({"error": "Something went wrong"}, status_code=500)
