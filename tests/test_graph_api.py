from sqlalchemy.orm import Session

from app.database import engine, create_db_and_tables
from app.api.graph import graph_for_session


def test_graph_api_returns_graph():
    create_db_and_tables()

    with Session(engine) as session:
        graph = graph_for_session(session)

    assert graph is not None
