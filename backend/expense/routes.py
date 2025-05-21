import logging

from fastapi import APIRouter, Depends
from backend.expense.models import MonthlyExpense
from backend.db import get_async_session
from backend.user.models import current_active_user
from sqlalchemy.ext.asyncio import AsyncSession
from backend.mixin import CRUDMixin
from .schemas import MonthlyExpenseCreate, MonthlyExpenseResponse
from backend.user.models import User
from fastapi import HTTPException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

expense_router = APIRouter()
crud_expense = CRUDMixin(MonthlyExpense)


@expense_router.get("")
async def get_expenses(
    db: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    expense: MonthlyExpense = Depends(current_active_user)
):
    return await crud_expense.get_all(db, limit=limit)


@expense_router.get("/{expense_id}")
async def get_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_async_session),
    expense: MonthlyExpense = Depends(current_active_user)
):
    return await crud_expense.get_by_id(db, expense_id)

@expense_router.post("", response_model=MonthlyExpenseResponse)
async def create_expense(
    expense: MonthlyExpenseCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    try:
        logger.info(f"Creating expense: {expense}")
        # Create dictionary first
        expense_data = expense.model_dump()
        logger.info(f"Creating expense dict: {expense_data}")
        # Then modify the dictionary
        expense_data["spent"] = 0
        expense_data["left_to_spend"] = expense_data["budget"]
        logger.info(f"Creating expense dict: {expense_data}")
        db_expense = MonthlyExpense(**expense_data)
        db.add(db_expense)
        await db.commit()
        await db.refresh(db_expense)
        return db_expense
    except Exception as e:
        logger.error(f"Error creating expense: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    