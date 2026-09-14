from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    source_id: Mapped[UUID] = mapped_column(
        ForeignKey("sources.id"),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    key: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    value: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )