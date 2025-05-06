from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database import get_async_session
from backend.auth.models import User

router = APIRouter()

@router.get("/users")
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/users/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @router.get("/protected-route")
# async def protected_route(user: User = Depends(fastapi_users.current_user())):
#     return {"message": f"Hello {user.email}!"}
