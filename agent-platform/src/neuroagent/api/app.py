"""FastAPI application for policy-harness runs."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from neuroagent.datasets import DATASETS, DEFAULT_DATASET_VERSION, load_dataset

from .routes import cases, episodes, hospitals, models, runs

logger = logging.getLogger(__name__)

# Paths relative to agent-platform/
DATA_ROOT = Path(__file__).resolve().parents[4] / "data"
RULES_DIR = Path(__file__).resolve().parents[3] / "config" / "hospital_rules"
PROFILES_DIR = Path(__file__).resolve().parents[3] / "config" / "profiles"
EPISODES_DIR = DATA_ROOT / "episodes"
WEB_DIST = Path(__file__).resolve().parents[4] / "web" / "dist"

# CORS: explicit allowlist instead of `*` (which, combined with credentials,
# would let any origin drive the API from a browser). Extra origins (e.g. a
# LAN-dev Vite server on another host) via NEUROAGENT_CORS_ORIGINS, comma-separated.
_DEFAULT_CORS_ORIGINS = [
    "http://localhost:8888",
    "http://127.0.0.1:8888",
]


def _cors_origins() -> list[str]:
    extra = os.environ.get("NEUROAGENT_CORS_ORIGINS", "")
    origins = list(_DEFAULT_CORS_ORIGINS)
    origins.extend(o.strip() for o in extra.split(",") if o.strip())
    return origins


def create_app() -> FastAPI:
    app = FastAPI(title="NeuroAgent Policy Harness API", version="2.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    dataset = DATASETS[DEFAULT_DATASET_VERSION]
    case_index, case_objects = load_dataset(dataset.path)
    logger.info("Loaded %d cases from %s", len(case_index), dataset.version)
    EPISODES_DIR.mkdir(parents=True, exist_ok=True)

    app.state.case_index = case_index
    app.state.case_objects = case_objects
    app.state.rules_dir = str(RULES_DIR)
    app.state.profiles_dir = PROFILES_DIR
    app.state.episodes_dir = EPISODES_DIR

    app.include_router(cases.router, prefix="/api/v1")
    app.include_router(hospitals.router, prefix="/api/v1")
    app.include_router(models.router, prefix="/api/v1")
    app.include_router(runs.router, prefix="/api/v1")
    app.include_router(episodes.router, prefix="/api/v1")

    # The dashboard build, when present, is served from the same origin as the API it calls.
    if WEB_DIST.is_dir():
        app.mount("/", StaticFiles(directory=WEB_DIST, html=True), name="web")

    return app


app = create_app()
