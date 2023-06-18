""" The application """


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# in-app imports
from app.routes import authentication, home, books, diary, reflections
from app.db.settings import create_db_and_tables
from app.services.authentication import (
    UserCreate,
    UserRead,
    UserUpdate,
    fastapi_users,
    auth_backend,
)

# Create the application
app = FastAPI(title="Nomsa App", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pages
app.include_router(home.router)
app.include_router(authentication.router)
app.include_router(books.router)
app.include_router(diary.router)
app.include_router(reflections.router)

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
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/cookie",
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


@app.on_event("startup")
async def startup_event():
    """Create database and tables"""
    await create_db_and_tables()
