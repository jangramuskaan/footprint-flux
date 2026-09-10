from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Source(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    platform: str
    url: str