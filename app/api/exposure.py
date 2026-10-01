from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analysis.exposure import calculate_exposure_score
from app.models import Observation


def exposure_for_session(session: Session) -> int:
    statement = select(Observation)

    observations = list(
        session.execute(statement).scalars().all()
    )

    return calculate_exposure_score(observations)