# Implementation progress / handoff checkpoint

**State as packaged:** Documentation and local infrastructure starter supplied. **No backend code, frontend code, Alembic migration, app tests, or deployment has been implemented.**

## Verified in starter pack

- Root documentation, AI instructions, step-by-step prompts, and fictional example data are present.
- `compose.yaml` defines local PostgreSQL (not a deployed database).
- GitHub Actions `ci.yml` validates the starter and conditionally runs app checks once app manifests are created.
- A dependency-free local scaffold checker is included.

## Verified progress

### B01 — Backend foundation (Verified)
- **Date / slice:** 2026-10-13 / B01 — FastAPI Backend Foundation
- **Git branch:** `main`
- **Exact files added or changed:**
  - Added: `backend/pyproject.toml` (PEP 621 packaging, FastAPI, Uvicorn, dev dependencies for Ruff, Pytest, HTTPX)
  - Added: `backend/README.md` (backend setup and commands guide)
  - Added: `backend/app/__init__.py`
  - Added: `backend/app/main.py` (FastAPI app initialization, metadata, `GET /health` endpoint)
  - Added: `backend/app/core/__init__.py`
  - Added: `backend/tests/__init__.py`
  - Added: `backend/tests/test_health.py` (Pytest test suite for health check, 404 behavior, and OpenAPI schema)
  - Removed: `backend/.gitkeep` (no longer needed)
  - Updated: `README.md`, `docs/LOCAL_DEVELOPMENT.md`, `docs/PROGRESS.md`, `AI_USAGE.md`
- **Commands run + results:**
  - `python3 scripts/check_scaffold.py`: Passed (21 required files, 34 Markdown files, no broken links).
  - `python3 -m venv backend/.venv`: Succeeded.
  - `./.venv/bin/python -m pip install -e ".[dev]"`: Succeeded (installed FastAPI 0.143.0, Uvicorn 0.54.0, Pytest 9.1.1, HTTPX 0.28.1, Ruff 0.17.0, Pydantic 2.14.1).
  - `./.venv/bin/ruff check .`: Succeeded (All checks passed).
  - `./.venv/bin/python -m pytest -q`: Succeeded (5 passed in 0.16s).
  - `./.venv/bin/uvicorn app.main:app --port 8000` + `curl http://localhost:8000/health`: Succeeded (`HTTP/1.1 200 OK`, `{"status":"ok"}`).
  - `curl http://localhost:8000/docs`: Succeeded (`HTTP/1.1 200 OK`, Swagger UI HTML).
- **Behaviors manually verified:**
  - `/health` endpoint responds with 200 OK and expected JSON payload without database dependency.
  - Non-existent route `/nonexistent-endpoint` responds with 404 Not Found.
  - OpenAPI docs are accessible at `/docs` and schema at `/openapi.json`.
- **Open issues and risks:**
  - Database persistence and migrations not yet connected (scoped for B02).
  - Appointment CRUD endpoints not yet implemented (scoped for B03-B05).

### B02 — PostgreSQL persistence & Alembic migrations (Verified)
- **Date / slice:** 2026-10-13 / B02 — PostgreSQL Persistence Foundation & Migrations
- **Git branch:** `main`
- **Exact files added or changed:**
  - Added: `backend/app/core/config.py` (Pydantic Settings for environment variables and defaults)
  - Added: `backend/app/db/__init__.py`, `backend/app/db/base.py` (SQLAlchemy 2.x DeclarativeBase)
  - Added: `backend/app/db/session.py` (database engine, sessionmaker, request-scoped `get_db` dependency)
  - Added: `backend/app/appointments/__init__.py`, `backend/app/appointments/models.py` (`Appointment` model, `AppointmentType`, `AppointmentStatus` StrEnums, CHECK constraints, TIMESTAMPTZ columns)
  - Added: `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/script.py.mako`, `backend/alembic/versions/848b204929ed_create_appointments_table.py` (Alembic configuration and initial migration)
  - Added: `backend/tests/conftest.py` (Alembic migration runner fixture and isolated test db_session fixture)
  - Added: `backend/tests/test_database.py` (8 automated tests verifying connection, schema, insert/query across sessions, constraints, timezone handling, session lifecycle)
  - Updated: `backend/pyproject.toml` (added SQLAlchemy, Alembic, Psycopg, Pydantic Settings; cleaned pytest warning filter)
  - Updated: `README.md`, `backend/README.md`, `docs/LOCAL_DEVELOPMENT.md`, `docs/PROGRESS.md`, `AI_USAGE.md`
  - Updated: `.github/workflows/ci.yml` (migrated actions/checkout, setup-python, setup-node to Node 24 compatible versions)
- **Commands run + results:**
  - `docker compose up -d db`: Container `visitdock-db-1` healthy on port 5433.
  - `python -m pip install -e ".[dev]"`: Succeeded.
  - `alembic upgrade head`: Applied revision `848b204929ed` (`create appointments table`).
  - `alembic current`: Output `848b204929ed (head)`.
  - `alembic history`: `<base> -> 848b204929ed (head), create appointments table`.
  - `alembic downgrade base` + `alembic upgrade head`: Verified clean rollback and re-application.
  - `ruff check .`: All checks passed.
  - `python -m pytest -v`: 13 passed in 0.21s (5 health tests + 8 PostgreSQL tests).
  - `python3 scripts/check_scaffold.py`: Passed (21 required files, 35 Markdown files).
