from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Source


def save_source(
    session: Session,
    source: Source,
) -> Source:
    session.add(source)
    session.commit()
    session.refresh(source)

    return source


def get_source(
    session: Session,
    source_id: UUID,
) -> Source | None:
    statement = select(Source).where(
        Source.id == source_id
    )

    return session.execute(statement).scalar_one_or_none()