# AI-assisted development and review — VisitDock

## 1. Overview

VisitDock is an internship demonstration for managing fictional clinic appointments. Its backend, frontend, tests and documentation were developed with AI assistance in small phases: B01–B06, F01–F03, Q01 and R01.

This summary separates three evidence levels:

- **Historical record:** earlier agent reports and committed diffs. A commit proves the code change, not who personally reviewed it.
- **Current AI verification:** repository inspection and commands executed by Codex during this review on 2026-10-13, against application commit `bc94216`.
- **Candidate verification:** personal review, learning and approval remain unconfirmed until the candidate records them in section 9.

The original work log, including prompts, slice results and commit references, is preserved in [AI_USAGE_HISTORY](docs/AI_USAGE_HISTORY.md). [PROGRESS](docs/PROGRESS.md) remains the chronological handoff. This is an AI-led review; no independent human review is claimed.

## 2. Tools and responsibilities

| Tool | Responsibility | Evidence boundary |
| --- | --- | --- |
| Earlier log: Gemini 3.8 Flash / Antigravity | B01–B03 backend foundation, database and create/list API | Attribution inherited from the original log; model identity and candidate involvement were not independently verified. Code and corrections are available in Git history. |
| Codex | B04–R01 implementation, regression testing, AI review and this documentation handoff | Current source, commit diffs and executed checks; candidate personal review remains pending. |
| Pytest / HTTPX / PostgreSQL | Backend API, schema, persistence and isolation checks | Real PostgreSQL; no SQLite replacement. |
| Vitest / Testing Library | Frontend request mapping, rendered states and form regressions | Mocked fetch and jsdom; not a substitute for real browser testing. |
| Playwright | Desktop/mobile CRUD and error recovery | Real API/database for CRUD; request interception for failure-state testing. |
| GitHub Actions | Repeatable checks on pushed commits | Inspect each job and actual test steps, not just a green scaffold badge. |

## 3. Development workflow

Inspect Git state and requirements → implement one feature → execute relevant checks → inspect failures/diffs → correct genuine defects → update evidence → commit and normally push → verify CI.

The repository uses a modular monolith: synchronous FastAPI/SQLAlchemy backend and a Next.js client workspace. Backend work preceded frontend integration. Feature boundaries and corrections remain visible in ordinary commits; no history rewrite or force push was used.

| Work | Commit |
| --- | --- |
| Safe test database isolation | `e6cf47a` |
| Create/list API | `1c1f057` |
| Retrieve/update/delete | `bdd831c` |
| Search, filters and clinic dates | `11239c7` |
| CORS and safe database failures | `bdd6bd0` |
| Frontend foundation / mock workspace / live integration | `54fbe99` / `288b69d` / `7cd20b8` |
| Source formatting | `8bb8e91` |
| Real browser CI | `5ccc8c4` |
| ISO validation and date boundaries | `c788ced` |
| Edit timestamp precision | `dcb268a` |
| Pinned backend dependencies | `7354eb0` |
| Final implementation documentation / CI checkpoint | `9ffebce` / `bc94216` |

## 4. AI-generated code review methodology

Compare requirements with routes, schemas, queries, migrations, UI and tests. Read the original and corrected Git versions for each claimed defect. Run the existing regression suite and inspect what the test actually proves. Check malformed inputs, timezones, missing records, database rollback, browser integration, feedback, keyboard behavior and responsive boundaries.

This review reran the entire automated suite and added temporary, uncommitted browser experiments for accepted 150-character names and datetime error descriptions. Those experiments revealed gaps that the normal passing suite does not cover. Their evidence and proposed follow-ups are in [TECHNICAL_REVIEW](docs/TECHNICAL_REVIEW.md). Application code was not changed in this documentation review.

## 5. Identified defects and corrections

### A. Test database safety — corrected in e6cf47a

**Historical risk/root cause:** the pre-fix fixture used configured `DATABASE_URL`, ran migrations without validating the target and executed `delete(Appointment)` without a WHERE clause after tests. If pointed at development, cleanup could delete unrelated records. This was confirmed by inspecting `git show e6cf47a^:backend/tests/conftest.py`; the dangerous version was not executed.

