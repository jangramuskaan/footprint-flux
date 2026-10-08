from uuid import UUID

from sqlalchemy.orm import Session

from app.services.timeline_stats import get_timeline_stats


def timeline_stats_for_person(
    session: Session,
    person_id: UUID,
) -> dict:
    return get_timeline_stats(
        session=session,
        person_id=person_id,
    )