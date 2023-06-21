""" Authentication service. """

import uuid
from typing import Optional, AsyncGenerator

from fastapi import Depends, Request, Response

from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, schemas
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.settings import async_session_maker
from app.db.models import AccessToken, User

# Database settings and connection.


SECRET = "SECRET"
cookie_transport = CookieTransport()


# Schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """User read class"""


class UserCreate(schemas.BaseUserCreate):
    """User create class"""


class UserUpdate(schemas.BaseUserUpdate):
    """User update class"""


# Dependencies


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async session"""
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Get user database"""
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    """Get access token database"""
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    """Get database strategy"""
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


# User management


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """User manager"""

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        """Actions after login"""
        print(f"User {user.id} has logged in.")
        response.headers["HX-Redirect"] = "/home"

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """Send verification email"""
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Send reset password email"""
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Send verification email"""
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    """Get user manager"""
    yield UserManager(user_db)


# FastAPI users


auth_backend = AuthenticationBackend(
    name="database",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])


current_active_user = fastapi_users.current_user(optional=True, active=True)
