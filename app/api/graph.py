from sqlalchemy.orm import Session

from app.services.graph_service import build_graph
from app.repositories.graph.node import get_nodes
from app.repositories.graph.edge import get_edges


def graph_for_session(
    session: Session,
):
    nodes = get_nodes(session)
    edges = get_edges(session)

    return build_graph(nodes, edges)
