
from uuid import UUID

from sqlalchemy.orm import Session

from app.services.privacy_report import generate_privacy_report


def get_privacy_recommendations(
    session: Session,
    person_id: UUID,
) -> list[str]:
    report = generate_privacy_report(
        session=session,
        person_id=person_id,
    )

    return report.get("recommendations", [])
