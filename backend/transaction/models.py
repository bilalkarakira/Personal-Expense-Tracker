from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.db import Base
from sqlalchemy import Integer, Float, String, Date, Boolean, ForeignKey
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.expense.models import MonthlyExpense

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[float] = mapped_column(Float)
    name: Mapped[str] = mapped_column(String)
    due_date: Mapped[date] = mapped_column(Date)
    sub_category: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    details: Mapped[str] = mapped_column(String)
    is_paid: Mapped[bool] = mapped_column(Boolean)
    monthly_expense_id: Mapped[int] = mapped_column(Integer, ForeignKey("monthly_expenses.id"))
    monthly_expense: Mapped["MonthlyExpense"] = relationship("MonthlyExpense", back_populates="transactions")
