from uuid import UUID

from sqlalchemy.orm import Session

from app.collectors.manual import create_observation
from app.models import Observation
from app.repositories.observation import save_observation


def collect_observation(
    session: Session,
    source_id: UUID,
    category: str,
    key: str,
    value: str,
) -> Observation:
    observation = create_observation(
        source_id=source_id,
        category=category,
        key=key,
        value=value,
    )

    return save_observation(
        session=session,
        observation=observation,
    )