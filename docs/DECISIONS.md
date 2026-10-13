# Architecture Decision Log

## Accepted at project start

| Decision | Why | Trade-off |
| --- | --- | --- |
| Backend first | Candidate preference; stabilize API for frontend | UI comes later |
| Python FastAPI (not Fastify) | Python stack with automatic OpenAPI and Pydantic | Separate frontend/backend processes |
| PostgreSQL + Alembic | Real persistence and migration discipline | Docker or local PostgreSQL setup |
| Simple service / feature modules | Easy to review in internship project | Avoid excessive abstraction |
| Single `appointments` table | Matches provided requirements without invented domain models | Doctor and patient are text, not entities |
| UUID IDs and timezone-aware datetimes | Stable public identifiers and correct instants | Need careful serialization/date filtering |
| Restrained VisitDock UI | Real receptionist workflow instead of template aesthetics | Requires intentional visual review |
| CI in GitHub Actions | Reviewers can see repeatable verification | CI checks must evolve as code is added |
| Deployment deferred | Hosting provider unknown; no reason to guess secrets/resources | Optional CD configured only after target selected |

## Add later decisions here

Use: `YYYY-MM-DD — Decision — Context — Alternatives — Consequences`. If an AI suggestion changes an accepted decision, document it and update affected tests/docs.
