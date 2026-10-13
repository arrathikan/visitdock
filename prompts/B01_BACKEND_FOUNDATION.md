# Copy-ready prompt B01 — FastAPI foundation

Implement **only B01** for VisitDock. Read `AGENTS.md`, `docs/PROGRESS.md`, and the API/architecture/CI docs; inspect `git status` and existing files first. Preserve existing work.

Deliver:
- Minimal `backend/` Python FastAPI application and clear feature-oriented project structure; avoid premature abstractions.
- `GET /health` returning HTTP 200 with a small stable JSON body such as `{"status":"ok"}`.
- `backend/pyproject.toml` with compatible app + `[project.optional-dependencies].dev` (or equivalent PEP 621 config) including pytest, HTTPX and Ruff, so the **existing CI command** `pip install -e ".[dev]"` works.
- A focused automated HTTP-level health test and Ruff setup.
- Working local create-venv/install/run/test commands in README/`docs/LOCAL_DEVELOPMENT.md`.
- Update `docs/PROGRESS.md` with actual verified results.

Constraints: Do **not** add PostgreSQL connection, ORM entities, migrations, appointment routes, frontend, or unrelated dependencies in B01. No fake test reports.

Run `ruff check .` and `python -m pytest -q` inside `backend/` and state results; if a required tool cannot run, state the blocker. Review diff and explain any human-check-worthy generated code. Recommend concise commit message and **STOP**; don't auto-push.
