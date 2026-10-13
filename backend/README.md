# VisitDock Backend

FastAPI backend service for VisitDock Clinic Appointment Management with PostgreSQL persistence, Alembic migrations, and automated test suite.

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
# Apply migrations to head on development database:
alembic upgrade head

# Check current revision in database:
alembic current

# Show migration history:
alembic history

# Downgrade by 1 revision (CAUTION: destructive to table data):
alembic downgrade -1
```

## Dedicated Test Database & Safety

Automated tests require a dedicated PostgreSQL test database (`visitdock_test`) and `APP_ENV=test`. Unsafe runs against the development database (`visitdock`) are rejected by test safeguards to prevent accidental data loss.

```bash
# 1. Create the dedicated test database once (non-destructive):
docker exec -i visitdock-db-1 psql -U visitdock -d postgres -c "CREATE DATABASE visitdock_test OWNER visitdock;"

# 2. Run the test suite against visitdock_test:
APP_ENV=test DATABASE_URL="postgresql+psycopg://visitdock:visitdock_dev_only@localhost:5433/visitdock_test" python -m pytest -q
```

All test cases execute within transaction savepoints that are automatically rolled back upon test completion, leaving zero residual records and requiring no destructive table-wide deletes.

## Running the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

- API Base: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- OpenAPI Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Implemented Endpoints (B01 - B03)

- `GET /health` — Lightweight service health check
- `POST /api/v1/appointments` — Create appointment with Pydantic v2 validation (201 Created)
- `GET /api/v1/appointments` — List appointments with database pagination (`page`, `page_size`, deterministic sorting by `appointment_at ASC, id ASC`)

## Tests and Linting

```bash
# Run test suite
APP_ENV=test DATABASE_URL="postgresql+psycopg://visitdock:visitdock_dev_only@localhost:5433/visitdock_test" python -m pytest -v

# Run linter
ruff check .
```
