"""FastAPI router for appointment endpoints."""

from datetime import UTC, datetime, time, timedelta
from datetime import date as CalendarDate
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.appointments.models import Appointment, AppointmentStatus
from app.appointments.schemas import (
    AppointmentCreate,
    AppointmentListResponse,
    AppointmentResponse,
)
from app.core.config import settings
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
    search: str | None = Query(default=None, max_length=150),
    doctor: str | None = Query(default=None, max_length=150),
    status: AppointmentStatus | None = Query(default=None),
    date: CalendarDate | None = Query(default=None),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page (max 100)"),
    db: Session = Depends(get_db),
) -> AppointmentListResponse:
    """List appointments with database-level pagination and stable sorting."""
    filters = []
    if search and search.strip():
        text = search.strip()
        filters.append(or_(
            Appointment.patient_name.icontains(text, autoescape=True),
            Appointment.doctor.icontains(text, autoescape=True),
        ))
    if doctor is not None:
        filters.append(func.lower(Appointment.doctor) == doctor.strip().lower())
    if status is not None:
        filters.append(Appointment.status == status.value)
    if date is not None:
        timezone = ZoneInfo(settings.CLINIC_TIMEZONE)
        start = datetime.combine(date, time.min, tzinfo=timezone)
        try:
            end = datetime.combine(date + timedelta(days=1), time.min, tzinfo=timezone)
        except OverflowError:
            raise HTTPException(status_code=422, detail="Date exceeds supported range") from None
        filters.extend([
            Appointment.appointment_at >= start.astimezone(UTC),
            Appointment.appointment_at < end.astimezone(UTC),
        ])
    total = db.scalar(select(func.count()).select_from(Appointment).where(*filters)) or 0
    offset = (page - 1) * page_size

    query = (
        select(Appointment)
        .where(*filters)
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


def find_appointment(db: Session, appointment_id: UUID) -> Appointment:
    """Resolve a record or return the documented missing-record response."""
    appointment = db.get(Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: UUID, db: Session = Depends(get_db)) -> Appointment:
    return find_appointment(db, appointment_id)


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: UUID, payload: AppointmentCreate, db: Session = Depends(get_db)
) -> Appointment:
    appointment = find_appointment(db, appointment_id)
    for field, value in payload.model_dump().items():
        setattr(appointment, field, value)
    # Every accepted replacement, including an identical PUT, advances the timestamp.
    appointment.updated_at = max(
        datetime.now(UTC), appointment.updated_at + timedelta(microseconds=1)
    )
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(appointment)
    return appointment


@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: UUID, db: Session = Depends(get_db)) -> Response:
    appointment = find_appointment(db, appointment_id)
    db.delete(appointment)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    return Response(status_code=204)
