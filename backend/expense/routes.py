from fastapi import APIRouter, Depends
from backend.expense.models import Expense
from backend.db import get_async_session
from backend.user.models import current_active_user
from sqlalchemy.ext.asyncio import AsyncSession
from backend.mixin import CRUDMixin
expense_router = APIRouter()
crud_expense = CRUDMixin(Expense)


@expense_router.get("")
async def get_expenses(
    db: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    expense: Expense = Depends(current_active_user)
):
    return await crud_expense.get_all(db, limit=limit)  # Added await here