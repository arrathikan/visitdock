# VisitDock — canonical instructions to AI coding agents

This file is authoritative for Codex, Cursor, Claude Code, GitHub Copilot, and any other code-generation assistant working **in this repository**. Tool-specific adapters point back here.

## Mission and context

Build a small **clinic appointment management** take-home application named **VisitDock**. The evaluation includes correctness, code quality, problem solving, AI use/review/corrections, testing, docs, and usability. **Use fictional records only**. No real patient or company data.

Read before editing: `README.md`, `docs/PRODUCT_REQUIREMENTS.md`, `docs/ARCHITECTURE.md`, `docs/API_CONTRACT.md`, `docs/DATA_MODEL.md`, `docs/TEST_PLAN.md`, `docs/SECURITY_AND_PRIVACY.md`, `docs/UI_DESIGN.md`, `docs/PROGRESS.md`, and the selected `prompts/*.md`.

## Locked-in technical direction

- **Backend first:** Python **FastAPI** (not Node/Fastify), SQLAlchemy 2.x, Alembic, Pydantic 2, PostgreSQL, Pytest + HTTPX, Ruff. Prefer clear synchronous SQLAlchemy sessions unless a real need for async arises.
- **Frontend later:** Next.js App Router + TypeScript + Tailwind CSS; npm with committed `package-lock.json`; accessible UI, responsive layout, no unnecessary dependency stack.
- Docker Compose for **local PostgreSQL**. This is a **modular monolith**, not microservices.
- No authentication, payments, notifications, patient histories, doctor accounts, or double-booking rules unless explicitly approved as scope extensions.
- Target current stable dependencies compatible with supported runtimes; commit lockfiles and explain any material choice. Do not introduce obsolete tutorials or patterns silently.

## Behavioral contract

- Required CRUD: create, list, retrieve, edit, delete appointments; search/filter.
- Core fields: `patient_name`, `appointment_at` (timezone-aware ISO 8601), `doctor`, `appointment_type`, `status`. UUID primary key; server-managed timestamps.
- Allowed statuses: `scheduled`, `completed`, `cancelled`.
- Allowed types: `consultation`, `follow_up`, `check_up`.
- Public API: `/api/v1/appointments`; the details in `docs/API_CONTRACT.md` win over guesses.
- Input is validated at the API boundary. Appropriate response statuses; database persists data. No real clinical information.
- Do not enforce past-date rejection or booking conflicts: not required by brief.

## Work policy — small slices

1. Inspect actual files and `git status` before modifying anything. Preserve existing user edits; never overwrite or delete blindly.
2. Read and implement **only the active slice**. Summarize a short plan; then implement it, run actual relevant checks, and STOP.
3. Prefer simple, readable, cohesive code. Avoid abstraction for abstraction's sake, huge generators, premature optimization, and fragile hard-coded logic.
4. Keep backend business rules out of HTTP route handlers when separation makes code clearer. Database migrations are versioned and reviewable.
5. Add/adjust tests alongside behavior. Test happy path, invalid input, missing records, search/filter edge cases, and persistence.
6. For frontend, follow `docs/UI_DESIGN.md` strictly: compact clinic workspace, not a generic AI dashboard.
7. Avoid leaking credentials or PII into code, logs, fixtures, traces, commits, or screenshots.
8. Before finishing, provide exact files changed, test/lint/build commands and **real** results, unresolved risks, and suggested commit message. Do not state commands passed if not run.
9. Update `docs/PROGRESS.md` with verified state. Assist the human in recording **actual** prompts/reviews/fixes in `AI_USAGE.md`—never manufacture evidence.
10. **Do not automatically deploy, push, create paid resources, or change repository settings** without the candidate's explicit approval. Local implementation/verification are allowed.

## How to resolve uncertainty

- For substantive inconsistencies, highlight them and propose a minimal decision rather than inventing hidden requirements.
- Keep existing interfaces stable when adding later features. Document intentional contract changes and update tests/docs together.
- Security/privacy and data-correctness reviews must not be skipped even when moving quickly.

## Completion is not a claim

This starter contains no working backend or frontend code. `docs/PROGRESS.md` is authoritative for confirmed implementation progress. Green **scaffold** checks are not proof that CRUD exists.
