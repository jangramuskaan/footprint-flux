from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ChangeType(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"


class Change(Base):
    __tablename__ = "changes"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    snapshot_before_id: Mapped[UUID] = mapped_column(
        ForeignKey("snapshots.id"),
        nullable=False,
    )

    snapshot_after_id: Mapped[UUID] = mapped_column(
        ForeignKey("snapshots.id"),
        nullable=False,
    )

    observation_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("observations.id"),
        nullable=True,
    )

    change_type: Mapped[ChangeType] = mapped_column(
        SQLEnum(ChangeType),
        nullable=False,
    )

    old_value: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )

    new_value: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )