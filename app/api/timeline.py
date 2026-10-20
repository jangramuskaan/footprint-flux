from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy.orm import Session

from app.database import engine
from app.services.timeline_service import get_timeline

router = APIRouter()


@router.get("/timeline/{person_id}")
def get_person_timeline(
    person_id: UUID,
    change_type: Optional[str] = Query(
        default=None,
        description="Filter changes by added, removed, or modified",
    ),
):
    with Session(engine) as session:
        return get_timeline(
            session=session,
            person_id=person_id,
            change_type=change_type,
        )

def timeline_for_person(
    session: Session,
    person_id: UUID,
):
    return get_timeline(
        session=session,
        person_id=person_id,
    )