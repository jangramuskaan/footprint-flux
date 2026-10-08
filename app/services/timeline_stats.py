from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Change, ChangeType, Snapshot


def get_timeline_stats(
    session: Session,
    person_id: UUID,
) -> dict:
    snapshots = (
        session.execute(
            select(Snapshot)
            .where(Snapshot.person_id == person_id)
            .order_by(Snapshot.captured_at.asc())
        )
        .scalars()
        .all()
    )

    changes = (
        session.execute(
            select(Change)
            .join(
                Snapshot,
                Change.snapshot_after_id == Snapshot.id,
            )
            .where(Snapshot.person_id == person_id)
        )
        .scalars()
        .all()
    )

    added = sum(
        1
        for change in changes
        if change.change_type == ChangeType.ADDED
    )

    removed = sum(
        1
        for change in changes
        if change.change_type == ChangeType.REMOVED
    )

    modified = sum(
        1
        for change in changes
        if change.change_type == ChangeType.MODIFIED
    )

    return {
        "total_snapshots": len(snapshots),
        "total_changes": len(changes),
        "added": added,
        "removed": removed,
        "modified": modified,
        "first_snapshot": (
            snapshots[0].captured_at
            if snapshots
            else None
        ),
        "latest_snapshot": (
            snapshots[-1].captured_at
            if snapshots
            else None
        ),
    }