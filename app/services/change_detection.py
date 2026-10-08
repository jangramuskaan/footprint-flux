from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Change, ChangeType, Observation, Snapshot
from app.services.change_service import save_change


def detect_changes(
    session: Session,
    snapshot_before: Snapshot,
    snapshot_after: Snapshot,
) -> list[Change]:
    before_map = {
        (observation.category, observation.key): observation
        for observation in snapshot_before.observations
    }

    after_map = {
        (observation.category, observation.key): observation
        for observation in snapshot_after.observations
    }

    changes: list[Change] = []

    all_keys = set(before_map) | set(after_map)

    for key in sorted(all_keys):
        before = before_map.get(key)
        after = after_map.get(key)

        if before is None and after is not None:
            change = Change(
                snapshot_before_id=snapshot_before.id,
                snapshot_after_id=snapshot_after.id,
                observation_id=after.id,
                change_type=ChangeType.ADDED,
                old_value=None,
                new_value=after.value,
            )

            changes.append(
                save_change(
                    session=session,
                    change=change,
                )
            )

        elif before is not None and after is None:
            change = Change(
                snapshot_before_id=snapshot_before.id,
                snapshot_after_id=snapshot_after.id,
                observation_id=before.id,
                change_type=ChangeType.REMOVED,
                old_value=before.value,
                new_value=None,
            )

            changes.append(
                save_change(
                    session=session,
                    change=change,
                )
            )

        elif before is not None and after is not None:
            if before.value != after.value:
                change = Change(
                    snapshot_before_id=snapshot_before.id,
                    snapshot_after_id=snapshot_after.id,
                    observation_id=after.id,
                    change_type=ChangeType.MODIFIED,
                    old_value=before.value,
                    new_value=after.value,
                )

                changes.append(
                    save_change(
                        session=session,
                        change=change,
                    )
                )

    return changes
