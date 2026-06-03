from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import Date, DateTime, Enum, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from expense_tracker.database import Base


class ExpenseCategory(StrEnum):
    food = "food"
    transport = "transport"
    housing = "housing"
    entertainment = "entertainment"
    health = "health"
    shopping = "shopping"
    other = "other"


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    category: Mapped[ExpenseCategory] = mapped_column(
        Enum(ExpenseCategory, native_enum=False, length=32),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    spent_on: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
