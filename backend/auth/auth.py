import uuid
import secrets

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from backend.auth.userManager import get_user_manager

from .models import User
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

print(secrets.token_hex(32)) 
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret="your-secret-key", lifetime_seconds=3600)  # Change this secret!

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)