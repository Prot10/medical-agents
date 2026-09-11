"""Where training weights live: EOS only.

The VM's local disk has no room for model weights; every checkpoint, adapter and final model is
written under the project's EOS checkpoints directory. Logs, rollouts and evaluations stay local.
"""

from __future__ import annotations

import os
from pathlib import Path

WEIGHTS_ROOT = "/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints"


def require_eos(path: str | Path) -> Path:
    """Return ``path`` as an absolute EOS path; refuse anything on the local disk."""
    absolute = Path(os.path.abspath(path))
    if absolute.parts[:2] != ("/", "eos"):
        raise ValueError(f"weights must be written on EOS (e.g. {WEIGHTS_ROOT}/<run>/<model>), got {absolute}")
    return absolute
