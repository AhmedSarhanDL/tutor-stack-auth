"""User schemas for FastAPI Users"""

from typing import Optional
from fastapi_users import schemas
import uuid


class UserRead(schemas.BaseUser[uuid.UUID]):
    """User read schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "student"


class UserCreate(schemas.BaseUserCreate):
    """User create schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "student"


class UserUpdate(schemas.BaseUserUpdate):
    """User update schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None 