# Test strategy and acceptance checks

> Verified locally: 106 backend tests and 12 frontend unit tests. The browser suite contains six desktop/mobile cases, including maximum-length name wrapping; verified results are recorded in PROGRESS.md. CI run evidence is recorded in PROGRESS.md.

## Backend tests (Pytest + HTTPX + PostgreSQL)

- Process health: `/health` returns 200 and stable JSON.
- Create: valid payload -> 201; GET returns persisted record.
- Validation: blank name/doctor; missing field; invalid enum; offset-less or malformed datetime; overlong strings -> 422.
- Read: existing UUID -> 200; missing valid UUID -> 404; malformed UUID -> 422.
- Update: edit each field -> 200, persisted; missing record -> 404.
- Delete: valid -> 204 and is no longer fetchable; missing -> 404.
- Filter: search matches patient or doctor case-insensitively; filters combine; unknown values return empty list; invalid query -> 422.
- Pagination: stable sort, total/page/page_size, empty page, size bounds.
- Date boundary: day filter respects configured IANA timezone, including edge-of-day cases.
- Database integration: real PostgreSQL and **Alembic migrations**, not just mocks or SQLite substituted for Postgres-specific behavior.
- Error behavior: 500s not leaked as raw stack traces; dependencies isolated across tests.

## Frontend checks

- Accessible labels, valid keyboard tab order, form validation, buttons and dialog semantics.
- Loading, empty list, no search results, API error, success feedback.
- Responsive desktop/mobile layouts; no horizontal overflow of form controls.
- Search/filter UI serializes correct backend parameters and displays results.
- Date/time shown in documented timezone.

## E2E smoke (Playwright)

1. Load app; verify appointment workspace.
2. Create fictional appointment.
3. Search and view it.
4. Edit doctor or status; verify saved update.
5. Filter by status; verify result.
6. Delete after confirmation; confirm absence.

## Manual candidate walkthrough

Use FastAPI `/docs` to test API first; then exercise UI in real browser. Include invalid input, empty database, and narrow phone-sized viewport. Screenshot only fictional records.

## Quality commands (to be introduced as code lands)

- Backend: `python -m pytest -q`, `ruff check .` in `backend/`.
- Frontend: `npm run lint`, `npm run typecheck`, `npm run test`, `npm run build` in `frontend/`.
- E2E: `npx playwright test` once configured.
- CI always validates scaffold; app jobs run when their manifests exist.

## Policy

Do not claim a passing command unless it actually ran successfully. Failures are evidence for improvement and can be documented in `AI_USAGE.md`.

See [BROWSER_TESTING](BROWSER_TESTING.md) for exact service setup, isolation, request interception boundaries and browser commands. Final audit added regressions for numeric datetime coercion, extreme date conversion and preserving seconds/milliseconds during edit. Those regressions failed before correction and passed afterward.

## Follow-up regressions

- Accepted 150-character unbroken patient/doctor names remain fully rendered inside table/mobile cells and confirmation dialogs without page overflow. The list-only fixture is mocked; no database row is created for this layout test.
- Date/time validation describes both the UTC help and its inline error. Type/status controls also expose specific errors; unit tests assert accessible descriptions and retained values.
- The environment rejection test now collects development, production, staging and empty-string cases. The pure guard is called before database use.
- ESLint 10.12 compatibility is verified with the official Next config, project lint/types/build and intentional invalid-code probes. Stale plugin peer warnings and the known dev audit chain remain disclosed.
