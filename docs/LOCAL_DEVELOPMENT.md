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

## Backend (after B01/B02)

The AI agent should add exact `python -m venv`, `pip install -e ".[dev]"`, Uvicorn, Alembic and Pytest commands to README when they actually work. Backend local config template: `backend/.env.example`. The database URL there points to host port 5433.

## Frontend (after F01)

The AI agent should install dependencies using npm, **commit the lockfile**, and document `npm ci`, `npm run dev`, lint, typecheck, test, build. `frontend/.env.example` contains only public API base URL. Do not place DB URL or server secrets in `NEXT_PUBLIC_*`.

## Smoke-check starter

```bash
python scripts/check_scaffold.py
```

This verifies packaging, not application behavior.
