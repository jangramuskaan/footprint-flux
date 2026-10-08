import os

import pytest
from sqlalchemy.orm import Session

os.environ["DATABASE_URL"] = "sqlite:///test_footprint.db"

from app.models import (
    Person,
    Source,
    Observation,
    Snapshot,
    Change,
)

from app.models.graph.node import Node
from app.models.graph.edge import Edge

from app.database import Base, engine


Base.metadata.create_all(bind=engine)


@pytest.fixture
def session():
    with Session(engine, expire_on_commit=False) as session:
        yield session
        session.rollback()