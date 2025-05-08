from pydantic import BaseModel
from datetime import date

class TransactionCreate(BaseModel):
    due_date: date
    amount: float
    sub_category: str
    category: str
    details: str
    is_paid: bool = False
    name: str

class TransactionResponse(BaseModel):
    id: int
    due_date: date
    amount: float
    sub_category: str
    category: str
    details: str
    is_paid: bool
    name: str