**Current correction:** [conftest.py](backend/tests/conftest.py) checks `APP_ENV=test` and a recognized test database name before migrations. Tests use an outer transaction with savepoints; API commits stay inside that transaction and teardown rolls it back. There is no table-wide delete. Auxiliary sessions share the test connection.

**Tests/outcome:** [test_isolation_guard.py](backend/tests/test_isolation_guard.py) verifies unsafe environment/database rejection and rollback. The full suite passed. Two additional CLI probes intentionally exited 1 with `pytest.UsageError` for development environment and a `visitdock` database target, before migration or connection use. Database-name checks are a practical safeguard, not a replacement for correctly provisioned isolated databases.

### B. Edit datetime precision — corrected in dcb268a

**Historical failure:** minute-only input converted `09:30:42.123Z` to `09:30:00.000Z` while changing only doctor. The prior conversion and added regression are visible in the commit diff; earlier failure output remains in the history log.

**Current correction:** [utcInstant](frontend/lib/api.ts) returns the original timestamp when the entered minute value equals the original minute value. A changed time is converted explicitly to UTC. [AppointmentForm](frontend/components/appointment-form.tsx) passes the original instant.

**Test/outcome:** the form regression “preserves timestamp precision when editing other fields” in [appointment-form.test.tsx](frontend/components/appointment-form.test.tsx) passed in this review and asserts the exact outgoing timestamp. This test uses mocked fetch; real CRUD is separately covered by Playwright.

### C. Numeric datetime coercion — corrected in c788ced

**Historical failure/root cause:** Pydantic datetime parsing accepted numeric and numeric-string epochs although the API contract requires an ISO datetime string. The earlier review recorded three responses of 201 instead of 422.

**Current correction:** [schemas.py](backend/app/appointments/schemas.py) validates string/time syntax before Pydantic parsing, then rejects missing offsets. [test_hardening.py](backend/tests/test_hardening.py) verifies integer, float and numeric-string values return 422. All three regressions passed now. The same commit guards extreme clinic-date UTC conversion; its regression also passed.

### D. Browser CORS and database responses — corrected in bdd6bd0

**Historical findings:** CORS settings existed but middleware was absent; database failures had no documented safe response. These are visible in the before/after diff. This review does not claim every historical 500 necessarily exposed credentials.

**Current correction:** [main.py](backend/app/main.py) activates explicit origin/method/header allowlists and returns generic 503 JSON for SQLAlchemy errors. Request sessions roll back and close on failure. ORM repr no longer includes names.

**Tests/outcome:** hardening tests passed for allowed preflight, rejected origin, redacted database error and name-free repr. The error regression injects an OperationalError; it does not stop a real database or test every failure mode. Browser CRUD also passed through the actual CORS path. CORS is not authentication.

### New review findings — open, not described as fixed

