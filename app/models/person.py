from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Person(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    display_name: str
    created_at: str