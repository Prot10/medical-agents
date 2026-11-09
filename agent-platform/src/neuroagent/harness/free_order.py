"""Free-order ablation: the agent orders any test in free text instead of picking from a catalogue.

SDBench (Nori et al., Science 2026) gives its agents no menu and lets a gatekeeper model answer
every order. Here only the interface changes: the agent sees one tool, ``request_test``, and a
translator model maps each order onto the typed catalogue. A mapped order is executed by the
unchanged ``NeuroBenchEnvironment`` (same MockServer answer, same price), and the policy reward
scores the translated actions, so a free-order run is directly comparable with a menu run.

Only an order the catalogue does not cover reaches the gatekeeper, which writes a findings-only
report from the case (normal unless the case documents otherwise, never naming the diagnosis) at
a fixed price. Vague orders, several tests in one order, and anything that is not a test are
never placed: the agent gets a one-line reply and the turn is spent.

Every translation and report is cached on disk, keyed by stage, model, prompt version and input,
so a re-run or another agent model sees identical answers (temperature 0 is not deterministic
on Vertex). The gatekeeper sees the case; the translator sees only the order and the catalogue.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from neuroagent_schemas import (
    ActionProposed,
    ClinicalEpisode,
    NeuroBenchCase,
    PluginEvent,
    ToolAction,
)

from ..tools.base import ToolResult
from .context import format_patient_info

REQUEST_TEST_NAME = "request_test"
TRANSLATION_NAMESPACE = "free_order.translation"
PROMPT_VERSION = "free-order-v5"

# Kinds of translated order. Only ``mapped`` and ``off_catalogue`` are placed and priced.
MAPPED = "mapped"
OFF_CATALOGUE = "off_catalogue"
UNPLACED_KINDS = frozenset({"vague", "multiple", "not_a_test"})
KINDS = frozenset({MAPPED, OFF_CATALOGUE, *UNPLACED_KINDS})

# Tool names the reward sees for orders that are not catalogue calls. They match no criterion, so
# they count as unjustified actions, as a schema-rejected call does in the menu arm.
OFF_CATALOGUE_TOOL = "off_catalogue_order"
UNPLACED_TOOL = "unplaced_order"

REQUEST_TEST_TOOL = {
    "type": "function",
    "function": {
        "name": REQUEST_TEST_NAME,
        "description": (
            "Order one diagnostic test, investigation or examination and receive its result. "
            "Name it specifically, as on an order form."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "test": {"type": "string", "description": "The test, as named on an order form."},
                "details": {
                    "type": "string",
                    "description": "Protocol, sequences, contrast, specimen, panels or other specification, if any.",
                },
            },
            "required": ["test"],
        },
    },
}

TRANSLATOR_PROMPT = """You translate a clinician's free-text order into a hospital's order catalogue.
The catalogue is the list of function definitions below. Answer with one JSON object only:
{"kind": "...", "tool_name": "...", "arguments": {...}, "message": "..."}

