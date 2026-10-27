from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy.orm import Session

from app.database import engine
from app.services.timeline_service import get_timeline
from app.services.timeline_activity import get_daily_activity

router = APIRouter()



@router.get("/timeline/{person_id}")
def get_person_timeline(
    person_id: UUID,
    change_type: Optional[str] = Query(
        default=None,
        description="Filter changes by added, removed, or modified",
    ),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    with Session(engine) as session:
        return get_timeline(
            session=session,
            person_id=person_id,
            change_type=change_type,
            limit=limit,
            offset=offset,
        )


def timeline_for_person(
    session: Session,
    person_id: UUID,
):
    return get_timeline(
        session=session,
        person_id=person_id,
    )


@router.get("/timeline/{person_id}/daily-activity")
def daily_activity_endpoint(
    person_id: UUID,
):
    with Session(engine) as session:
        activity = get_daily_activity(
            session=session,
            person_id=person_id,
        )

    return {
        "person_id": str(person_id),
        "daily_activity": activity,
    }