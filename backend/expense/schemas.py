from pydantic import BaseModel, Field
from datetime import date
from backend.transaction.schemas import TransactionResponse
from typing import Optional
class MonthlyExpenseCreate(BaseModel):
    start_date: date
    end_date: date
    budget: float
    spent: Optional[float] = None
    left_to_spend: Optional[float] = None

class MonthlyExpenseResponse(BaseModel):
    id: int
    start_date: date
    end_date: date
    budget: float
    spent: float
    left_to_spend: float
    transactions: list[TransactionResponse]