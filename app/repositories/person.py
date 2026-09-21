from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Person


def save_person(
    session: Session,
    person: Person,
) -> Person:
    session.add(person)
    session.commit()
    session.refresh(person)

    return person


def get_person(
    session: Session,
    person_id: UUID,
) -> Person | None:
    statement = select(Person).where(
        Person.id == person_id
    )

    return session.execute(statement).scalar_one_or_none()