
from uuid import UUID

from sqlalchemy.orm import Session

from app.services.recommendations import get_privacy_recommendations


def recommendations_for_person(
    session: Session,
    person_id: UUID,
) -> list[str]:
    return get_privacy_recommendations(
        session=session,
        person_id=person_id,
    )
