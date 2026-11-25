"""Agent-mode configuration: the sections, their fixed case sets and where their records go.

``config/review/agent_mode_sets.yaml`` declares the sections. The synthetic section serves frozen
copies of NeuroBench cases kept in the repo, so a later case edit never changes what a physician
worked on. The MIMIC section exists only where the deployment names its two directories in the
environment; its cases are read from there at start-up and nothing of it is written in the repo.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import random
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from neuroagent_schemas import NeuroBenchCase
from pydantic import ValidationError

from neuroagent.datasets import REPO_ROOT
from neuroagent.harness.profile import HarnessProfile, load_profiles

logger = logging.getLogger(__name__)

PROFILES_DIR = REPO_ROOT / "agent-platform" / "config" / "profiles"
_ID_PATTERN = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")
# Section key (URL and storage) → the `sections` entry a reviewer code needs to open it.
SECTION_ACCESS = {"synthetic": "agent_synthetic", "mimic": "agent_mimic"}


@dataclass(frozen=True, slots=True)
class AgentSectionConfig:
    key: str
    access: str
    set_id: str
    title: str
    description: str
    case_ids: tuple[str, ...]  # the fixed order; a case's number is its 1-based position
    cases: Mapping[str, NeuroBenchCase] = field(repr=False)
    case_sha256: Mapping[str, str] = field(repr=False)  # of the case file's bytes
    records_dir: Path
    # True for cases derived from patient records (MIMIC): their logs stay out of the repo.
    record_derived: bool = False

    @property
    def set_sha256(self) -> str:
        return hashlib.sha256(json.dumps(list(self.case_ids)).encode()).hexdigest()

    def number_of(self, case_id: str) -> int:
        return self.case_ids.index(case_id) + 1

    def case_at(self, number: int) -> NeuroBenchCase | None:
        if 1 <= number <= len(self.case_ids):
            return self.cases[self.case_ids[number - 1]]
        return None


@dataclass(frozen=True, slots=True)
class AgentModeConfig:
    profile: HarnessProfile  # the checked policy profile whose limits the physician works under
    limits_from: str
    # The agent is never told its turn budget; neither is the physician unless this is set.
    show_step_budget: bool
    sections: Mapping[str, AgentSectionConfig]


def _inside_repo(path: Path) -> bool:
    return path.resolve().is_relative_to(REPO_ROOT.resolve())


def read_cases(directory: Path, *, quiet_errors: bool = False) -> tuple[dict[str, NeuroBenchCase], dict[str, str]]:
    """Every case under ``directory/cases`` (or ``directory`` itself), with its file's sha256.

    Raises:
        ValueError: A file is not a valid case. With ``quiet_errors`` the message names the file
            and the failing fields only, never the content (record-derived cases).
    """
    folder = directory / "cases" if (directory / "cases").is_dir() else directory
    cases: dict[str, NeuroBenchCase] = {}
    hashes: dict[str, str] = {}
    for path in sorted(folder.glob("*.json")):
        raw = path.read_bytes()
        try:
            case = NeuroBenchCase.model_validate_json(raw)
        except ValidationError as exc:
            if quiet_errors:
                fields = sorted({".".join(str(p) for p in error["loc"]) for error in exc.errors()})
                raise ValueError(f"invalid case file {path.name}: fields {fields}") from None
            raise ValueError(f"invalid case file {path}: {exc}") from exc
        cases[case.case_id] = case
        hashes[case.case_id] = hashlib.sha256(raw).hexdigest()
    return cases, hashes


def _synthetic(key: str, body: Mapping[str, Any], records_root: Path) -> AgentSectionConfig:
    cases_dir = REPO_ROOT / str(body["cases_dir"])
    cases, hashes = read_cases(cases_dir)
    case_ids = tuple(body.get("cases") or ())
    if not case_ids or len(set(case_ids)) != len(case_ids):
        raise ValueError(f"agent-mode section {key!r}: cases must be a non-empty list without repeats")
    missing = [case_id for case_id in case_ids if case_id not in cases]
    extra = sorted(set(cases) - set(case_ids))
    if missing or extra:
        raise ValueError(f"agent-mode section {key!r}: {cases_dir} is missing {missing} and holds unlisted {extra}")
    return AgentSectionConfig(
        key=key,
        access=SECTION_ACCESS[key],
        set_id=str(body["set_id"]),
        title=str(body.get("title") or key),
        description=str(body.get("description") or "").strip(),
        case_ids=case_ids,
        cases=cases,
        case_sha256=hashes,
        records_dir=records_root,
    )


def _record_section(key: str, body: Mapping[str, Any], env: Mapping[str, str]) -> AgentSectionConfig | None:
    """A section whose cases and logs live where the environment says, or None when it is unset."""
    cases_env, records_env = str(body["cases_dir_env"]), str(body["records_dir_env"])
    cases_value, records_value = env.get(cases_env, "").strip(), env.get(records_env, "").strip()
    if not cases_value and not records_value:
        return None
    if not cases_value or not records_value:
        raise ValueError(f"agent-mode section {key!r} needs both {cases_env} and {records_env}")
    cases_dir, records_dir = Path(cases_value).expanduser(), Path(records_value).expanduser()
    if _inside_repo(cases_dir) or _inside_repo(records_dir):
        raise ValueError(f"agent-mode section {key!r}: record-derived cases and logs must stay outside the repository")
    if not cases_dir.is_dir():
        raise ValueError(f"agent-mode section {key!r}: {cases_env} is not a directory")
    cases, hashes = read_cases(cases_dir, quiet_errors=True)
    if not cases:
        raise ValueError(f"agent-mode section {key!r}: no case files under {cases_env}")
    list_file = env.get(str(body.get("case_list_env") or ""), "").strip()
    if list_file:
        case_ids = Path(list_file).expanduser().read_text().split()
        unknown = len([case_id for case_id in case_ids if case_id not in cases])
        if unknown or len(set(case_ids)) != len(case_ids):
            raise ValueError(f"agent-mode section {key!r}: the case list repeats ids or names {unknown} unknown case(s)")
    else:
        case_ids = sorted(cases)
        random.Random(int(body.get("order_seed", 0))).shuffle(case_ids)
    expected = body.get("expected_cases")
    if expected is not None and len(case_ids) != int(expected):
        logger.warning("Agent-mode section %s serves %d cases, %s expected", key, len(case_ids), expected)
    records_dir.mkdir(parents=True, exist_ok=True)
    return AgentSectionConfig(
        key=key,
        access=SECTION_ACCESS[key],
        set_id=str(body["set_id"]),
        title=str(body.get("title") or key),
        description=str(body.get("description") or "").strip(),
        case_ids=tuple(case_ids),
        cases=cases,
        case_sha256=hashes,
        records_dir=records_dir,
        record_derived=True,
    )


def load_agent_mode(
    path: Path, *, records_root: Path, env: Mapping[str, str] | None = None
) -> AgentModeConfig | None:
    """Read the agent-mode file; a missing file means the study is not served at all.

    ``records_root`` is where the synthetic section's records go. A record-derived section is
    present only when its environment variables are set.

    Raises:
        ValueError: The file names an unknown profile or section, or a section is inconsistent.
    """
    if not path.exists():
        return None
    env = os.environ if env is None else env
    raw: dict[str, Any] = yaml.safe_load(path.read_text()) or {}
    profiles = load_profiles(PROFILES_DIR)
    profile_id = str(raw.get("profile"))
    if profile_id not in profiles:
        raise ValueError(f"agent-mode: unknown profile {profile_id!r}")
    sections: dict[str, AgentSectionConfig] = {}
    for key, body in (raw.get("sections") or {}).items():
        if key not in SECTION_ACCESS or not _ID_PATTERN.fullmatch(str(body.get("set_id", ""))):
            raise ValueError(f"agent-mode: bad section {key!r} or set_id")
        section = _record_section(key, body, env) if body.get("cases_dir_env") else _synthetic(key, body, records_root)
        if section is not None:
            sections[key] = section
            logger.info("Agent-mode section %s: %d cases (set %s)", key, len(section.case_ids), section.set_id)
    return AgentModeConfig(
        profile=profiles[profile_id],
        limits_from=profile_id,
        show_step_budget=bool(raw.get("show_step_budget", False)),
        sections=sections,
    )
