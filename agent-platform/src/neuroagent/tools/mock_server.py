from __future__ import annotations
from neuroagent_schemas import (
    NeuroBenchCase, EEGReport, MRIReport, ECGReport, LabResults, CSFResults,
    LiteratureSearchResult, DrugInteractionResult,
    CTReport, EchoReport, CardiacMonitoringReport,
    AdvancedImagingReport, SpecializedTestReport,
)
from .base import ToolCall, ToolResult
from .followup_matcher import resolve_followup
from .vocabulary import (
    advanced_imaging_modalities,
    assessment_types,
    body_imaging_studies,
    echocardiogram_types,
    microbiology_specimens,
    specialized_test_types,
    tissue_procedures,
)
from typing import Any
from pydantic import BaseModel


class MockServer:
    """Serves pre-generated tool outputs from a NeuroBenchCase."""

    def __init__(self, case: NeuroBenchCase):
        self.case = case
        self.call_log: list[ToolCall] = []
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
        "order_specialized_test": ("test_type", specialized_test_types),
        "obtain_tissue_diagnosis": ("procedure", tissue_procedures),
        "perform_clinical_assessment": ("assessment_type", assessment_types),
    }
    # `order_cardiac_monitoring` is deliberately absent. Its variants differ in duration and
    # setting, not in the question asked — a 48-hour Holter and a 24-hour one both report the
    # rhythm — so serving the case's stored recording for a longer monitor is a fair simulation.
    # The guard is for tools whose variants answer *different* questions: a different specimen,
    # region, tracer or procedure.

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
        spec = self._DISCRIMINATOR.get(tool_name)
        if spec is None or output is None:
            return True
        call_key, vocabulary = spec
        wanted = parameters.get(call_key)
        if wanted is None:
            return True
        got = getattr(output, call_key, None) if isinstance(output, BaseModel) else None
        if got in (None, ""):
            return True
        folded = self._fold(got)
        if folded not in {self._fold(term) for term in vocabulary()}:
            return True  # the report names the study in prose; not ours to adjudicate
        return folded == self._fold(wanted)

    def _match_by_discriminator(self, tool_name: str, parameters: dict[str, Any]) -> Any | None:
        """The follow-up whose stored report IS the study this call names, if there is one."""
        spec = self._DISCRIMINATOR.get(tool_name)
        if spec is None or parameters.get(spec[0]) is None:
            return None
        for followup in self.case.followup_outputs or []:
            if followup.tool_name != tool_name:
                continue
            if self._fold(getattr(followup.output, spec[0], "")) == self._fold(
                parameters[spec[0]]
            ):
                return followup
        return None

    def get_output(self, tool_name: str, parameters: dict[str, Any]) -> ToolResult:
        # Whether this tool was already called BEFORE this call (a re-order).
        is_repeat_call = any(c.tool_name == tool_name for c in self.call_log)
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
        followup = self._match_by_discriminator(tool_name, parameters)
        if followup is None:
            followup = resolve_followup(
                tool_name, parameters, self.case.followup_outputs,
                self._served_triggers,
                has_initial_output=initial is not None,
                is_repeat_call=is_repeat_call,
            )
        if followup is not None and not self._answers_the_question(
            tool_name, parameters, followup.output
        ):
            followup = None
        if followup is not None:
            self._served_triggers.add(followup.trigger_action)
            output = followup.output
            return ToolResult(
                tool_name=tool_name, success=True,
                output=output.model_dump() if isinstance(output, BaseModel) else output,
            )

        # Initial tool output (first, parameter-light order on the pathway).
        if initial is not None:
            return ToolResult(
                tool_name=tool_name, success=True,
                output=initial.model_dump() if isinstance(initial, BaseModel) else initial,
            )

        # Off-pathway fallback: a clinically coherent normal / non-contributory result for a
        # tool that is not on this case's diagnostic pathway. The discriminator guard does NOT
        # apply here — a fallback makes no claim about which study was run, it says the study
        # did not contribute, so it answers any variant of the tool.
        output = self._match_fallback_output(tool_name, parameters)
        if output is not None:
            return ToolResult(
                tool_name=tool_name, success=True, from_fallback=True,
                output=output.model_dump() if isinstance(output, BaseModel) else output,
            )

        return ToolResult(
            tool_name=tool_name, success=False, output=None,
            error_message=(
                f"No {tool_name} data available for this patient. "
                f"Consider whether this test is appropriate."
            ),
        )

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
