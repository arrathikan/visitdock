> **Current implementation:** B01–B06, F01–F03 and browser CI are implemented. Follow the root [README](README.md) to run the app and [final review](docs/FINAL_REVIEW.md) for submission. The original starter onboarding below is historical guidance.

# Start here: building VisitDock with AI

This is a ready-to-copy **project context and workflow pack**, **not** a generated working appointment application.

## 1. Extract and open

Extract the ZIP. Keep the included folder named `visitdock` and open that folder as the coding agent's workspace. If using an existing GitHub repository, copy the **contents** of `visitdock/` into its root, including hidden `.github`, `.cursor`, `.gitignore`, and `.env.example` files. Do not copy this starter over existing work without reviewing differences.

## 2. Initialize Git

If this is a new local repository:

```bash
git init
git branch -M main
python scripts/check_scaffold.py
git add .
git commit -m "chore: scaffold visitdock project context"
```

Create a GitHub repo called `visitdock` and link/push via GitHub's displayed commands. The ZIP contains **no `.git` history** and no secrets. GitHub Actions begins on push/PR when this workflow is present.

## 3. Set up local database (can be deferred until B02)

```bash
cp .env.example .env
docker compose up -d db
docker compose ps
```

- Docker maps host port **5433** to database port **5432** to reduce conflict with a locally installed PostgreSQL.
- Passwords in `.env.example` are **development placeholders only**.
- Do not put real secrets in Git.

## 4. Give AI its context

Most repo-aware agents read `AGENTS.md` or an adapter. Regardless, **paste** [`prompts/00_AGENT_ONBOARDING.md`](prompts/00_AGENT_ONBOARDING.md) at the beginning of the AI coding session so the agent explicitly confirms the repo, current state, and rules.

Then paste [`prompts/B01_BACKEND_FOUNDATION.md`](prompts/B01_BACKEND_FOUNDATION.md). Let it complete B01 **only**. Inspect code, run tests, and commit after verification. Continue with B02, B03, etc. from [`prompts/README.md`](prompts/README.md).

## 5. Review the output instead of blindly accepting AI code

For each slice, ask your friend to explain the change, inspect `git diff`, run the stated checks, and try the behavior manually. Record **real** AI assistance and corrections in `AI_USAGE.md`.

## 6. Required order

**Backend foundation → database/migration → CRUD → search/filter → backend testing/review → frontend design → frontend API integration → E2E and final review.**

Do not start the Next.js interface before the backend's contract and tests have been stabilized unless the candidate intentionally changes the plan and documents why.

## 7. At submission

Follow [`docs/SUBMISSION_CHECKLIST.md`](docs/SUBMISSION_CHECKLIST.md). Most important: the app must actually work; the user must be able to run it from the README; AI review claims must be truthful.
