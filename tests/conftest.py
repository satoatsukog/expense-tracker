import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

from expense_tracker.database import Base, engine
from expense_tracker.main import app


@pytest.fixture(autouse=True)
def _reset_database() -> None:
    from expense_tracker.database import init_db

    Base.metadata.drop_all(bind=engine)
    init_db()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
