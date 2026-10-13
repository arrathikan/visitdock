# VisitDock UI — anti-generic visual brief

## Concept

**A calm clinic reception workspace, not a generic SaaS dashboard.** Compact, deliberately organized, quick to scan, with an editorial touch. Working title/brand throughout: **VisitDock**. Tagline (optional): “Every appointment in its place.”

## Tokens

| Token | Value | Use |
| --- | --- | --- |
| Canvas | `#F8F7F3` | Warm off-white application background |
| Primary | `#245C50` | Forest-green actions / accents |
| Ink | `#25332B` | Primary text |
| Border | `#E3E7DF` | Quiet separators |
| Secondary text | `#6A776E` | Supporting details |
| Caution | `#B6694B` | Destructive confirmations / subdued warning |

Typography: **Instrument Sans** is a good base font; optionally **Newsreader** for a rare display heading only. Use tabular numerals for appointment times. Default radii **6–8px**, thin borders, barely any shadows.

## Main screen — Appointments workspace

- Small **top navigation** with brand and 1–2 destinations. No permanent sidebar for such a tiny app.
- Useful title, selected date, New Appointment primary action.
- Search field and clear, compact filters (doctor, status, date). Include reset/clear filters and result count.
- Scannable appointment table/rows with date/time, patient, doctor, type, status, and edit/delete actions.
- Pagination or another simple predictable bounded list behavior.
- Create/edit form as a desktop side drawer, full-screen sheet on mobile. Good labels, keyboard/focus management, inline validation, Cancel/Save actions.
- Deletion requires a deliberate confirmation dialog with focus management.
- Clear loading, empty, no-results, API failure and success states.
- Optional mini-calendar or week schedule **only after** required CRUD and testing are done.

## Anti-patterns

**Avoid** purple gradients, neon status badges, enormous KPI cards, random medical illustrations, glassmorphism, shadcn demo styling left uncustomized, excessive rounded corners, heavy shadows, meaningless analytics, marketing hero sections, and dense giant sidebars.

## Responsive behavior

- Desktop: compact grid/table with aligned times and actions.
- Mobile: stacked appointment rows with time/date/patient/doctor/status and accessible overflow actions; forms become full-screen.
- Meet practical WCAG principles: contrast, labels, keyboard access, visible focus, dialog semantics, clear errors.

## Design review before calling done

Can someone find a patient in seconds? Is the date timezone understandable? Can they fix a mistake without losing inputs? Are errors helpful? Does it feel like real reception software rather than a template?
