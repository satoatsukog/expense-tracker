from datetime import date
from decimal import Decimal

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from expense_tracker.models import Expense, ExpenseCategory
from expense_tracker.schemas import CategoryTotal, ExpenseCreate, ExpenseUpdate, MonthlyReport


def create_expense(db: Session, data: ExpenseCreate) -> Expense:
    spent_on = data.spent_on or date.today()
    expense = Expense(
        amount=data.amount,
        category=data.category,
        description=data.description,
        spent_on=spent_on,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expense(db: Session, expense_id: int) -> Expense | None:
    return db.get(Expense, expense_id)


def list_expenses(
    db: Session,
    *,
    date_from: date | None = None,
    date_to: date | None = None,
    category: ExpenseCategory | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Expense]:
    stmt: Select[tuple[Expense]] = select(Expense).order_by(
        Expense.spent_on.desc(),
        Expense.id.desc(),
    )
    if date_from is not None:
        stmt = stmt.where(Expense.spent_on >= date_from)
    if date_to is not None:
        stmt = stmt.where(Expense.spent_on <= date_to)
    if category is not None:
        stmt = stmt.where(Expense.category == category)
    stmt = stmt.offset(skip).limit(min(limit, 500))
    return list(db.scalars(stmt).all())


def update_expense(db: Session, expense: Expense, data: ExpenseUpdate) -> Expense:
    payload = data.model_dump(exclude_unset=True)
    for key, value in payload.items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense: Expense) -> None:
    db.delete(expense)
    db.commit()


def monthly_report(db: Session, year: int, month: int) -> MonthlyReport:
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

    rows = db.execute(
        select(
            Expense.category,
            func.sum(Expense.amount),
            func.count(Expense.id),
        )
        .where(Expense.spent_on >= start, Expense.spent_on < end)
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
    ).all()

    by_category = [
        CategoryTotal(
            category=row[0],
            total=Decimal(str(row[1] or 0)),
            count=int(row[2] or 0),
        )
        for row in rows
    ]
    total = sum((item.total for item in by_category), Decimal("0"))

    return MonthlyReport(year=year, month=month, total=total, by_category=by_category)


def expenses_for_export(
    db: Session,
    *,
    date_from: date | None = None,
    date_to: date | None = None,
    category: ExpenseCategory | None = None,
) -> list[Expense]:
    return list_expenses(
        db,
        date_from=date_from,
        date_to=date_to,
        category=category,
        skip=0,
        limit=500,
    )
