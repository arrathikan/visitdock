# Copy-ready prompt B04 — Details, update, delete

Implement **only B04**. Read `AGENTS.md`, `docs/API_CONTRACT.md`, current `docs/PROGRESS.md`; inspect Git state and existing handlers.

Deliver:
- `GET /api/v1/appointments/{id}`: 200 or 404.
- `PUT /api/v1/appointments/{id}`: replace all editable fields, validate like create, persist, return updated 200 or missing 404. Define and test `updated_at` change.
- `DELETE /api/v1/appointments/{id}`: 204 empty response or 404; deletion verified by subsequent lookup.
- Invalid UUID is 422. No internal stack trace leaks.
- Real database-backed API tests for each path and validation/error case.

Constraints: No auth, doctor master table, frontend, conflict detection, or advanced filtering in this slice.

Run lint and tests, report exact changed files, verified results and code-review issues; update progress; STOP for candidate review/commit.
