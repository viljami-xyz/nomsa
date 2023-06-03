""" Home page routing """

from fastapi import Request, FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

templates = Jinja2Templates(directory="templates")

app = FastAPI(prefix="/", tags=["home"])

@app.get("/")
async def home(request: Request):
    """ Home page """
    return templates.TemplateResponse("home/index.html", {"request":request})



@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Exception handler for HTTPException with status code 404"""
    if exc.status_code == 404:
        return templates.TemplateResponse("errors/404.html", {"request":request}, status_code=404)
    # Handle other HTTPExceptions if needed
    if exc.status_code == 307:
        return templates.TemplateResponse("home/index.html", {"request":request})
    return JSONResponse({"error": "Something went wrong"}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Exception handler for RequestValidationError"""
    return JSONResponse({"error": "Validation error"}, status_code=400)

@app.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(request, exc):
    """ Exception handler for StarletteHTTPException
    """
    print(exc.status_code)
    if exc.status_code == 404:
        return templates.TemplateResponse("errors/404.html", {"request":request}, status_code=404)
    # Handle other HTTPExceptions if needed
    return JSONResponse({"error": "Something went wrong"}, status_code=500)

