# Copy-ready prompt D01 — Optional deployment only after explicit approval

This is **not** part of the required take-home scope. Do not run this prompt unless the candidate has selected a hosting provider and approved associated costs, domains, secrets, and GitHub environment configuration.

Read `AGENTS.md`, `docs/CI_CD.md`, `docs/SECURITY_AND_PRIVACY.md`, and current repo/progress. Ask for **only missing material choices** (frontend host, backend host, PostgreSQL host, rollout method), then propose a real provider-specific deployment plan, secrets in GitHub Environment, Alembic migrate step, smoke tests and rollback procedure.

The packaged `docs/templates/deploy.example.yml` intentionally fails and **must not** be activated as production CD. Never replace the guard with fake shell echoes or claim CD is configured without verifying live deployment. Do not provision paid infrastructure or push/deploy without explicit approval.
