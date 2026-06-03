from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from expense_tracker.models import ExpenseCategory


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2, max_digits=12)
    category: ExpenseCategory
    description: str | None = Field(default=None, max_length=500)
    spent_on: date | None = None


class ExpenseUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2, max_digits=12)
    category: ExpenseCategory | None = None
    description: str | None = Field(default=None, max_length=500)
    spent_on: date | None = None


class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    category: ExpenseCategory
    description: str | None
    spent_on: date
    created_at: datetime


class CategoryTotal(BaseModel):
    category: ExpenseCategory
    total: Decimal
    count: int


class MonthlyReport(BaseModel):
    year: int
    month: int
    total: Decimal
    by_category: list[CategoryTotal]
