# GitHub Actions CI and optional deployment (CD)

## CI included **now**

`.github/workflows/ci.yml` runs on push to `main`, pull requests, and manual dispatch. Its jobs:

1. **Scaffold integrity:** Python standard-library check for required project documentation/AI prompt infrastructure.
2. **Backend verification:** Activates automatically when `backend/pyproject.toml` exists. Installs `.[dev]`, starts ephemeral PostgreSQL 17, runs Ruff and Pytest. B01 must establish these exact commands; B02+ must keep DB tests/migrations compatible.
3. **Frontend verification:** Activates when `frontend/package.json` exists. Requires committed `package-lock.json` and scripts `lint`, `typecheck`, `test`, and `build`; runs `npm ci` and all four scripts.

Initially backend and frontend jobs are **skipped** because no application has been created. A green scaffold job does not mean appointment functionality is implemented. Once code is added, all active checks must be green.

### Repo settings suggestion

On GitHub, consider enabling branch protection requiring the relevant status checks after first successful runs. **Do not make skipped jobs required** until they are active. `CI / scaffold` is safe to require initially; later require backend and frontend checks after they have run and are named correctly. Optionally use PRs for reviewable changes.

## Release / deployment **not enabled**

CD needs a chosen frontend host, backend host, and managed PostgreSQL. No provider has been selected, so shipping a fake working deployment workflow would be misleading and could incur costs. A **disabled example** lives at [`templates/deploy.example.yml`](templates/deploy.example.yml). It must **not** be copied into `.github/workflows` until the actual provider steps, credentials, rollback policy, and environment are known.

Suggested future flow after provider is chosen:

- CI passes for backend, frontend and E2E.
- Protected GitHub Environment (`production`) requires an explicit reviewer approval.
- Deploy backend with secrets in GitHub Environment (never committed).
- Apply Alembic migration as an explicit deploy step with backup/rollback consideration.
- Deploy frontend with only public API URL in client build.
- Smoke-test `/health`, API and frontend; record release and rollback steps.

## Security and maintenance

- GitHub Actions permissions default to `contents: read`; workflow uses minimal permissions.
- The PostgreSQL container in CI uses throwaway credentials only.
- `.github/dependabot.yml` updates GitHub Actions. Expand to npm/pip ecosystems **after** package manifests exist.
- Protect secrets and don't push to remote or provision infrastructure without candidate approval.

## Notes for AI agents

When app manifests appear, verify that workflows genuinely run and fail on incorrect code. Never silence broken tests using `continue-on-error`, empty placeholder tests, or skipped steps. Update README, this doc, and `AI_USAGE.md` to reflect real outcomes.
