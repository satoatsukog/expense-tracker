from contextlib import asynccontextmanager

from fastapi import FastAPI

from expense_tracker import __version__
from expense_tracker.database import init_db
from expense_tracker.routers import expenses


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Expense Tracker API",
    description="REST API for personal expense tracking — Python portfolio project.",
    version=__version__,
    lifespan=lifespan,
)

app.include_router(expenses.router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
