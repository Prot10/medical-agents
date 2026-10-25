from __future__ import annotations
from neuroagent_schemas import (
    NeuroBenchCase, EEGReport, MRIReport, ECGReport, LabResults, CSFResults,
    LiteratureSearchResult, DrugInteractionResult,
    CTReport, EchoReport, CardiacMonitoringReport, LabValue,
    AdvancedImagingReport, SpecializedTestReport,
)
from .base import ToolCall, ToolResult
from .fallback_library import FallbackLibrary, default_library
from .followup_matcher import match_followup, resolve_followup
from .lab_matching import (
    LabMatcher, like as lab_like, mentions, specimen_compatible, split_sentences, tokens as lab_tokens,
)
from .vocabulary import (
    DOMAIN_PACKS,
    advanced_imaging_modalities,
    assessment_timings,
    assessment_types,
    body_imaging_studies,
    by_type_values,
    csf_sources,
    echocardiogram_types,
    eeg_types,
    genetic_panels,
    microbiology_specimens,
    mri_protocols,
    specialized_test_types,
    tissue_procedures,
)
from typing import Any, Iterable
import json
import re
from pydantic import BaseModel


class MockServer:
    """Serves pre-generated tool outputs from a NeuroBenchCase."""

    def __init__(self, case: NeuroBenchCase, library: FallbackLibrary | None = None):
        self.case = case
        self.library = library or default_library()
        # The vocabulary this case's catalogue advertises, so a stored report naming a pack term
        # (a recorded `abdomen_xray`) is adjudicated like any other study.
        self.packs = DOMAIN_PACKS[case.domain]
        self.call_log: list[ToolCall] = []
        self._labs = LabMatcher(self.library.analyte_tests)
        # Trigger slugs of follow-ups already served this session. Lets distinct
        # re-orders of the same tool escalate through distinct follow-ups.
        self._served_triggers: set[str] = set()

    # The parameter that says *which study* was ordered, and the field the stored report uses to
    # say which study it is. A tool that stands in for several studies must not answer one
    # question with another study's report: ordering ascitic fluid in a case that stored a blood
    # culture returned the blood culture, and a brain FDG-PET returned a cardiac one. Both were
    # invisible while each tool served a single study per case.
    _DISCRIMINATOR: dict[str, tuple[str, Any]] = {
        "order_microbiology": ("specimen", microbiology_specimens),
        "order_body_imaging": ("study", body_imaging_studies),
        "order_advanced_imaging": ("modality", advanced_imaging_modalities),
        "order_echocardiogram": ("echo_type", echocardiogram_types),
        # Genetic panels are vocabulary too: without them a stored `genetic_panel:ALS` report
        # passed as prose and was served for an `emg_ncs` order whose context mentioned ALS.
        "order_specialized_test": (
            "test_type",
            lambda packs=(): specialized_test_types(packs=packs)
            + [f"genetic_panel:{p}" for p in genetic_panels(packs=packs)],
        ),
        "obtain_tissue_diagnosis": ("procedure", tissue_procedures),
        "perform_clinical_assessment": ("assessment_type", assessment_types),
        # Added on the October 2026 review. The monitors were once left out as "variants of one
        # question", but a recording's duration decides what it can capture: a 24-hour Holter
        # order received the case's 30-day monitor or 12 months of pacemaker diagnostics, and
        # with them the paroxysmal AF the short recording was meant to miss (VASC-DEM M04, P08,
        # P09, S07, S09; MIG-AURA-P07 needed a separate follow-up to work around it).
        "order_cardiac_monitoring": (
            "monitor_type", lambda packs=(): by_type_values("order_cardiac_monitoring", packs=packs)
        ),
        # Added 24 Oct 2026. A routine order received the case's stored video-EEG (FND, the
        # habitual events captured on video) or its continuous ICU recording (SE), and with them
        # what a 30-minute interictal recording would usually miss.
        "analyze_eeg": ("eeg_type", eeg_types),
    }

    # Discriminators whose omitted parameter names the schema default (`_ENUM_DEFAULTS`). An EEG
    # order without `eeg_type` is billed, and placed, as a routine EEG, so it is routed as one.
    # The other primary discriminators leave an omitted parameter unadjudicated, as before.
    _DEFAULTED = frozenset({"analyze_eeg"})

    # Terms of one discriminator that are the same study for routing. Continuous EEG in the ICU is
    # a video-EEG recording (ACNS 2015 consensus on critical-care cEEG); the two terms differ in
    # the unit and the indication, not in what the recording captures. SE and NMDAR-ENC policies
    # accept either for one criterion, and with exact routing the second alternative received a
    # normal library recording in a patient in status. Ambulatory EEG stays apart: it has no video.
    _SAME_STUDY: dict[str, tuple[frozenset[str], ...]] = {
        "analyze_eeg": (frozenset({"video", "continuous_icu"}),),
    }

    # One-way stand-ins (25 Oct 2026, SE-routing CENTRAL 5): an order for the key study is answered
    # by a stored report of a listed study when the case stores no report of the key study itself
    # (initial, follow-up or case fallback). A sleep-deprived EEG is the routine 20 to 40 minute
    # recording made after sleep deprivation, to raise the yield of interictal discharges: what the
    # routine recording showed, it would have shown, so the patient's own routine report is the
    # fair answer, where the library's normal recording contradicted a patient in non-convulsive
    # status or with temporal discharges. The reverse is never served (a routine order does not get
    # a sleep-deprived recording's extra yield), the same rule as the monitoring tiers. Ambulatory
    # EEG is left out: a 24 to 72 hour recording captures events a 30-minute report cannot speak for.
    _STANDS_IN: dict[str, dict[str, tuple[str, ...]]] = {
        "analyze_eeg": {"sleep_deprived": ("routine",)},
    }

    def _stored_reports(self, tool_name: str) -> list[Any]:
        initial = self._match_initial_output(tool_name, {})
        fallback = self._match_fallback_output(tool_name, {})
        followups = [fu.output for fu in self.case.followup_outputs or [] if fu.tool_name == tool_name]
        return [report for report in (initial, *followups, fallback) if isinstance(report, BaseModel)]

    def _stands_in(self, tool_name: str, wanted: Any, got: Any) -> bool:
        """May a stored report of study `got` answer an order for study `wanted` (`_STANDS_IN`)?"""
        spec = self._DISCRIMINATOR.get(tool_name)
        table = self._STANDS_IN.get(tool_name)
        if spec is None or not table:
            return False
        stand_ins = next((terms for term, terms in table.items() if self._fold(term) == self._fold(wanted)), ())
        if not any(self._fold(term) == self._fold(got) for term in stand_ins):
            return False
        key = spec[0]
        return not any(
            getattr(report, key, None) and self._same_study(tool_name, getattr(report, key), wanted)
            for report in self._stored_reports(tool_name)
        )

    def _wanted(self, tool_name: str, parameters: dict[str, Any]) -> Any:
        """The study the call orders by its primary discriminator (`None`: not stated)."""
        spec = self._DISCRIMINATOR.get(tool_name)
        if spec is None:
            return None
        value = parameters.get(spec[0])
        if value is None and tool_name in self._DEFAULTED:
            value = self._ENUM_DEFAULTS[tool_name][1]
        return value

    def _canonical(self, tool_name: str, value: Any) -> frozenset[str]:
        folded = self._fold(value)
        for group in self._SAME_STUDY.get(tool_name, ()):
            if any(folded == self._fold(term) for term in group):
                return frozenset({"|".join(sorted(group))})
        return folded

    def _same_study(self, tool_name: str, a: Any, b: Any) -> bool:
        return self._canonical(tool_name, a) == self._canonical(tool_name, b)

    # A second routed parameter, read with its schema default (24 Oct 2026). The stored report says
    # which variant it is in the same field; a report that leaves the field empty is not
    # adjudicated. Unlike `_DISCRIMINATOR`, an order that leaves the parameter out names the
    # default, because here the default is the common study and the variant the exception: NPH
    # stores the baseline timed gait and the post-tap reassessment as the same assessment type, and
    # the baseline order received the post-tap result (NPH R4); a lumbar-drain report must not
    # answer the tap test, nor the tap the drainage trial (NPH-P08, R3).
    _SECONDARY_DISCRIMINATOR: dict[str, tuple[str, Any, str]] = {
        "perform_clinical_assessment": ("timing", assessment_timings, "baseline"),
        "analyze_csf": ("source", csf_sources, "lumbar_puncture"),
    }

    # A boolean order flag and the report field that states it (24 Oct 2026). An omitted flag is
    # false (the schema default), and a report that leaves the field None is not adjudicated. Only
    # ALZ-EARLY-RS06 stores a non-contrast and a contrast MRI of one patient and states which is
    # which; every other case stores one MRI study, so there is nothing to route to.
    _FLAG_DISCRIMINATOR: dict[str, tuple[str, str]] = {
        "analyze_brain_mri": ("contrast", "contrast_used"),
    }

    def _flag_answers(self, tool_name: str, parameters: dict[str, Any], output: Any) -> bool:
        flag = self._FLAG_DISCRIMINATOR.get(tool_name)
        if flag is None or not isinstance(output, BaseModel):
            return True
        got = getattr(output, flag[1], None)
        return got is None or got is bool(parameters.get(flag[0]))

    def _secondary_answers(self, tool_name: str, parameters: dict[str, Any], output: Any) -> bool:
        if not self._flag_answers(tool_name, parameters, output):
            return False
        spec = self._SECONDARY_DISCRIMINATOR.get(tool_name)
        if spec is None or output is None:
            return True
        key, vocabulary, default = spec
        got = getattr(output, key, None) if isinstance(output, BaseModel) else None
        folded = self._fold(got) if got not in (None, "") else frozenset()
        if not folded or folded not in {self._fold(term) for term in vocabulary(packs=self.packs)}:
            return True  # not stated, or prose: not ours to adjudicate
        return folded == self._fold(parameters.get(key) or default)

    def _study_key(self, tool_name: str, parameters: dict[str, Any]) -> tuple:
        """Which study a call orders, by its routed parameters, defaults resolved (`None`: unknown)."""
        key: list[Any] = []
        spec = self._DISCRIMINATOR.get(tool_name)
        if spec is not None:
            value = parameters.get(spec[0])
            default = self._ENUM_DEFAULTS.get(tool_name)
            if value is None and default is not None and default[0] == spec[0]:
                value = default[1]
            key.append(self._canonical(tool_name, value) if value is not None else None)
        secondary = self._SECONDARY_DISCRIMINATOR.get(tool_name)
        if secondary is not None:
            key.append(self._fold(parameters.get(secondary[0]) or secondary[2]))
        flag = self._FLAG_DISCRIMINATOR.get(tool_name)
        if flag is not None:
            key.append(bool(parameters.get(flag[0])))
        return tuple(key)

    def _is_repeat_call(self, tool_name: str, parameters: dict[str, Any]) -> bool:
        """Was the same study ordered before this call (NPH R5)?

        A plain re-order follow-up escalates past the initial output only on a repeat order. Counting
        every earlier call to the tool made a first order of one study a "repeat" because another
        study of the same tool had been ordered (a timed gait after a cognitive screen, a lumbar drain
        after the tap). Now an earlier call counts only when it ordered the same study by the tool's
        routed parameters; when either call leaves a routed parameter unknown, it still counts, as
        before.
        """
        mine = self._study_key(tool_name, parameters)
        for call in self.call_log:
            if call.tool_name != tool_name:
                continue
            theirs = self._study_key(tool_name, call.parameters or {})
            if all(a is None or b is None or a == b for a, b in zip(mine, theirs)):
                return True
        return False

    # Every scalar enum a tool advertises, for the follow-up matcher: a trigger token that
    # belongs to one of the called tool's own terms identifies a study only with its whole
    # term (followup_matcher.match_followup). Lab panels, CSF assays and molecular assays are
    # assay lists, not study names, and are left to the set-valued rule below.
    _ENUM_TERMS: dict[str, Any] = {
        "analyze_brain_mri": mri_protocols,
        "analyze_csf": csf_sources,
    }

    # The schema default of each scalar enum (the tool classes' `parameter_schema`; pinned by
    # tests/test_followup_enum_tokens.py): a call that leaves the parameter out names that term.
    _ENUM_DEFAULTS: dict[str, tuple[str, str]] = {
        "analyze_eeg": ("eeg_type", "routine"),
        "analyze_csf": ("source", "lumbar_puncture"),
        "order_echocardiogram": ("echo_type", "TTE"),
        "order_cardiac_monitoring": ("monitor_type", "holter_24h"),
    }

    def _implied_terms(self, tool_name: str, parameters: dict[str, Any]) -> list[str]:
        spec = self._ENUM_DEFAULTS.get(tool_name)
        return [spec[1]] if spec is not None and parameters.get(spec[0]) is None else []

    def _index_terms(self, tool_name: str, parameters: dict[str, Any], initial: Any) -> list[str]:
        """The called term, when the stored initial output positively is that study."""
        spec = self._DISCRIMINATOR.get(tool_name)
        if spec is None or initial is None or parameters.get(spec[0]) is None:
            return []
        got = getattr(initial, spec[0], None) if isinstance(initial, BaseModel) else None
        wanted = parameters[spec[0]]
        return [str(wanted)] if got and self._same_study(tool_name, got, wanted) else []

    def _enum_terms(self, tool_name: str) -> list[str]:
        spec = self._DISCRIMINATOR.get(tool_name)
        source = spec[1] if spec is not None else self._ENUM_TERMS.get(tool_name)
        return list(source(packs=self.packs)) if source is not None else []

    # Monitoring tiers (ESC 2018 syncope, AHA/ASA 2021 cryptogenic stroke): hours to a week
    # (telemetry, Holter), weeks (external event monitors), months (loop recorder). The upper
    # bound in hours of each tier, and the tier of each ordered monitor (`_monitor_answers`).
    _MONITOR_TIER_HOURS: tuple[int, ...] = (7 * 24, 31 * 24)
    _MONITOR_TIER: dict[str, int] = {
        "telemetry": 0, "holter_24h": 0, "holter_48h": 0,
        "event_monitor_14d": 1, "event_monitor_30d": 1,
        "implantable_loop_recorder": 2,
    }

    @staticmethod
    def _fold(value: Any) -> frozenset[str]:
        """Word-order-insensitive identity of a study name.

        Reports name the study in prose written by hand: `"Single-fiber EMG"` for what the
        vocabulary spells `emg_single_fiber`. Comparing folded strings made that a mismatch and the
        case's own SFEMG report was refused while its repetitive-stimulation report was offered
        instead. Comparing token sets is enough, and safe: no two terms in any of the ten
        vocabularies share a token set.
        """
        text = str(value).strip().lower()
        for separator in ("-", " ", "/", ":", ","):
            text = text.replace(separator, "_")
        return frozenset(token for token in text.split("_") if token)

    def _answers_the_question(
        self, tool_name: str, parameters: dict[str, Any], output: Any
    ) -> bool:
        """Does this stored report describe the study that was actually ordered?

        Decides only when it can. Most reports predate the closed vocabulary and name the study
        in prose — `"Electromyography (EMG) and Nerve Conduction Study (NCS)"` for what a call
        spells `emg_ncs` — so the guard applies only when the report's own value IS a term of
        that tool's vocabulary. A prose value, a missing field, or a call that pins nothing is
        served exactly as before.
        """
        if not self._secondary_answers(tool_name, parameters, output):
            return False
        spec = self._DISCRIMINATOR.get(tool_name)
        if spec is None or output is None:
            return True
        call_key, vocabulary = spec
        wanted = self._wanted(tool_name, parameters)
        if wanted is None:
            return True
        if tool_name == "order_body_imaging":
            return self._body_study_matches(str(wanted), output)
        got = getattr(output, call_key, None) if isinstance(output, BaseModel) else None
        folded = self._fold(got) if got not in (None, "") else frozenset()
        if tool_name == "order_cardiac_monitoring":
            return self._monitor_answers(str(wanted), got, output)
        if folded and folded in {self._fold(term) for term in vocabulary(packs=self.packs)}:
            return self._same_study(tool_name, got, wanted) or self._stands_in(tool_name, wanted, got)
        return True  # the report names the study in prose; not ours to adjudicate

    def _monitor_answers(self, wanted: str, got: Any, output: Any) -> bool:
        """A stored rhythm recording answers an order for a monitor of its tier or a longer one.

        The leak runs one way: a 30-day monitor, a loop recorder or a pacemaker's stored
        diagnostics served for a Holter hands over the paroxysmal AF the short recording was
        meant to miss. The other way is a fair simulation (what a Holter found, a 30-day monitor
        would have found), and refusing it would answer the longer order with a normal library
        report that contradicts the case. Within a tier (a 48-hour Holter for a 24-hour order,
        72 hours of telemetry for a Holter) the yield is the same question and is served. A
        device interrogation is not a recording made for the order, so it answers, and is
        answered by, only its own type. A report's tier is read from its `duration_hours`, else
        from its `monitor_type`.
        """
        got_term = next(
            (term for term in by_type_values("order_cardiac_monitoring", packs=self.packs)
             if got and self._fold(term) == self._fold(got)),
            None,
        )
        if "device_interrogation" in (wanted, got_term):
            return got_term == wanted
        ordered = self._MONITOR_TIER.get(wanted)
        hours = getattr(output, "duration_hours", 0) or 0
        if hours:
            stored = sum(hours > bound for bound in self._MONITOR_TIER_HOURS)
        else:
            stored = self._MONITOR_TIER.get(got_term or "")
        if ordered is None or stored is None:
            return True  # nothing to compare: not ours to adjudicate
        return stored <= ordered

    _BODY_MODALITIES = frozenset({"ct", "cta", "mri", "ultrasound", "xray", "duplex"})

    @classmethod
    def _body_study_matches(cls, wanted: str, output: Any) -> bool:
        """`study` fuses region and modality (`mediastinum_CT`); the report carries them apart.

        The modality decides when the report's is a vocabulary term (a stored MRI does not answer
        a CT order); the region decides when the report names one (a spine study does not answer
        a mediastinal order). Prose or empty fields are not adjudicated, as for the other tools.
        """
        region_part, _, modality_part = wanted.rpartition("_")
        got_modality = cls._fold(getattr(output, "modality", "") or "")
        if got_modality and got_modality <= cls._BODY_MODALITIES and got_modality != cls._fold(modality_part):
            return False
        got_region = cls._fold(getattr(output, "region", "") or "")
        if not got_region:
            return True
        return bool(cls._region_stems(cls._fold(region_part)) & cls._region_stems(got_region))

    # Reports say "testes", "pelvic", "mediastinal", "thorax" for what the vocabulary spells
    # testicular, pelvis, mediastinum, chest: compare word stems, with the few anatomical synonyms
    # a stem cannot bridge.
    _REGION_SYNONYMS = (
        frozenset({"chest", "thorax", "thoracic", "lung", "lungs"}),
        frozenset({"peripheral", "nerve", "nerves", "plexus", "brachial", "lumbosacral"}),
        frozenset({"testicular", "testes", "testis", "scrotal", "scrotum"}),
    )

    @classmethod
    def _region_stems(cls, tokens: frozenset[str]) -> frozenset[str]:
        stems = {token[:4] for token in tokens if len(token) >= 4}
        for group in cls._REGION_SYNONYMS:
            if tokens & group:
                stems |= {token[:4] for token in group}
        return frozenset(stems)

    # Tools whose study identity is a *set* of assays rather than one named study. A set gives the
    # trigger matcher many values to match against, and one hit is enough for it to declare a
    # specific re-order: a status-epilepticus case ordering
    # `[CBC, CMP, magnesium, AED_levels, lactate, ABG, ESR, CRP, beta-hCG, urinalysis]` shares the
    # token `aed` with `request_aed_optimization`, so the whole first-line order was answered by
    # the post-dose-escalation drug level, and the case's own first-line panel — which contains all
    # ten — was served instead to a later action asking for an autoimmune panel it does not carry.
    # The two were crossed. Same shape as the CT/CTA crossing, on a set-valued parameter.
    _SET_DISCRIMINATOR: dict[str, str] = {
        "interpret_labs": "panels",
        "analyze_csf": "special_tests",
        "obtain_tissue_diagnosis": "molecular_assays",
    }

    # Words that identify no assay on their own; a hit on `panel` proves nothing about a lab report.
    # `anti` is here for the same reason it is non-discriminating in the trigger matcher: it prefixes
    # every antibody name, so without it a Miller-Fisher ganglioside panel counted as answering an
    # order for myasthenia antibodies and the measurement flattered the routing it was checking.
    _UNINFORMATIVE = frozenset({
        "panel", "panels", "level", "levels", "test", "tests", "study", "studies", "screen",
        "screening", "profile", "markers", "marker", "workup", "serum", "blood", "and", "for",
        "anti",
    })

    @classmethod
    def _assays_named(cls, output: Any, requested: Iterable[Any]) -> int:
        """How many of the requested assays this stored report names.

        Matching is deliberately generous — reports name assays in prose (`Anti-GM1 IgG` for
        `anti-GM1 IgM`) — and is only ever used to *compare* two stored payloads answering the same
        order, where a generous measure applied to both sides is sound. It is never used to judge
        whether one report is adequate on its own. The probe that measured this defect imports it
        rather than reimplementing it, so the measurement and the behaviour cannot drift apart —
        a hand-maintained second copy of a rule is exactly what shipped the stale tool catalogue.
        """
        payload = output.model_dump() if isinstance(output, BaseModel) else output
        blob = json.dumps(payload, default=str).lower()
        hits = 0
        for name in requested:
            tokens = [t for t in re.split(r"[^a-z0-9]+", str(name).lower())
                      if len(t) >= 3 and t not in cls._UNINFORMATIVE]
            # A token counts at the start of a word, after an optional "anti" ("Anticardiolipin"):
            # "lipid" inside "antiphospholipid" named a lipid panel the payload does not carry
            # (VASC-DEM-P05/P06, 25 Oct 2026).
            if tokens and any(re.search(r"(?<![a-z0-9])(?:anti-?)?" + re.escape(t[:5]), blob) for t in tokens):
                hits += 1
        return hits

    def _initial_answers_more(
        self, tool_name: str, parameters: dict[str, Any], initial: Any, candidate: Any
    ) -> bool:
        """True when the initial output names strictly more of a set-valued order than the follow-up.

        The comparison, not a threshold: the share of the order a trigger names does not separate
        the crossed calls from the sound ones — 35 legitimate matches name one item of four, the
        same shape as the crossings. What separates them is whether another stored payload answers
        more of the question, which is what answering a question means.
        """
        key = self._SET_DISCRIMINATOR.get(tool_name)
        if key is None or initial is None or candidate is None:
            return False
        requested = parameters.get(key)
        if isinstance(requested, str):
            requested = [requested]
        if not isinstance(requested, (list, tuple, set)) or not requested:
            return False
        if (tool_name == "interpret_labs" and isinstance(initial, LabResults)
                and isinstance(candidate, LabResults)):
            # 24 Oct 2026: a lab follow-up none of whose panels answers the order, while the initial
            # payload does, is a token accident of the trigger (MS-RR-RM01: `NMDAR_IgG_cell_based`
            # matched `request_aqp4_mog_cell_based_assay` on "cell" and "based").
            def answered(payload: LabResults) -> int:
                return sum(any(self._lab_answers(name, rows, assay) for name, rows in payload.panels.items())
                           for assay in requested)
            if answered(candidate) == 0 and answered(initial) > 0:
                return True
        if len(requested) < 2:
            return False
        return self._assays_named(initial, requested) > self._assays_named(candidate, requested)

    def _match_by_discriminator(
        self, tool_name: str, parameters: dict[str, Any], initial: Any = None,
        is_repeat_call: bool = False,
    ) -> Any | None:
        """The follow-up whose stored report IS the study this call names, if there is one.

        A candidate must also pass the full guard (`_answers_the_question`, which includes the
        secondary discriminator), and a refused one does not end the search: the NPH baseline gait
        order skips the stored post-tap reassessment instead of stopping at it. A tool routed by a
        secondary parameter alone (`analyze_csf.source`) matches here only when the call names a
        non-default value that a stored report carries exactly (the lumbar drain).

        When the stored initial output already is the study named (its own field says so), the
        first order of it gets the initial output, and a repeat order the first stored follow-up of
        that study not yet served (24 Oct 2026). Before, the discriminator served the follow-up on
        the first order: SE's index cEEG order received the recording made after the
        benzodiazepine trial or the sedation wean (SE CENTRAL: `request_continuous_eeg_monitoring`
        capturing the index `continuous_icu` order). An exact term is preferred over a same-study
        term (`_SAME_STUDY`).
        """
        flag = self._FLAG_DISCRIMINATOR.get(tool_name)
        if flag is not None:
            return self._match_by_flag(tool_name, parameters, flag, initial, is_repeat_call)
        spec = self._DISCRIMINATOR.get(tool_name)
        secondary = self._SECONDARY_DISCRIMINATOR.get(tool_name)
        if spec is not None:
            wanted = self._wanted(tool_name, parameters)
            if wanted is None:
                return None
            key = spec[0]
        elif secondary is not None and parameters.get(secondary[0]) not in (None, secondary[2]):
            key, wanted = secondary[0], parameters[secondary[0]]
        else:
            return None
        got = getattr(initial, key, "") if isinstance(initial, BaseModel) else ""
        if got and self._same_study(tool_name, got, wanted) and self._answers_the_question(
            tool_name, parameters, initial
        ):
            if not is_repeat_call:
                return None
        else:
            is_repeat_call = False  # the initial output is another study: serve in stored order
        exact, same = [], []
        for followup in self.case.followup_outputs or []:
            if followup.tool_name != tool_name:
                continue
            stored = getattr(followup.output, key, "")
            if not stored or not self._same_study(tool_name, stored, wanted):
                continue
            if self._answers_the_question(tool_name, parameters, followup.output):
                (exact if self._fold(stored) == self._fold(wanted) else same).append(followup)
        candidates = exact + same
        if is_repeat_call:
            unserved = [fu for fu in candidates if fu.trigger_action not in self._served_triggers]
            candidates = unserved or candidates
        return candidates[0] if candidates else None

    def _match_by_flag(
        self, tool_name: str, parameters: dict[str, Any], flag: tuple[str, str], initial: Any,
        is_repeat_call: bool,
    ) -> Any | None:
        """`_match_by_discriminator` for a boolean flag: the follow-up that states the value ordered."""
        wanted = bool(parameters.get(flag[0]))
        if isinstance(initial, BaseModel) and getattr(initial, flag[1], None) is wanted and not is_repeat_call:
            return None
        hits = [
            followup for followup in self.case.followup_outputs or []
            if followup.tool_name == tool_name
            and getattr(followup.output, flag[1], None) is wanted
            and self._answers_the_question(tool_name, parameters, followup.output)
        ]
        if is_repeat_call:
            hits = [fu for fu in hits if fu.trigger_action not in self._served_triggers] or hits
        return hits[0] if hits else None

    def get_output(self, tool_name: str, parameters: dict[str, Any]) -> ToolResult:
        # Whether this study was already ordered BEFORE this call (a re-order; see _is_repeat_call).
        is_repeat_call = self._is_repeat_call(tool_name, parameters)
        self.call_log.append(ToolCall(tool_name=tool_name, parameters=parameters))

        initial = self._match_initial_output(tool_name, parameters)
        if not self._answers_the_question(tool_name, parameters, initial):
            initial = None

        # Precedence: a matching follow-up for this specific re-order OVERRIDES the
        # (stale) initial output; a bare first call to a tool still returns its
        # initial output. See followup_matcher.resolve_followup for the full rule.
        #
        # Ahead of all of it: if the call names a study and some stored follow-up *is* that
        # study, serve that one. The token matcher scores trigger slugs, and family tokens are
        # not discriminating — a call for `FDG_PET` scored equally against `request_amyloid_pet`
        # and `request_fdg_pet` and could take the wrong one while the right report sat in the
        # same case. The discriminator is not a heuristic, so it goes first.
        followup = self._match_by_discriminator(tool_name, parameters, initial, is_repeat_call)
        if followup is None:
            # Candidates that do not describe the study ordered are dropped before the choice,
            # not after it: SE-M05's pelvic ultrasound order tied between its MRI and ultrasound
            # follow-ups, took the MRI by declaration order, had it refused on modality, and fell
            # to the library normal while the case's ultrasound sat unserved.
            followup = resolve_followup(
                tool_name, parameters, self.case.followup_outputs,
                self._served_triggers,
                has_initial_output=initial is not None,
                is_repeat_call=is_repeat_call,
                enum_terms=self._enum_terms(tool_name),
                implied_terms=self._implied_terms(tool_name, parameters),
                index_terms=self._index_terms(tool_name, parameters, initial),
                accepts=lambda fu: self._answers_the_question(tool_name, parameters, fu.output),
            )
            # A set-valued order names several assays, and the trigger matcher can capture it on a
            # single shared token. When the initial output names more of what was ordered, it is the
            # answer to that order and the follow-up stays available for the narrower re-order it
            # was written for. Applied only to the token match: a discriminator hit above is not a
            # heuristic, so coverage does not get to overrule it.
            if followup is not None and self._initial_answers_more(
                tool_name, parameters, initial, followup.output
            ):
                followup = None
        if followup is not None and not self._answers_the_question(
            tool_name, parameters, followup.output
        ):
            followup = None
        if followup is not None:
            self._served_triggers.add(followup.trigger_action)
            output = self._merge_lab_order(tool_name, parameters, followup.output, followup, initial)
            output = self._complete_lab_order(tool_name, parameters, output)
            return ToolResult(
                tool_name=tool_name, success=True,
                output=output.model_dump() if isinstance(output, BaseModel) else output,
            )

        # Initial tool output (first, parameter-light order on the pathway). A laboratory order
        # receives only the stored panels that answer what it names (`_lab_order_from`); when none
        # does, the order falls through to the fallback tiers like any unstored study.
        if initial is not None and tool_name == "interpret_labs":
            initial = self._lab_order_from(parameters, initial, pathway=True)
        if initial is not None:
            return ToolResult(
                tool_name=tool_name, success=True,
                output=initial.model_dump() if isinstance(initial, BaseModel) else initial,
            )

        # Off-pathway fallback: a clinically coherent normal / non-contributory result for a
        # tool that is not on this case's diagnostic pathway. The discriminator guard applies
        # only where the fallback names its study with a vocabulary term: a fallback written as
        # an `amino_acid_PET` report is that study, and served for an `FDG_PET` order it
        # answered one question with another study's report (GLIO-HG; NMDAR-ENC CENTRAL 4). A
        # fallback that names no study, or names it in prose, still answers any variant, which
        # the library tier below would otherwise do with a less patient-specific report.
        output = self._match_fallback_output(tool_name, parameters)
        if output is not None and not self._answers_the_question(tool_name, parameters, output):
            output = None
        if output is not None and tool_name == "interpret_labs":
            output = self._lab_order_from(parameters, output, pathway=False)
        if output is not None:
            return ToolResult(
                tool_name=tool_name, success=True, from_fallback=True,
                output=output.model_dump() if isinstance(output, BaseModel) else output,
            )
        # A recorded case holds what the clinicians ordered and nothing else. Any other order has
        # no result, and a normal report from the library would invent the patient's data. The
        # agent therefore learns that the study was not done, which a synthetic case hides: a
        # property of real records, stated in docs/benchmark/tool-contract.md. The order is still
        # placed and billed. Literature and drug-interaction look-ups read no patient data, so
        # they are answered as in any case.
        if self.case.provenance == "record" and tool_name not in self._KNOWLEDGE_TOOLS:
            return ToolResult(
                tool_name=tool_name, success=False, output=None, unavailable=True,
                error_message=(
                    f"Not available: {self._study_label(tool_name, parameters)} was not "
                    "performed during this recorded encounter, so there is no result."
                ),
            )
        # Last tier: the benchmark-level library, the same normal report in every case, so an
        # off-pathway order never reveals that it was off-pathway.
        output = self.library.resolve(tool_name, parameters)
        if output is not None:
            return ToolResult(tool_name=tool_name, success=True, from_fallback=True, library=True, output=output.model_dump())
        return ToolResult(
            tool_name=tool_name, success=False, output=None,
            error_message=f"No {tool_name} data available for this patient.",
        )

    _KNOWLEDGE_TOOLS = frozenset({"search_medical_literature", "check_drug_interactions"})

    @classmethod
    def _panel_names(cls, name: str, rows: list[LabValue], assay: Any) -> bool:
        """Does this stored panel (its name and its row tests) name the assay, every token of it?

        Stricter than `_assays_named`, which is generous on purpose and reads the whole report:
        here a hit decides that the panel is the answer to that assay, so all of the assay's
        informative tokens must appear in what the panel measures, never in its interpretation.
        """
        tokens = [t for t in re.split(r"[^a-z0-9]+", str(assay).lower())
                  if len(t) >= 3 and t not in cls._UNINFORMATIVE]
        measured = [row.test for row in rows if specimen_compatible(row.test, name, str(assay))]
        if len(measured) < len(rows) and not measured:
            return False  # every row is another specimen's (a urinalysis for a blood order)
        blob = " ".join([name, *measured]).lower()
        words = set(re.split(r"[^a-z0-9]+", blob)) | set(lab_tokens(blob))
        # Word stems, not five-letter prefixes anywhere in the text: `complement` shares "compl"
        # with "Complete Blood Count" and an anti-dsDNA + complement order received the CBC
        # (SE-routing CENTRAL 4, 25 Oct 2026).
        return bool(tokens) and all(any(lab_like(t, word) for word in words if word) for t in tokens)

    def _merge_lab_order(
        self, tool_name: str, parameters: dict[str, Any], served: Any, served_followup: Any, initial: Any
    ) -> Any:
        """One laboratory order naming several assays receives every stored result it names.

        Each laboratory payload of a case was authored for one order: the first-line panels in
        the initial output, a second-tier assay in a follow-up. An order that names assays from
        several of them was answered by one payload only: MG-P04's single order for AChR, MuSK,
        LRP4 and TSH antibodies got back the LRP4 follow-up alone, SE-P05's first order with
        cholinesterase the first-line panels alone (SE CENTRAL 5, FTD CENTRAL 3). The served
        payload stays the base; for each ordered assay none of its panels names, the panels that
        do name it are added from the initial output, or from the follow-up whose trigger names
        that assay on its own (the re-order it was written for). The assay is matched on the
        panel names and row tests with every informative token (`_panel_names`), so a repeat
        measurement of an assay the base already carries is never merged into the first order.
        Merged follow-ups count as served. Laboratory orders only: CSF and tissue payloads are
        single specimens and are not combined.
        """
        from neuroagent_schemas import LabResults

        requested = parameters.get("panels")
        if isinstance(requested, str):
            requested = [requested]
        if (tool_name != "interpret_labs" or not isinstance(requested, (list, tuple))
                or len(requested) < 2 or not isinstance(served, LabResults)):
            return served
        panels = dict(served.panels)
        interpretations = [served.interpretation] if served.interpretation else []
        summary = list(served.abnormal_values_summary)
        followups = [
            fu for fu in self.case.followup_outputs or []
            if fu.tool_name == tool_name and fu is not served_followup and isinstance(fu.output, LabResults)
        ]
        contributed: set[int] = set()
        for assay in requested:
            if any(self._lab_answers(name, rows, assay) for name, rows in panels.items()):
                continue
            source = None
            if isinstance(initial, LabResults) and initial is not served and any(
                self._lab_answers(name, rows, assay) for name, rows in initial.panels.items()
            ):
                source = self._filter_lab_payload(initial, [assay])
            else:
                hit = match_followup(tool_name, {"panels": [assay]}, followups, self._served_triggers)
                if hit is not None:
                    source = hit.output
                    self._served_triggers.add(hit.trigger_action)
            if source is None:
                continue
            added = {name: rows for name, rows in source.panels.items()
                     if name not in panels and self._lab_answers(name, rows, assay)}
            if not added:
                continue
            panels.update(added)
            if id(source) not in contributed:
                contributed.add(id(source))
                for sentence in split_sentences(source.interpretation or ""):
                    if sentence not in " ".join(interpretations):
                        interpretations.append(sentence)
            tests = [row.test.lower() for rows in added.values() for row in rows]
            summary += [line for line in source.abnormal_values_summary
                        if line not in summary and any(test[:8] in line.lower() for test in tests)]
        if panels.keys() == served.panels.keys():
            return served
        return LabResults(panels=panels, interpretation=" ".join(interpretations),
                          abnormal_values_summary=summary)

    # ------------------------------------------------------------------ laboratory orders
    #
    # 24 Oct 2026. The first `interpret_labs` order received the whole stored initial payload,
    # whatever it named: MS-RR's AQP4/MOG-IgG, stored with the first-line panels, reached a basic
    # labs order, and an order for an assay the case does not store got the first-line labs again
    # instead of a result for that assay. Now an order receives the stored panels that answer what it
    # names (`tools/lab_matching.py`), and each assay no stored panel answers gets the case's own
    # fallback panel for it, else the library normal, or, in a recorded case, a "not available" line.

    def _lab_answers(self, name: str, rows: list[LabValue], assay: Any) -> bool:
        """Does this stored panel answer the ordered assay (by components, by name, or by tokens)?"""
        return self._labs.panel_answers(name, rows, str(assay)) or self._panel_names(name, rows, assay)

    @staticmethod
    def _requested_assays(parameters: dict[str, Any]) -> list[str]:
        requested = parameters.get("panels")
        if isinstance(requested, str):
            requested = [requested]
        return [str(item) for item in requested] if isinstance(requested, (list, tuple)) else []

    def _filter_lab_payload(self, payload: LabResults, requested: list[str]) -> LabResults:
        """The panels of a stored payload that answer the order, with the prose about them.

        A sentence of the interpretation (or a line of the abnormal-values summary) is dropped when
        it names a test of a dropped panel and none of a kept one, so a result the order did not
        ask for is not read out in the prose either. A payload whose panels all answer is returned
        unchanged.
        """
        kept = {name: rows for name, rows in payload.panels.items()
                if any(self._lab_answers(name, rows, assay) for assay in requested)}
        if kept.keys() == payload.panels.keys():
            return payload
        dropped = [row.test for name, rows in payload.panels.items() if name not in kept for row in rows]
        dropped += [name for name in payload.panels if name not in kept and len(lab_tokens(name)) >= 2]
        kept_tests = [row.test for rows in kept.values() for row in rows]

        def keep(text: str) -> bool:
            return any(mentions(text, test) for test in kept_tests) or not any(
                mentions(text, test) for test in dropped
            )

        interpretation = " ".join(s for s in split_sentences(payload.interpretation) if keep(s))
        return LabResults(
            panels=kept,
            interpretation=interpretation or "Results of the requested assays are listed.",
            abnormal_values_summary=[line for line in payload.abnormal_values_summary if keep(line)],
        )

    def _lab_order_from(self, parameters: dict[str, Any], payload: Any, pathway: bool) -> Any | None:
        """A stored laboratory payload cut to the order; `None` when no panel of it answers."""
        requested = self._requested_assays(parameters)
        if not requested or not isinstance(payload, LabResults):
            return payload  # an order naming nothing receives the first-line labs, as before
        served = self._filter_lab_payload(payload, requested)
        if pathway:
            # A first order naming an assay stored only in a follow-up still receives it.
            served = self._merge_lab_order("interpret_labs", parameters, served, None, None)
        if not served.panels:
            return None
        return self._complete_lab_order("interpret_labs", parameters, served, case_fallback=pathway)

    def _complete_lab_order(
        self, tool_name: str, parameters: dict[str, Any], served: Any, case_fallback: bool = True,
    ) -> Any:
        """Add a result for every ordered assay the served payload does not answer."""
        if tool_name != "interpret_labs" or not isinstance(served, LabResults):
            return served
        missing = [assay for assay in self._requested_assays(parameters)
                   if not any(self._lab_answers(name, rows, assay) for name, rows in served.panels.items())]
        if not missing:
            return served
        fallback = self.case.fallback_tool_outputs.labs if (
            case_fallback and self.case.fallback_tool_outputs is not None
        ) else None
        panels = dict(served.panels)
        normal: list[str] = []
        unavailable: list[str] = []
        interpretation = [served.interpretation] if served.interpretation else []
        for assay in missing:
            if isinstance(fallback, LabResults):
                own = self._filter_lab_payload(fallback, [assay])
                if own.panels:
                    panels.update({name: rows for name, rows in own.panels.items() if name not in panels})
                    if own.interpretation not in " ".join(interpretation):
                        interpretation.append(own.interpretation)
                    continue
            if self.case.provenance == "record":
                unavailable.append(assay)
                continue
            library = self.library.resolve(tool_name, {"panels": [assay]})
            if isinstance(library, LabResults) and library.panels:
                panels.update({name: rows for name, rows in library.panels.items() if name not in panels})
                normal.append(assay)
        if normal:
            interpretation.append(f"{', '.join(normal)}: within the reference ranges.")
        if unavailable:
            interpretation.append(
                f"Not available: {', '.join(unavailable)} was not performed during this recorded "
                "encounter, so there is no result."
            )
        return LabResults(panels=panels, interpretation=" ".join(interpretation),
                          abnormal_values_summary=list(served.abnormal_values_summary))

    def _study_label(self, tool_name: str, parameters: dict[str, Any]) -> str:
        """`order_body_imaging (study=abdomen_xray)`: the tool, and the study the call names."""
        spec = self._DISCRIMINATOR.get(tool_name)
        if spec is not None and parameters.get(spec[0]) is not None:
            return f"{tool_name} ({spec[0]}={parameters[spec[0]]})"
        return tool_name

    def _match_initial_output(self, tool_name: str, parameters: dict[str, Any]) -> BaseModel | None:
        mapping = {
            "analyze_eeg": self.case.initial_tool_outputs.eeg,
            "analyze_brain_mri": self.case.initial_tool_outputs.mri,
            "analyze_ecg": self.case.initial_tool_outputs.ecg,
            "interpret_labs": self.case.initial_tool_outputs.labs,
            "analyze_csf": self.case.initial_tool_outputs.csf,
            "order_ct_scan": self.case.initial_tool_outputs.ct,
            "order_echocardiogram": self.case.initial_tool_outputs.echo,
            "order_cardiac_monitoring": self.case.initial_tool_outputs.cardiac_monitoring,
            "order_advanced_imaging": self.case.initial_tool_outputs.advanced_imaging,
            "order_specialized_test": self.case.initial_tool_outputs.specialized_test,
            # Added with the four post-review tools.
            "order_body_imaging": self.case.initial_tool_outputs.body_imaging,
            "order_microbiology": self.case.initial_tool_outputs.microbiology,
            "obtain_tissue_diagnosis": self.case.initial_tool_outputs.tissue_diagnosis,
            "perform_clinical_assessment": self.case.initial_tool_outputs.clinical_assessment,
        }

        # Direct mapping for diagnostic tools
        if tool_name in mapping:
            return mapping[tool_name]

        # Literature search: match by query parameter
        if tool_name == "search_medical_literature" and self.case.initial_tool_outputs.literature_search:
            query = parameters.get("query", "")
            # Try exact match first, then return first available
            if query in self.case.initial_tool_outputs.literature_search:
                return self.case.initial_tool_outputs.literature_search[query]
            results = list(self.case.initial_tool_outputs.literature_search.values())
            return results[0] if results else None

        # Drug interaction: match by drug parameter
        if tool_name == "check_drug_interactions" and self.case.initial_tool_outputs.drug_interactions:
            drug = parameters.get("drug", "")
            if drug in self.case.initial_tool_outputs.drug_interactions:
                return self.case.initial_tool_outputs.drug_interactions[drug]
            results = list(self.case.initial_tool_outputs.drug_interactions.values())
            return results[0] if results else None

        return None

    def _match_fallback_output(self, tool_name: str, parameters: dict[str, Any]) -> BaseModel | None:
        """Resolve a tool call against the off-pathway fallback tier."""
        fb = self.case.fallback_tool_outputs
        if fb is None:
            return None

        mapping = {
            "analyze_eeg": fb.eeg,
            "analyze_brain_mri": fb.mri,
            "analyze_ecg": fb.ecg,
            "interpret_labs": fb.labs,
            "analyze_csf": fb.csf,
            "order_ct_scan": fb.ct,
            "order_echocardiogram": fb.echo,
            "order_cardiac_monitoring": fb.cardiac_monitoring,
            "order_advanced_imaging": fb.advanced_imaging,
            "order_specialized_test": fb.specialized_test,
            "order_body_imaging": fb.body_imaging,
            "order_microbiology": fb.microbiology,
            "obtain_tissue_diagnosis": fb.tissue_diagnosis,
            "perform_clinical_assessment": fb.clinical_assessment,
        }
        if tool_name in mapping:
            return mapping[tool_name]

        if tool_name == "search_medical_literature" and fb.literature_search:
            results = list(fb.literature_search.values())
            return results[0] if results else None

        if tool_name == "check_drug_interactions" and fb.drug_interactions:
            results = list(fb.drug_interactions.values())
            return results[0] if results else None

        return None

    def get_call_log(self) -> list[ToolCall]:
        return list(self.call_log)
