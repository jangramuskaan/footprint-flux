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
        change.change_type == ChangeType.ADDED
        for change in changes
    )
    removed = sum(
        change.change_type == ChangeType.REMOVED
        for change in changes
    )
    modified = sum(
        change.change_type == ChangeType.MODIFIED
        for change in changes
    )

    total_snapshots = len(snapshots)
    total_changes = len(changes)

    change_rate = (
        round(total_changes / (total_snapshots - 1), 2)
        if total_snapshots > 1
        else 0
    )

    if not snapshots:
        activity_status = "no_data"
    elif not changes:
        activity_status = "no_changes"
    else:
        activity_status = "changes_detected"

    return {
        "total_snapshots": total_snapshots,
        "total_changes": total_changes,
        "added": added,
        "removed": removed,
        "modified": modified,
        "change_rate": change_rate,
        "activity_status": activity_status,
        "first_snapshot": (
            snapshots[0].captured_at if snapshots else None
        ),
        "latest_snapshot": (
            snapshots[-1].captured_at if snapshots else None
        ),
    }
