# Security and fictional-data policy

The assignment is a demonstration app. **Use fictional data only.** This still matters even if authentication is outside scope.

- Never put real names, patient/contact details, medical notes, credentials, private company files, or screenshots of production systems in the repo or AI prompts.
- Do not log request bodies containing patient names at production verbosity; never expose DB credentials or stack traces in API errors.
- `.env` and `frontend/.env.local` are ignored. Commit only `*.env.example` with local placeholders.
- Use Pydantic validation, parameterized SQL through SQLAlchemy, bounded pagination, and safe CORS origins.
- Separate non-secret `NEXT_PUBLIC_API_BASE_URL` from backend database secret.
- The local PostgreSQL password in example config is for an isolated developer machine only. Replace all secrets if deploying.
- No login/auth is implemented because the company did not require it. This is **not production-ready for sensitive patient data**. Document this limitation honestly.
- Validate any AI-suggested third-party dependencies and avoid adding needless packages.
- Never commit API keys or tokens; if one is accidentally exposed, revoke/rotate and purge it according to applicable policy.

## Verified implementation safeguards

Explicit configured CORS origins/methods, generic database-failure responses, name-free ORM repr, ISO datetime validation, enum checks, escaped parameterized search and bounded pagination are covered by regressions. Pytest requires APP_ENV=test plus a recognized test database; E2E cleans only generated IDs.

Production npm dependency audit reported 0 vulnerabilities on 2026-10-13. The development-only Next ESLint braces dependency advisory remains documented in [final review](FINAL_REVIEW.md); no forced major-version downgrade was used. No authentication or production hosting is included.
