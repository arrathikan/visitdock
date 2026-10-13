# VisitDock Backend

FastAPI backend service for VisitDock Clinic Appointment Management with PostgreSQL persistence, Alembic migrations, and automated test suite.

## Development Setup

```bash
# 1. From repository root, start PostgreSQL (runs on localhost:5433):
docker compose up -d db

# 2. From backend directory:
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.lock
python -m pip install -e ".[dev]" --no-deps
```

## Database Migrations (Alembic)

```bash
# Apply migrations to head on development database:
alembic upgrade head

# Check current revision in database:
alembic current

# Show migration history:
alembic history

# Schema inspection without modifying records:
alembic history
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

## Implemented Endpoints (B01–B06)

- `GET /health` — Lightweight service health check
- `POST /api/v1/appointments` — Create appointment with Pydantic v2 validation (201 Created)
- `GET /api/v1/appointments` — Search patient/doctor and combine doctor, status, clinic-date filters with bounded SQL pagination.
- `GET /api/v1/appointments/{id}` — Details, 200 or 404; malformed UUID is 422.
- `PUT /api/v1/appointments/{id}` — Full replacement with create validation; every accepted replacement advances updated_at, even identical values.
- `DELETE /api/v1/appointments/{id}` — Empty 204 or 404.

Settings validate IANA clinic timezones. Date windows use midnight in CLINIC_TIMEZONE converted to UTC (including DST); unsupported boundary dates return 422. Datetimes must be offset-aware ISO strings, never numeric epochs. DB errors return generic 503; CORS allows explicit configured origins. Fictional records only. The full suite contains 106 tests, including collected rejection cases for development, production, staging and empty environment strings.

## Tests and Linting

```bash
# Run test suite
APP_ENV=test DATABASE_URL="postgresql+psycopg://visitdock:visitdock_dev_only@localhost:5433/visitdock_test" python -m pytest -v

# Run linter
ruff check .
```