- **Behaviors manually verified:**
  - Appointment model persists to PostgreSQL with UUID generation and server-managed timestamps.
  - Check constraints for appointment_type and status reject invalid values with IntegrityError.
  - Timezone-aware datetimes (+05:30) correctly persist the UTC instant in TIMESTAMPTZ.
  - `/health` endpoint remains completely independent of database connectivity.
- **Open issues and risks:**
  - Database test isolation in `backend/tests/conftest.py` identified as potentially destructive (erasing development database on run). Corrected in B03.
- **Next smallest feature:**
  - **B03 — Create and List Appointments**: Pydantic request/response schemas, `POST /api/v1/appointments` with validation, and `GET /api/v1/appointments` listing.

### B03 — Create & List Appointments API and Test Database Isolation (Verified)
- **Date / slice:** 2026-10-13 / B03 — Create & List Appointments API
- **Git branch:** `main`
- **Exact files added or changed:**
  - Added: `backend/app/appointments/schemas.py` (`AppointmentCreate`, `AppointmentResponse`, `AppointmentListResponse` Pydantic v2 schemas with trimming, bounds, timezone validation, and UTC ISO serialization)
  - Added: `backend/app/appointments/router.py` (`POST /api/v1/appointments` returning 201, `GET /api/v1/appointments` with SQL-level pagination and deterministic ordering)
  - Added: `backend/tests/test_isolation_guard.py` (10 regression tests for test target safeguards and transaction rollback isolation)
  - Added: `backend/tests/test_appointments_api.py` (23 integration tests for POST/GET endpoints, validation bounds, invalid enums/dates, pagination, and tie-breaking)
  - Updated: `backend/tests/conftest.py` (replaced unconditional table deletes with savepoint transaction rollback; added target environment/DB name safeguards and `client` fixture)
  - Updated: `backend/app/main.py` (registered `appointments_router` under `/api/v1`)
  - Updated: `README.md`, `backend/README.md`, `docs/LOCAL_DEVELOPMENT.md`, `docs/PROGRESS.md`, `AI_USAGE.md`
- **Commands run + results:**
  - `docker exec -i visitdock-db-1 psql -U visitdock -d postgres -c "CREATE DATABASE visitdock_test OWNER visitdock;"`: Database created.
  - `alembic current`: Output `848b204929ed (head)`.
  - `ruff check .`: Passed cleanly (All checks passed).
  - `APP_ENV=test DATABASE_URL="postgresql+psycopg://visitdock:visitdock_dev_only@localhost:5433/visitdock_test" python -m pytest -v`: 58 passed in 0.27s (5 health + 8 DB + 12 isolation guard + 33 API tests).
  - `APP_ENV=development python -m pytest -q`: Rejected immediately with `pytest.UsageError` (safeguard verified).
  - `APP_ENV=test DATABASE_URL=".../visitdock" python -m pytest -q`: Rejected immediately with `pytest.UsageError` (safeguard verified).
  - `python3 scripts/check_scaffold.py`: Passed (21 required files, 35 Markdown files).
  - `uvicorn app.main:app --port 8000`:
    - `curl -X POST /api/v1/appointments`: Returned HTTP 201 Created with generated UUID and UTC instant.
    - `curl GET /api/v1/appointments?page=1&page_size=20`: Returned HTTP 200 OK with `{items, total, page, page_size}`.
    - `curl POST with naive datetime / whitespace name`: Returned HTTP 422 Unprocessable Content.
    - `curl GET with page_size=101`: Returned HTTP 422 Unprocessable Content.
- **Behaviors manually verified:**
  - Dedicated test database `visitdock_test` isolated from development database `visitdock`.
  - Unconditional `delete(Appointment)` removed from fixtures; test runs leave zero residual data via transaction rollback.
  - Smoke test appointment created in development database remains intact across test runs and API restart.
  - `/health` endpoint remains unaffected and operational.
  - `/docs` and `/openapi.json` display both appointment endpoints with complete schemas.
- **Open issues and risks:**
  - Single appointment retrieval (`GET /api/v1/appointments/{id}`), update (`PUT`), and delete (`DELETE`) are not yet implemented (scheduled for B04).
  - Search and query filtering (`search`, `status`, `doctor`, `date`) are not yet implemented (scheduled for B05).
- **Next smallest feature:**
  - **B04 — Retrieve, Update, and Delete Appointments**: `GET /api/v1/appointments/{id}`, `PUT /api/v1/appointments/{id}`, `DELETE /api/v1/appointments/{id}` with 404 handling.

### B04 — verified by Codex, 2026-10-13

- Implemented UUID retrieval, full PUT replacement, DELETE with empty 204, and 404/422 handling.
- Every accepted PUT advances updated_at, including identical replacements; created_at remains unchanged.
- Added 18 database-backed regression cases in tests/test_appointment_details.py.
- Checks actually run: Ruff passed; dedicated visitdock_test PostgreSQL suite: **76 passed**. Initial sandbox execution could not connect; approved rerun passed.
- AI review: inspected full-field validation, immutable metadata, deletion persistence, and timestamp behavior. Human review remains pending.
- Next: B05 search/filter/date semantics.
