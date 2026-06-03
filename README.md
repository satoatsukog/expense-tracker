# Expense Tracker API

A small **Python REST API** for tracking personal expenses. Built for a GitHub portfolio: tests, Docker, CI, and interactive API docs.

## Features

| Action | Description |
|--------|-------------|
| Create expense | Amount, category, description, date |
| List expenses | Filter by date range and category |
| Monthly report | Total spend and breakdown by category |
| Export CSV | Download for Excel / Google Sheets |
| Update / delete | By expense id |

**Categories:** `food`, `transport`, `housing`, `entertainment`, `health`, `shopping`, `other`.

## Tech stack

- Python 3.11+
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- SQLite (`expense_tracker.db`)
- pytest, ruff, GitHub Actions

## Quick start

### 1. Install Python

Python **3.11+** required:

```bash
python3 --version
```

### 2. Go to the project folder

```bash
cd /path/to/portfolio/python
```

### 3. Virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 4. Configuration (optional)

```bash
cp .env.example .env
```

By default the database file is `expense_tracker.db` in the project root.

### 5. Run the server

```bash
uvicorn expense_tracker.main:app --reload
```

If you see `ModuleNotFoundError: No module named 'expense_tracker'`:

**macOS (common):** Python 3.12 ignores hidden `.pth` files. Run:

```bash
./scripts/fix-venv.sh
python -c "import expense_tracker; print('OK')"
```

Then reinstall if needed:

```bash
pip install -e ".[dev]"
./scripts/fix-venv.sh
```

**Any OS:** use the helper script (sets `PYTHONPATH` automatically):

```bash
./scripts/run.sh
```

Open in the browser:

- **Interactive API docs:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

## How to test

There are **two ways** to test: automated tests (pytest) and manual testing in the browser.

### A. Automated tests (recommended)

With the virtual environment activated:

```bash
cd /path/to/portfolio/python
source .venv/bin/activate
pytest
```

You should see **7 passed**. These tests check create/read/update/delete, filters, monthly report, CSV export, and validation.

Optional: run the linter too:

```bash
ruff check src tests
```

### B. Manual testing in the browser (no coding)

1. Start the server (see **Quick start** step 5).
2. Open http://127.0.0.1:8000/docs
3. Try this flow:

**Step 1 — Create an expense**

- Open `POST /expenses` → **Try it out**
- Request body example:

```json
{
  "amount": "350",
  "category": "food",
  "description": "Coffee",
  "spent_on": "2025-06-03"
}
```

- Click **Execute** → you should get `201` and an `id` in the response.

**Step 2 — List expenses**

- Open `GET /expenses` → **Try it out** → **Execute**
- Your new expense should appear in the list.

**Step 3 — Monthly report**

- Open `GET /expenses/report/monthly`
- Set `year` = `2025`, `month` = `6` → **Execute**
- Check `total` and `by_category`.

**Step 4 — Export CSV**

- Open `GET /expenses/export.csv` → **Try it out** → **Execute**
- Download the file and open it in Excel or a text editor.

**Step 5 — Health check**

- Open http://127.0.0.1:8000/health in a new tab
- You should see: `{"status":"ok"}`

### C. Manual testing with curl (terminal)

Server must be running.

```bash
# Create
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"amount": "350", "category": "food", "description": "Coffee", "spent_on": "2025-06-03"}'

# List (June 2025)
curl "http://127.0.0.1:8000/expenses?date_from=2025-06-01&date_to=2025-06-30"

# Monthly report
curl "http://127.0.0.1:8000/expenses/report/monthly?year=2025&month=6"

# Download CSV
curl -OJ "http://127.0.0.1:8000/expenses/export.csv"
```

## Docker

```bash
docker build -t expense-tracker .
docker run -p 8000:8000 -v "$(pwd)/data:/app/data" expense-tracker
```

To persist the database between restarts, set in `.env`:

`DATABASE_URL=sqlite:////app/data/expense_tracker.db`

## Project structure

```
python/
├── src/expense_tracker/   # application code
│   ├── main.py            # FastAPI entry point
│   ├── models.py          # database tables
│   ├── crud.py            # data access
│   └── routers/           # HTTP routes
├── tests/                 # automated tests
├── pyproject.toml         # dependencies
└── README.md
```

## Publish to GitHub

1. Create a new repository on [github.com](https://github.com) (empty, if you copy this README).
2. In the project folder:

```bash
git init
git add .
git commit -m "Add expense tracker API portfolio project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/expense-tracker.git
git push -u origin main
```

3. Add topics on GitHub: `python`, `fastapi`, `sqlalchemy`, `rest`, `pytest`.

## License

MIT — free to use in portfolios and learning.
