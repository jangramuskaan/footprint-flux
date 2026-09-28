from sqlalchemy.orm import Session

from app.models import Snapshot


def get_person_timeline(
    session: Session,
    person_id,
) -> list[Snapshot]:
    snapshots = (
        session.query(Snapshot)
        .filter(Snapshot.person_id == person_id)
        .order_by(Snapshot.captured_at.asc())
        .all()
    )

    return snapshots