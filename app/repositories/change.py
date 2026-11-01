from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Change


def save_change(
    session: Session,
    change: Change,
) -> Change:

    statement = select(Change).where(
        Change.snapshot_before_id == change.snapshot_before_id,
        Change.snapshot_after_id == change.snapshot_after_id,
        Change.observation_id == change.observation_id,
        Change.change_type == change.change_type,
    )

    existing_change = session.execute(statement).scalar_one_or_none()

    if existing_change is not None:
        return existing_change

    session.add(change)
    session.commit()
    session.refresh(change)

    return change


def get_change(
    session: Session,
    change_id: UUID,
) -> Change | None:
    statement = select(Change).where(
        Change.id == change_id
    )

    return session.execute(statement).scalar_one_or_none()


def get_changes_between_snapshots(
    session: Session,
    snapshot_before_id: UUID,
    snapshot_after_id: UUID,
) -> list[Change]:
    statement = select(Change).where(
        Change.snapshot_before_id == snapshot_before_id,
        Change.snapshot_after_id == snapshot_after_id,
    )

    return list(session.execute(statement).scalars().all())