from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class ChangeType(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"


class Change(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    snapshot_before_id: UUID
    snapshot_after_id: UUID
    observation_id: UUID | None = None
    change_type: ChangeType
    old_value: str | None = None
    new_value: str | None = None
    detected_at: datetime