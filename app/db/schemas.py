""" Database schemas """


import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """User read class"""


class UserCreate(schemas.BaseUserCreate):
    """User create class"""


class UserUpdate(schemas.BaseUserUpdate):
    """User update class"""
