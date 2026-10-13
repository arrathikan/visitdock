# VisitDock Backend

FastAPI backend service for VisitDock Clinic Appointment Management with PostgreSQL persistence and Alembic migrations.

## Development Setup

```bash
# 1. From repository root, start PostgreSQL (runs on localhost:5433):
docker compose up -d db

# 2. From backend directory:
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Database Migrations (Alembic)

```bash
# Apply migrations to head:
alembic upgrade head

# Check current revision in database:
alembic current

# Show migration history:
alembic history

# Downgrade by 1 revision (CAUTION: destructive to table data):
alembic downgrade -1
```

## Running the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

- API Base: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- OpenAPI Docs: `http://localhost:8000/docs`

## Tests and Linting

```bash
# Run test suite (verifies health endpoints and PostgreSQL integration)
python -m pytest -q

# Run linter
ruff check .
```
