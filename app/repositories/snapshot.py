from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Observation, Snapshot


def create_snapshot(
    session: Session,
    person_id: UUID,
    observations: list[Observation],
) -> Snapshot:
    snapshot = Snapshot(
        person_id=person_id,
        captured_at=datetime.now(timezone.utc),
    )

    snapshot.observations = observations

    session.add(snapshot)
    session.commit()
    session.refresh(snapshot)

    return snapshot


def get_snapshot(
    session: Session,
    snapshot_id: UUID,
) -> Snapshot | None:
    statement = select(Snapshot).where(
        Snapshot.id == snapshot_id
    )

    return session.execute(statement).scalar_one_or_none()