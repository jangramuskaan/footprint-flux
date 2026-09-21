from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database import engine
from app.models import Person, Source, Observation
from app.repositories.snapshot import create_snapshot, get_snapshot


def test_create_and_get_snapshot():
    person = Person(
        display_name="Snapshot Test User",
        created_at=datetime.now(timezone.utc),
    )

    source = Source(
        platform="GitHub",
        url="https://github.com/example",
    )

    with Session(engine) as session:
        session.add(person)
        session.add(source)
        session.flush()

        observation = Observation(
            source_id=source.id,
            category="profile",
            key="username",
            value="snapshot_user",
            observed_at=datetime.now(timezone.utc),
        )

        session.add(observation)
        session.flush()

        snapshot = create_snapshot(
            session=session,
            person_id=person.id,
            observations=[observation],
        )

        assert snapshot.id is not None
        assert snapshot.person_id == person.id
        assert snapshot.captured_at is not None
        assert len(snapshot.observations) == 1
        assert snapshot.observations[0].id == observation.id

        retrieved = get_snapshot(
            session=session,
            snapshot_id=snapshot.id,
        )

        assert retrieved is not None
        assert retrieved.id == snapshot.id
        assert retrieved.person_id == person.id
        assert len(retrieved.observations) == 1
        assert retrieved.observations[0].value == "snapshot_user"