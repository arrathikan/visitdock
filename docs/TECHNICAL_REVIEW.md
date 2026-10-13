# VisitDock technical review and verification

Date: 2026-10-13, Asia/Colombo. Reviewed application commit: `bc94216b07912ef2ad5bc68e1f539b4350fa0c5b`, branch `main`, remote `https://github.com/arrathikan/visitdock.git`. Checkout was clean and matched origin/main before edits. This is an AI-led review; candidate and independent human sign-off are not established.

## Assessment

The required API and standard UI flows are implemented and their automated checks passed again. Historical safety/precision/validation/CORS corrections were checked against actual current code and Git diffs. Two additional UX defects were reproduced outside the existing suite. **Documentation handoff is prepared; unconditional UX/submission sign-off remains pending.** This documentation task records findings without changing application behavior.

## Current open findings

### Medium — accepted long names overflow desktop and mobile

Evidence: [globals.css](../frontend/app/globals.css), lines 189–215, defines table/cells without wrapping long tokens. [workspace.tsx](../frontend/components/workspace.tsx) displays accepted names directly. The API accepts up to 150 characters for patient and doctor.

Reproduction: in a temporary Playwright experiment, intercept only the list response with a fictional patient `Fictional` + 141 `X` characters and doctor `Fictional` + 141 `Y` characters. Each name has 150 characters. No database record is created. After rendering the row, compare document scrollWidth to innerWidth:

| Viewport | Document scrollWidth | Outcome |
| --- | --- | --- |
| 1280px desktop | 3203px | Horizontal overflow |
| 390px mobile | 1492px | Horizontal overflow |

Follow-up: wrap long patient/doctor tokens without hiding essential information and add a desktop/mobile maximum-length regression. Existing Playwright overflow assertions pass for ordinary short fictional names; they do not cover this case. Resolve before claiming all accepted input remains responsive.

### Low — datetime inline error lacks its field description association

Evidence: [appointment-form.tsx](../frontend/components/appointment-form.tsx), lines 116–119. The time input always has `aria-describedby="time-help"`; its rendered validation span has id `appointment_at-error` but is not included in that attribute.

Reproduction: use a valid fictional form and intercept its POST with a 422 validation error for appointment_at. Browser DOM inspection returned describedBy `time-help` and inline error id `appointment_at-error`. The error is visible and a general alert is present, but its specific message is not associated with the input for assistive technology.

Follow-up: include both help and conditional error IDs and verify the accessible description. This is a DOM/semantic finding, not a claim of an executed screen-reader test. Type/status error spans also lack explicit description wiring by code inspection; the browser reproduction targeted the datetime field.

### Low — unused test stub is not coverage

Evidence: [test_isolation_guard.py](../backend/tests/test_isolation_guard.py), lines 12–14: `invalid_env_raises_usage_error` contains only pass and its name does not match pytest's test prefix. It is not among the 103 collected/passing tests. Other real tests cover development/production rejection; this stub adds no assertions for staging/empty strings.

Follow-up: remove it or turn it into a real parametrized guard test. Do not count its four parameters as tested cases. The actual guard still rejects every value other than `test` by direct code inspection.

### Medium maintenance concern — installed ESLint line is unsupported

