from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.database import engine
from app.models import Source, Observation
from app.repositories.observation import (
    save_observation,
    get_observation,
)


def test_save_and_get_observation():
    with Session(engine, expire_on_commit=False) as session:
        source = Source(
            platform="Test Platform",
            url="https://example.com",
        )

        session.add(source)
        session.commit()

        observation = Observation(
            source_id=source.id,
            category="profile",
            key="username",
            value="test_user",
            observed_at=datetime.now(timezone.utc),
        )

        saved = save_observation(session, observation)

        assert saved.id is not None

        loaded = get_observation(
            session,
            saved.id,
        )

        assert loaded is not None
        assert loaded.id == saved.id
        assert loaded.key == "username"
        assert loaded.value == "test_user"