from uuid import UUID

from sqlalchemy.orm import Session

from app.services.exposure_score import calculate_exposure_score


def generate_recommendations(
    session: Session,
    person_id: UUID,
    snapshot_id: UUID | None = None,
) -> list[str]:
    exposure = calculate_exposure_score(
        session=session,
        person_id=person_id,
        snapshot_id=snapshot_id,
    )

    recommendations = []

    for factor in exposure.get("factors", []):
        name = factor.get("factor", "").lower()

        if "username" in name:
            recommendations.append(
                "Review where your username is publicly visible "
                "and avoid reusing it across sensitive accounts."
            )

        elif "repository" in name:
            recommendations.append(
                "Review your public repositories for accidentally "
                "exposed personal information, API keys, or secrets."
            )

        elif "bio" in name:
            recommendations.append(
                "Review your public profile bio and remove "
                "unnecessary personal details."
            )

        elif "profile" in name:
            recommendations.append(
                "Review your public profile and limit information "
                "that you do not want publicly discoverable."
            )

        elif "followers" in name or "following" in name:
            recommendations.append(
                "Review your public social connections and "
                "their visibility settings."
            )

    if not recommendations:
        recommendations.append(
            "Continue reviewing your public profiles periodically "
            "and create new snapshots to detect changes."
        )

    return list(dict.fromkeys(recommendations))


def get_privacy_recommendations(
    session: Session,
    person_id: UUID,
    snapshot_id: UUID | None = None,
) -> list[str]:
    return generate_recommendations(
        session=session,
        person_id=person_id,
        snapshot_id=snapshot_id,
    )


def recommendations_for_person(
    session: Session,
    person_id: UUID,
    snapshot_id: UUID | None = None,
) -> list[str]:
    return generate_recommendations(
        session=session,
        person_id=person_id,
        snapshot_id=snapshot_id,
    )