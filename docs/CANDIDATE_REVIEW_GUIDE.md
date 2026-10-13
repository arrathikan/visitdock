# VisitDock candidate review guide

Prepared on 2026-10-13, Asia/Colombo. This guide is a study aid and manual verification plan. Suggested answers describe the implemented code; they do not attest that the candidate wrote, reviewed or executed it personally. The automated review and its limits are recorded in [TECHNICAL_REVIEW](TECHNICAL_REVIEW.md).

## Explain the application

VisitDock is a fictional clinic reception workspace. A Next.js client sends JSON requests to FastAPI; Pydantic validates the five appointment fields; a request-scoped SQLAlchemy session reads or commits PostgreSQL records. Alembic manages the schema. The backend and frontend are separate folders in one repository, with no extra service or state-management framework.

The API implements create, paginated list, single-record retrieval, full update and deletion. Search matches patient or doctor; optional status, exact doctor and clinic-date filters combine. UUIDs and timestamps are server-managed. Missing records return 404, invalid input returns 422, successful deletion returns an empty 204, and database failures return a generic 503.

Appointments store instants in TIMESTAMPTZ. The form explicitly accepts UTC, while the list and date filter use the configured clinic timezone. A local clinic day becomes an inclusive start and exclusive next midnight in UTC, including daylight-saving transitions. No authentication, booking conflicts, clinical histories or deployment are included.

## Read these files first

| File | What to understand |
| --- | --- |
| [README](../README.md), [API_CONTRACT](API_CONTRACT.md), [DATA_MODEL](DATA_MODEL.md) | Setup, endpoints, fields, validation and timezone contract. |
| [main.py](../backend/app/main.py) | Router registration, CORS and generic database-failure response. |
| [router.py](../backend/app/appointments/router.py) | CRUD commits, lookup/404, combined filters, SQL pagination and day boundaries. |
| [schemas.py](../backend/app/appointments/schemas.py) | Trimmed names, enums, forbidden metadata and ISO-string/offset validation. |
| [models.py](../backend/app/appointments/models.py), [initial migration](../backend/alembic/versions/848b204929ed_create_appointments_table.py) | UUID, TIMESTAMPTZ, constraints and indexes; model/migration agreement. |
| [session.py](../backend/app/db/session.py), [conftest.py](../backend/tests/conftest.py) | Request session lifecycle versus isolated test transactions. |
| [workspace.tsx](../frontend/components/workspace.tsx) | Search cancellation, filters, pagination, drawer and delete confirmation. |
| [appointment-form.tsx](../frontend/components/appointment-form.tsx), [api.ts](../frontend/lib/api.ts) | Field errors, HTTP handling, UTC conversion and preserved precision. |
| [dialog.tsx](../frontend/components/dialog.tsx), [globals.css](../frontend/app/globals.css) | Modal behavior, focus and responsive styling. |
| [browser tests](../frontend/e2e/appointments.spec.ts), [CI workflow](../.github/workflows/ci.yml) | Real API/database coverage versus intercepted errors, and executed CI jobs. |

## Five technical questions with suggested answers

### 1. What happens when someone creates an appointment?

The frontend gathers all five fields, trims the names and converts the labelled UTC input to an ISO timestamp. POST reaches the appointment router after Pydantic validation. SQLAlchemy adds and commits the model, then refreshes it for the response. FastAPI returns 201 with generated ID and timestamps. The UI closes the form and reloads the list. Invalid fields produce 422; failed requests keep the form available for correction. Database exceptions roll back and receive a generic 503 response.

### 2. Why does PUT require all editable fields, and how do 404 and 422 differ?

The contract defines full replacement, so PUT reuses the required create schema. The server finds the UUID and replaces all editable fields, preserves created_at and advances updated_at, including an identical replacement. A malformed UUID or invalid/missing field returns 422 at the input boundary. A valid UUID with no record returns 404. The frontend fetches current details before opening edit; an unchanged minute input preserves the original timestamp's seconds and milliseconds.

### 3. How do search, filters and pagination work together?

