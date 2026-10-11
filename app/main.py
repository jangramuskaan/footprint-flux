from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import engine
from app.api.graph import graph_for_session
from app.api.exposure import exposure_for_person
from uuid import UUID
from app.services.exposure_score import calculate_exposure_score
from sqlalchemy import select
from app.models import Person
from app.api.privacy_report import privacy_report_for_person

from app.services.timeline_stats import get_timeline_stats

import networkx as nx

app = FastAPI(
    title="Footprint Flux API",
    version="1.0.0",
)


# Frontend
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

templates = Jinja2Templates(
    directory="app/templates",
)


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.get("/api/health")
def health():
    return {
        "name": "Footprint Flux",
        "status": "running",
    }


@app.get("/api/stats")
def get_stats():
    with Session(engine) as session:
        observations = session.execute(
            text("SELECT COUNT(*) FROM observations")
        ).scalar_one()

        sources = session.execute(
            text("SELECT COUNT(*) FROM sources")
        ).scalar_one()

        changes = session.execute(
            text("SELECT COUNT(*) FROM changes")
        ).scalar_one()

        snapshots = session.execute(
            text("SELECT COUNT(*) FROM snapshots")
        ).scalar_one()

        graph_nodes = session.execute(
            text("SELECT COUNT(*) FROM graph_nodes")
        ).scalar_one()

        graph_edges = session.execute(
            text("SELECT COUNT(*) FROM graph_edges")
        ).scalar_one()

    return {
        "observations": observations,
        "sources": sources,
        "changes": changes,
        "snapshots": snapshots,
        "graph_nodes": graph_nodes,
        "graph_edges": graph_edges,
    }

@app.get("/graph")
def get_graph():
    with Session(engine) as session:
        graph = graph_for_session(session)

        return nx.node_link_data(
            graph,
            edges="links",
        )



@app.get("/api/exposure")
def get_exposure():
    with Session(engine) as session:
        people = session.execute(select(Person)).scalars().all()

        if not people:
            return {
                "score": 0,
                "risk_level": "low",
                "factors": [],
            }

        return calculate_exposure_score(
            session=session,
            person_id=people[0].id,
        )




@app.get("/timeline/{person_id}/stats")
def get_timeline_stats_api(
    person_id: UUID,
):
    with Session(engine) as session:
        return get_timeline_stats(
            session=session,
            person_id=person_id,
        )


@app.get("/exposure/{person_id}")
def get_exposure_score(person_id: UUID):
    with Session(engine) as session:
        return exposure_for_person(
            session=session,
            person_id=person_id,
        )


@app.get("/privacy-report/{person_id}")
def get_privacy_report(person_id: UUID):
    with Session(engine) as session:
        return privacy_report_for_person(
            session=session,
            person_id=person_id,
        )