
from datetime import datetime, timezone
from uuid import uuid4

from app.models import Person, Source, Observation
from app.services.exposure_score import calculate_exposure_score


def test_exposure_score_with_github_observations(session):
    person = Person(
        display_name="GitHub Test User",
        created_at=datetime.now(timezone.utc),
    )
    session.add(person)
    session.flush()

    source = Source(
        platform="GitHub",
        url="https://github.com/testuser",
    )
    session.add(source)
    session.flush()

    snapshot = __import__(
        "app.models", fromlist=["Snapshot"]
    ).Snapshot(
        person_id=person.id,
        captured_at=datetime.now(timezone.utc),
    )

    session.add(snapshot)
    session.flush()

    observations = [
        Observation(
            source_id=source.id,
            category="profile",
            key="username",
            value="testuser",
            observed_at=datetime.now(timezone.utc),
        ),
        Observation(
            source_id=source.id,
            category="profile",
            key="profile_url",
            value="https://github.com/testuser",
            observed_at=datetime.now(timezone.utc),
        ),
        Observation(
            source_id=source.id,
            category="profile",
            key="public_repos",
            value="3",
            observed_at=datetime.now(timezone.utc),
        ),
    ]

    snapshot.observations = observations
    session.add_all(observations)
    session.commit()

    result = calculate_exposure_score(
        session=session,
        person_id=person.id,
    )

    assert result["score"] == 31
    assert result["risk_level"] == "low"
    assert len(result["factors"]) == 3
