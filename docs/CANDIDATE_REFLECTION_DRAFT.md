# Candidate reflection — VisitDock

Prepared on 2026-10-13. This draft uses first person for involvement confirmed by the candidate's requests. Technical results are attributed to AI-executed verification. Personal code review, hands-on test execution and learning outcomes are not established by the conversation and are not invented here.

## My role and use of AI

I used AI assistance to continue the existing VisitDock internship project. My role in the recorded workflow was to direct the work, set its order and constraints, and request evidence for the result. I asked for the remaining backend phases to be completed before the frontend, followed by real API integration, browser testing and final documentation.

I required fictional patient data, preservation of unrelated changes and databases, small feature commits and normal Git pushes. I excluded force pushes, history rewriting and deployment without separate approval. I then requested an evidence-based technical review, an organized AI usage log and a candidate review guide.

The AI handled implementation, technical code review, automated checks and documentation preparation. I have kept those activities attributed to the AI workflow rather than presenting its test execution or defect discovery as my own.

## What the project implements

VisitDock provides appointment creation, listing, details, full updates and confirmed deletion. It supports patient/doctor search, doctor and status filters, clinic-date filtering and pagination. FastAPI validates requests; SQLAlchemy stores records in PostgreSQL; Alembic versions the schema. The Next.js frontend provides a responsive appointment workspace, create/edit drawer, delete confirmation and loading, empty and error states.

The API uses timezone-aware timestamps. Clinic-day filters convert local midnight boundaries to UTC. The form labels UTC entry explicitly, and editing another field preserves the original appointment instant, including seconds and milliseconds.

## What AI-assisted review found

One early test fixture could delete unrelated records because it used the configured database and unrestricted table cleanup. The correction requires a dedicated test database and rolls back an outer transaction instead of deleting every appointment.

Another correction prevents a doctor-only edit from losing timestamp precision. A third rejects numeric epoch inputs where the contract requires ISO datetime strings. CORS middleware and a generic database-failure response were also added and tested.

These are genuine changes visible in Git history. The current AI review checked their code and regression tests. It also found open issues: long unbroken names can overflow the layout, the datetime field does not reference its inline validation error, a test stub is not collected, and the installed lint-tool line needs maintenance. Those findings remain visible in the handoff.

## Verification evidence

The AI review reran the checks on 2026-10-13: 103 backend tests, 9 frontend tests and 4 desktop/mobile browser tests passed. Dependency consistency, Ruff, ESLint, TypeScript, the production build and Alembic schema comparison passed. The browser CRUD path used real FastAPI and PostgreSQL; failure-state tests used request interception.

GitHub Actions run [38353180884](https://github.com/arrathikan/visitdock/actions/runs/38353180884) passed for application commit bc94216, including the actual browser step. The documentation handoff has its own later commit and CI result.

Production-only npm audit reported zero vulnerabilities. The full development dependency audit reported five high entries from one lint-tool dependency chain. No production security certification, real-device Safari test or screen-reader certification is claimed.

## Personal verification status

My confirmed contribution in this record is directing the AI-assisted workflow and requesting its evidence and handoff. This draft does not claim that I personally inspected particular code files, ran commands, reproduced defects or learned specific concepts. Those statements require real personal review before inclusion in a submission.

The [candidate guide](CANDIDATE_REVIEW_GUIDE.md) supplies suggested technical answers and a manual walkthrough. The [technical review](TECHNICAL_REVIEW.md) lists the remaining engineering findings. Personal technical sign-off and company submission/visibility confirmation remain unverified.

This reflection can be used as a factual account of the recorded workflow. Any later first-person statement about hands-on review or learning should be added only after it actually occurs.
