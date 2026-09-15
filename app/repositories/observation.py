from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Observation


def save_observation(
    session: Session,
    observation: Observation,
) -> Observation:
    session.add(observation)
    session.commit()
    session.refresh(observation)

    return observation


def get_observation(
    session: Session,
    observation_id: UUID,
) -> Observation | None:
    statement = select(Observation).where(
        Observation.id == observation_id
    )

    return session.execute(statement).scalar_one_or_none()