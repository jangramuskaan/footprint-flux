from datetime import datetime, timezone
from uuid import UUID

from app.models import Observation


def create_observation(
    source_id: UUID,
    category: str,
    key: str,
    value: str,
) -> Observation:
    return Observation(
        source_id=source_id,
        category=category,
        key=key,
        value=value,
        observed_at=datetime.now(timezone.utc),
    )