kind is one of:
- "mapped": the catalogue contains this same test. Give tool_name and arguments of exactly one
  catalogue call. Never substitute a different test and never add tests the order did not ask
  for, with one exception: a test the catalogue offers only inside a panel maps to that panel, as
  the laboratory would run it (a single paraneoplastic antibody is the paraneoplastic panel). In
  an order of several tests of which only some are in the catalogue, map those and leave out the
  rest; it is off_catalogue only when none is. Set an argument only when the order names that value or its exact equivalent
  ("continuous EEG" is the continuous ICU recording); leave out every optional argument the
  order does not name, even when the catalogue offers several values (the hospital's default
  applies). Set clinical_context to the order text. Several tests that are one catalogue call
  (for example several lab panels) are one mapped call. An order for a catalogue procedure that
  adds a purpose, volume or technique the catalogue does not model is still that procedure (a
  large-volume lumbar puncture or CSF tap test is a lumbar puncture); the detail stays in
  clinical_context. One assay that the catalogue splits into subtypes maps to all of them (VGCC
  antibodies are the P/Q- and N-type assays). A step the order makes conditional ("if negative,
  MRI"; "CSF if a lumbar puncture is done") is not part of the order: map the unconditional
  test. Before calling an order off_catalogue, look in every enum of every catalogue function
  for the same test under a synonym or abbreviation; a related, broader or different test is
  not the same test.
- "vague": the order names a test but leaves out a value of an argument the catalogue marks as
  required (which study, specimen, procedure, test type), names a whole family of tests
  ("basic labs", "hypercoagulable panel"), or leaves the choice between alternatives open
  ("Holter or event recorder"). A missing optional argument is never vague. message is a short question asking
  for the missing specification. Never list or suggest catalogue options.
- "multiple": the order needs more than one catalogue call. message asks to order one test at a time.
- "off_catalogue": a real test, examination or investigation the catalogue does not contain.
- "not_a_test": a treatment, consultation, referral, admission or anything else that is not a
  test. message says that only tests, investigations and examinations can be ordered.
Use only enum values that appear in the catalogue. Leave tool_name and arguments empty unless
kind is "mapped".

Catalogue:
"""

GATEKEEPER_PROMPT = """You are the results service of a simulated hospital. A clinician ordered a test
that the hospital's structured catalogue does not cover. Write its result for this patient, using
the true case below, under these rules:
- Report findings only, as the performing department would write them: measurements and
  observations, with no impression, no interpretation that names a diagnosis, no recommendation.
- Abnormal only where the documented case implies this test would be abnormal; otherwise a
  normal result. When unsure, normal.
- Never contradict the documented findings and results. Never name the final diagnosis, its
  synonyms or its codes. Never say that the case is simulated.
- Keep it to a few lines, like a real report.
Answer with one JSON object only: {"result": "..."}"""


def normalize_order(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().strip(".;,").lower()


def _sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _parse_json_object(content: str | None) -> dict[str, Any]:
    text = (content or "").strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError(f"no JSON object in the answer: {text[:200]!r}")
    value = json.loads(text[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("the answer is not a JSON object")
    return value


class GatekeeperLLM:
    """OpenAI-compatible chat call to the CERN AI gateway, without streaming.

    The key is read from ``key_file`` at the first call, never logged. GLM-5.3 on Vertex returns
    one empty chunk when streamed and reasons before answering, so ``max_tokens`` stays high.
    """

    def __init__(
        self,
        *,
        model: str,
        base_url: str = "https://aigw.cern.ch/v1",
        key_file: str = "~/.config/cern-ml/aigw.key",
        max_tokens: int = 100_000,
        timeout: float = 600.0,
        attempts: int = 4,
    ) -> None:
        self.model = model
        self.base_url = base_url
        self.key_file = key_file
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.attempts = attempts
        self._client = None
        self._lock = threading.Lock()

    def _openai(self):
        with self._lock:
            if self._client is None:
                from openai import OpenAI

                key = Path(self.key_file).expanduser().read_text().strip()
                self._client = OpenAI(base_url=self.base_url, api_key=key, timeout=self.timeout, max_retries=0)
            return self._client

    def complete(self, system: str, user: str) -> dict[str, Any]:
        last: Exception | None = None
        for attempt in range(self.attempts):
            started = time.perf_counter()
            try:
                response = self._openai().chat.completions.create(
                    model=self.model,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                    temperature=0,
                    max_tokens=self.max_tokens,
                    stream=False,
                )
            except Exception as exc:  # transient gateway errors (504, timeouts) are retried
                last = exc
                time.sleep(min(60, 5 * 2**attempt))
                continue
            choice = response.choices[0]
            usage = response.usage
            return {
                "content": choice.message.content,
                "reasoning": getattr(choice.message, "reasoning_content", None),
                "finish_reason": choice.finish_reason,
                "prompt_tokens": int(usage.prompt_tokens) if usage else 0,
                "completion_tokens": int(usage.completion_tokens) if usage else 0,
                "seconds": round(time.perf_counter() - started, 2),
            }
        raise RuntimeError(f"gateway call failed after {self.attempts} attempts: {last}")


class FreeOrderGatekeeper:
    """Translator and off-catalogue report writer with a content-addressed disk cache."""

    def __init__(
        self,
        llm: Any,
        *,
        cache_dir: str | Path,
        off_catalogue_cost_usd: float = 150.0,
    ) -> None:
        self.llm = llm
        self.cache_dir = Path(cache_dir)
        self.off_catalogue_cost_usd = off_catalogue_cost_usd
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()

    def config(self) -> dict[str, Any]:
        return {
            "model": getattr(self.llm, "model", type(self.llm).__name__),
            "prompt_version": PROMPT_VERSION,
            "prompts_sha256": _sha256([TRANSLATOR_PROMPT, GATEKEEPER_PROMPT, REQUEST_TEST_TOOL]),
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "cache_dir": str(self.cache_dir),
            "off_catalogue_cost_usd": self.off_catalogue_cost_usd,
        }

    def _cached(
        self, stage: str, key_material: dict[str, Any], system: str, user: str, parse, fallback=None
    ) -> tuple[dict, bool]:
        """Return (parsed record, came_from_cache). One call per key even under concurrency.

        An answer that fails ``parse`` is asked once more with the error; if the second answer
        fails too, ``fallback(error)`` is stored (flagged) when given, else the error is raised.
        """
        key = _sha256({"stage": stage, "model": getattr(self.llm, "model", ""), "v": PROMPT_VERSION, **key_material})
        path = self.cache_dir / stage / f"{key}.json"
        with self._locks_guard:
            lock = self._locks.setdefault(key, threading.Lock())
        with lock:
            if path.exists():
                return json.loads(path.read_text()), True
            raw = self.llm.complete(system, user)
            if raw.get("finish_reason") == "length":
                raise RuntimeError(f"{stage} answer cut at max_tokens")
            try:
                parsed = parse(_parse_json_object(raw.get("content")))
            except (ValueError, KeyError) as exc:
                # One retry with the parse error; a second failure is the gateway's, not the agent's.
                raw = self.llm.complete(system, f"{user}\n\nYour previous answer was invalid ({exc}). Answer with the JSON object only.")
                try:
                    parsed = parse(_parse_json_object(raw.get("content")))
                except (ValueError, KeyError) as second:
                    if fallback is None:
                        raise
                    parsed = {**fallback(second), "fallback": str(second)}
            record = {"key": key_material, "parsed": parsed, "llm": raw}
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(record, indent=2, ensure_ascii=False))
            tmp.replace(path)
            return record, False

    def translate(self, test: str, details: str, catalogue: list[dict[str, Any]], *, error: str | None = None) -> tuple[dict, bool]:
        order = {"test": normalize_order(test), "details": normalize_order(details)}
        catalogue_text = json.dumps(catalogue, sort_keys=True, ensure_ascii=False)
        user = f"Order: {json.dumps(order, ensure_ascii=False)}"
        if error:
            user += f"\n\nA previous translation of this order was refused by the catalogue: {error}"

        def parse(value: dict[str, Any]) -> dict[str, Any]:
            kind = value.get("kind")
            if kind not in KINDS:
                raise ValueError(f"unknown kind {kind!r}")
            if kind == MAPPED and not value.get("tool_name"):
                raise ValueError("a mapped order needs tool_name")
            return {
                "kind": kind,
                "tool_name": (value.get("tool_name") or None) if kind == MAPPED else None,
                "arguments": dict(value.get("arguments") or {}) if kind == MAPPED else {},
                "message": str(value.get("message") or ""),
            }

        record, cached = self._cached(
            "translate",
            {"order": order, "catalogue_sha256": _sha256(catalogue_text), "error": error},
            TRANSLATOR_PROMPT + catalogue_text,
            user,
            parse,
        )
        return record["parsed"], cached

    def report(self, case: NeuroBenchCase, test: str, details: str) -> tuple[dict, bool]:
        order = {"test": normalize_order(test), "details": normalize_order(details)}
        truth = case.ground_truth
        dump = case.model_dump(mode="json", exclude_none=True)
        user = "\n\n".join(
            [
                "Presentation:\n" + format_patient_info(case),
                "Final diagnosis: " + "; ".join(truth.diagnosis.accepted[:3]),
                "Key clinical evidence: " + json.dumps(dump["ground_truth"].get("key_clinical_evidence", []), ensure_ascii=False),
                "Documented results: "
                + json.dumps(
                    {k: dump.get(k) for k in ("initial_tool_outputs", "followup_outputs", "fallback_tool_outputs")},
                    ensure_ascii=False,
                ),
                f"Order: {json.dumps(order, ensure_ascii=False)}",
            ]
        )
        banned = leak_terms(case)

        def parse(value: dict[str, Any]) -> dict[str, Any]:
            result = str(value["result"]).strip()
            if not result:
                raise ValueError("empty result")
            hits = sorted(term for term in banned if term in result.lower())
            if hits:
                raise ValueError(f"the result names the diagnosis ({', '.join(hits)}); rewrite it without it")
            return {"result": result}

        record, cached = self._cached(
            "report",
            {"case_id": case.case_id, "case_sha256": _sha256(dump), "order": order},
            GATEKEEPER_PROMPT,
            user,
            parse,
            # Twice naming the diagnosis: serve a bare normal line rather than the leak.
            fallback=lambda _error: {"result": "Study performed. No abnormality reported."},
        )
        return record["parsed"], cached


def leak_terms(case: NeuroBenchCase) -> set[str]:
    """Diagnosis labels and codes a generated report must never contain (lower case)."""
    truth = case.ground_truth.diagnosis
    terms = {label.lower() for label in truth.accepted if len(label) >= 4}
    terms |= {code.lower() for code in truth.icd_codes}
    return terms


@dataclass
class FreeOrderEnvironment:
    """Wraps the typed environment behind one free-text ``request_test`` tool."""

    inner: Any
    gatekeeper: FreeOrderGatekeeper
    environment_id: str = "neurobench-v2+free-order"
    translations: list[dict[str, Any]] = field(default_factory=list)

    @property
    def case(self) -> NeuroBenchCase:
        return self.inner.case

    def tool_definitions(self) -> list[dict[str, Any]]:
        return [REQUEST_TEST_TOOL]

    def direct_observations(self):
        return self.inner.direct_observations()

    def execute(self, action: ToolAction) -> ToolResult:
        test = str(action.arguments.get("test") or "")
        details = str(action.arguments.get("details") or "")
        if action.tool_name != REQUEST_TEST_NAME or not test.strip():
            return self._record(
                {"kind": "vague", "message": "Name the test to order."},
                ToolResult(tool_name=REQUEST_TEST_NAME, success=False, error_message="Name the test to order.", rejected=True, cost_usd=0.0),
                cached=True,
            )
        catalogue = self.inner.tool_definitions()
        translation, cached = self.gatekeeper.translate(test, details, catalogue)
        if translation["kind"] == MAPPED:
            result = self._place(translation)
            if result.rejected:
                translation, cached = self.gatekeeper.translate(test, details, catalogue, error=result.error_message)
                result = self._place(translation) if translation["kind"] == MAPPED else None
                if result is not None and result.rejected:
                    translation = {**translation, "kind": OFF_CATALOGUE, "translation_error": result.error_message}
                    result = None
            if result is not None:
                return self._record(translation, result, cached=cached)
        if translation["kind"] == OFF_CATALOGUE:
            report, report_cached = self.gatekeeper.report(self.case, test, details)
            result = ToolResult(
                tool_name=REQUEST_TEST_NAME,
                success=True,
                output={"test": test, "result": report["result"]},
                cost_usd=self.gatekeeper.off_catalogue_cost_usd,
            )
            return self._record({**translation, "report_cached": report_cached}, result, cached=cached)
        message = translation.get("message") or "Order one specific test at a time."
        result = ToolResult(tool_name=REQUEST_TEST_NAME, success=False, error_message=message, rejected=True, cost_usd=0.0)
        return self._record(translation, result, cached=cached)

    def _place(self, translation: dict[str, Any]) -> ToolResult:
        typed = ToolAction(tool_name=translation["tool_name"], arguments=translation["arguments"])
        return self.inner.execute(typed)

    def _record(self, translation: dict[str, Any], result: ToolResult, *, cached: bool) -> ToolResult:
        """Keep the typed translation for the reward; the agent sees only ``request_test``."""
        self.translations.append({**translation, "cached": cached})
        return result.model_copy(update={"tool_name": REQUEST_TEST_NAME})


def translation_event(turn: int, translation: dict[str, Any]) -> PluginEvent:
    return PluginEvent(turn=turn, namespace=TRANSLATION_NAMESPACE, payload=translation)


def typed_episode(episode: ClinicalEpisode) -> ClinicalEpisode:
    """The episode as the reward must see it: each free-text order replaced by its typed action.

    A mapped order becomes its catalogue call; an off-catalogue order and an order never placed
    become actions no criterion matches. Episodes from other loops are returned unchanged.
    """
    by_turn = {
        event.turn: event.payload
        for event in episode.events
        if isinstance(event, PluginEvent) and event.namespace == TRANSLATION_NAMESPACE
    }
    if not by_turn:
        return episode
    events = []
    for event in episode.events:
        action = getattr(event, "action", None)
        if isinstance(event, ActionProposed) and isinstance(action, ToolAction) and action.tool_name == REQUEST_TEST_NAME:
            translation = by_turn.get(event.turn, {})
            kind = translation.get("kind")
            if kind == MAPPED:
                typed = ToolAction(tool_name=translation["tool_name"], arguments=translation["arguments"])
            else:
                typed = ToolAction(
                    tool_name=OFF_CATALOGUE_TOOL if kind == OFF_CATALOGUE else UNPLACED_TOOL,
                    arguments=dict(action.arguments),
                )
            event = event.model_copy(update={"action": typed})
        events.append(event)
    return episode.model_copy(update={"events": events})


def translation_counts(episode: ClinicalEpisode) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in episode.events:
        if isinstance(event, PluginEvent) and event.namespace == TRANSLATION_NAMESPACE:
            kind = str(event.payload.get("kind"))
            counts[kind] = counts.get(kind, 0) + 1
    return counts
