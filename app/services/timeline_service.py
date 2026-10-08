from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Change, Snapshot


def get_timeline(
    session: Session,
    person_id: UUID,
) -> list[dict]:
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
            .order_by(Change.detected_at.asc())
        )
        .scalars()
        .all()
    )

    timeline = []

    for snapshot in snapshots:
        timeline.append(
            {
                "type": "snapshot",
                "timestamp": snapshot.captured_at,
                "snapshot_id": str(snapshot.id),
            }
        )

    for change in changes:
        timeline.append(
            {
                "type": "change",
                "timestamp": change.detected_at,
                "change_id": str(change.id),
                "change_type": change.change_type.value,
                "old_value": change.old_value,
                "new_value": change.new_value,
            }
        )

    timeline.sort(key=lambda item: item["timestamp"])

    return timeline

def get_person_timeline(
    session: Session,
    person_id: UUID,
) -> list[dict]:
    return get_timeline(
        session=session,
        person_id=person_id,
    )