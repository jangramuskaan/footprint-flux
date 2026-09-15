from sqlalchemy.orm import Session

from app.database import engine
from app.models import Source
from app.services.collection import collect_observation


def test_collect_observation():
    with Session(engine, expire_on_commit=False) as session:
        source = Source(
            platform="Test Platform",
            url="https://example.com",
        )

        session.add(source)
        session.commit()

        observation = collect_observation(
            session=session,
            source_id=source.id,
            category="profile",
            key="username",
            value="test_user",
        )

        assert observation.id is not None
        assert observation.source_id == source.id
        assert observation.category == "profile"
        assert observation.key == "username"
        assert observation.value == "test_user"