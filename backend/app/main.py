"""FastAPI application entrypoint and route configuration for VisitDock."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.appointments.router import router as appointments_router
from app.core.config import settings

app = FastAPI(
    title="VisitDock API",
    version="0.1.0",
    description="VisitDock Clinic Appointment Management API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)


@app.exception_handler(SQLAlchemyError)
async def database_error(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Return a safe failure without SQL, credentials or appointment details."""
    return JSONResponse(status_code=503, content={"detail": "Appointment service unavailable"})


app.include_router(appointments_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Lightweight process health check."""
    return {"status": "ok"}
