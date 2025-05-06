from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base
from sqlalchemy import Integer, Float, String

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String)
