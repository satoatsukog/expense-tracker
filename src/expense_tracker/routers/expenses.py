import csv
import io
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from expense_tracker import crud
from expense_tracker.database import get_db
from expense_tracker.models import ExpenseCategory
from expense_tracker.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate, MonthlyReport

router = APIRouter(prefix="/expenses", tags=["expenses"])

CATEGORY_LABELS = {
    ExpenseCategory.food: "Food",
    ExpenseCategory.transport: "Transport",
    ExpenseCategory.housing: "Housing",
    ExpenseCategory.entertainment: "Entertainment",
    ExpenseCategory.health: "Health",
    ExpenseCategory.shopping: "Shopping",
    ExpenseCategory.other: "Other",
}


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)) -> ExpenseRead:
    return crud.create_expense(db, data)


@router.get("", response_model=list[ExpenseRead])
def list_expenses(
    date_from: date | None = Query(default=None, description="Start date (inclusive)"),
    date_to: date | None = Query(default=None, description="End date (inclusive)"),
    category: ExpenseCategory | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[ExpenseRead]:
    return crud.list_expenses(
        db,
        date_from=date_from,
        date_to=date_to,
        category=category,
        skip=skip,
        limit=limit,
    )


@router.get("/export.csv")
def export_csv(
    date_from: date | None = None,
    date_to: date | None = None,
    category: ExpenseCategory | None = None,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    expenses = crud.expenses_for_export(
        db, date_from=date_from, date_to=date_to, category=category
    )

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["id", "date", "category", "category_label", "amount", "description"])
    for item in expenses:
        writer.writerow(
            [
                item.id,
                item.spent_on.isoformat(),
                item.category.value,
                CATEGORY_LABELS.get(item.category, item.category.value),
                f"{item.amount:.2f}",
                item.description or "",
            ]
        )

    buffer.seek(0)
    filename = f"expenses_{date.today().isoformat()}.csv"
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/report/monthly", response_model=MonthlyReport)
def monthly_report(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
) -> MonthlyReport:
    return crud.monthly_report(db, year, month)


@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: int, db: Session = Depends(get_db)) -> ExpenseRead:
    expense = crud.get_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.patch("/{expense_id}", response_model=ExpenseRead)
def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    db: Session = Depends(get_db),
) -> ExpenseRead:
    expense = crud.get_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    if not data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one field is required to update an expense",
        )
    return crud.update_expense(db, expense, data)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)) -> None:
    expense = crud.get_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    crud.delete_expense(db, expense)
