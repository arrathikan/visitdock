# Final AI review — 2026-10-13

## Verdict

Implementation and automated acceptance checks are complete for the agreed fictional-data internship scope. Human candidate code review, personal reflection and submission/visibility confirmation remain pending. No deployment was performed or authorized. This is an AI-led audit, not a fabricated independent human review.

## Confirmed findings and corrections

| Severity | Evidence / reproduction | Result |
| --- | --- | --- |
| Medium | `frontend/lib/api.ts:66`: editing only doctor converted 09:30:42.123 to 09:30:00.000. Added form regression failed before correction. | Preserve the original instant when minute input is unchanged; regression passes. Commit dcb268a. |
| Medium | `backend/app/appointments/schemas.py:33`: numeric and numeric-string epoch values bypassed the ISO string contract; three regressions returned 201. | Require ISO date/time strings; all three return 422. Commit c788ced. |
| Low | `backend/app/appointments/router.py:83`: date 0001-01-01 in Asia/Colombo overflowed converting midnight to UTC; regression reproduced exception. | Guard both start/end UTC conversions; invalid boundary returns 422. Commit c788ced. |
| Medium | Backend CI originally installed open-ended dependency ranges. | Added tested dependency snapshot and used it in CI; fresh Python 3.13 environment installs, pip check and 103 tests pass. Commit 7354eb0. |
| Documentation | README, progress, AI log, API/architecture/test/CI docs retained contradictory starter-state assertions. | Updated current state and actual commands while preserving historical checkpoint evidence. |

Earlier B06 fixes activated explicit CORS, sanitized database 503 responses and removed names from ORM repr. Q01 failures were test locators and timeout-invalidated cleanup, not fabricated application defects; the genuine failures/corrections are logged in AI_USAGE.

## Verification actually executed

- Fresh pinned Python 3.13 environment: install, `pip check`, `ruff check .`, dedicated PostgreSQL `APP_ENV=test ... python -m pytest -q`: **103 passed**.
- Alembic current and upgrade head on visitdock_test: revision **848b204929ed**. No destructive downgrade performed by Codex.
- Frontend Node 24.19: `npm run lint`, `npm run typecheck`, `npm run test`: **9 passed**; `npm run build`: production build passed.
- `PLAYWRIGHT_CHANNEL=chrome npm run test:e2e`: **4 passed** against real PostgreSQL/FastAPI, desktop and Chromium-emulated mobile. Desktop/mobile screenshots inspected and overflow assertion passed. The API-failure test alone intercepts network responses.
- Q01 GitHub run [38351468077](https://github.com/arrathikan/visitdock/actions/runs/38351468077): scaffold, detection, backend, frontend and actual real PostgreSQL browser step all succeeded. Final implementation/build commit 7354eb0 also passed [run 38352870395](https://github.com/arrathikan/visitdock/actions/runs/38352870395); subsequent documentation-only CI is reported in the conversation.
- Production `npm audit --omit=dev`: **0 vulnerabilities**. Full npm audit: five high entries from one development-only braces/micromatch/fast-glob chain under Next ESLint. The advisory [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) describes deeply nested-pattern denial of service. No user pattern reaches this lint path; do not treat untrusted lint configuration as safe. Audit suggested a major Next ESLint downgrade, which was not applied. Track an upstream compatible fix.

## Security and scope

All added test and preview records are explicitly fictional. SQLAlchemy uses parameterized predicates; LIKE search escapes wildcards. Page sizes are bounded; sorting and filtered counts are stable. Database tests use a recognized test database and savepoint rollback. E2E deletes only its own record ID; two interrupted-run leftovers were individually identified and removed. No table-wide cleanup, force push, history rewrite, repository settings change or deployment occurred.

The app intentionally has no authentication, rate limiting, conflict detection or clinical information. CORS is an origin policy, not authentication. Do not host it for sensitive or real patient data. Normal concurrent edits use last-write-wins; optimistic locking is outside the brief. UTC form entry is explicit; public clinic timezone must match backend configuration. No real-device iOS/Safari, Firefox, screen-reader or formal WCAG certification is claimed; mobile checks use Chromium emulation.

## Two-minute demo

1. Start PostgreSQL, apply Alembic, start API and UI using README. Show empty book and fictional-only notice.
2. Create a fictional appointment with patient, doctor, UTC date/time, type and status.
3. Search its patient/doctor, apply clinic date/status/doctor filters, then clear them.
4. Edit doctor/status in the drawer; verify retained fields and saved row. Explain UTC storage and clinic date windows.
5. Open deletion, cancel once, then confirm. Show disappearance and API 404.
6. Show passing CI and genuine AI review regressions. Candidate explains validation, test isolation and remaining deployment/authentication limitations.

## Candidate-owned remaining actions

Review code and the AI corrections personally, add genuine reflection to AI_USAGE.md, confirm company repository visibility/submission rules, and submit according to the company's process. The implementation agent cannot truthfully complete these human-owned checks.
