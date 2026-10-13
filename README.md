# VisitDock

A compact clinic appointment workspace for an internship take-home assignment. **Fictional data only.** Backend-first implementation: FastAPI, SQLAlchemy, Alembic and PostgreSQL 17; Next.js App Router, TypeScript and Tailwind frontend.

Implemented: create, paginated list, details, full update, confirmed deletion, patient/doctor search, combined doctor/status/clinic-date filters, responsive rows, accessible modal drawers, and loading/empty/error/retry states. No authentication, booking-conflict rules or deployment is included.

## Run locally

Requirements: Python **3.13** (tested), Node **24.15+**, npm, Docker Desktop with Compose. PostgreSQL is exposed on host port **5433**.

From repository root:

```bash
cp .env.example .env
docker compose up -d db
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.lock
python -m pip install -e '.[dev]' --no-deps
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

In another terminal, from `frontend/`:

```bash
cp .env.example .env.local
npm ci
npm run dev
```

Open [VisitDock](http://localhost:3000), [API documentation](http://localhost:8000/docs), or [process health](http://localhost:8000/health). On Windows activate the environment using `.venv\Scripts\Activate.ps1`; copy files with `Copy-Item`.

Environment variables override `backend/.env`. Set backend `CLINIC_TIMEZONE` and frontend `NEXT_PUBLIC_CLINIC_TIMEZONE` to the **same IANA timezone** (both default UTC). Rebuild the frontend after changing public variables. The list and date filter use clinic time; the form explicitly accepts **UTC** to avoid ambiguous local DST times. Editing another field preserves the original instant, including seconds and milliseconds. `CORS_ORIGINS` is a comma-separated allowlist; use `http://localhost:3000` when opening the app.

## Verify

Create the isolated test database once, from repository root (skip if it exists):

```bash
docker exec -i visitdock-db-1 psql -U visitdock -d postgres -c "CREATE DATABASE visitdock_test OWNER visitdock;"
```

From `backend/`, with the environment active:

```bash
ruff check .
APP_ENV=test DATABASE_URL=postgresql+psycopg://visitdock:visitdock_dev_only@localhost:5433/visitdock_test python -m pytest -q
```

Pytest rejects non-test environments/databases and uses transaction rollback. Never run it against development records. From `frontend/`:

```bash
npm run lint
npm run typecheck
npm run test
npm run build
```

For real browser tests, start **test-database** API and production frontend services using [browser testing instructions](docs/BROWSER_TESTING.md), then run `npm run test:e2e`. CI runs scaffold, 103 backend tests, frontend lint/types/9 unit tests/build, and desktop/mobile PostgreSQL-backed browser tests. See [verified progress](docs/PROGRESS.md) for actual run results and commit history.

`python3 scripts/check_scaffold.py` checks documentation packaging and links; it does not validate app functionality. `docker compose down` preserves the database volume.

## API

Base path: `/api/v1/appointments`.

| Method | Path | Behavior |
| --- | --- | --- |
| POST | base | Create, 201 |
| GET | base | Search/filter/paginate, 200 |
| GET | `/{id}` | Details, 200 / 404 |
| PUT | `/{id}` | Replace all five editable fields, 200 / 404 |
| DELETE | `/{id}` | Empty 204 / 404 |

Validation errors return 422; database failures return a generic 503. UUIDs and timestamps are server managed. Search is a literal case-insensitive substring across patient/doctor; doctor filtering is case-insensitive exact matching. Date windows use clinic midnight boundaries converted to UTC, including DST. Ordering is appointment time then UUID. Page size is 1–100. See the [full API contract](docs/API_CONTRACT.md).

## Review and submission

- [Architecture](docs/ARCHITECTURE.md), [data model](docs/DATA_MODEL.md), [visual brief](docs/UI_DESIGN.md)
- [Test strategy](docs/TEST_PLAN.md), [CI](docs/CI_CD.md), [local setup](docs/LOCAL_DEVELOPMENT.md)
- [Security and privacy](docs/SECURITY_AND_PRIVACY.md), [AI work log](AI_USAGE.md), [final review](docs/FINAL_REVIEW.md)
- [Submission checklist](docs/SUBMISSION_CHECKLIST.md)

Use invented names only. This demonstration has no authentication and is not suitable for sensitive records or public production use. Human candidate review, personal AI-use reflection and company submission/visibility confirmation remain candidate-owned tasks. No human review has been fabricated. No license is presumed.
