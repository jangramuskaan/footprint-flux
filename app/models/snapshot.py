from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Snapshot(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    person_id: UUID
    captured_at: datetime
    observation_ids: list[UUID] = Field(default_factory=list)