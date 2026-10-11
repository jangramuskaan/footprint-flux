
from uuid import UUID

from sqlalchemy.orm import Session

from app.services.exposure_score import calculate_exposure_score


def exposure_for_person(
    session: Session,
    person_id: UUID,
) -> dict:
    return calculate_exposure_score(
        session=session,
        person_id=person_id,
    )
