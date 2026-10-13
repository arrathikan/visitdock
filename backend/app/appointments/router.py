"""FastAPI router for appointment endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.appointments.models import Appointment
from app.appointments.schemas import (
    AppointmentCreate,
    AppointmentListResponse,
    AppointmentResponse,
)
from app.db.session import get_db

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new appointment",
    description="Create and persist a new clinic appointment with validated details.",
)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
) -> Appointment:
    """Create a new appointment and persist it to PostgreSQL."""
    appointment = Appointment(
        patient_name=payload.patient_name,
        appointment_at=payload.appointment_at,
        doctor=payload.doctor,
        appointment_type=payload.appointment_type.value,
        status=payload.status.value,
    )
    db.add(appointment)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(appointment)
    return appointment


@router.get(
    "",
    response_model=AppointmentListResponse,
    status_code=status.HTTP_200_OK,
    summary="List appointments",
    description="Retrieve a paginated list of clinic appointments ordered deterministically.",
)
def list_appointments(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page (max 100)"),
    db: Session = Depends(get_db),
) -> AppointmentListResponse:
    """List appointments with database-level pagination and stable sorting."""
    total = db.scalar(select(func.count()).select_from(Appointment)) or 0
    offset = (page - 1) * page_size

    query = (
        select(Appointment)
        .order_by(Appointment.appointment_at.asc(), Appointment.id.asc())
        .offset(offset)
        .limit(page_size)
    )
    items = list(db.scalars(query).all())

    return AppointmentListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )
