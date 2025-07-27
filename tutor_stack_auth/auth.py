"""Authentication configuration for the auth service"""

import os
from fastapi_users.authentication import JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .database import async_session_maker
from fastapi_users.manager import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from .schemas import UserCreate
from typing import Optional
import uuid

# JWT Configuration
SECRET_PRIVATE_KEY_PATH = os.getenv("SECRET_PRIVATE_KEY_PATH", "/keys/jwtRS256.key")
SECRET_PUBLIC_KEY_PATH = os.getenv("SECRET_PUBLIC_KEY_PATH", "/keys/jwtRS256.key.pub")

SECRET = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[object] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[object] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Optional[object] = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


def get_jwt_strategy() -> JWTStrategy:
    """Get JWT strategy with RS256 algorithm"""
    try:
        with open(SECRET_PRIVATE_KEY_PATH, "r") as f:
            secret = f.read()
    except FileNotFoundError:
        # Fallback for development
        secret = "dev-secret-key-change-in-production"
    
    return JWTStrategy(
        secret=secret,
        algorithm="RS256",
        lifetime_seconds=3600  # 1 hour
    )


async def get_user_db() -> SQLAlchemyUserDatabase:
    """Get user database adapter"""
    async with async_session_maker() as session:
        yield SQLAlchemyUserDatabase(session, User) 

async def get_user_manager():
    async for user_db in get_user_db():
        yield UserManager(user_db) 