# Architecture and engineering boundaries

## Overview

```text
 Browser (Next.js / TypeScript / Tailwind)
        |  HTTP JSON /api/v1/appointments
        v
 FastAPI router + Pydantic validation
        |  application logic (simple service when useful)
        v
 SQLAlchemy 2 session / persistence
        |  Alembic migrations
        v
 PostgreSQL
```

Backend and frontend live in separate directories within one repository. No service mesh, distributed system, or authentication service is needed.

## Backend structure — intended, not yet created

```text
backend/
  app/
    main.py
    core/config.py
    db/session.py
    appointments/
      models.py       # SQLAlchemy model
      schemas.py      # Pydantic request/response schemas
      router.py       # HTTP boundary
      service.py      # application rules only if warranted
  alembic/
  tests/
  pyproject.toml
```

A separate repository abstraction is **optional**; choose it only if testing/clarity improves rather than creating unnecessary layers. Small feature-oriented modules are preferable to sprawling “utils” folders.

## Data and time

- Store timestamps as timezone-aware PostgreSQL `TIMESTAMPTZ`; normalize to UTC at the boundary/persistence layer.
- Frontend formatting uses `CLINIC_TIMEZONE` (default `UTC` in starter) and visibly labels the selected timezone where confusion is likely.
- `GET date=YYYY-MM-DD` refers to a calendar date in `CLINIC_TIMEZONE`; convert the day window to UTC in the backend before querying.
- Avoid naive datetimes. Test timezone conversion and inclusive/exclusive date boundaries when date filter is implemented.

## Environment / ports

- PostgreSQL container: host `localhost:5433`, container `db:5432`.
- FastAPI: `localhost:8000` when implemented.
- Next.js: `localhost:3000` when implemented.
- Browser makes requests to FastAPI using the API base URL in `frontend/.env.local`; explicitly configure local CORS.
- Never expose DB credentials through `NEXT_PUBLIC_*` variables.

## Reviewable choices

- Python/FastAPI for strong input validation and straightforward API docs.
- PostgreSQL for durable persistence and realistic relational queries.
- SQLAlchemy 2 + Alembic for explicit migrations (no schema creation on every startup).
- Next.js for the frontend but no SSR complexity when a simple client-side workspace suffices.
- Test actual API and database behavior; avoid mock-only confidence.

See also [`DECISIONS.md`](DECISIONS.md) for decisions and non-goals.
