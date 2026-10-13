"""SQLAlchemy ORM models for appointments."""

import uuid
from datetime import datetime
from enum import StrEnum

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AppointmentType(StrEnum):
    """Allowed appointment types."""

    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    CHECK_UP = "check_up"


class AppointmentStatus(StrEnum):
    """Allowed appointment statuses."""

    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Appointment(Base):
    """Appointment entity for clinic bookings."""

    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    patient_name: Mapped[str] = mapped_column(
        sa.String(150),
        nullable=False,
    )
    appointment_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    doctor: Mapped[str] = mapped_column(
        sa.String(150),
        nullable=False,
        index=True,
    )
    appointment_type: Mapped[str] = mapped_column(
        sa.String(50),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        sa.String(50),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )

    __table_args__ = (
        sa.CheckConstraint(
            "appointment_type IN ('consultation', 'follow_up', 'check_up')",
            name="check_appointment_type_valid",
        ),
        sa.CheckConstraint(
            "status IN ('scheduled', 'completed', 'cancelled')",
            name="check_appointment_status_valid",
        ),
    )

    def __repr__(self) -> str:
        return f"<Appointment(id={self.id}, status={self.status!r})>"
