# Copy-ready prompt B05 — Search, filters, pagination

Implement **only B05**, following `docs/API_CONTRACT.md` exactly. Read `AGENTS.md`, `docs/ARCHITECTURE.md`, and current progress; inspect repo state.

Add query support for `search` (case-insensitive substring of patient_name OR doctor), `doctor` (case-insensitive exact trimmed match), `status`, optional `date` (calendar day in configured IANA `CLINIC_TIMEZONE`), `page`, and `page_size` (1–100). Combine filters safely, sort by appointment_at ascending with UUID tie-break, return `{items,total,page,page_size}`.

Use SQLAlchemy parameterized filters; never concatenate raw SQL. Convert clinic-date start/end into UTC to query TIMESTAMPTZ correctly, including boundary tests. Avoid fetching every row into Python to filter or paginate.

Test search, combined filters, empty matches, invalid inputs, page bounds, and deterministic ordering with real PostgreSQL. Update API docs/progress only when verified. Run lint and full backend tests. Report true outcome and STOP.
