# CI and deployment boundaries

`.github/workflows/ci.yml` runs on pushes to main, pull requests and manual dispatch. Permissions are `contents: read`; concurrent older runs on the same ref are cancelled.

- Scaffold: checks required documentation and local links.
- Backend: Python 3.13, pinned requirements-dev.lock, ephemeral PostgreSQL 17 `visitdock_test`, Ruff and real Pytest integration tests (106 cases).
- Frontend: Node 24, npm ci, lint, typecheck, 12 unit tests and production build. A separate PostgreSQL 17 service in this job supports Alembic, FastAPI and production Next.js startup, followed by six Playwright Chromium desktop/mobile tests, including maximum-length name layout. Failed checks fail the job.

The Q01 run [38351468077](https://github.com/arrathikan/visitdock/actions/runs/38351468077) succeeded, with all four jobs and the actual PostgreSQL browser step executed. Later audit fixes and final handoff runs are recorded in [PROGRESS](PROGRESS.md).

No deployment is enabled. The optional [disabled deployment example](templates/deploy.example.yml) remains outside active workflows. Deployment, paid services and repository settings require explicit approval. Local example passwords and CI credentials are fictional disposable values; do not reuse them for deployment.

Branch protection is a candidate/repository-owner decision. Require active checks only; no settings were changed by this task. Browser traces/reports stay in ignored local directories. See [browser instructions](BROWSER_TESTING.md) for local reproduction.
