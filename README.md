# Expense Tracker API

REST API for tracking personal expenses, built with Python and FastAPI. It comes with automated tests, a Dockerfile and a GitHub Actions workflow, and it serves interactive API docs out of the box.

The browser interface for this API lives in [expense-tracker-frontend](https://github.com/satoatsukog/expense-tracker-frontend).

<!-- After deploying, add here: **Live demo:** https://your-deployed-url/docs -->

## Features

| Action | Description |
|--------|-------------|
| Create expense | Amount, category, description, date |
| List expenses | Filter by date range and category |
| Monthly report | Total spend and breakdown by category |
| Export CSV | Download for Excel or Google Sheets |
| Update / delete | By expense id |

Categories: `food`, `transport`, `housing`, `entertainment`, `health`, `shopping`, `other`.

## Tech stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- pytest, ruff
- Docker
- GitHub Actions

## Quick start

```bash
git clone https://github.com/satoatsukog/expense-tracker.git
cd expense-tracker
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env             # optional
uvicorn expense_tracker.main:app --reload
```

Then open:

- Interactive API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

By default the database is the file `expense_tracker.db` in the project root.

If you get `ModuleNotFoundError: No module named 'expense_tracker'` (Python 3.12 on macOS ignores hidden `.pth` files), run `./scripts/fix-venv.sh`, or start the server with `./scripts/run.sh`, which sets `PYTHONPATH` for you.

## Example requests

```bash
# Create
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"amount": "350", "category": "food", "description": "Coffee", "spent_on": "2025-06-03"}'

# List expenses for June 2025
curl "http://127.0.0.1:8000/expenses?date_from=2025-06-01&date_to=2025-06-30"

# Monthly report
curl "http://127.0.0.1:8000/expenses/report/monthly?year=2025&month=6"

# Download CSV
curl -OJ "http://127.0.0.1:8000/expenses/export.csv"
```

The full list of endpoints, including update and delete, is in the interactive docs at `/docs`.

## Tests

```bash
pytest
ruff check src tests
```

The suite (7 tests) covers create, read, update and delete, filters, the monthly report, CSV export and input validation.

## Docker

```bash
docker build -t expense-tracker .
docker run -p 8000:8000 -v "$(pwd)/data:/app/data" expense-tracker
```

To keep the database between restarts, set `DATABASE_URL=sqlite:////app/data/expense_tracker.db` in `.env`.

## Project structure

```
expense-tracker/
├── src/expense_tracker/   # application code
│   ├── main.py            # FastAPI entry point
│   ├── models.py          # database tables
│   ├── crud.py            # data access
│   └── routers/           # HTTP routes
├── tests/                 # automated tests
├── scripts/               # helper scripts
├── Dockerfile
├── pyproject.toml         # dependencies
└── README.md
```

## License

MIT
