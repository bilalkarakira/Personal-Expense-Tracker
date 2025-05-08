import uvicorn
from fastapi import Depends, FastAPI

from backend.db import User, create_db_and_tables
from backend.auth.schemas import UserCreate, UserRead, UserUpdate
from backend.user.models import auth_backend, current_active_user, fastapi_users
from backend.transaction.routes import transaction_router
from backend.expense.routes import expense_router
app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
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

app.include_router(
    transaction_router,
    prefix="/transactions",
    tags=["transactions"],
)

app.include_router(
    expense_router,
    prefix="/expenses",
    tags=["expenses"],
)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", log_level="info")