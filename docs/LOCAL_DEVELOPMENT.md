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

## Backend (verified in B01)

The backend uses Python 3.12+ (tested with 3.13) and FastAPI.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
ruff check .
python -m pytest -q
uvicorn app.main:app --reload --port 8000
```

- Process health endpoint: `http://localhost:8000/health`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Backend local environment configuration template is in `backend/.env.example`. Database connection settings will be utilized starting from slice B02.

## Frontend (after F01)

The AI agent should install dependencies using npm, **commit the lockfile**, and document `npm ci`, `npm run dev`, lint, typecheck, test, build. `frontend/.env.example` contains only public API base URL. Do not place DB URL or server secrets in `NEXT_PUBLIC_*`.

## Smoke-check starter

```bash
python scripts/check_scaffold.py
```

This verifies packaging, not application behavior.
