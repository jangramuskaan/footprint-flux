
from uuid import UUID

from sqlalchemy.orm import Session

from app.database import engine
from app.models import Snapshot


def compare_snapshots(
    snapshot_before_id: UUID,
    snapshot_after_id: UUID,
) -> dict:
    with Session(engine) as session:
        before = session.get(Snapshot, snapshot_before_id)
        after = session.get(Snapshot, snapshot_after_id)

        if before is None or after is None:
            return {"error": "One or both snapshots were not found."}

        if before.person_id != after.person_id:
            return {"error": "Snapshots must belong to the same person."}

        if before.captured_at >= after.captured_at:
            return {"error": "The before snapshot must be earlier."}

        before_observations = {
            (obs.category, obs.key): obs
            for obs in before.observations
        }
        after_observations = {
            (obs.category, obs.key): obs
            for obs in after.observations
        }

        changes = []

        for key in sorted(
            before_observations.keys() | after_observations.keys()
        ):
            old_obs = before_observations.get(key)
            new_obs = after_observations.get(key)

            if old_obs is None:
                changes.append({
                    "change_type": "added",
                    "category": key[0],
                    "key": key[1],
                    "old_value": None,
                    "new_value": new_obs.value,
                })

            elif new_obs is None:
                changes.append({
                    "change_type": "removed",
                    "category": key[0],
                    "key": key[1],
                    "old_value": old_obs.value,
                    "new_value": None,
                })

            elif old_obs.value != new_obs.value:
                changes.append({
                    "change_type": "modified",
                    "category": key[0],
                    "key": key[1],
                    "old_value": old_obs.value,
                    "new_value": new_obs.value,
                })

        return {
            "snapshot_before_id": str(snapshot_before_id),
            "snapshot_after_id": str(snapshot_after_id),
            "changes": changes,
            "total_changes": len(changes),
        }
