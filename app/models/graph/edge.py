from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Edge(Base):
    __tablename__ = "graph_edges"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    source_node_id: Mapped[UUID] = mapped_column(
        ForeignKey("graph_nodes.id"),
        nullable=False,
    )

    target_node_id: Mapped[UUID] = mapped_column(
        ForeignKey("graph_nodes.id"),
        nullable=False,
    )

    relationship: Mapped[str] = mapped_column(
        nullable=False,
    )