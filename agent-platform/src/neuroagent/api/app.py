"""FastAPI application for the NeuroAgent web dashboard."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from neuroagent_schemas import NeuroBenchCase

from neuroagent.datasets import DATASETS, DEFAULT_DATASET_VERSION, load_dataset

from .routes import cases, hospitals, agent, models, traces, copilot

logger = logging.getLogger(__name__)

# Paths relative to agent-platform/
DATA_ROOT = Path(__file__).resolve().parents[4] / "data"
RULES_DIR = Path(__file__).resolve().parents[3] / "config" / "hospital_rules"
TRACES_DIR = DATA_ROOT / "traces"
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

    # Pre-load all datasets
    all_datasets: dict[str, tuple[dict[str, dict[str, Any]], dict[str, NeuroBenchCase]]] = {}
    for version, info in DATASETS.items():
        idx, objs = load_dataset(info.path)
        all_datasets[version] = (idx, objs)
        logger.info("Loaded %d cases from %s", len(idx), version)

    default_version = DEFAULT_DATASET_VERSION
    app.state.active_dataset = default_version
    app.state.all_datasets = all_datasets
    app.state.case_index = all_datasets[default_version][0]
    app.state.case_objects = all_datasets[default_version][1]

    # Ensure traces directory exists
    TRACES_DIR.mkdir(parents=True, exist_ok=True)

    # Store shared state on app
    app.state.rules_dir = str(RULES_DIR)
    app.state.traces_dir = TRACES_DIR
    app.state.dataset_path = DATASETS[default_version].path

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
