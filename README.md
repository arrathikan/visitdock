# VisitDock

**Clinic Appointment Management System** — an internship take-home project.

> **Current state:** AI-ready starter repository only. The application is **not implemented yet**. This starter contains the project brief, engineering decisions, AI instructions, prompts, local PostgreSQL infrastructure, and a GitHub Actions CI scaffold. Do **not** describe CRUD, tests, or deployment as completed until verified.

## What we're building

A small, usable web application that lets clinic staff **create, view, edit, delete, search, and filter** fictional patient appointments. Every appointment includes a patient name, appointment date/time, doctor, type, and status.

**Backend-first implementation:** Python / FastAPI, PostgreSQL, SQLAlchemy 2, Alembic, Pydantic 2, Pytest; then Next.js App Router / TypeScript / Tailwind CSS. The visual direction is a restrained, editorial clinic workspace rather than a generic AI dashboard.

## First five minutes

1. Extract the ZIP. Open the `visitdock/` folder in Cursor, VS Code, Claude Code, Codex, or a similar coding agent.
2. Read [`START_HERE.md`](START_HERE.md) and [`AGENTS.md`](AGENTS.md).
3. Optional local database: install Docker Desktop, then run:
   ```bash
   cp .env.example .env
   docker compose up -d db
   ```
   On Windows PowerShell, use `Copy-Item .env.example .env` instead of `cp`.
4. Check the starter contents using `python scripts/check_scaffold.py`.
5. Give the coding agent the text in [`prompts/00_AGENT_ONBOARDING.md`](prompts/00_AGENT_ONBOARDING.md), then **only** [`prompts/B01_BACKEND_FOUNDATION.md`](prompts/B01_BACKEND_FOUNDATION.md).
6. After each slice: inspect diff → run checks → manually review → update [`AI_USAGE.md`](AI_USAGE.md) and [`docs/PROGRESS.md`](docs/PROGRESS.md) → commit.

**Important:** FastAPI is the Python framework. **Fastify** is a separate Node.js framework; this repo intentionally uses **FastAPI**.

## Scope and status

| Area | Planned | Implemented |
| --- | --- | --- |
| FastAPI foundation & `/health` endpoint | Yes | **Implemented (B01)** |
| Create/view/edit/delete appointments | Yes | No (Planned B03-B04) |
| Search + filters | Yes | No (Planned B05) |
| Validation and helpful errors | Yes | No (Planned B03-B06) |
| PostgreSQL persistence + migrations | Yes | **Implemented (B02)** |
| Automated API and browser tests | Yes | **Backend health & PostgreSQL integration tests implemented (B02)**; browser tests pending |
| Responsive VisitDock UI | Yes | No (Planned F01-F03) |
| Local Docker PostgreSQL | Yes | **Verified & active on port 5433** |
| GitHub Actions CI | Yes | **Scaffold check + backend CI active with PostgreSQL 17** |
| Automatic production deployment | Optional | **Not configured** |

## Quick reference

- Project brief and acceptance criteria: [`docs/PRODUCT_REQUIREMENTS.md`](docs/PRODUCT_REQUIREMENTS.md)
- Architecture and boundaries: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- API contract: [`docs/API_CONTRACT.md`](docs/API_CONTRACT.md)
- Data contract: [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md)
- Visual direction: [`docs/UI_DESIGN.md`](docs/UI_DESIGN.md)
- Tests and manual QA: [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md)
- Responsible use of AI: [`AI_USAGE.md`](AI_USAGE.md)
- CI/CD setup: [`docs/CI_CD.md`](docs/CI_CD.md)
- Build and hand-in checklist: [`docs/SUBMISSION_CHECKLIST.md`](docs/SUBMISSION_CHECKLIST.md)

## Repository overview

```text
visitdock/
├── AGENTS.md                  # Canonical instructions for coding agents
├── CLAUDE.md                  # Claude Code adapter
├── START_HERE.md              # Step-by-step human launch guide
├── AI_USAGE.md                # Evidence-based AI work log
├── backend/                   # FastAPI backend service (B01-B02 implemented)
│   ├── alembic/               # Database migrations (initial schema)
│   ├── app/                   # Application package
│   │   ├── appointments/      # Appointment models and domain logic
│   │   ├── core/              # Settings & config
│   │   └── db/                # Engine, DeclarativeBase, session dependency
│   ├── tests/                 # Automated Pytest suite (health & DB integration)
│   ├── alembic.ini            # Alembic configuration
│   ├── pyproject.toml         # Dependencies and tool configurations
│   └── README.md              # Backend-specific instructions
├── frontend/                  # Added only after backend completion
├── docs/                      # Product, API, UX, test, ops, CI/CD docs
├── prompts/                   # Copy-ready prompts for each small slice
├── fixtures/                  # Fictional examples only
├── scripts/check_scaffold.py  # Dependency-free starter checks
├── .github/workflows/ci.yml   # Scaffold checks; conditional app checks
└── compose.yaml               # Local PostgreSQL only
```

## Commands available **right now**

### Starter and local database

```bash
python3 scripts/check_scaffold.py
cp .env.example .env        # Windows PowerShell: Copy-Item .env.example .env
docker compose up -d db
docker compose ps
docker compose down         # preserves Postgres volume
```

### Backend development (verified in B01 & B02)

From the repository root or `backend/` directory:

```bash
# 1. Start local PostgreSQL (runs on localhost:5433)
docker compose up -d db

# 2. Navigate to backend directory
cd backend

# 3. Create isolated virtual environment
python3 -m venv .venv

# 4. Activate virtual environment
# macOS / Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

# 5. Install backend in editable mode with development dependencies
python -m pip install -e ".[dev]"

# 6. Run database migrations
alembic upgrade head

# 7. Inspect migration status
alembic current
alembic history

# 8. Run linting
ruff check .

# 9. Run automated tests (runs both health and PostgreSQL integration tests)
python -m pytest -q

# 10. Start local development server
uvicorn app.main:app --reload --port 8000
```

Once running:
- Health check: [http://localhost:8000/health](http://localhost:8000/health) (returns `{"status":"ok"}`)
- Interactive OpenAPI documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- OpenAPI schema JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Data and privacy

This is a **fictional-data-only** demonstration. Never enter real patient names, medical history, contact information, or confidential company information. See [`docs/SECURITY_AND_PRIVACY.md`](docs/SECURITY_AND_PRIVACY.md).

## Project ownership / license

This is a candidate's take-home project scaffold. Verify the company's submission and public-repository rules before publishing; no license has been presumed.
