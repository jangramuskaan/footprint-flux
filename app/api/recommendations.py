from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import engine
from app.services.recommendations import generate_recommendations


def recommendations_for_person(person_id: UUID):
    with Session(engine) as session:
        recommendations = generate_recommendations(
            session=session,
            person_id=person_id,
        )

    return {
        "person_id": str(person_id),
        "recommendations": recommendations,
    }
