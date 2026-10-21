from sqlalchemy import select
from app.models import Change, Snapshot
from collections import defaultdict
from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.services.timeline_service import get_timeline


def get_daily_activity(
    session: Session,
    person_id: UUID,
) -> list[dict]:
    timeline = get_timeline(
        session=session,
        person_id=person_id,
    )

    daily = defaultdict(
        lambda: {
            "date": None,
            "snapshots": 0,
            "changes": 0,
            "added": 0,
            "removed": 0,
            "modified": 0,
        }
    )

    for event in timeline:
        timestamp = event["timestamp"]
        day = timestamp.date()

        if isinstance(day, date):
            day_key = day.isoformat()
        else:
            day_key = str(day)

        entry = daily[day_key]
        entry["date"] = day_key

        if event["type"] == "snapshot":
            entry["snapshots"] += 1
        elif event["type"] == "change":
            entry["changes"] += 1
            change_type = event.get("change_type", "").lower()

            if change_type in ("added", "removed", "modified"):
                entry[change_type] += 1

    return [
        daily[day]
        for day in sorted(daily)
    ]
