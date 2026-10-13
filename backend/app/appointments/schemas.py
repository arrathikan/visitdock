"""Pydantic v2 schemas for appointment requests and responses."""

import uuid
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator

from app.appointments.models import AppointmentStatus, AppointmentType


class AppointmentCreate(BaseModel):
    """Payload schema for creating a new clinic appointment."""

    model_config = ConfigDict(extra="forbid")

    patient_name: str
    appointment_at: datetime
    doctor: str
    appointment_type: AppointmentType
    status: AppointmentStatus

    @field_validator("patient_name", "doctor")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Trim leading/trailing whitespace and enforce length bounds."""
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Field must not be empty or contain only whitespace.")
        if len(trimmed) > 150:
            raise ValueError("Field must not exceed 150 characters.")
        return trimmed

    @field_validator("appointment_at", mode="before")
    @classmethod
    def validate_iso_datetime_string(cls, value: object) -> str:
        """Reject epoch coercion: the API contract requires an ISO datetime string."""
        if not isinstance(value, str) or "T" not in value.upper():
            raise ValueError("Datetime must be an ISO 8601 string with time and timezone.")
        return value

    @field_validator("appointment_at")
    @classmethod
    def validate_timezone_aware(cls, value: datetime) -> datetime:
        """Ensure the datetime contains an explicit timezone offset."""
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError(
                "Datetime must include an explicit timezone offset or 'Z' (e.g., +00:00, Z)."
            )
        return value


class AppointmentResponse(BaseModel):
    """Serialized representation of a persisted appointment."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    patient_name: str
    appointment_at: datetime
    doctor: str
    appointment_type: AppointmentType
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    @field_serializer("appointment_at", "created_at", "updated_at", when_used="json")
    def serialize_utc_datetime(self, dt: datetime) -> str:
        """Serialize datetime values to standard ISO 8601 UTC representation."""
        utc_dt = dt.astimezone(UTC) if dt.tzinfo is not None else dt.replace(tzinfo=UTC)
        return utc_dt.isoformat().replace("+00:00", "Z")


class AppointmentListResponse(BaseModel):
    """Paginated list response containing appointment items and pagination metadata."""

    items: list[AppointmentResponse]
    total: int
    page: int
    page_size: int
