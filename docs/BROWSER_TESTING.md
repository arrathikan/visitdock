# Real browser testing

Requires Node >=24.15, Python 3.13, PostgreSQL 17, and a dedicated `visitdock_test` database. Never point automated checks at real patient data.

## Local services

From `backend/` with its virtual environment active:

```bash
export APP_ENV=test
export DATABASE_URL=postgresql+psycopg://visitdock:visitdock_dev_only@localhost:5433/visitdock_test
export CLINIC_TIMEZONE=UTC
export CORS_ORIGINS=http://localhost:3000
alembic upgrade head
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal, from `frontend/`:

```bash
npm ci
npm run build
npm start -- --hostname 127.0.0.1 --port 3000
```

In a third terminal, from `frontend/`:

```bash
npx playwright install chromium
npm run test:e2e
```

If Chrome is already installed, `PLAYWRIGHT_CHANNEL=chrome npm run test:e2e` is supported. This is how the local run was verified; CI installs Playwright Chromium. Open the UI at `http://localhost:3000` to match the configured CORS origin. Do not run the backend Pytest suite concurrently with E2E against the same database.

## Coverage and isolation

Desktop Chrome and a Chromium-emulated iPhone viewport cover create, persisted details, edit, status/date/search filtering, cancel/confirm deletion, Escape and focus restoration, no horizontal overflow, and API failure/retry. Browser request interception is used only for the failure-state test; the CRUD path uses real FastAPI and PostgreSQL.

Each run creates a unique fictional name and deletes only its generated record ID. Cleanup uses an independent API context so a browser timeout cannot invalidate it. Successful deletion is verified with an API 404. No table-wide cleanup is performed. The two records from the initial failed run were removed individually after identifying their generated names, doctor and exact timestamp.

Screenshots, traces and HTML reports are ignored local artifacts. `npx playwright show-report` opens the latest report.

## CI

The frontend CI job starts a separate PostgreSQL 17 service named `visitdock_test`, installs the API, applies Alembic, starts the production frontend and API, waits for both services, then runs both browser projects. Backend tests run in their own service/job. Failing checks fail CI. No deployment is configured.
