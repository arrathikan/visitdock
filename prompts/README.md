# AI prompt library — follow in order

**How to use:** Give your repo-aware AI tool [`00_AGENT_ONBOARDING.md`](00_AGENT_ONBOARDING.md) once at the beginning of the session, then paste **only one** implementation prompt at a time. All prompts assume the agent has read `AGENTS.md` and `docs/PROGRESS.md`. Do not ask it to implement the entire app in one shot.

| Order | Prompt | Exit condition |
| --- | --- | --- |
| 0 | [`00_AGENT_ONBOARDING.md`](00_AGENT_ONBOARDING.md) | Agent understands current repo and scope; no code edited. |
| B01 | [`B01_BACKEND_FOUNDATION.md`](B01_BACKEND_FOUNDATION.md) | FastAPI `/health`, basic backend tests + Ruff |
| B02 | [`B02_DATABASE_MIGRATIONS.md`](B02_DATABASE_MIGRATIONS.md) | PostgreSQL connection, Appointment model, Alembic migration |
| B03 | [`B03_CREATE_LIST.md`](B03_CREATE_LIST.md) | POST + GET list, persisted and tested |
| B04 | [`B04_GET_UPDATE_DELETE.md`](B04_GET_UPDATE_DELETE.md) | Detail, edit, delete and 404 cases |
| B05 | [`B05_SEARCH_FILTERS.md`](B05_SEARCH_FILTERS.md) | Search, status/doctor/date filters, pagination |
| B06 | [`B06_BACKEND_HARDENING.md`](B06_BACKEND_HARDENING.md) | Edge cases + backend review and docs |
| F01 | [`F01_FRONTEND_FOUNDATION.md`](F01_FRONTEND_FOUNDATION.md) | Next.js shell + VisitDock tokens and tooling |
| F02 | [`F02_APPOINTMENTS_UI.md`](F02_APPOINTMENTS_UI.md) | Date-first, responsive appointment workspace |
| F03 | [`F03_FORMS_AND_INTEGRATION.md`](F03_FORMS_AND_INTEGRATION.md) | Real API CRUD form, filters, delete confirmation |
| Q01 | [`Q01_E2E_AND_CI.md`](Q01_E2E_AND_CI.md) | E2E, CI checks, real smoke passes |
| R01 | [`R01_FINAL_REVIEW.md`](R01_FINAL_REVIEW.md) | Candidate walkthrough + accurate documentation |
| Optional | [`D01_DEPLOYMENT_OPTIONAL.md`](D01_DEPLOYMENT_OPTIONAL.md) | Only after hosting approval; deployment is not required |

**Per-slice rule:** inspect → implement minimal scope → test and review → summarize results → update `docs/PROGRESS.md` and `AI_USAGE.md` with actual evidence → candidate commits. Stop after each slice.
