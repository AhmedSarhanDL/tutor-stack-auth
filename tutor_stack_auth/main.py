"""Main FastAPI application for the auth service"""

import os
import uuid
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users.manager import UserManagerDependency
from httpx_oauth.clients.google import GoogleOAuth2

from .models import User, OAuthAccount
from .database import engine, Base
from .auth import get_jwt_strategy, get_user_db, get_user_manager
from .schemas import UserRead, UserCreate, UserUpdate

# Create FastAPI app
app = FastAPI(
    title="Tutor Stack Auth Service",
    description="Authentication service with JWT and OAuth support",
    version="1.0.0"
)

# Create bearer transport
bearer_transport = BearerTransport(tokenUrl="jwt/login")

# Create authentication backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Initialize FastAPI Users
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# Get current user dependency
current_active_user = fastapi_users.current_user(active=True)

# Include routers
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    google_oauth_client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    
    # Get the private key for OAuth
    try:
        with open(os.getenv("SECRET_PRIVATE_KEY_PATH", "/keys/jwtRS256.key"), "r") as f:
            secret = f.read()
    except FileNotFoundError:
        secret = "dev-secret-key-change-in-production"
    
    app.include_router(
        fastapi_users.get_oauth_router(
            google_oauth_client,
            auth_backend,
            secret
        ),
        prefix="/google",
        tags=["auth"]
    )


@app.on_event("startup")
async def startup():
    """Create database tables on startup"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Tutor Stack Auth Service",
        "endpoints": {
            "jwt_login": "/jwt/login",
            "jwt_logout": "/jwt/logout",
            "register": "/register",
            "users": "/users/me",
            "google_oauth": "/google/authorize" if GOOGLE_CLIENT_ID else None
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth"} 