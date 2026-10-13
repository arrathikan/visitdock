"""FastAPI application entrypoint and route configuration for VisitDock."""

from fastapi import FastAPI

from app.appointments.router import router as appointments_router

app = FastAPI(
    title="VisitDock API",
    version="0.1.0",
    description="VisitDock Clinic Appointment Management API",
)

app.include_router(appointments_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Lightweight process health check."""
    return {"status": "ok"}
