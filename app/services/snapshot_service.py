from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Observation, Snapshot
from app.repositories.snapshot import create_snapshot as repository_create_snapshot
from app.repositories.snapshot import get_snapshot as repository_get_snapshot


def create_snapshot(
    session: Session,
    person_id: UUID,
    observations: list[Observation],
) -> Snapshot:
    return repository_create_snapshot(
        session=session,
        person_id=person_id,
        observations=observations,
    )


def get_snapshot(
    session: Session,
    snapshot_id: UUID,
) -> Snapshot | None:
    return repository_get_snapshot(
        session=session,
        snapshot_id=snapshot_id,
    )