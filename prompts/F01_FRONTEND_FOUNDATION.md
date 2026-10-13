# Copy-ready prompt F01 — Next.js + VisitDock visual foundation

Backend contract and tests should be stable before starting. Read `AGENTS.md`, `docs/API_CONTRACT.md`, `docs/UI_DESIGN.md`, `docs/PROGRESS.md`, `docs/CI_CD.md`; inspect the actual repo and Git state.

Implement **only F01**:
- Initialize `frontend/` Next.js App Router + TypeScript + Tailwind using a compatible **current stable** stack and **npm**; commit generated `package-lock.json`.
- Create a clean top navigation/app shell, VisitDock wordmark and design tokens: canvas `#F8F7F3`, forest `#245C50`, ink `#25332B`, muted borders; accessible keyboard/focus defaults.
- Establish scripts `lint`, `typecheck`, `test`, `build` that genuinely execute. Add one small test for a rendered UI element; ensure the existing GitHub workflow can run.
- Provide `.env.local` guidance matching `frontend/.env.example`; no DB credentials in browser.

No API integration or big appointments UI yet. Avoid generic gradients, giant stats, sidebar, glassmorphism, and uncustomized component-library presets. Run lint/typecheck/test/build; report actual results, changed files and progress. STOP.
