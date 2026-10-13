# Local development notes

## Requirements now

- Git and Python 3.12+ (to run the scaffold checker; backend implementation chooses/records exact runtime)
- Docker Desktop / Docker Compose for local PostgreSQL
- Later: Node.js LTS / npm for Next.js

## Database only (starter)

```bash
cp .env.example .env
docker compose up -d db
docker compose ps
docker compose logs db
```

Connection from host: `localhost:5433`. Host password, db, and username are in ignored `.env` with development defaults. From another Compose service, hostname is `db`, port `5432` (different `DATABASE_URL`).

```bash
docker compose down
```

The command above preserves data. To deliberately erase local database data: `docker compose down -v` — **destructive**.

## Backend (verified in B01, B02 & B03)

The backend uses Python 3.12+ (tested with 3.13), FastAPI, SQLAlchemy 2.x, Alembic, and PostgreSQL 17.

```bash
# 1. Start database container
docker compose up -d db

# 2. Setup and run backend
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"

# 3. Apply database migrations to development database
alembic upgrade head

# 4. Check migration status
alembic current
alembic history

# 5. Linting
ruff check .

# 6. Automated tests (requires dedicated test database)
# Create test database once:
docker exec -i visitdock-db-1 psql -U visitdock -d postgres -c "CREATE DATABASE visitdock_test OWNER visitdock;"

# Run tests with test database isolation:
APP_ENV=test DATABASE_URL="postgresql+psycopg://visitdock:visitdock_dev_only@localhost:5433/visitdock_test" python -m pytest -q

# 7. Start development server
uvicorn app.main:app --reload --port 8000
```

- Process health endpoint: `http://localhost:8000/health`
- Create appointment endpoint: `POST http://localhost:8000/api/v1/appointments`
- List appointments endpoint: `GET http://localhost:8000/api/v1/appointments?page=1&page_size=20`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Test Database Isolation Safeguards
Pytest requires `APP_ENV=test` and a dedicated test database (e.g. `visitdock_test`). Runs against the development database (`visitdock`) or non-test databases are automatically blocked to prevent data loss. Tests run inside nested savepoint transactions that roll back cleanly upon completion.

Backend local environment configuration template is in `backend/.env.example`. Environment variables override local `.env` settings. Local PostgreSQL runs on host port `5433` (`DATABASE_URL=postgresql+psycopg://visitdock:visitdock_dev_only@localhost:5433/visitdock`), while CI runs on port `5432`.

## Frontend (after F01)

The AI agent should install dependencies using npm, **commit the lockfile**, and document `npm ci`, `npm run dev`, lint, typecheck, test, build. `frontend/.env.example` contains only public API base URL. Do not place DB URL or server secrets in `NEXT_PUBLIC_*`.

## Smoke-check starter

```bash
python scripts/check_scaffold.py
```

This verifies packaging, not application behavior.
