from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Observation, Snapshot
from app.models.snapshot import snapshot_observations


def calculate_exposure_score(
    session: Session,
    person_id: UUID,
) -> dict:
    statement = (
        select(Observation)
        .join(
            snapshot_observations,
            Observation.id == snapshot_observations.c.observation_id,
        )
        .join(
            Snapshot,
            Snapshot.id == snapshot_observations.c.snapshot_id,
        )
        .where(Snapshot.person_id == person_id)
    )

    observations = (
        session.execute(statement)
        .scalars()
        .all()
    )

    score = 0
    factors = []
    seen_keys = set()

    for observation in observations:
        key = (
            observation.category,
            observation.key,
        )

        if key in seen_keys:
            continue

        seen_keys.add(key)

        if observation.key == "username":
            score += 15
            factors.append({
                "factor": "Username exposure",
                "points": 15,
            })

        elif observation.key == "profile_url":
            score += 10
            factors.append({
                "factor": "Public profile",
                "points": 10,
            })

        elif observation.key == "public_repos":
            repo_count = int(observation.value or 0)

            if repo_count > 0:
                points = min(repo_count * 2, 20)
                score += points

                factors.append({
                    "factor": "Public repositories",
                    "points": points,
                })

        elif observation.key == "bio":
            if observation.value.strip():
                score += 5
                factors.append({
                    "factor": "Public bio",
                    "points": 5,
                })

        elif observation.key in {
            "followers",
            "following",
        }:
            score += 3
            factors.append({
                "factor": f"Public {observation.key} count",
                "points": 3,
            })

    score = min(score, 100)

    if score >= 70:
        risk_level = "high"
    elif score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "score": score,
        "risk_level": risk_level,
        "factors": factors,
    }