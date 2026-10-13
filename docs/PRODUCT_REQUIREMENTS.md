# Product requirements — VisitDock

## Context

Build a **small web application to manage appointments** as an internship take-home assignment. The reviewer checks correctness, code structure, problem-solving, AI usage and review, tests, documentation, and overall usability.

## Users and intended workflow

The primary user is a fictional clinic receptionist or coordinator. They open a practical appointments workspace, find the relevant day/appointment, add or change a booking, and remove a booking after confirmation.

## Must-have features / acceptance criteria

| ID | Requirement | Acceptance criteria |
| --- | --- | --- |
| R1 | Create appointment | Persist a valid appointment with all five required fields; show useful errors for invalid input. |
| R2 | View appointments | Show a list of persisted appointments plus details for a single record. |
| R3 | Edit appointment | Update any required field and reliably persist the change. |
| R4 | Delete appointment | Explicit confirmation in UI, then remove the target appointment; missing ID responds appropriately. |
| R5 | Search/filter | Text search by patient name and doctor; filtering by status and doctor; optional date-based selection in final UI. |
| R6 | Test data | All demonstrated records are clearly fictional; no real personal/clinical/company information. |
| R7 | Usability | Responsive UI; loading/empty/error states; accessible form labels and keyboard operability. |
| R8 | Testing / docs | Automated API tests, a browser E2E happy path, clear local setup, and genuine AI-review evidence. |

## Required data fields

1. Patient Name
2. Appointment Date and Time
3. Doctor
4. Appointment Type
5. Status

App-owned metadata (`id`, `created_at`, `updated_at`) is permitted.

## Explicit non-goals

- Real patient records, sensitive medical information, doctor scheduling accounts, authentication/authorization
- Billing, email/SMS, appointment reminders, multi-tenant hospitals
- AI chatbot, real-time websockets, microservices, Kafka, Kubernetes
- Automatic slot conflict checking; no business rule for it was specified
- Production deployment unless candidate chooses one later

## Definition of done

Running local app; all CRUD + search/filter paths pass manual walkthrough; PostgreSQL holds data; API tests pass; Playwright happy-path passes; instructions reproducible; GitHub Actions app jobs green; candidate can explain architecture and actual AI reviews/corrections.
