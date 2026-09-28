from sqlalchemy.orm import Session

from app.models import Snapshot, Change


def get_timeline_stats(
    session: Session,
    person_id,
) -> dict:
    snapshots = (
        session.query(Snapshot)
        .filter(Snapshot.person_id == person_id)
        .order_by(Snapshot.captured_at.asc())
        .all()
    )

    snapshot_ids = [snapshot.id for snapshot in snapshots]

    changes = []

    if snapshot_ids:
        changes = (
            session.query(Change)
            .filter(
                Change.snapshot_before_id.in_(snapshot_ids)
                | Change.snapshot_after_id.in_(snapshot_ids)
            )
            .all()
        )

    return {
        "total_snapshots": len(snapshots),
        "total_changes": len(changes),
        "first_snapshot": (
            snapshots[0].captured_at if snapshots else None
        ),
        "latest_snapshot": (
            snapshots[-1].captured_at if snapshots else None
        ),
    }