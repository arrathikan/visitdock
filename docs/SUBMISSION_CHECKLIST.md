# Internship submission checklist

## Application behavior

- [ ] Create an appointment with all five fields and persist it.
- [ ] List, inspect, and update an appointment.
- [ ] Delete an appointment only after UI confirmation.
- [ ] Search by patient or doctor; filter by doctor/status (and optionally date).
- [ ] Required field, enum, timezone and missing-record errors are helpful.
- [ ] App works after restart against PostgreSQL.

## Quality

- [ ] Clean formatting/lint, manageable modules, no unnecessary abstractions.
- [ ] Backend automated tests use realistic API/DB behavior.
- [ ] Frontend build/lint/typecheck/unit checks pass.
- [ ] Playwright real browser CRUD walkthrough passes.
- [ ] Mobile viewport, keyboard use, focus states and empty/error states reviewed.
- [ ] CI backend/front jobs run and pass — not merely scaffold checks.
- [ ] No real patient data or committed secrets.

## Documentation and AI evidence

- [ ] README updated with **actual** backend/frontend start/test instructions.
- [ ] `.env.example` values match implemented code; local setup reproducible.
- [ ] Alembic migration instructions and seed/fixture steps documented.
- [ ] `AI_USAGE.md` contains truthful prompts, candidate review, real fixes, tests and reflection.
- [ ] `docs/PROGRESS.md` has final verified checkpoint.
- [ ] Git commits are meaningful; working tree clean.
- [ ] Repo visibility and allowed submission procedure confirmed with company.
- [ ] Optional short demo/screenshots use invented names only.

## Candidate explanation drill

Explain FastAPI vs Fastify, PostgreSQL choice, model and validation, routes/errors, date/time zone handling, filtering/query logic, migration flow, frontend API calls, tests, AI review/corrections, and remaining limitations.
