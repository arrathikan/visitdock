# REST API contract — v1 (planned)

> This describes the **intended interface**. None of these application endpoints exist in the starter.

**Base path:** `/api/v1`  
**Content type:** `application/json`  
**Fields:** snake_case, including `appointment_at`; timestamps include timezone offset or `Z`.

## Endpoints

| Method | Endpoint | Response | Purpose |
| --- | --- | --- | --- |
| GET | `/health` | 200 | Lightweight process health; implemented in B01 |
| POST | `/api/v1/appointments` | 201 + object | Create appointment |
| GET | `/api/v1/appointments` | 200 + paginated list | List/search/filter appointments |
| GET | `/api/v1/appointments/{id}` | 200 + object, or 404 | Retrieve one |
| PUT | `/api/v1/appointments/{id}` | 200 + object, or 404 | Replace editable fields |
| DELETE | `/api/v1/appointments/{id}` | 204 with empty body, or 404 | Delete one |

## Create / replace request

```json
{
  "patient_name": "Emma Wilson",
  "appointment_at": "2026-10-20T09:30:00+05:30",
  "doctor": "Dr. Maya Carter",
  "appointment_type": "consultation",
  "status": "scheduled"
}
```

## Response object (illustrative)

```json
{
  "id": "07aa3705-ef58-432b-87d9-3d3a838ca00e",
  "patient_name": "Emma Wilson",
  "appointment_at": "2026-10-20T04:00:00Z",
  "doctor": "Dr. Maya Carter",
  "appointment_type": "consultation",
  "status": "scheduled",
  "created_at": "2026-10-13T08:00:00Z",
  "updated_at": "2026-10-13T08:00:00Z"
}
```

## List / filters

`GET /api/v1/appointments?search=emma&status=scheduled&doctor=Dr.%20Maya%20Carter&date=2026-10-20&page=1&page_size=20`

- `search`: case-insensitive substring match against **patient name or doctor**.
- `status`: exact enum value; optional.
- `doctor`: optional case-insensitive exact match after trimming.
- `date`: optional ISO `YYYY-MM-DD`; means the day in configured `CLINIC_TIMEZONE` (default `UTC`), not necessarily a UTC day.
- `page`: integer >= 1, default 1.
- `page_size`: integer 1–100, default 20.
- Combine filters with AND; search matches either text field with OR.
- Sort by `appointment_at ASC`, then `id ASC` for stable pagination.

Response:

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 20
}
```

## Errors

- `422` Pydantic validation error for malformed IDs, missing/invalid fields, invalid enum/date/page values, and datetime without timezone.
- `404` JSON `{"detail": "Appointment not found"}` when an existing-format UUID does not identify a record.
- `204` no body on successful delete.
- Do not expose SQL statements, internal tracebacks, DB credentials, or personal information in error messages.

## OpenAPI

FastAPI `/docs` and `/openapi.json` become available when the backend is implemented. The API contract and tests should stay in sync.
