
from uuid import UUID

from sqlalchemy.orm import Session

from app.services.exposure_score import calculate_exposure_score
from app.services.timeline_stats import get_timeline_stats


def generate_privacy_report(
    session: Session,
    person_id: UUID,
) -> dict:
    exposure = calculate_exposure_score(
        session=session,
        person_id=person_id,
    )

    timeline = get_timeline_stats(
        session=session,
        person_id=person_id,
    )

    recommendations = []

    for factor in exposure.get("factors", []):
        name = factor.get("factor", "").lower()

        if "username" in name:
            recommendations.append(
                "Review where your username is publicly visible."
            )
        elif "repositories" in name:
            recommendations.append(
                "Review public repositories for accidentally exposed "
                "personal information or secrets."
            )
        elif "bio" in name or "profile" in name:
            recommendations.append(
                "Review public profile information and remove "
                "unnecessary personal details."
            )

    if not recommendations:
        recommendations.append(
            "Review your public profiles periodically and collect "
            "new snapshots to detect changes."
        )

    return {
        "person_id": str(person_id),
        "exposure": exposure,
        "timeline": timeline,
        "recommendations": list(dict.fromkeys(recommendations)),
    }

