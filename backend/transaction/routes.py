from fastapi import APIRouter, Depends
from backend.transaction.models import Transaction
from backend.db import get_async_session
from backend.user.models import current_active_user
from sqlalchemy.ext.asyncio import AsyncSession
from backend.mixin import CRUDMixin
from .schemas import TransactionCreate, TransactionResponse
from backend.user.models import User
from fastapi import HTTPException
import logging

transaction_router = APIRouter()
crud_transaction = CRUDMixin(Transaction)
logger = logging.getLogger(__name__)


@transaction_router.get("/{expense_id}")
async def get_transactions(
    expense_id: int,
    db: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    expense: Transaction = Depends(current_active_user)
):
    return await crud_transaction.get_all(db, limit=limit, expense_id=expense_id)  # Added await here


@transaction_router.post("/{monthly_expense_id}", response_model=TransactionResponse)
async def create_transaction(
    monthly_expense_id: int,
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    try:
        # Create transaction object directly
        db_transaction = Transaction(
            amount=transaction.amount,
            name=transaction.name,
            due_date=transaction.due_date,
            sub_category=transaction.sub_category,
            category=transaction.category,
            details=transaction.details,
            is_paid=transaction.is_paid,
            monthly_expense_id=monthly_expense_id
        )
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        logger.error(f"Error creating transaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@transaction_router.put("/{transaction_id}/{expense_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    expense_id: int,
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    try:
        return await crud_transaction.update(db, transaction_id, transaction, expense_id=expense_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@transaction_router.delete("/{transaction_id}/{expense_id}", response_model=TransactionResponse)
async def delete_transaction(
    transaction_id: int,
    expense_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    try:
        return await crud_transaction.delete(db, transaction_id, expense_id=expense_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))