Accepted long unbroken names cause horizontal overflow; datetime inline errors are not linked through aria-describedby; the isolation test module contains an uncollected empty stub. The installed ESLint 9 line is end-of-life according to [ESLint's support page](https://eslint.org/version-support/). See the prioritized evidence in [TECHNICAL_REVIEW](docs/TECHNICAL_REVIEW.md). Candidate UX sign-off remains conditional on follow-up.

## 6. Regression testing evidence

Commands below were executed during this review; earlier results are preserved separately.

| Verification | Actual result |
| --- | --- |
| Backend `.venv/bin/python -m pip check` | No broken requirements found |
| `.venv/bin/ruff check .` | All checks passed |
| `APP_ENV=test DATABASE_URL=.../visitdock_test .venv/bin/python -m pytest -q --tb=short` | **103 passed in 1.96s** |
| `alembic current` on isolated database | `848b204929ed (head)` |
| `alembic check` | No new upgrade operations detected |
| `npm ci` under Node 24.19 | Clean locked install succeeded; audit/deprecation findings reported below |
| `npm run lint` / `npm run typecheck` | Passed |
| `npm run test` | **9 passed** in four files |
| `npm run build` | Production webpack build passed |
| `PLAYWRIGHT_CHANNEL=chrome npm run test:e2e` | **4 passed in 21.3s**, real PostgreSQL CRUD on desktop/mobile |
| Full npm audit / production-only audit | **5 high dependency-chain entries / 0 vulnerabilities** |

GitHub run [38353180884](https://github.com/arrathikan/visitdock/actions/runs/38353180884), for `bc94216`, was independently retrieved: all four jobs succeeded, including the actual real PostgreSQL browser step. That evidence predates this documentation commit; its new run is reported after push. [Browser setup](docs/BROWSER_TESTING.md) documents the exact isolated service commands.

## 7. Architecture and implementation decisions

Repository decisions, not unconfirmed candidate personal choices:

- FastAPI/Pydantic handle HTTP validation; SQLAlchemy parameterized statements handle persistence. PostgreSQL TIMESTAMPTZ preserves instants; Alembic versions the schema.
- Search is a literal case-insensitive patient-or-doctor match. Optional exact doctor/status/date filters combine with AND. SQL count/offset/limit and appointment-time/UUID ordering provide bounded pagination.
- Clinic midnight boundaries are converted to UTC, including 23/25-hour DST days. Form entry explicitly uses UTC; frontend/public and backend clinic settings must match.
- A client workspace and typed fetch helper avoid an unnecessary state framework. Native dialogs support modal focus and Escape; request cancellation limits stale search responses.
- No authentication, booking conflicts, payments or deployment were required. Tests use fictional records only. Lockfiles/snapshots record tested dependencies.

## 8. Limitations

Passing tests cover the specified scenarios, not all input or accessibility cases. The new long-name and error-description findings remain open. No real-device iOS/Safari, screen-reader certification or formal WCAG audit was performed. No manual server-restart walkthrough was executed in this review.

Full npm audit still reports five high entries in the development-only Next ESLint → fast-glob → micromatch → braces chain. The [braces advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) concerns deeply nested-pattern denial of service and lists no patched version. Production-only npm audit reported zero; this is not a comprehensive security certification. A maintained, compatible lint-tool upgrade needs separate verification. No forced major downgrade was used.

This review checked Python dependency consistency, not a Python CVE scanner. The application has no authentication and must not handle sensitive patient data. Concurrent edits are last-write-wins. Earlier B01–B03 tool/model and human-validation claims remain inherited, not personally attested.

## 9. Candidate Review — Confirmed Involvement and Verification Status

This completed account uses the candidate's instructions in this conversation as evidence of participation. It does not infer personal code inspection or test execution from ownership of the repository or Git author metadata.

### Candidate account

I used AI assistance to continue the existing VisitDock repository and complete its planned implementation phases. I directed the order of work: finish the backend first, then build the frontend, integrate the real API, add browser tests and prepare the final documentation.

I required the work to use fictional patient data, preserve unrelated changes and databases, avoid force pushes and history rewrites, and leave deployment outside the approved scope. I asked for feature-sized commits and normal pushes to GitHub.

I requested real automated verification, GitHub Actions evidence, review of earlier AI-generated corrections and a candidate-friendly handoff. I also requested an organized AI usage log and reflection draft. The AI implemented and reviewed the code and executed the technical checks recorded in this document. These results are attributed to the AI workflow.

The review records corrections for unsafe test cleanup, datetime precision loss, numeric datetime coercion and browser/database error handling. It also records open UX and dependency findings. The documentation preserves those AI findings and results with their verification limits.

### Verification status

| Activity | Status supported by the conversation |
| --- | --- |
| Directed continuation, work order and scope | Confirmed by candidate requests |
| Required fictional data, database preservation and safe Git operations | Confirmed by candidate requests |
| Requested feature commits, pushes, tests, CI and final review | Confirmed by candidate requests |
| Requested documentation and reflection preparation | Confirmed by candidate requests |
| Personally inspected source files or ran the checks | Not established by this record |
| Personally reproduced the manual CRUD/restart walkthrough | Not established by this record |
| Demonstrated understanding of the architecture or corrections | Suggested answers provided in the guide; personal understanding not assessed |
| Confirmed company submission/visibility rules | Not established by this record |

The narrative of confirmed involvement is complete. Personal technical sign-off remains unverified and must not be represented as completed. The [candidate review guide](docs/CANDIDATE_REVIEW_GUIDE.md) provides a practical walkthrough and self-study answers; the [reflection draft](docs/CANDIDATE_REFLECTION_DRAFT.md) uses the same evidence boundaries.
