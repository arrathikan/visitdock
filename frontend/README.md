# VisitDock frontend

Next.js App Router, React, TypeScript and Tailwind. Node >=24.15 is required; verified locally with Node 24.19. Dependencies are pinned in package.json and package-lock.json.

```bash
cp .env.example .env.local
npm ci
npm run dev
```

Open http://localhost:3000 with the API on port 8000. Only public API URL and clinic timezone belong in frontend environment configuration. Rebuild after changing public values. The frontend clinic timezone must match backend `CLINIC_TIMEZONE`; UTC is the default. Forms explicitly enter UTC, while list dates use clinic time.

```bash
npm run lint
npm run typecheck
npm run test
npm run build
npm start
npm run format
```

The nine unit tests cover rendered headings, request/query mapping, error/retry handling, form validation/input retention and edit timestamp precision. The native dialog supplies focus containment and Escape support, with focus restoration on close. The drawer is full-screen on mobile. Search requests are debounced and cancelled to prevent stale results.

See [browser instructions](../docs/BROWSER_TESTING.md) for real desktop/mobile CRUD tests and test-database setup. The production build uses webpack for predictable local and CI builds; no external font download is required. Georgia and system sans fallbacks implement the editorial visual direction without an extra font network dependency.
