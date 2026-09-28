from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Change
from app.repositories.change import (
    save_change as repository_save_change,
    get_change as repository_get_change,
    get_changes_between_snapshots as repository_get_changes_between_snapshots,
)


def save_change(
    session: Session,
    change: Change,
) -> Change:
    return repository_save_change(
        session=session,
        change=change,
    )


def get_change(
    session: Session,
    change_id: UUID,
) -> Change | None:
    return repository_get_change(
        session=session,
        change_id=change_id,
    )


def get_changes_between_snapshots(
    session: Session,
    snapshot_before_id: UUID,
    snapshot_after_id: UUID,
) -> list[Change]:
    return repository_get_changes_between_snapshots(
        session=session,
        snapshot_before_id=snapshot_before_id,
        snapshot_after_id=snapshot_after_id,
    )