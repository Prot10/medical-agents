"""FastAPI app for the NeuroBench dataset review tool.

Run with::

    uv run uvicorn neuroagent.review_api.app:app --port 8889 --host 0.0.0.0
"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import (
    ANNOTATIONS_DIR,
    AVAILABLE_DATASETS,
    DEFAULT_DATASET_VERSION,
    REVIEWER_CODES_PATH,
    WEB_DIST,
)
from .services.annotation_store import AnnotationStore
from .services.dataset_loader import load_dataset
from .services.reviewer_codes import ReviewerCodeRegistry

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="NeuroBench Review API",
        description="Dataset review and annotation API for NeuroBench cases.",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Pre-load every registered dataset at startup so per-case GETs are fast.
    all_datasets: dict[str, tuple[dict, dict]] = {}
    for version, info in AVAILABLE_DATASETS.items():
        idx, objs = load_dataset(info["path"])
        all_datasets[version] = (idx, objs)
        logger.info("Loaded %d cases from %s", len(idx), version)

    app.state.all_datasets = all_datasets
    app.state.default_dataset_version = DEFAULT_DATASET_VERSION
    app.state.annotations_dir = ANNOTATIONS_DIR
    app.state.reviewer_codes_path = REVIEWER_CODES_PATH

    # Ensure on-disk locations exist.
    ANNOTATIONS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWER_CODES_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Reviewer registry — reloads automatically when the YAML mtime changes.
    app.state.reviewer_registry = ReviewerCodeRegistry(REVIEWER_CODES_PATH)

    # Annotation store — filesystem-backed.
    app.state.annotation_store = AnnotationStore(ANNOTATIONS_DIR)

    from .routes import admin as admin_routes
    from .routes import annotations as annotations_routes
    from .routes import datasets as datasets_routes
    from .routes import methodology as methodology_routes
    from .routes import progress as progress_routes
    from .routes import reviewers as reviewers_routes

    app.include_router(reviewers_routes.router, prefix="/api/v1")
    app.include_router(datasets_routes.router, prefix="/api/v1")
    app.include_router(annotations_routes.router, prefix="/api/v1")
    app.include_router(progress_routes.router, prefix="/api/v1")
    app.include_router(methodology_routes.router, prefix="/api/v1")
    app.include_router(admin_routes.router, prefix="/api/v1")

    if WEB_DIST.exists():
        app.mount("/", StaticFiles(directory=str(WEB_DIST), html=True), name="static")

    return app


app = create_app()
