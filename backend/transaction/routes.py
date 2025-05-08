from fastapi import APIRouter, Depends
from backend.transaction.models import Transaction
from backend.db import get_async_session
from backend.user.models import current_active_user
from sqlalchemy.ext.asyncio import AsyncSession
from backend.mixin import CRUDMixin
from .schemas import TransactionCreate, TransactionResponse
from backend.user.models import User
from fastapi import HTTPException

transaction_router = APIRouter()
crud_transaction = CRUDMixin(Transaction)


@transaction_router.get("/{expense_id}")
async def get_transactions(
    expense_id: int,
    db: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    expense: Transaction = Depends(current_active_user)
):
    return await crud_transaction.get_all(db, limit=limit, expense_id=expense_id)  # Added await here


@transaction_router.post("/{expense_id}", response_model=TransactionResponse)
async def create_transaction(
    expense_id: int,
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    try:
        return await crud_transaction.create(db, transaction, expense_id=expense_id)
    except Exception as e:
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