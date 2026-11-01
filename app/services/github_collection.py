from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.collectors.github import GitHubCollector
from app.models import Observation, Source
from app.repositories.observation import save_observation
from app.services.graph_builder import save_relationship

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
        if item["key"] == "username":
             save_relationship(
                session=session,
                observation_type="username",
                source_value=source.url,
                target_value=item["value"],
            )

        elif item["key"] == "profile_url":
            save_relationship(
                session=session,
                observation_type="url",
                source_value=source.url,
                target_value=item["value"],
            )

    return saved_observations