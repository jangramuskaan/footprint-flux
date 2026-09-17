from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.collectors.github import GitHubCollector
from app.models import Observation, Source
from app.repositories.observation import save_observation


def collect_github_profile(
    session: Session,
    username: str,
) -> list[Observation]:
    collector = GitHubCollector(username)

    observations = collector.collect()

    source = Source(
        platform="GitHub",
        url=f"https://github.com/{username}",
    )

    session.add(source)
    session.commit()
    session.refresh(source)

    saved_observations = []

    for item in observations:
        observation = Observation(
            source_id=source.id,
            category=item["category"],
            key=item["key"],
            value=item["value"],
            observed_at=datetime.now(timezone.utc),
        )

        saved = save_observation(
            session=session,
            observation=observation,
        )

        saved_observations.append(saved)

    return saved_observations