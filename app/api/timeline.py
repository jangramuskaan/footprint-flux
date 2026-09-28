from uuid import UUID

from sqlalchemy.orm import Session

from app.services.timeline_service import get_person_timeline


def timeline_for_person(
    session: Session,
    person_id: UUID,
):
    return get_person_timeline(
        session=session,
        person_id=person_id,
    )