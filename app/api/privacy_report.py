
from uuid import UUID

from sqlalchemy.orm import Session

from app.services.privacy_report import generate_privacy_report


def privacy_report_for_person(
    session: Session,
    person_id: UUID,
) -> dict:
    return generate_privacy_report(
        session=session,
        person_id=person_id,
    )
