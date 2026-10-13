# Copy-ready prompt Q01 — Browser E2E + GitHub Actions quality gate

Read `AGENTS.md`, `docs/TEST_PLAN.md`, `docs/CI_CD.md`, `docs/SUBMISSION_CHECKLIST.md`, and progress. Inspect Git state and current workflow.

Implement Playwright E2E test with **fictional** records covering create → search/view → edit → filter → delete. Make test data deterministic and isolated; document how to run against FastAPI, PostgreSQL and Next.js locally and in CI. Avoid flaky sleeps; use stable locators and condition-based waits. Verify API/backend tests and frontend lint/typecheck/unit tests/build continue to work.

Integrate E2E into CI **only if its database + backend + frontend service setup is real and repeatable**. If CI E2E is not feasible in this slice, document the exact blocker rather than adding a fake passing step.

Run what is available, review failed cases, report exact results and changed files, update progress and genuine `AI_USAGE.md`. STOP.
