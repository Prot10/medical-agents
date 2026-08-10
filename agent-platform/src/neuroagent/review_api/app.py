"""FastAPI app for the NeuroBench dataset review tool.

Run with::

    uv run uvicorn neuroagent.review_api.app:app --port 8889 --host 0.0.0.0
"""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from .config import (
    ANNOTATIONS_DIR,
    AVAILABLE_DATASETS,
    CONDITION_TOOL_GUIDANCE_PATH,
    CONDITIONS_YAML_PATH,
    DEFAULT_DATASET_VERSION,
    REVIEWER_CODES_PATH,
    TOOL_COSTS_PATH,
    TOOL_REVIEWS_DIR,
    WEB_DIST,
)
from .services.annotation_store import AnnotationStore
from .services.dataset_loader import load_dataset
from .services.rate_limit import AuthRateLimiter
from .services.reviewer_codes import ReviewerCodeRegistry
from .services.tool_catalog import build_catalog
from .services.tool_review_store import ToolReviewStore

logger = logging.getLogger(__name__)

# Reject request bodies larger than this (annotations are small; this guards
# the Pi against a single oversized upload). Override via env.
MAX_BODY_BYTES = int(os.environ.get("REVIEW_MAX_BODY_BYTES", 1_000_000))

# Content-Security-Policy for the served SPA. 'unsafe-inline' on style is
# required for framer-motion's inline element styles; scripts are external
# hashed files so script-src stays strict.
_CSP = (
    "default-src 'self'; "
    "img-src 'self' data:; "
    "style-src 'self' 'unsafe-inline'; "
    "script-src 'self'; "
    "connect-src 'self'; "
    "font-src 'self' data:; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)


def _allowed_origins() -> list[str]:
    """CORS allowlist from REVIEW_ALLOWED_ORIGINS (comma-separated).

    Defaults to local dev origins so a misconfigured prod deploy fails closed
    (no wildcard) rather than open.
    """
    raw = os.environ.get("REVIEW_ALLOWED_ORIGINS", "")
    origins = [o.strip() for o in raw.split(",") if o.strip()]
    return origins or ["http://localhost:5174", "http://127.0.0.1:5174"]


def create_app() -> FastAPI:
    app = FastAPI(
        title="NeuroBench Review API",
        description="Dataset review and annotation API for NeuroBench cases.",
        version="0.1.0",
    )

    # Security headers + request-body cap. Added first so it runs outermost.
    @app.middleware("http")
    async def _security_middleware(request: Request, call_next):
        cl = request.headers.get("content-length")
        if cl is not None:
            try:
                if int(cl) > MAX_BODY_BYTES:
                    return JSONResponse(
                        status_code=413, content={"detail": "Request body too large"}
                    )
            except ValueError:
                return JSONResponse(
                    status_code=400, content={"detail": "Invalid Content-Length"}
                )
        response: Response = await call_next(request)
        response.headers.setdefault("Content-Security-Policy", _CSP)
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        return response

    # CORS — explicit allowlist (no wildcard), no credentials (auth is a header,
    # not a cookie). Set REVIEW_ALLOWED_ORIGINS to the public hostname in prod.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins(),
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["X-Reviewer-Code", "Content-Type", "Accept"],
    )

    # Pre-load every registered dataset at startup so per-case GETs are fast.
    all_datasets: dict[str, tuple[dict, dict]] = {}
    for version, info in AVAILABLE_DATASETS.items():
        idx, objs = load_dataset(info.path)
        all_datasets[version] = (idx, objs)
        logger.info("Loaded %d cases from %s", len(idx), version)

    app.state.all_datasets = all_datasets
    app.state.default_dataset_version = DEFAULT_DATASET_VERSION
    app.state.annotations_dir = ANNOTATIONS_DIR
    app.state.reviewer_codes_path = REVIEWER_CODES_PATH

    # Tool catalog (read-only) — built once per dataset version at startup.
    tool_catalogs = {
        version: build_catalog(
            version,
            objs,
            CONDITIONS_YAML_PATH,
            TOOL_COSTS_PATH,
            CONDITION_TOOL_GUIDANCE_PATH,
        )
        for version, (_idx, objs) in all_datasets.items()
    }
    app.state.tool_catalogs = tool_catalogs

    # Ensure on-disk locations exist.
    ANNOTATIONS_DIR.mkdir(parents=True, exist_ok=True)
    TOOL_REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWER_CODES_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Reviewer registry — reloads automatically when the YAML mtime changes.
    app.state.reviewer_registry = ReviewerCodeRegistry(REVIEWER_CODES_PATH)

    # Brute-force throttle on the auth path (codes are bearer secrets).
    app.state.auth_limiter = AuthRateLimiter()

    # Annotation store — filesystem-backed.
    app.state.annotation_store = AnnotationStore(ANNOTATIONS_DIR)
    app.state.tool_review_store = ToolReviewStore(TOOL_REVIEWS_DIR)

    from .routes import admin as admin_routes
    from .routes import annotations as annotations_routes
    from .routes import datasets as datasets_routes
    from .routes import methodology as methodology_routes
    from .routes import progress as progress_routes
    from .routes import reviewers as reviewers_routes
    from .routes import tool_review as tool_review_routes

    app.include_router(reviewers_routes.router, prefix="/api/v1")
    app.include_router(datasets_routes.router, prefix="/api/v1")
    app.include_router(annotations_routes.router, prefix="/api/v1")
    app.include_router(progress_routes.router, prefix="/api/v1")
    app.include_router(methodology_routes.router, prefix="/api/v1")
    app.include_router(tool_review_routes.router, prefix="/api/v1")
    app.include_router(admin_routes.router, prefix="/api/v1")

    if WEB_DIST.exists():
        app.mount("/", StaticFiles(directory=str(WEB_DIST), html=True), name="static")

    return app


app = create_app()
