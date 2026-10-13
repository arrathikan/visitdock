# Internship submission checklist

## Application behavior

- [x] Create an appointment with all five fields and persist it.
- [x] List, inspect, and update an appointment.
- [x] Delete an appointment only after UI confirmation.
- [x] Search by patient or doctor; filter by doctor/status (and optionally date).
- [x] Required field, enum, timezone and missing-record errors are helpful.
- [x] Real PostgreSQL persistence verified through API/database sessions.
- [ ] Candidate repeats the manual process-restart walkthrough before submission.

## Quality

- [x] Clean formatting/lint, manageable modules, no unnecessary abstractions.
- [x] Backend automated tests use realistic API/DB behavior.
- [x] Frontend build/lint/typecheck/unit checks pass.
- [x] Playwright real browser CRUD walkthrough passes.
- [x] Mobile viewport, keyboard use, focus states and empty/error states reviewed.
- [x] CI backend/front jobs run and pass — not merely scaffold checks.
- [x] No real patient data or committed secrets.

## Documentation and AI evidence

- [x] README updated with **actual** backend/frontend start/test instructions.
- [x] `.env.example` values match implemented code; local setup reproducible.
- [x] Alembic migration instructions and seed/fixture steps documented.
- [x] `AI_USAGE.md` contains actual AI work, genuine failures/corrections and executed checks.
- [ ] Candidate personally reviews code and writes genuine reflection.
- [x] `docs/PROGRESS.md` has final verified checkpoint.
- [x] Git commits are meaningful; working tree clean.
- [ ] Repo visibility and allowed submission procedure confirmed with company.
- [x] Automated browser screenshots use invented names only.

## Candidate explanation drill

Explain FastAPI vs Fastify, PostgreSQL choice, model and validation, routes/errors, date/time zone handling, filtering/query logic, migration flow, frontend API calls, tests, AI review/corrections, and remaining limitations.

## Follow-up review status — 2026-10-13

The earlier checked items describe standard flows and executed automated verification. They are not personal candidate attestations. See [TECHNICAL_REVIEW](TECHNICAL_REVIEW.md) for original reproductions, verified corrections and remaining verification limits.

- [x] Accepted 150-character name overflow corrected and covered by desktop/mobile cell/page/confirmation regression.
- [x] Datetime, type and status errors associated with controls; accessible-description/retention regressions passed.
- [x] Unsafe environment cases collected; ESLint 10.12 runtime compatibility verified with official Next config and active-rule probes.
- [x] Separate upstream development dependency advisory and outdated plugin peer metadata are documented.
- [ ] Continue monitoring those upstream dependencies for compatible updates.
- [x] Candidate direction, scope and verification requests documented from conversation evidence.
- [x] Reflection draft and suggested technical answers prepared without invented hands-on involvement.
- [ ] Candidate personally reviews source, performs the manual walkthrough/restart and records genuine learning.
- [ ] Company submission/visibility rules confirmed by the candidate.
