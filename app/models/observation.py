from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Observation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source_id: UUID
    category: str
    key: str
    value: str
    observed_at: datetime