# AI Assistance, Review, and Corrections Log

> **Starter state:** No AI-generated application implementation exists yet. This document is a **template**, not evidence that any application tests, review, or corrections have been performed.

The take-home task explicitly allows AI, and evaluators want to understand **how AI suggestions were checked and corrected**. Record truthful, candidate-owned decisions. Do not fabricate a bug, a fix, a prompt, or a result.

## Tools used (fill in as actually used)

| Tool / model | Task performed | Date / slice | Human validation |
| --- | --- | --- | --- |
| Gemini 3.8 Flash (Medium) / Antigravity | B01 FastAPI backend foundation, tests, configuration, documentation | 2026-10-13 / B01 | Verified commands, tests, endpoints, and diffs |

## Slices

### B01 FastAPI backend foundation — 2026-10-13

- **Goal:** Establish minimal, maintainable FastAPI backend foundation with `GET /health`, PEP 621 packaging compatible with CI `pip install -e ".[dev]"`, Pytest automated tests, and Ruff linting.
- **AI tool used:** Gemini 3.8 Flash (Medium) via Antigravity IDE
- **Prompt / reference:** [`prompts/B01_BACKEND_FOUNDATION.md`](prompts/B01_BACKEND_FOUNDATION.md)
- **AI suggestion/output:** Created `backend/pyproject.toml`, `backend/app/main.py`, `backend/app/core/__init__.py`, `backend/tests/test_health.py`, `backend/README.md`.
- **What was checked:**
  - Verified PEP 621 metadata compatibility with `pip install -e ".[dev]"`.
  - Checked `ruff check .` output.
  - Checked `python -m pytest -q` output.
  - Inspected starlette deprecation warning regarding TestClient and added appropriate pytest warning filters.
  - Tested live uvicorn server startup and curled `/health` and `/docs`.
  - Validated markdown links with `scripts/check_scaffold.py`.
- **Issue found:** During initial pytest execution, `StarletteDeprecationWarning` was surfaced during import of `TestClient` in Starlette 1.7.0. Added explicit filter in `pyproject.toml` so test runs are clean and predictable.
- **Correction and reason:** Configured `filterwarnings` in `[tool.pytest.ini_options]` in `backend/pyproject.toml`.
- **Commands actually run and outcome:**
  - `python3 -m venv backend/.venv`: Exit code 0.
  - `./.venv/bin/python -m pip install -e ".[dev]"`: Exit code 0.
  - `./.venv/bin/ruff check .`: Exit code 0 (All checks passed).
  - `./.venv/bin/python -m pytest -q`: Exit code 0 (5 passed).
  - `curl http://localhost:8000/health`: HTTP 200 OK `{"status":"ok"}`.
  - `curl http://localhost:8000/docs`: HTTP 200 OK Swagger UI.
  - `python3 scripts/check_scaffold.py`: Exit code 0 (Starter checks passed).
- **Candidate review & reflection:**
  - _Candidate to review and record notes before final submission._

## Entry template — copy this section for each meaningful slice

### [Slice ID] [Short title] — [date]

- **Goal:**
- **AI tool used:**
- **Prompt / reference:** Link to `prompts/...` or summarize any ad hoc question.
- **AI suggestion/output:**
- **What I manually checked:** Files, edge cases, review method.
- **Issue I found:** Specific flaw **if one was actually found**; otherwise write “none found in this review.”
- **Correction and reason:** Include links to commit/diff if possible.
- **Commands actually run and outcome:**
- **What I learned / would improve:**

## Final reflection — complete before submission

Explain which decisions were human-made, how the candidate validated AI output, what genuine defects were fixed, and what limitations remain. Avoid vague claims such as “AI built everything perfectly.”
