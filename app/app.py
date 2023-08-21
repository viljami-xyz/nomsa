""" The application """


from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.db.models import User
from app.db.settings import create_db_and_tables

# in-app imports
from app.routes import authentication, home, reflections, validate
from app.routes.exception_handlers import (
    http_exception_handler,
    starlette_exception_handler,
    validation_exception_handler,
)
from app.services.authentication import (
    UserCreate,
    UserRead,
    UserUpdate,
    auth_backend,
    current_active_user,
    fastapi_users,
)

# Create the application
app = FastAPI(title="Nomsa-App", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pages
app.include_router(home.router, prefix="/home", tags=["home"])
app.include_router(authentication.router, tags=["authentication"])
app.include_router(reflections.router, tags=["reflections"])
app.include_router(validate.router, prefix="/validate", tags=["validate"])

# Authentication
app.include_router(
    fastapi_users.get_auth_router(
        auth_backend,
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.add_exception_handler(StarletteHTTPException, starlette_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/")
async def root(user: User = Depends(current_active_user)):
    """Root page"""
    if user:
        return RedirectResponse("/home")
    return RedirectResponse("/sign-in")


@app.on_event("startup")
def startup_event():
    """Create database and tables"""
    create_db_and_tables()
