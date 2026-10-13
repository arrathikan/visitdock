# Copy-ready prompt B03 — Create and list appointments

Implement **only B03**. Read root `AGENTS.md`, `docs/API_CONTRACT.md`, `docs/DATA_MODEL.md`, and current progress. Inspect existing code and Git state.

Deliver:
- Pydantic v2 create/response schemas with trimmed required patient/doctor names, allowed type/status values, timezone-aware `appointment_at`, and safe bounds.
- `POST /api/v1/appointments` returns 201 with UUID and server-managed timestamps, persists into PostgreSQL.
- `GET /api/v1/appointments` returns stable `{items,total,page,page_size}`; page/page_size can be basic now, full filters come in B05.
- Focused API integration tests using real PostgreSQL for happy path and several invalid-input cases. Use fictional fixtures only.
- Ensure `/docs` reflects endpoint contracts.

Constraints: Do not add get-one, edit, delete, filters, frontend, authentication or scheduling conflict logic in B03.

Run lint, tests, and manual Swagger checks when available. Report exact evidence, limitations, changed files and suggested commit; update `docs/PROGRESS.md`; STOP.