Evidence: [package.json](../frontend/package.json) pins ESLint 9.39.5; clean npm ci emitted a deprecation warning. The [official support page](https://eslint.org/version-support/) confirms ESLint 9 reached end-of-life on 2026-08-06. Lint currently passes, but ongoing maintenance is absent for that line.

Follow-up: verify a maintained version with the current Next ESLint configuration in a separate dependency change. No version compatibility or upgrade success is presumed here.

### Known development dependency advisory — still present

Full npm audit reports five high entries from the same Next ESLint/fast-glob/micromatch/braces dependency chain; production-only audit reports zero. The [primary advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) lists deeply nested-pattern denial of service in braces <=3.0.3 with no patched version. The reviewed application does not pass appointment input to lint glob patterns. This limits exposure; it does not erase the development-tool finding. No unsafe forced downgrade or fabricated fix is claimed.

## Backend review

- **HTTP structure:** main registers the feature router under /api/v1. Health is process-only. Sync sessions suit this small monolith; a repository/service layer is not required for the current rule size.
- **Validation:** trimmed names, 150-character limit, enum fields, forbidden client metadata, ISO-string pre-validation and timezone requirement. POST and full PUT use the same schema. UUID parsing gives 422; missing records use documented 404 JSON.
- **Transactions:** create/update/delete commit, roll back on exceptions and refresh response objects where needed. The dependency closes sessions and rolls back failures. SQLAlchemy exceptions receive generic 503; the regression injects a failure rather than stopping PostgreSQL.
- **Persistence/schema:** UUID key, TIMESTAMPTZ, server timestamp defaults, enum CHECK constraints and query indexes agree with the migration. PostgreSQL tests and Alembic check passed. Separate test sessions share an outer test transaction; real browser requests exercise actual commits.
- **Search/filter:** parameterized SQL predicates, escaped LIKE wildcards, AND-combined optional filters, accurate filtered count, bounded SQL pagination and time/UUID ordering.
- **Timezone:** validated IANA configuration, local-day UTC windows with exclusive next midnight. Colombo and New York DST boundary regressions passed; extreme conversion returns 422.
- **Isolation:** APP_ENV/test-name guard occurs before migration. Savepoint rollback replaces whole-table deletion. Current CLI probes rejected unsafe targets before DB use. Name-based safeguards require correct database provisioning; they are not a production access-control boundary.

No new confirmed backend functional defect was identified in the exercised scope. This is not proof that every adversarial boundary or deployment configuration works.

## Frontend review

App Router shell, client workspace, typed fetch mapping and native modal components remain small and understandable. All five editable fields are present. Create/edit retain inputs on failure; 404/422/network errors are mapped; delete requires cancel/confirmation. Search is debounced and aborted on change. Pagination is bounded by API totals, with recovery after deleting the final row on a page. UTC input and clinic display are labelled; unchanged time preserves the original instant.

Labels, visible focus, skip link, dialog semantics and Escape/focus restoration are implemented. Browser tests verified ordinary mobile layout and keyboard close/restoration. The two UX findings above qualify broader responsiveness/accessibility claims. TypeScript passing is compile-time evidence, not runtime validation of arbitrary remote JSON. No screen-reader or real-device Safari test is claimed.

## Actual verification in this review

| Check | Command/result |
| --- | --- |
| Python dependencies | `.venv/bin/python -m pip check`: no broken requirements |
| Backend lint | `.venv/bin/ruff check .`: passed |
| API/database suite | `APP_ENV=test DATABASE_URL=.../visitdock_test .venv/bin/python -m pytest -q --tb=short`: **103 passed in 1.96s** |
| Unsafe target probes | development/test-db and test/development-db combinations: expected exit 1, pytest.UsageError before migration/connect |
| Alembic | current: **848b204929ed (head)**; check: **No new upgrade operations detected** |
| Frontend clean install | Node 24.19, `npm ci`: succeeded, 452 packages added; dev advisory/deprecation warnings recorded |
| Frontend quality | lint/typecheck passed; Vitest **9 passed** in 4 files; production webpack build passed |
| Real browser tests | installed Chrome via PLAYWRIGHT_CHANNEL; **4 passed in 21.3s** on desktop/mobile, real test DB for CRUD |
| Edge experiments | list-only mock for long strings and mocked 422 for field description; reproduced findings, not counted as passing regression tests |
| Dependency audit | full: 5 high; `--omit=dev`: 0 |
| Existing GitHub CI | run **38353180884**, commit bc94216: all four jobs and real PostgreSQL browser step succeeded |

No migration downgrade, development-data cleanup, deployment, history rewrite or real patient input occurred. Temporary review servers were stopped. Backend Pytest and real browser CRUD were not run concurrently against the same test DB. The prior local Chromium download failed; this review used installed Chrome. CI uses installed Playwright Chromium. Python CVE scanning and manual server restart are outside the checks executed here.

## Historical correction verification

| Correction | Historical evidence | Current code/test evidence | Candidate status |
| --- | --- | --- | --- |
| A: unsafe cleanup | e6cf47a parent fixture and correction diff | guarded setup + outer rollback; guard/rollback tests and CLI probes passed | No personal attestation |
| B: edit precision | dcb268a diff and prior failed regression record | utcInstant original-value branch; exact outgoing timestamp form assertion passed | No personal attestation |
| C: numeric datetime | c788ced diff and prior 201-vs-422 failures | before-validator and three 422 regressions passed | No personal attestation |
| D: CORS/DB errors | bdd6bd0 before/after main.py | allowed/rejected preflight and generic 503 tests passed; real browser CRUD passed | No personal attestation |

Details and limits are in [AI_USAGE](../AI_USAGE.md). Dangerous historical cleanup was inspected, never executed during this review. Prior failure results were not falsely relabelled as new executions.

## Documentation and candidate handoff

The AI log is organized into nine requested sections with a qualified historical archive. The [candidate guide](CANDIDATE_REVIEW_GUIDE.md) contains code-reading priorities, questions and manual checks; the [reflection draft](CANDIDATE_REFLECTION_DRAFT.md) uses first person for confirmed candidate direction and separates it from AI-executed checks and unverified hands-on review. Existing progress/final-review/submission documents point to this fresh review.

Candidate next steps: understand A–D, review the open findings, resolve or explicitly record acceptable limitations, personally exercise CRUD and restart persistence, fill genuine reflection, verify CI at the commit being submitted, and confirm company visibility/submission rules. No candidate completion statement is invented.
