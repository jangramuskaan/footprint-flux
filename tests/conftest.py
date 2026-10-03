import os

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
