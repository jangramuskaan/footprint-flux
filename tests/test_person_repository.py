from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database import engine
from app.models import Person
from app.repositories.person import save_person, get_person


def test_save_and_get_person():
    person = Person(
        display_name="Repository User",
        created_at=datetime.now(timezone.utc),
    )

    with Session(engine) as session:
        saved = save_person(
            session=session,
            person=person,
        )

        assert saved.id is not None
        assert saved.display_name == "Repository User"

        retrieved = get_person(
            session=session,
            person_id=saved.id,
        )

        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.display_name == "Repository User"