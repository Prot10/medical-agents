"""GitHub Copilot device flow authentication and token management."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import httpx
from fastapi import APIRouter

router = APIRouter(tags=["copilot"])
logger = logging.getLogger(__name__)

# VS Code's publicly known Copilot client ID
GITHUB_CLIENT_ID = "01ab8ac9400c4e429b23"
COPILOT_API_BASE = "https://api.githubcopilot.com"

# Token persistence file (next to traces dir)
_TOKEN_FILE = Path(__file__).resolve().parents[5] / "data" / ".copilot_token.json"

# In-memory token cache
_github_token: str | None = None
_copilot_token: str | None = None
_copilot_token_expires: float = 0

# Static model list for Copilot
COPILOT_MODELS = [
    {"id": "oswe-vscode-prime", "name": "Raptor Mini", "vendor": "Microsoft"},
    {"id": "grok-code-fast-1", "name": "Grok Code Fast 1", "vendor": "xAI"},
    {"id": "claude-haiku-4.5", "name": "Claude Haiku 4.5", "vendor": "Anthropic"},
    {"id": "claude-sonnet-4.6", "name": "Claude Sonnet 4.6", "vendor": "Anthropic"},
    {"id": "claude-opus-4.6", "name": "Claude Opus 4.6", "vendor": "Anthropic"},
    {"id": "gemini-3-flash", "name": "Gemini 3 Flash", "vendor": "Google"},
    {"id": "gemini-3.1-pro", "name": "Gemini 3.1 Pro", "vendor": "Google"},
    {"id": "gpt-5-mini", "name": "GPT-5 Mini", "vendor": "OpenAI"},
    {"id": "gpt-5.4", "name": "GPT-5.4", "vendor": "OpenAI"},
    {"id": "gpt-5.1-codex-mini", "name": "GPT-5.1-Codex-Mini", "vendor": "OpenAI"},
    {"id": "gpt-5.3-codex", "name": "GPT-5.3-Codex", "vendor": "OpenAI"},
]


def _save_token(token: str) -> None:
    """Persist GitHub token to disk."""
    try:
        _TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        _TOKEN_FILE.write_text(json.dumps({"github_token": token}))
    except Exception as e:
        logger.warning(f"Failed to save token: {e}")


def _load_token() -> str | None:
    """Load persisted GitHub token from disk."""
    try:
        if _TOKEN_FILE.exists():
            data = json.loads(_TOKEN_FILE.read_text())
            return data.get("github_token")
    except Exception as e:
        logger.warning(f"Failed to load token: {e}")
    return None


def _delete_token() -> None:
    """Delete persisted token from disk."""
    try:
        if _TOKEN_FILE.exists():
            _TOKEN_FILE.unlink()
    except Exception as e:
        logger.warning(f"Failed to delete token: {e}")


def _ensure_loaded() -> None:
    """Load persisted token into memory on first access."""
    global _github_token
    if _github_token is None:
        _github_token = _load_token()


@router.post("/copilot/device-code")
async def start_device_flow() -> dict:
    """Start GitHub OAuth device flow. Returns user_code and verification_uri."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            "https://github.com/login/device/code",
            headers={"Accept": "application/json"},
            data={"client_id": GITHUB_CLIENT_ID, "scope": "read:user"},
        )
        if resp.status_code != 200:
            return {"error": f"GitHub returned {resp.status_code}"}
        data = resp.json()
        if "error" in data:
            return {"error": data.get("error_description", data["error"])}
        return {
            "device_code": data["device_code"],
            "user_code": data["user_code"],
            "verification_uri": data["verification_uri"],
            "expires_in": data["expires_in"],
            "interval": data["interval"],
        }


@router.post("/copilot/poll-token")
async def poll_token(body: dict) -> dict:
    """Poll GitHub for OAuth token after user enters the code."""
    global _github_token

    device_code = body.get("device_code")
    if not device_code:
        return {"status": "error", "error": "device_code required"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
        )
        data = resp.json()

        if "error" in data:
            error = data["error"]
            if error == "authorization_pending":
                return {"status": "pending"}
            if error == "slow_down":
                return {"status": "pending", "interval": data.get("interval", 10)}
            if error == "expired_token":
                return {"status": "expired"}
            if error == "access_denied":
                return {"status": "denied"}
            return {"status": "error", "error": data.get("error_description", error)}

        if "access_token" in data:
            _github_token = data["access_token"]
            _save_token(_github_token)
            return {"status": "complete"}

        return {"status": "error", "error": "Unexpected response"}


@router.get("/copilot/status")
async def copilot_status() -> dict:
    """Check if we have a valid Copilot connection."""
    _ensure_loaded()
    if not _github_token:
        return {"authenticated": False, "copilot_access": False}

    token = await _get_copilot_token()
    if token:
        return {"authenticated": True, "copilot_access": True}
    return {"authenticated": True, "copilot_access": False}


@router.get("/copilot/models")
async def get_copilot_models() -> list[dict]:
    """Return available Copilot models (requires authentication)."""
    _ensure_loaded()
    if not _github_token:
        return []

    token = await _get_copilot_token()
    if not token:
        return []

    return [
        {
            "key": f"copilot:{m['id']}",
            "name": f"{m['name']}",
            "hf_model_id": m["id"],
            "description": f"Copilot · {m['vendor']}",
            "status": "ready",
            "provider": "copilot",
        }
        for m in COPILOT_MODELS
    ]


@router.post("/copilot/logout")
async def copilot_logout() -> dict:
    """Clear stored tokens."""
    global _github_token, _copilot_token, _copilot_token_expires
    _github_token = None
    _copilot_token = None
    _copilot_token_expires = 0
    _delete_token()
    return {"status": "ok"}


async def get_copilot_api_token() -> str | None:
    """Get a valid Copilot API token for use by agent endpoints."""
    _ensure_loaded()
    return await _get_copilot_token()


async def _get_copilot_token() -> str | None:
    """Get or refresh the Copilot API token."""
    global _github_token, _copilot_token, _copilot_token_expires

    if not _github_token:
        return None

    # Return cached if still valid (5 min buffer)
    if _copilot_token and _copilot_token_expires > time.time() + 300:
        return _copilot_token

    # Exchange GitHub token for Copilot token
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://api.github.com/copilot_internal/v2/token",
                headers={
                    "Authorization": f"token {_github_token}",
                    "Accept": "application/json",
                    "User-Agent": "NeuroAgent/1.0",
                },
            )
            if resp.status_code != 200:
                logger.warning(f"Copilot token exchange failed: {resp.status_code}")
                if resp.status_code == 401:
                    _github_token = None
                    _delete_token()
                return None
            data = resp.json()
            _copilot_token = data["token"]
            _copilot_token_expires = data["expires_at"]
            return _copilot_token
    except Exception as e:
        logger.warning(f"Failed to get Copilot token: {e}")
        return None
