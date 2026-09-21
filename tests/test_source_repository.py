from app.database import engine
from app.models import Source
from app.repositories.source import save_source, get_source
from sqlalchemy.orm import Session


def test_save_and_get_source():
    source = Source(
        platform="GitHub",
        url="https://github.com/example",
    )

    with Session(engine) as session:
        saved = save_source(
            session=session,
            source=source,
        )

        assert saved.id is not None
        assert saved.platform == "GitHub"
        assert saved.url == "https://github.com/example"

        retrieved = get_source(
            session=session,
            source_id=saved.id,
        )

        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.platform == "GitHub"
        assert retrieved.url == "https://github.com/example"