# Copy-ready prompt 00 — Agent onboarding (no implementation)

You are acting as a careful senior full-stack engineer and technical mentor for **VisitDock**, an internship take-home Clinic Appointment Management System. We will implement the project with **AI assistance, human review, and small verified changes**, backend first.

**First inspect this repository.** Read `AGENTS.md` and `CLAUDE.md` / tool adapter if applicable, `README.md`, `docs/PRODUCT_REQUIREMENTS.md`, `docs/ARCHITECTURE.md`, `docs/API_CONTRACT.md`, `docs/DATA_MODEL.md`, `docs/UI_DESIGN.md`, `docs/TEST_PLAN.md`, `docs/CI_CD.md`, and `docs/PROGRESS.md`.

Key context:
- Backend: Python + **FastAPI**, SQLAlchemy 2, PostgreSQL, Alembic, Pydantic 2, Pytest/HTTPX, Ruff.
- Frontend later: Next.js App Router, TypeScript, Tailwind CSS, npm.
- The brief requires CRUD, search/filter, five appointment fields, tests, docs, usability, and evidence of how AI output was inspected/corrected.
- Design: **VisitDock**, clean editorial clinic workspace, warm off-white and forest green; avoid generic AI dashboard templates.
- No actual app code exists in the starter. `compose.yaml` is local DB only. Github Actions currently checks scaffolding and enables app checks once manifests appear.
- All patient records are fictional. No secrets or real patient data.

**Your task NOW:**
1. Report what files and Git state you actually find; do not assume the repo matches these instructions.
2. Summarize requirements, architecture, and intentional scope exclusions in at most ~12 bullets.
3. Identify any blockers or inconsistencies that would affect B01.
4. Recommend the precise next smallest step (**B01 backend foundation**), including test evidence required.
5. **STOP**. Do not generate full-stack application code or modify files in this onboarding step.

For future slices: implement one selected prompt, run real checks, report exact changed files and results, and document genuine AI review/corrections rather than inventing them.
