# Copy-ready prompt B06 — Backend quality gate

Review the **entire implemented backend** of VisitDock before starting frontend. Read `AGENTS.md`, `docs/PRODUCT_REQUIREMENTS.md`, `docs/API_CONTRACT.md`, `docs/TEST_PLAN.md`, `docs/SECURITY_AND_PRIVACY.md` and `docs/PROGRESS.md`.

First **audit without editing**: compare required features to actual routes, migrations, validation, database tests, CI, error behavior, timezones, deterministic queries, privacy, and README run commands. Enumerate real findings by severity with file/line evidence. Do not invent bugs.

Then fix only confirmed high/medium issues within backend scope, add regression tests and rerun Ruff/Pytest/real DB migration smoke checks. Do not add new product features.

Update `docs/PROGRESS.md` and guide the candidate to record genuine prompts/review/corrections in `AI_USAGE.md`. Provide changed files, exact checks/results, remaining risks, concise commit suggestion. STOP. Frontend starts at F01 only after verified backend passes.
