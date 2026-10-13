# Data model / validation contract

## Appointment

| Column | Storage | Validation / meaning |
| --- | --- | --- |
| `id` | UUID PK | Server-generated, immutable |
| `patient_name` | VARCHAR(150) | Required, strip surrounding whitespace, non-empty; fictional data only |
| `appointment_at` | TIMESTAMPTZ | Required timezone-aware datetime; preserve correct instant |
| `doctor` | VARCHAR(150) | Required, trim, non-empty; stored as a string (no doctor table needed) |
| `appointment_type` | VARCHAR or DB enum | One of `consultation`, `follow_up`, `check_up` |
| `status` | VARCHAR or DB enum | One of `scheduled`, `completed`, `cancelled` |
| `created_at` | TIMESTAMPTZ | Server-managed UTC timestamp |
| `updated_at` | TIMESTAMPTZ | Server-managed; changes on update |

Use length limits and input validation as appropriate; return predictable FastAPI validation errors. A database CHECK constraint for enumerated values is useful if not using native enum. No patient/doctor master tables are required.

## JSON example

```json
{
  "patient_name": "Emma Wilson",
  "appointment_at": "2026-10-20T09:30:00+05:30",
  "doctor": "Dr. Maya Carter",
  "appointment_type": "consultation",
  "status": "scheduled"
}
```

All example names are invented. Don't seed real contacts, clinical notes, or medical history.

## Rules intentionally not introduced

No double-booking rejection, appointment duration, recurring events, patient identity matching, doctor availability schedules, or blanket ban on past appointments. If expanded, amend the requirements and tests before implementation.
