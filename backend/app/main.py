from fastapi import FastAPI

app = FastAPI(
    title="VisitDock API",
    version="0.1.0",
    description="VisitDock Clinic Appointment Management API",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Lightweight process health check."""
    return {"status": "ok"}
