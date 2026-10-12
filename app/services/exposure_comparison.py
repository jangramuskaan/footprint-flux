
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Snapshot
from app.services.exposure_score import calculate_exposure_score


def compare_exposure(
    session: Session,
    person_id: UUID,
    snapshot_before_id: UUID,
    snapshot_after_id: UUID,
) -> dict:
    before = session.get(Snapshot, snapshot_before_id)
    after = session.get(Snapshot, snapshot_after_id)

    if before is None or after is None:
        raise ValueError("One or both snapshots were not found.")

    if before.person_id != person_id or after.person_id != person_id:
        raise ValueError("Both snapshots must belong to the requested person.")

    if before.captured_at >= after.captured_at:
        raise ValueError("The earlier snapshot must precede the later snapshot.")

    before_score = calculate_exposure_score(
        session=session,
        person_id=person_id,
        snapshot_id=snapshot_before_id,
    )

    after_score = calculate_exposure_score(
        session=session,
        person_id=person_id,
        snapshot_id=snapshot_after_id,
    )

    difference = after_score["score"] - before_score["score"]

    if difference > 0:
        trend = "increased"
    elif difference < 0:
        trend = "decreased"
    else:
        trend = "unchanged"

    return {
        "person_id": str(person_id),
        "snapshot_before_id": str(snapshot_before_id),
        "snapshot_after_id": str(snapshot_after_id),
        "before_score": before_score["score"],
        "after_score": after_score["score"],
        "difference": difference,
        "trend": trend,
    }
