# Copy-ready prompt B02 — Postgres persistence foundation

Implement **only B02**, assuming B01 is verified. Read `AGENTS.md`, `docs/DATA_MODEL.md`, `docs/ARCHITECTURE.md`, `docs/CI_CD.md`, `docs/PROGRESS.md`; inspect repo/git state first.

Deliver:
- Connection settings from `backend/.env` (template exists), SQLAlchemy 2 database engine/session dependency with reasonable lifecycle.
- Appointment SQLAlchemy model exactly matching `docs/DATA_MODEL.md`, including UUID, required fields, timezone-aware timestamp, status/type validation, created/updated.
- Alembic configuration and first reviewable migration creating appointments table. **Do not auto-create schema on app startup.**
- One real PostgreSQL integration test applying the migration and proving insert/reload (with fictional data). Fixture must keep tests isolated. CI PostgreSQL is on localhost:5432; developer DB is localhost:5433. Keep both supported via `DATABASE_URL`.
- Actual migration command instructions; report whether Docker was available to verify.

Constraints: No CRUD HTTP endpoints and no frontend yet. Keep no unrelated tables or fabricated business rules. No real patients.

Run Ruff, backend tests, and migration smoke-check if possible; report exact outcomes, changed files and tradeoffs. Update `docs/PROGRESS.md`; stop after B02 for review and candidate commit.