Search uses a case-insensitive literal substring across patient name OR doctor, with LIKE wildcard characters escaped. Exact doctor, status and clinic-date conditions are added with AND. The server counts the filtered rows, then applies bounded SQL offset/limit and orders by appointment_at and UUID. The response contains items, total, page and page_size. This avoids fetching the whole database into the browser and makes equal appointment times deterministic. Offset pagination can still shift under concurrent inserts; the application does not promise snapshot consistency.

### 4. Why use a clinic timezone when storage and form entry use UTC?

An instant and a calendar day are different concepts. PostgreSQL TIMESTAMPTZ represents the instant; UTC input avoids ambiguous daylight-saving wall times. Reception staff filter the clinic's local day, so the backend converts its midnight boundaries to UTC before querying. A daylight-saving day may span 23 or 25 hours. Backend CLINIC_TIMEZONE and frontend NEXT_PUBLIC_CLINIC_TIMEZONE must match; changing public frontend settings requires rebuilding. Tests cover Colombo and New York boundaries, but passing those examples is not proof of every possible timezone configuration.

### 5. What do the tests prove, and how are records protected during testing?

Backend tests use real PostgreSQL and migrations. The fixture requires APP_ENV=test and a recognized dedicated test database before migrating. Tests run inside an outer transaction with savepoints, so application commits remain within that transaction and teardown rolls it back. Playwright uses a separate test database service in CI, makes real API commits and deletes only IDs it created. Frontend unit tests use mocked fetch/jsdom; browser interception covers failure feedback. These layers verify their specific scenarios, not full accessibility or security certification. CORS controls allowed browser origins; it is not authentication.

## Three genuine AI defects and corrections to explain

Read the original/corrected versions and the regression before describing a correction as your own review. The historical attribution and executed evidence are in [AI_USAGE](../AI_USAGE.md) and [AI_USAGE_HISTORY](AI_USAGE_HISTORY.md).

