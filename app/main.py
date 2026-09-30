from fastapi import FastAPI
from sqlalchemy.orm import Session
import networkx as nx

from app.database import engine
from app.api.graph import graph_for_session
from app.repositories import graph


app = FastAPI(
    title="Footprint Flux API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "name": "Footprint Flux",
        "status": "running",
    }


@app.get("/graph")
def get_graph():
    with Session(engine) as session:
        graph = graph_for_session(session)

    return nx.node_link_data(graph, edges="links")