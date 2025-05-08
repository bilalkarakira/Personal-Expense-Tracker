from sqlalchemy import Integer, Float, String, Date, ForeignKey, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from backend.db import Base
from backend.transaction.models import Transaction

class MonthlyExpense(Base):
    __tablename__ = "monthly_expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    spent: Mapped[float] = mapped_column(Float, nullable=False)
    left_to_spend: Mapped[float] = mapped_column(Float, nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="monthly_expense",
        primaryjoin="and_(Transaction.monthly_expense_id==MonthlyExpense.id, "
                   "Transaction.due_date>=MonthlyExpense.start_date, "
                   "Transaction.due_date<=MonthlyExpense.end_date)"
    )