| Correction | Original defect | Actual fix and evidence |
| --- | --- | --- |
| [e6cf47a](https://github.com/arrathikan/visitdock/commit/e6cf47a) — test database safety | The earlier fixture used the configured database and deleted every appointment during cleanup. A wrong target could destroy development records. | Validate environment/database before migrations; replace table-wide deletion with outer-transaction/savepoint rollback. Read conftest and [guard tests](../backend/tests/test_isolation_guard.py). Inspect the dangerous historical version only; do not execute it. |
| [dcb268a](https://github.com/arrathikan/visitdock/commit/dcb268a) — edit timestamp precision | Changing only another field could turn 09:30:42.123Z into 09:30:00.000Z through minute-only form conversion. | utcInstant returns the original instant when the minute input is unchanged. [Form regression](../frontend/components/appointment-form.test.tsx) asserts the exact outgoing timestamp. Its request is mocked; real CRUD is covered separately. |
| [c788ced](https://github.com/arrathikan/visitdock/commit/c788ced) — numeric datetime coercion | Pydantic accepted numeric and numeric-string epochs despite the ISO-string API contract. Earlier regressions returned 201 instead of 422. | A before-validator requires a string with time syntax; subsequent validation requires an offset. [Hardening tests](../backend/tests/test_hardening.py) cover integer, float and numeric-string rejection. |

## Manual fictional CRUD and restart walkthrough

This is a plan to execute, not a claim of a completed candidate walkthrough. Follow [README](../README.md) for installation and service startup. Use only your local fictional development records; keep automated tests on visitdock_test. Do not run Pytest and browser CRUD concurrently against the same test database.

1. Confirm the backend and frontend clinic timezone settings match. For this example use the documented UTC defaults, and open http://localhost:3000. Choose a unique fictional name such as **Fictional Candidate Walkthrough 20261013**, doctor **Dr Fictional Demo**, time **2026-10-20 09:30 UTC**, type **Consultation** and status **Scheduled**. Save and verify the success notice and row.
2. In http://localhost:8000/docs, list appointments using the unique search string. Copy that record's generated UUID, retrieve it by ID and record its appointment_at, created_at and updated_at. Keep the UUID for targeted cleanup.
3. Search by part of the fictional patient name and then by doctor. Combine the exact doctor filter with Scheduled and clinic date 2026-10-20. Check the expected single result, an intentionally unmatched filter and Clear filters. If using another clinic timezone, derive the expected displayed day from the same instant.
4. Edit the created row: change the doctor to **Dr Fictional Review** and status to **Completed**. Save, retrieve the same UUID again and verify the changed fields, unchanged appointment instant/created_at and advanced updated_at. Check keyboard navigation; Escape should close an open drawer and restore focus.
5. Stop the API with Ctrl+C in its own terminal and restart it with the same documented command and database settings. Reload the browser and retrieve the UUID again. The edited record should persist because the request committed to PostgreSQL. Record the actual result. A browser reload alone is not evidence of server-restart persistence.
6. Optionally restart only the local PostgreSQL container with docker compose restart db, then verify the record again after the database is ready. This is an additional check, not required evidence already gathered by the AI. Preserve the volume; never use down -v, reset the schema or delete unrelated records.
7. Open Delete and choose **Keep appointment**; confirm the record remains. Then open it again and confirm **Delete appointment**. Verify the row disappears and GET by its recorded UUID returns 404. Remove only this walkthrough's own record.
8. Try an empty required field in the form and an invalid enum or offset-less datetime in API docs. Verify the actual validation response. Inspect a narrow viewport and the review findings below; do not report all accepted inputs as responsive merely because the ordinary name fits.

Write the date, actual commands/actions, expected versus observed results, and any failures in the personal reflection only after executing them. Do not use another person's or an agent's result as your own.

## Findings to review before sign-off

At application commit bc94216, the AI review reproduced horizontal overflow for accepted 150-character unbroken patient/doctor names: a 1280px viewport had document width 3203px; a 390px viewport had width 1492px. It also reproduced a datetime inline error whose ID was missing from the field's aria-describedby. Code inspection found an uncollected pass-only isolation-test stub and an unsupported ESLint 9 dependency line. These are open findings, not completed fixes. The development-only braces advisory also remains documented.

Use [TECHNICAL_REVIEW](TECHNICAL_REVIEW.md) for exact reproductions, severity and limits. Recheck the submitted commit if application code or dependencies change. No screen-reader or real-device Safari verification is claimed.

## Verify CI for the commit being submitted

The historical verified checkpoint is commit bc94216b07912ef2ad5bc68e1f539b4350fa0c5b and [run 38353180884](https://github.com/arrathikan/visitdock/actions/runs/38353180884). Its four jobs succeeded, including the real PostgreSQL browser step. A later documentation commit needs its own matching run; the older green run does not attest to a newer commit.

1. Read the current commit with git rev-parse HEAD and confirm the normal push placed it on the intended remote branch.
2. Open [GitHub Actions](https://github.com/arrathikan/visitdock/actions). Select the run whose head commit exactly matches the submitted commit, not just the most recently displayed green badge.
3. Inspect scaffold, manifest detection, backend and frontend job results. Ensure app jobs were executed rather than skipped. Inspect backend test totals, frontend unit tests/build, and **Real PostgreSQL browser CRUD on desktop and mobile**. Scaffold validates file packaging/links only.
4. Record the full commit SHA, run URL, conclusion and actual relevant test totals in the handoff. If a run is pending or failed, say so and inspect its logs; do not mark it verified before completion.

Optional CLI inspection uses gh run list --branch main --limit 5 --json databaseId,headSha,status,conclusion,url and gh run view RUN_ID. Substitute the selected actual run ID. These are instructions, not claimed executions by the candidate.

## Personal sign-off checklist

Leave an item unchecked until it reflects your actual involvement.

- [ ] I can trace a create/edit request through frontend, schema, route and database commit.
- [ ] I personally read the files/commits I identify in my reflection and understand the three corrections above.
- [ ] I executed the fictional CRUD/restart walkthrough and recorded its real results or explicit limitations.
- [ ] I can explain what each automated test layer covers and what it does not cover.
- [ ] I reviewed the open UX, accessibility and dependency findings and recorded a real resolution or acceptance decision.
- [ ] I checked the GitHub CI run that matches the exact submitted commit.
- [ ] My [AI_USAGE](../AI_USAGE.md) and [reflection draft](CANDIDATE_REFLECTION_DRAFT.md) distinguish my actual direction/review from AI implementation and verification.
- [ ] I confirmed the company's repository visibility/submission instructions and approved the final wording.

Personal sign-off is not established by generating this guide. Candidate name/date and completed evidence must come from actual participation.
