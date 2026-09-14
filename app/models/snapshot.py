from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


snapshot_observations = Table(
    "snapshot_observations",
    Base.metadata,
    Column(
        "snapshot_id",
        ForeignKey("snapshots.id"),
        primary_key=True,
    ),
    Column(
        "observation_id",
        ForeignKey("observations.id"),
        primary_key=True,
    ),
)


class Snapshot(Base):
    __tablename__ = "snapshots"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    person_id: Mapped[UUID] = mapped_column(
        ForeignKey("people.id"),
        nullable=False,
    )

    captured_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )