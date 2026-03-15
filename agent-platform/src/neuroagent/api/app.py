"""FastAPI application for the NeuroAgent web dashboard."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from neuroagent_schemas import NeuroBenchCase

from .routes import cases, hospitals, agent, models, traces, copilot

logger = logging.getLogger(__name__)

# Paths relative to agent-platform/
DATASET_PATH = Path(__file__).resolve().parents[4] / "data" / "neurobench_v1"
RULES_DIR = Path(__file__).resolve().parents[3] / "config" / "hospital_rules"
TRACES_DIR = Path(__file__).resolve().parents[4] / "data" / "traces"
WEB_DIST = Path(__file__).resolve().parents[4] / "web" / "dist"


def create_app() -> FastAPI:
    app = FastAPI(title="NeuroAgent Dashboard API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Load case index on startup
    case_index: dict[str, dict[str, Any]] = {}
    case_objects: dict[str, NeuroBenchCase] = {}

    cases_dir = DATASET_PATH / "cases"
    if cases_dir.exists():
        for case_file in sorted(cases_dir.glob("*.json")):
            try:
                data = json.loads(case_file.read_text())
                case = NeuroBenchCase.model_validate(data)
                case_objects[case.case_id] = case
                case_index[case.case_id] = {
                    "case_id": case.case_id,
                    "condition": case.condition.value,
                    "difficulty": case.difficulty.value,
                    "encounter_type": case.encounter_type.value,
                    "age": case.patient.demographics.age,
                    "sex": case.patient.demographics.sex,
                    "chief_complaint": case.patient.chief_complaint,
                }
            except Exception as e:
                logger.error("Failed to load case %s: %s", case_file.name, e)

    logger.info("Loaded %d cases into index", len(case_index))

    # Ensure traces directory exists
    TRACES_DIR.mkdir(parents=True, exist_ok=True)

    # Store shared state on app
    app.state.case_index = case_index
    app.state.case_objects = case_objects
    app.state.rules_dir = str(RULES_DIR)
    app.state.traces_dir = TRACES_DIR
    app.state.dataset_path = DATASET_PATH

    # Register routes
    app.include_router(cases.router, prefix="/api/v1")
    app.include_router(hospitals.router, prefix="/api/v1")
    app.include_router(models.router, prefix="/api/v1")
    app.include_router(agent.router, prefix="/api/v1")
    app.include_router(traces.router, prefix="/api/v1")
    app.include_router(copilot.router, prefix="/api/v1")

    # Serve frontend static files in production
    if WEB_DIST.exists():
        app.mount("/", StaticFiles(directory=str(WEB_DIST), html=True), name="static")

    return app


app = create_app()
