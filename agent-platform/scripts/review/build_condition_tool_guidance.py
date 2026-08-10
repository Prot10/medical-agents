"""Turn the clinical reviewers' per-condition tool comments into a served config file.

The July 2026 tool review produced 91 annotations on `condition_tool:{condition}:{tool}`
rows, and most of them carry a block headed "Revised description (to be inserted)". That
text had nowhere to live: `ToolMeta.description` is one string per tool, rendered
identically under all conditions, so "for MS, brain *and cord* MRI with an MS protocol"
cannot be stored there without being wrong in the other nineteen conditions — and without
handing the agent the diagnosis it is meant to infer. The condition-specific half of the
review was therefore applied to the vocabulary and to the case ground truth and then
dropped on the floor as text: a reviewer logging back in would still read the string they
had asked us to delete.

This script builds `agent-platform/config/review/condition_tool_guidance.yaml`, which the
review API serves alongside each condition→tool row. Three properties matter:

* **The text is theirs, sliced not retyped.** Every `guidance`, `rationale` and `source`
  value is cut out of the stored annotation by literal markers, so nothing is paraphrased
  and a diff against the source data is meaningful.
* **Their text lands on the tool that now performs the study.** Eleven annotations describe
  a study that did not exist in the twelve-tool action space, so they were filed under
  whichever row was closest — the NMDAR tumour screen under brain MRI, the meningitis blood
  cultures under laboratory studies, the glioma biopsy under brain MRI. Those are re-pointed
  at `order_body_imaging`, `order_microbiology`, `obtain_tissue_diagnosis` and
  `perform_clinical_assessment`, with `filed_under` recording where the reviewer put it.
* **Every entry carries our answer.** `status` and `our_response` say what happened to that
  specific comment, including the ones where we did the opposite of what was asked. A review
  is not closed by reading it.

Input is `data/review/tool_reviews/neurobench/*.json` — reviewer runtime data, gitignored,
so this script cannot run in CI. The generated YAML is committed; the test that guards it
(`tests/test_condition_tool_guidance.py`) checks the YAML alone.

Reviewer 1 took the chronic conditions, reviewer 2 the acute ones; no reviewer code appears
in the output, because those strings are bearer credentials.

    uv run python agent-platform/scripts/review/build_condition_tool_guidance.py --write
"""

from __future__ import annotations

import argparse
import glob
import json
import pathlib
import re
import sys

REVIEWS = "data/review/tool_reviews/neurobench/*.json"
OUT = pathlib.Path("agent-platform/config/review/condition_tool_guidance.yaml")

# Reviewer code -> the split they describe in their own email. Codes are secrets and never
# reach the output; only this 1/2 label does.
REVIEWER_NUMBER = {"NB-KSC3-TWUA-QDTM": 1, "NB-87MF-FBTV-TPWE": 2}

# Markers that end a guidance block, in the order they appear in the reviewers' template.
_END_OF_GUIDANCE = (
    "Elements removed and rationale",
    "Elements removed",
    "Rationale for the change",
    "\nSource",
    "\nsource",
    "\nSources",
)
_SOURCE_MARKERS = ("\nSource:", "\nSource\n", "\nsource:", "\nSources:", "\nSource ",
                   " Source:", " Sources:")
# Lines that are form scaffolding rather than clinical text: the reviewers' template headings
# and the tier declarations that repeat what `requested_tier` records.
_BOOKKEEPING = re.compile(
    r"^\s*("
    r"Item:?|Tier:?|Source:?|Sources:?|"
    r"Current description \(to be removed\)|"
    r"New item[^\n]*|NEW ITEM[^\n]*|"
    r"(?:REQUIRED|OPTIONAL)\s*(?:[—:-][^\n]*)?|"
    r"Current[^\n]*(?:REQUIRED|OPTIONAL)[^\n]*|"
    r"unchanged[^\n]*|"
    r"\d+\.\d+ Note for the tool \(EN\)"
    r")\s*$",
    re.M,
)
# The label itself, wherever it sits — several comments write it inline before the text.
_REVISED_LABEL = re.compile(r"Revised description(?:\s*\(to be inserted\))?\s*:?\s*")
_RATIONALE_LABEL = re.compile(
    r"^\s*(Rationale for the change|Elements? (?:removed|added)(?: and rationale)?)\s*:?\s*$", re.M)


def _clean(text: str) -> str:
    """Drop the reviewer's form scaffolding, keep every clinical sentence."""
    text = _REVISED_LABEL.sub("", text)
    text = _RATIONALE_LABEL.sub("", text)
    # …and the same label written inline, ahead of the first sentence.
    text = re.sub(r"^\s*(Rationale for the change|Elements? (?:removed|added)"
                  r"(?: and rationale)?)\s*:?\s*", "", text.strip())
    text = _BOOKKEEPING.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _slice(comment: str, start: str | None, end: str | None) -> str:
    body = comment
    if start is not None:
        i = body.find(start)
        if i < 0:
            raise SystemExit(f"marker not found: {start!r}")
        # Keep the marker: for reviewer 2 it is the item heading ("Spinal and peripheral nerve
        # imaging"), for reviewer 1 the opening words of the clause. _BOOKKEEPING strips the
        # bare form-labels that come with it.
        body = body[i:]
    if end is not None:
        j = body.find(end)
        if j < 0:
            raise SystemExit(f"end marker not found: {end!r}")
        body = body[:j]
    return body


def _split_guidance(segment: str) -> tuple[str, str, str]:
    """(guidance, rationale, source) from one reviewer segment."""
    src = ""
    for marker in _SOURCE_MARKERS:
        i = segment.rfind(marker)
        if i >= 0:
            src = segment[i + len(marker) :].strip()
            segment = segment[:i]
            break
    for marker in ("Revised description (to be inserted)", "Revised description"):
        i = segment.find(marker)
        if i >= 0:
            segment = segment[i:]
            break
    rationale = ""
    for marker in _END_OF_GUIDANCE:
        i = segment.find(marker)
        if i >= 0:
            rationale = segment[i:].strip()
            segment = segment[:i]
            break
    return _clean(segment), _clean(rationale), _clean(src)


# --- Where each comment goes, and what we did about it -----------------
#
# One row per (annotation segment). `filed` is the row the reviewer annotated; `tool` is the
# tool that performs the study they describe. They differ for the eleven comments that
# describe a study the twelve-tool action space could not express — those were filed against
# whichever row was nearest, and `filed_under` preserves that fact in the output.
#
# `seg` cuts a multi-item comment: reviewer 2 wrote several items into one annotation,
# separated by their own "Item" headings. Two segments may target the same tool, in which
# case their guidance is joined — that is how the GBS respiratory-function item ends up
# beside the electrodiagnostic guidance on `order_specialized_test`, where it is orderable.
#
# `status` is the accounting, and it is the reason this file exists:
#   applied      — the case ground truth and the vocabulary now behave as the comment asks
#   partial      — applied in part; `our_response` says what is missing
#   confirm      — we did something other than what was asked and need their answer
#   no_change    — the reviewer asked for none
#   open         — a question to them, not a change to make
#   retired      — the condition itself is gone
SPEC: list[dict[str, object]] = [
    # === subarachnoid haemorrhage (reviewer 2) ===
    dict(cond="subarachnoid_hemorrhage", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="required_conditional", status="applied",
         response="Applied as a conditional requirement, which is what the comment asks for: "
                  "the 3 cases whose CT is negative carry a required lumbar puncture, and the "
                  "27 whose CT is diagnostic carry a stated exemption in "
                  "metadata.panel_required_exemptions rather than a silent omission."),
    dict(cond="subarachnoid_hemorrhage", filed="order_advanced_imaging",
         tool="order_advanced_imaging", reviewer=2, tier="optional", status="applied",
         response="Transcranial Doppler already existed and is now ordered in all 30 cases; the "
                  "review app had been showing 6 of 12 modalities, which is why it looked absent. "
                  "The audit that followed this comment found something worse: cerebral "
                  "angiography was not priced at all — only the coronary study was — so the "
                  "gold standard of the aneurysmal pathway was unorderable. It is now priced at "
                  "2530 EUR and ordered in the 3 cases that document a DSA."),
    dict(cond="subarachnoid_hemorrhage", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=2, tier="required", status="applied",
         response="Applied. Non-contrast CT and CT angiography are now two separate actions in "
                  "all 30 cases. The comment also led us to a routing defect: 30 CT angiograms "
                  "were stored under a label naming the DSA and 3 DSA reports under labels "
                  "naming the CTA, so the two studies were crossed and 54 required angiograms "
                  "were unreachable by the call that names them."),
    dict(cond="subarachnoid_hemorrhage", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: thyroid, inflammatory and autoimmune/paraneoplastic panels are out of "
                  "the required set in all 30 cases, and genetic testing is restricted to the "
                  "cases with a family history or a connective-tissue phenotype."),

    # === ischaemic stroke (reviewer 2) ===
    dict(cond="ischemic_stroke", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=2, tier="required", status="applied",
         response="Applied, and it exposed the most serious defect in the dataset: 21 of the 30 "
                  "cases had no non-contrast CT at all — the study that excludes haemorrhage "
                  "before thrombolysis. All 30 now have it as a required action, with CT "
                  "angiography as a separate one."),
    dict(cond="ischemic_stroke", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="optional", status="applied",
         response="Applied: no case requires EEG, and the two that reference it do so for a "
                  "suspected seizure mimic."),
    dict(cond="ischemic_stroke", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="optional", status="applied",
         seg=(None, "NEW ITEM OPTIONAL"),
         response="Applied: brain MRI is optional in all 30 cases."),
    dict(cond="ischemic_stroke", filed="analyze_brain_mri", tool="order_advanced_imaging",
         reviewer=2, tier="optional", status="applied",
         seg=("NEW ITEM OPTIONAL", None),
         response="Applied: CT_perfusion was added to the imaging vocabulary and priced, so "
                  "tissue-based selection is orderable; perfusion MRI already existed."),
    dict(cond="ischemic_stroke", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: glucose before thrombolysis and a baseline troponin are named "
                  "analytes in the required set, not a generic 'metabolic' bucket, and the "
                  "do-not-delay sequencing is in the case reasoning."),

    # === bacterial meningitis (reviewer 2) ===
    dict(cond="bacterial_meningitis", filed="interpret_labs", tool="order_microbiology",
         reviewer=2, tier="required", status="applied",
         seg=(None, "Item\nLaboratory studies"),
         response="Applied. order_microbiology now exists and is required in all 30 cases. The "
                  "comment also uncovered a leak: in 28 cases across the dataset the blood "
                  "cultures were stored inside the laboratory payload, so the organism — the "
                  "finding that selects the antibiotic — arrived without any microbiology being "
                  "ordered."),
    dict(cond="bacterial_meningitis", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         seg=("Item\nLaboratory studies", None),
         response="Applied: the required laboratory set is named analytes, and blood cultures are "
                  "no longer reachable through this tool."),
    dict(cond="bacterial_meningitis", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied, and it found a billed study that returned nothing: 13 cases have a "
                  "required order for the multiplex meningitis PCR panel (322 EUR) and no case "
                  "reported a result for it — in 9 of the 13 the Gram stain is negative and the "
                  "culture still pending, which is exactly where that panel decides. The result "
                  "is now present in all 13. Separately, 21 culture reports named the organism in "
                  "one field and denied it in another; a test now blocks that."),
    dict(cond="bacterial_meningitis", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: MRI is recommended rather than required in 27 cases and required in "
                  "the 2 with a suspected intracranial complication."),
    dict(cond="bacterial_meningitis", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=2, tier="unchanged", status="confirm",
         response="Kept, and we would like your confirmation. No case requires it; it stays in "
                  "the catalog at negligible cost as a differential action. If you would rather "
                  "it disappear from this condition, say so and it goes."),

    # === hepatic encephalopathy (reviewer 2) ===
    dict(cond="hepatic_encephalopathy", filed="interpret_labs", tool="order_microbiology",
         reviewer=2, tier="required", status="applied",
         seg=(None, "Item\nLaboratory studies."),
         response="Applied: blood cultures in all 30 cases, urine in all 30, and diagnostic "
                  "paracentesis in the 13 with ascites — 73 required microbiology actions where "
                  "before there was no tool able to sample anything outside the CNS."),
    dict(cond="hepatic_encephalopathy", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         seg=("Item\nLaboratory studies.", None),
         response="Applied: ammonia, electrolytes, renal and liver function, CRP, TSH and zinc "
                  "are named; autoimmune, paraneoplastic and genetic panels are out."),
    dict(cond="hepatic_encephalopathy", filed="analyze_brain_mri", tool="order_body_imaging",
         reviewer=2, tier="optional", status="partial",
         seg=(None, "Item\nBrain MRI."),
         response="The tool exists — order_body_imaging can now image the portal circulation, "
                  "which nothing in the twelve-tool space could — but no hepatic-encephalopathy "
                  "case orders it yet. The trigger conditions you wrote (recurrent or persistent "
                  "HE, no recovery at 48-72 h) identify which cases should carry it, and that is "
                  "case authoring we have not done."),
    dict(cond="hepatic_encephalopathy", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         seg=("Item\nBrain MRI.", None),
         response="Applied: brain MRI is required in only the 5 cases with genuine diagnostic "
                  "doubt and absent elsewhere."),
    dict(cond="hepatic_encephalopathy", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=2, tier="unchanged", status="no_change",
         response="No change requested and none made."),
    dict(cond="hepatic_encephalopathy", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="optional", status="applied",
         response="Applied: EEG is no longer required in any case (recommended in 23, optional "
                  "in 1)."),
    dict(cond="hepatic_encephalopathy", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=2, tier="optional", status="confirm",
         response="Not applied, deliberately, and this is the one place we are asking you to "
                  "overrule us. All 30 cases still require the head CT. Your reasoning is "
                  "explicit (ACG 2026 suggests against routine imaging without focal deficits) "
                  "and we accept it in principle; what stopped us is that dropping an exclusion "
                  "step before an invasive procedure, on our own reading, is not our call. Tell "
                  "us to demote it and we will."),

    # === high-grade glioma (reviewer 2) ===
    dict(cond="brain_tumor_glioma", filed="analyze_brain_mri", tool="obtain_tissue_diagnosis",
         reviewer=2, tier="required", status="applied",
         seg=(None, "Item\nBrain MRI."),
         response="Applied, and your reading of why it was missing was exactly right. All 30 "
                  "cases already held the neuropathology and the molecular panel — filed as an "
                  "interpret_labs follow-up. The integrated diagnosis was therefore obtainable by "
                  "ordering blood tests, and no action anywhere required obtaining tissue. Now "
                  "obtain_tissue_diagnosis is required in all 30, with a WHO CNS5 layered report, "
                  "and the laboratory route is removed."),
    dict(cond="brain_tumor_glioma", filed="interpret_labs", tool="obtain_tissue_diagnosis",
         reviewer=2, tier="required", status="applied",
         seg=(None, "Item\nLaboratory studies."),
         response="Applied: the molecular assays you name are the vocabulary of the tool "
                  "(IDH1 IHC, IDH1/IDH2 sequencing, 1p/19q, ATRX, CDKN2A/B, TERT, EGFR, chr7/10, "
                  "H3 K27, MGMT by methylation not IHC), each priced, and the required assay set "
                  "differs per case as your conditions require."),
    dict(cond="brain_tumor_glioma", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         seg=("Item\nLaboratory studies.", None),
         response="Applied: laboratory studies in this condition are treatment-safety and "
                  "follow-up, and tumour molecular profiling is no longer reachable through them."),
    dict(cond="brain_tumor_glioma", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         seg=("Item\nBrain MRI.", None),
         response="Applied: contrast is not optional in these cases. The sweep this triggered "
                  "also found a cervical-cord glioblastoma being imaged by a brain MRI."),
    dict(cond="brain_tumor_glioma", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="unchanged", status="applied",
         seg=(None, "Item\nAdvanced imaging"),
         response="Applied: no case requires EEG for the tumour itself."),
    dict(cond="brain_tumor_glioma", filed="analyze_eeg", tool="order_advanced_imaging",
         reviewer=2, tier="optional", status="applied",
         seg=("Item\nAdvanced imaging", None),
         response="Applied: amino_acid_PET was added with the tracers EANO names, and perfusion "
                  "MRI plus MR spectroscopy are recommended actions in all 30 cases. FDG-PET is "
                  "not among them, per your note."),
    dict(cond="brain_tumor_glioma", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=2, tier="unchanged", status="no_change",
         response="No change requested and none made."),
]

SPEC += [
    # === Guillain-Barre (reviewer 2) ===
    dict(cond="guillain_barre", filed="order_cardiac_monitoring", tool="order_cardiac_monitoring",
         reviewer=2, tier="required", status="applied",
         seg=(None, "Item\nRespiratory function monitoring"),
         response="Applied: required in all 30 cases, and a telemetry report was authored from "
                  "each case's own autonomic picture first, because raising a tier without a "
                  "result makes the required act unanswerable."),
    dict(cond="guillain_barre", filed="order_cardiac_monitoring", tool="order_specialized_test",
         reviewer=2, tier="required", status="applied",
         seg=("Item\nRespiratory function monitoring", None),
         response="Applied: respiratory_function already existed — the review app was showing 9 of "
                  "21 specialized tests, which is why it looked absent — and it is now a required "
                  "action in all 30 cases."),
    dict(cond="guillain_barre", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=2, tier="unchanged", status="applied",
         seg=(None, "Item\nSpinal and peripheral nerve imaging"),
         response="Applied: emg_ncs is required in all 30 cases."),
    dict(cond="guillain_barre", filed="order_specialized_test", tool="order_body_imaging",
         reviewer=2, tier="optional", status="partial",
         seg=("Item\nSpinal and peripheral nerve imaging", None),
         response="Half done, and we would rather say so. The tool exists and whole-spine MRI is "
                  "orderable and priced, so cord compression is no longer outside the action "
                  "space; but no Guillain-Barre case orders it yet. Your trigger list — sensory "
                  "level, extensor plantars, sphincter involvement, fever at onset — is what "
                  "identifies the cases that should carry it, and that authoring is outstanding."),
    dict(cond="guillain_barre", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: required in all 30, and 14-3-3/RT-QuIC are gone from this condition."),
    dict(cond="guillain_barre", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied. The anti-GQ1b point also caught a routing defect elsewhere: a "
                  "myasthenia case was being served a Miller-Fisher ganglioside panel because the "
                  "matcher treated the token 'anti' as identifying an antibody."),
    dict(cond="guillain_barre", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied in the strongest form: no Guillain-Barre case images the brain at all. "
                  "The sweep this comment started moved 63 spine studies out of the brain-MRI "
                  "tool across the whole dataset."),
    dict(cond="guillain_barre", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=2, tier="unchanged", status="no_change",
         response="No change requested. The ECG is a recommended baseline in all 30 cases, which "
                  "is the role your note describes."),

    # === myasthenia gravis (reviewer 2) ===
    dict(cond="myasthenia_gravis", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied — and this is the comment that found the worst defect in the dataset. "
                  "Myasthenia was the one condition nobody reviewed (these five annotations "
                  "arrived filed under peripheral neuropathy), and checking it because of them "
                  "showed that in all 9 cases holding an acetylcholine-receptor panel the report "
                  "was unreachable: the required action orders anti-AChR, anti-MuSK, anti-LRP4 and "
                  "TSH, while the result was stored under a label naming the disease. Eight cases "
                  "answered with an exclusion panel and one with the Miller-Fisher ganglioside "
                  "panel. The benchmark asked for serological confirmation of myasthenia and did "
                  "not deliver the serology. Fixed in all nine without touching a word of the "
                  "reports."),
    dict(cond="myasthenia_gravis", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=2, tier="unchanged", status="applied",
         seg=(None, "Item\nMediastinal (thymic) imaging"),
         response="Applied: repetitive nerve stimulation is required in 27 cases and single-fibre "
                  "EMG is ordered in 24 (6 required, 17 recommended, 1 optional). emg_single_fiber "
                  "already existed and was one of the values the stale catalog hid from you."),
    dict(cond="myasthenia_gravis", filed="order_specialized_test", tool="order_body_imaging",
         reviewer=2, tier="required", status="applied",
         seg=("Item\nMediastinal (thymic) imaging", None),
         response="Applied: mediastinum_CT is a required action in all 30 cases. Before "
                  "order_body_imaging existed the agent could image only the brain, so the thymus "
                  "was unreachable."),
    dict(cond="myasthenia_gravis", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: exactly one case orders a brain MRI, and no case orders it as a "
                  "first-line study."),
    dict(cond="myasthenia_gravis", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied in the strongest form: no myasthenia case orders CSF studies."),
    dict(cond="myasthenia_gravis", filed="order_advanced_imaging", tool="order_advanced_imaging",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied, and your scoping turned out to describe the cases exactly: the only "
                  "two required advanced-imaging actions in this condition are whole-body FDG-PET "
                  "in the two cases whose diagnosis is Lambert-Eaton myasthenic syndrome — the "
                  "occult-tumour search you say belongs there and not to myasthenia."),

    # === cardiac syncope (reviewer 2) ===
    dict(cond="syncope_cardiac", filed="order_cardiac_monitoring", tool="order_cardiac_monitoring",
         reviewer=2, tier="required", status="applied",
         response="Applied: required in all 30 cases, with the modality selected by event "
                  "frequency rather than left to an unqualified Holter."),
    dict(cond="syncope_cardiac", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: required in all 30 cases."),
    dict(cond="syncope_cardiac", filed="order_echocardiogram", tool="order_echocardiogram",
         reviewer=2, tier="unchanged", status="applied",
         seg=(None, "Item\nAdvanced cardiac imaging"),
         response="Applied: required in 29 of the 30 cases, and recommended in the thirtieth "
                  "(SYNC-CARD-P03), a Brugada syndrome where the diagnosis is electrocardiographic "
                  "and the echocardiogram excludes structural disease rather than establishing the "
                  "cause. Exercise echocardiography was added as its own study (exercise_echo, "
                  "priced) because one case had been modelling a provoked outflow gradient as a "
                  "treadmill stress test — a different study at a different price."),
    dict(cond="syncope_cardiac", filed="order_echocardiogram", tool="order_advanced_imaging",
         reviewer=2, tier="optional", status="applied",
         seg=("Item\nAdvanced cardiac imaging", None),
         response="Applied. Half of this was already satisfied — cardiac MRI existed and 18 of 30 "
                  "cases order it — and the rest was added and priced: coronary CTA, coronary "
                  "angiography, cardiac FDG-PET, chest CT angiography. Your prediction that "
                  "offering brain MRI and no cardiac imaging is 'the arrangement most likely to "
                  "produce the wrong imaging choice' was already true in the data: one case was "
                  "requesting a CT pulmonary angiogram through the head-CT tool."),
    dict(cond="syncope_cardiac", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="optional", status="applied",
         response="Applied, and the numbers were worse than the comment assumed: TSH was in the "
                  "required panel of 29 of 30 cases and BNP of 27. Thyroid now survives only in "
                  "the 4 cases with a thyroid mechanism on the differential and BNP in the 3 where "
                  "a guideline risk-stratifies with it; the step is required in 11 cases and "
                  "recommended in 19. Mandated laboratory spend fell from 6108 to 4686 EUR. A "
                  "hard sequence rule requiring labs before monitoring in 28 cases had to go with "
                  "it, or an agent that correctly skipped the panel took a violation."),
    dict(cond="syncope_cardiac", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: no case requires EEG; two carry it as optional for the "
                  "pseudosyncope/epilepsy question."),
    dict(cond="syncope_cardiac", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: exactly one case requires a brain MRI, and it is one where the "
                  "presentation points at a central cause rather than at an uncomplicated "
                  "syncope."),

    # === status epilepticus (reviewer 2) ===
    dict(cond="status_epilepticus", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: EEG is required in all 30 cases."),
    dict(cond="status_epilepticus", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied. Your point that antiseizure drug levels are the highest-yield finding "
                  "also exposed a scoring hole: an agent ordering 'valproate level' — the "
                  "clinically correct request — got no credit for a gold action naming "
                  "'AED levels', while the vague term scored. The specific order now satisfies the "
                  "class request, and not the other way round."),
    dict(cond="status_epilepticus", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied. One case also had its paraneoplastic panel — carrying an anti-Hu "
                  "titre that mandates an urgent cancer search — stored where no call could "
                  "reach it."),
    dict(cond="status_epilepticus", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="partial",
         response="The epilepsy-oriented protocol and the indication list are applied, and MRI is "
                  "required in 17 cases and absent where the cause is already established. "
                  "MR_venography exists in the vocabulary and is priced, but no "
                  "status-epilepticus case orders it yet: the venous question you raise has a "
                  "tool and no case."),
    dict(cond="status_epilepticus", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: non-contrast head CT is required in all 30 cases."),
]

SPEC += [
    # === multiple sclerosis (reviewer 1) ===
    dict(cond="multiple_sclerosis", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Applied, and the comment found something no automatic check could: all 30 cases "
                  "already carried both a brain and a cord study, but both went through the "
                  "brain-MRI tool with the same parameter, so for the score they were one "
                  "examination. Imaging the brain alone gave full coverage and the cord study was "
                  "invisible. They are now separate, orderable and scored."),
    dict(cond="multiple_sclerosis", filed="analyze_brain_mri", tool="order_body_imaging",
         reviewer=1, tier="required", status="applied",
         response="This is where 'brain and spinal cord' now lives: spine_MRI is a required "
                  "order_body_imaging action in all 30 cases, priced separately from the brain "
                  "study."),
    dict(cond="multiple_sclerosis", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="optional", status="applied",
         response="Applied: CSF is optional in 29 cases and recommended in 1."),
    dict(cond="multiple_sclerosis", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="optional", status="applied",
         response="Applied: optical coherence tomography and visual evoked potentials are ordered "
                  "in all 30 cases and nothing else is. Both already existed in the vocabulary — "
                  "OCT was one of the values the stale catalog hid from you."),
    dict(cond="multiple_sclerosis", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="required", status="applied",
         response="Applied: the required panel is the mimic-exclusion set you list."),
    dict(cond="multiple_sclerosis", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="applied",
         response="Removed: no multiple-sclerosis case orders an EEG."),
    dict(cond="multiple_sclerosis", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed: no multiple-sclerosis case orders an ECG."),

    # === migraine with aura (reviewer 1) ===
    dict(cond="migraine_with_aura", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="optional", status="applied",
         seg=(None, "Migraine with aura is primarily a clinical diagnosis. The true required"),
         response="Applied: MRI is optional in 15 cases, recommended in 5 and absent in the other "
                  "10 — no case requires it."),
    dict(cond="migraine_with_aura", filed="analyze_brain_mri", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("Migraine with aura is primarily a clinical diagnosis. The true required", None),
         response="Applied, and it closed a hole that makes the point better than we could. The "
                  "structured ICHD-3 history is now a required action in all 30 cases. Before "
                  "that, and after the MRI was demoted, 15 of the 30 cases had a required set "
                  "consisting only of the two zero-cost universal tools: an agent scored full "
                  "required coverage without performing a single diagnostic act. Your sentence — "
                  "that the ICHD-3 history is the only true required test here — was the fix."),
    dict(cond="migraine_with_aura", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="confirm",
         response="Almost removed: 29 of 30 cases have no EEG. The exception is MIG-AURA-RM11, "
                  "whose diagnosis is hemiplegic migraine *with migralepsy* — a seizure during "
                  "aura, ICHD-3 1.4.4 — so the 24 h video EEG is the study that establishes half "
                  "of the diagnosis rather than routine headache evaluation. We kept it required "
                  "there. Tell us if you disagree and it goes."),
    dict(cond="migraine_with_aura", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed: no migraine case orders an ECG."),
    dict(cond="migraine_with_aura", filed="order_echocardiogram", tool="order_echocardiogram",
         reviewer=1, tier="remove", status="confirm",
         response="We looked at this three times and each time reached the opposite of what we "
                  "first wrote, so here is the full answer. Three cases order an echocardiogram at "
                  "required, and none of them is a routine migraine: MIG-AURA-P03 is a migrainous "
                  "infarction whose diagnosis rests on secondary causes having been excluded, "
                  "MIG-AURA-P07 is a cardioembolic PCA infarct that is explicitly *not* migrainous "
                  "infarction, and MIG-AURA-P08 is genetically confirmed MELAS where cardiomyopathy "
                  "screening is standard. In each the echo is embolic-source or cardiomyopathy "
                  "work-up. The routine migraine echo your comment targets does not exist in the "
                  "cases — but the condition label is still 'migraine with aura', so you should "
                  "decide whether that is acceptable or whether those cases belong elsewhere."),
    dict(cond="migraine_with_aura", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="remove", status="confirm",
         response="Almost removed: one case (MIG-AURA-RM11) keeps it as recommended, on a "
                  "suspicion of secondary headache — the same case that keeps the video EEG for "
                  "its migralepsy. No case requires it. If you consider a lumbar puncture "
                  "unjustifiable even on that suspicion, tell us and it goes."),
    dict(cond="migraine_with_aura", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied: no case requires blood tests; 4 carry them as optional and 1 as "
                  "recommended, on a secondary-headache suspicion."),

    # === early Alzheimer's disease (reviewer 1) ===
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Kept required in all 30 cases, as asked."),
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("1) structured cognitive", "2) non-contrast"),
         src_seg=("Source:", None),
         response="Applied: a structured cognitive assessment is a required action in all 30 "
                  "cases, scored against the functional criterion, so the 10 mild-cognitive-"
                  "impairment cases are not required to have lost independence. This is one of "
                  "the four mandatory steps you named that had no tool behind them at all."),
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="order_ct_scan",
         reviewer=1, tier="optional", status="partial",
         seg=("2) non-contrast", "3) FDG-PET"),
         src_seg=("Source:", None),
         response="Not done: the tool and the study exist, but no Alzheimer case uses head CT as "
                  "the MRI alternative, because every case has an MRI. If you want the "
                  "MRI-unavailable pathway represented, it needs a case built for it."),
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="order_advanced_imaging",
         reviewer=1, tier="optional", status="applied",
         seg=("3) FDG-PET", "Suggested diagnostic sequence"),
         src_seg=("Source:", None),
         response="Applied: FDG-PET and amyloid PET are ordered across the 30 cases (18 amyloid "
                  "recommended, 12 required, 16 FDG optional, 6 required), and no case treats "
                  "either as a first-line test."),
    dict(cond="alzheimers_early", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="required", status="applied",
         response="Applied: the required panel is the reversible-cause set you list."),
    dict(cond="alzheimers_early", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="confirm",
         response="Downgraded rather than removed, and we would like your ruling. One case "
                  "(ALZ-EARLY-RP04) keeps EEG as optional because its differential includes "
                  "Creutzfeldt-Jakob disease and an encephalopathy. The criterion we used is your "
                  "own, from the syncope panel: the label is the hypothesis under test, so an agent "
                  "that correctly suspects something else must still be able to act. If you would "
                  "rather it be deleted outright, we will edit the case."),
    dict(cond="alzheimers_early", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed: no Alzheimer case orders an ECG."),
    dict(cond="alzheimers_early", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="optional", status="applied",
         seg=(None, "Add amyloid PET"),
         response="Applied: CSF biomarkers are required in the 13 cases where the diagnosis needs "
                  "biomarker confirmation and recommended in the other 17."),
    dict(cond="alzheimers_early", filed="analyze_csf", tool="order_advanced_imaging",
         reviewer=1, tier="optional", status="applied",
         seg=("Add amyloid PET", None),
         response="Applied: amyloid PET is available as the alternative to CSF biomarkers, and no "
                  "case orders both where the CSF result is already conclusive."),

    # === frontotemporal dementia (reviewer 1) ===
    dict(cond="ftd", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="required", status="applied",
         response="Applied: the required panel is the reversible-cause set, and autoimmune, "
                  "paraneoplastic and genetic testing are no longer part of a fixed broad panel."),
    dict(cond="ftd", filed="order_advanced_imaging", tool="order_advanced_imaging",
         reviewer=1, tier="optional", status="applied",
         response="Applied: no FTD case requires advanced imaging (27 optional, 32 recommended), "
                  "and FDG-PET is the modality it points at."),
    dict(cond="ftd", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="required", status="applied",
         response="Applied: the validated neuropsychological battery is required in all 30 cases; "
                  "genetic testing is optional in 10, recommended in 7 and required only in the 10 "
                  "with young onset or a strong family history. Your bracketed request — put "
                  "genetics in Alzheimer's too, as optional — is done."),
    dict(cond="ftd", filed="order_specialized_test", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("Validated neuropsychological testing must be REQUIRED", "Genetic testing should"),
         src_seg=("Source:", None),
         response="Applied as a separate act: a structured cognitive and behavioural assessment is "
                  "required in all 30 cases, scored against the six Rascovsky features, each "
                  "marked present only where the history describes it."),
    dict(cond="ftd", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=1, tier="optional", status="partial",
         response="Applied as far as the catalog goes — CT angiography, carotid duplex and "
                  "transcranial Doppler are not FTD actions in any case — but only one case uses "
                  "head CT as the MRI alternative. The same gap as in Alzheimer's: the pathway is "
                  "described and barely exercised."),

    # === Parkinson's disease (reviewer 1) ===
    dict(cond="parkinsons", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied: blood tests are optional in all 30 cases."),
    dict(cond="parkinsons", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="applied",
         response="Removed: no Parkinson case orders an EEG."),
    dict(cond="parkinsons", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed: no Parkinson case orders an ECG."),
    dict(cond="parkinsons", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="optional", status="applied",
         response="Applied, and the residue is worth reading case by case: no case orders EMG/NCS, "
                  "repetitive nerve stimulation, a biopsy or evoked potentials. The 10 remaining "
                  "required actions are autonomic testing in the multiple-system-atrophy cases, "
                  "polysomnography for REM-sleep behaviour disorder, and the neuropsychological "
                  "battery in the cases whose diagnosis is dementia with Lewy bodies, progressive "
                  "supranuclear palsy or Parkinson's with cognitive impairment — which is the "
                  "'when cognition is clinically relevant' exception you wrote."),
    dict(cond="parkinsons", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="MRI is required in all 30 cases."),
    dict(cond="parkinsons", filed="analyze_brain_mri", tool="order_ct_scan",
         reviewer=1, tier="optional", status="partial",
         response="Not done: no Parkinson case uses CT as the alternative to MRI."),

    # === amyotrophic lateral sclerosis (reviewer 1) ===
    dict(cond="als", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="required", status="applied",
         response="Applied: EMG/NCS is required in all 30 cases, respiratory function too, and "
                  "genetic testing is recommended in 26 and required in 4. No case orders "
                  "repetitive nerve stimulation, a biopsy, evoked potentials or tilt testing."),
    dict(cond="als", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Applied: required in all 30."),
    dict(cond="als", filed="analyze_brain_mri", tool="order_body_imaging",
         reviewer=1, tier="required", status="applied",
         response="Applied, and this comment found the same defect as in multiple sclerosis, one "
                  "step worse: the exclusion of cervical myelopathy — the mimic that must be ruled "
                  "out before a motor-neuron diagnosis — was buried inside the brain-MRI report in "
                  "all 30 cases, so no action asked for it and no score could see it. spine_MRI is "
                  "now a required order_body_imaging action in all 30."),
    dict(cond="als", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="required", status="applied",
         response="Applied. Auditing this panel also caught an error of ours that a clinical "
                  "reader would have spotted immediately: the androgen-receptor CAG repeat for "
                  "Kennedy disease — an X-linked test — was in the ordered panel of 11 female "
                  "patients, one of whom was even given a result, while the action's own text "
                  "said '(in males)'."),
    dict(cond="als", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="optional", status="applied",
         response="Applied: CSF is recommended, never required, in all 30 cases."),

    # === normal pressure hydrocephalus (reviewer 1) ===
    dict(cond="nph", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Applied: required in all 30, and the reports carry the NPH-specific markers you "
                  "list rather than a generic structural read."),
    dict(cond="nph", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied: blood tests are optional in all 30 cases."),
    dict(cond="nph", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="required", status="applied",
         response="Applied: required in all 30, as the large-volume tap with opening pressure."),
    dict(cond="nph", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="remove", status="applied",
         response="Applied, and this was still outstanding until we answered your comments one by "
                  "one. The standalone neuropsychological battery had stayed REQUIRED in all 30 "
                  "cases beside the new pre/post assessment — the duplication you objected to. It "
                  "is now optional, and the redundant sequence rule that said 'battery before the "
                  "tap' went with it, because leaving it would have penalised an agent that "
                  "performs the mandatory assessment and skips the optional battery. No case "
                  "orders EMG/NCS, a biopsy, evoked potentials or tilt testing."),
    dict(cond="nph", filed="order_specialized_test", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("If Specialized test is kept as REQUIRED", "Neuropsychological testing"),
         src_seg=("Sources:", None),
         response="Applied exactly as written: perform_clinical_assessment"
                  "{gait_and_balance_timed} is required in all 30 cases and its report carries the "
                  "before-and-after comparison, with each case's own timed-up-and-go and 10-metre "
                  "figures where it states them and the >=20% threshold where it does not. "
                  "NPH-P08's negative tap is preserved as negative."),
    dict(cond="nph", filed="order_advanced_imaging", tool="order_advanced_imaging",
         reviewer=1, tier="remove", status="confirm",
         response="Kept as optional in all 30 rather than removed, and we want your ruling. Every "
                  "one of the 30 cases uses amyloid or FDG PET for the Alzheimer differential, not "
                  "as a test for NPH — the distinction your own syncope comment draws. The tier is "
                  "now uniformly optional across all 30. If you would rather it be deleted, say so."),

    # === temporal lobe epilepsy (reviewer 1) ===
    dict(cond="focal_epilepsy_temporal", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="required", status="applied",
         response="Applied, and it caught a gap in the vocabulary: the sleep-deprived study you "
                  "name as the second-line recording did not exist as an orderable value, so the "
                  "request could be neither made nor scored. sleep_deprived is now priced (276 "
                  "EUR, CPT 95819) and derives into the tool enum, the catalog and the cost "
                  "tracker. Routine EEG comes first in the cases, with video or ambulatory "
                  "recording where events have to be captured, and no case uses continuous ICU "
                  "monitoring."),
    dict(cond="focal_epilepsy_temporal", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Applied: required in all 30 with a dedicated epilepsy protocol."),
    dict(cond="focal_epilepsy_temporal", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied: optional in all 30 cases."),
    dict(cond="focal_epilepsy_temporal", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="optional", status="applied",
         response="Applied as your note describes: the ECG survives in the 2 cases presenting as a "
                  "first suspected seizure or transient loss of consciousness, and nowhere else."),
    dict(cond="focal_epilepsy_temporal", filed="order_echocardiogram", tool="order_echocardiogram",
         reviewer=1, tier="remove", status="confirm",
         response="Downgraded to optional rather than removed, in the 2 cases initially worked up "
                  "as syncope or pulmonary embolism (FEPI-TEMP-P05, -RP02). Answering your "
                  "comments one by one caught that these had been left at *recommended*, not "
                  "optional, which made the account we were about to send you wrong; they are "
                  "optional now. The criterion we used is your own, from the syncope panel: the "
                  "label is the hypothesis under test, so an agent that correctly suspects a "
                  "cardiac cause must still be able to act. If you would rather the item be "
                  "deleted from this condition outright, say so and we will edit both cases."),
    dict(cond="focal_epilepsy_temporal", filed="order_cardiac_monitoring",
         tool="order_cardiac_monitoring", reviewer=1, tier="remove", status="confirm",
         response="Same as the echocardiogram: optional in the 2 cases with syncope on the "
                  "differential, and corrected from recommended to optional while answering this "
                  "comment. Same question back to you — delete it from the condition, or leave it "
                  "reachable for the agent that correctly suspects a cardiac cause?"),

    # === functional neurological disorder (reviewer 1) ===
    dict(cond="functional_neurological_disorder", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier=None, status="open",
         response="Your question, answered in the reply: yes, diagnostic overuse is an objective — "
                  "cost tracking against Medicare reference rates is one of the project's main "
                  "components — so we take your second option and keep the condition, with the "
                  "diagnostic tools optional. Checking the cases showed your doubt was better "
                  "founded than our answer: all 30 required a gadolinium brain MRI and a "
                  "laboratory battery, none performed a functional-signs examination, no action "
                  "anywhere was optional, and the required pathway cost 1303 EUR on average — more "
                  "than bacterial meningitis (1204) or Guillain-Barre (1223). The condition meant "
                  "to measure restraint was rewarding the opposite, and the ground truth encoded "
                  "the diagnosis-of-exclusion model the literature has abandoned. Now the "
                  "functional-signs examination is the mandatory act in all 30, the MRI is optional "
                  "in 23 and recommended once without contrast in 7, laboratories are optional in "
                  "27, and EMG/NCS and evoked potentials are scored as useless calls in all 30 "
                  "instead of being forbidden in prose. One deliberate departure: video-EEG stays "
                  "required in the 22 cases with paroxysmal events, because a recorded habitual "
                  "event without ictal correlate is the positive diagnostic act for psychogenic "
                  "non-epileptic seizures (ILAE 2013), not an exclusion test. Say the word and we "
                  "demote that too."),
]

SPEC += [
    # === anti-NMDA receptor encephalitis (reviewer 2) ===
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_brain_mri",
         tool="order_body_imaging", reviewer=2, tier="required", status="applied",
         seg=(None, "Item:\nBrain MRI"),
         response="Applied: chest, abdomen and pelvis CT is a required action in all 30 cases. "
                  "You called this the highest-priority finding in the review and you were right "
                  "that no existing item covered it — before order_body_imaging existed the agent "
                  "could image the brain and nothing else, so an ovarian teratoma was outside the "
                  "action space entirely."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_brain_mri",
         tool="analyze_brain_mri", reviewer=2, tier="unchanged", status="applied",
         seg=("Item:\nBrain MRI", None),
         response="Applied: the MRI stays required in all 30 cases and its role in the ground "
                  "truth is exclusion of alternatives, not confirmation."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: the serum cell-based assay for anti-GluN1 is named in the required "
                  "panel and read together with the CSF result, not alone."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied, and it uncovered a defect of exactly the kind you found in myasthenia: "
                  "in two cases the anti-NMDAR result — the antibody that defines the disease — "
                  "was stored under a trigger no call an agent can make could reach, so the "
                  "required order was answered by an unrelated payload. Both are fixed; no report "
                  "text changed."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: EEG is required in all 30 cases and extreme delta brush is named."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=2, tier="unchanged", status="no_change",
         response="No change requested and none made."),
]

# The one comment whose target no longer exists, kept so the answer is not lost with the row.
RETIRED = [
    dict(cond="peripheral_neuropathy", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier=None, status="retired",
         response="Done: peripheral neuropathy is retired and vascular dementia is in its place, "
                  "with 30 new cases. This annotation therefore points at a condition the catalog "
                  "no longer has, so nothing renders it — which is why it is recorded here. Your "
                  "file is untouched: it is your record, not ours to rewrite."),
]

HEADER = """\
# Per-condition tool guidance from the July 2026 clinical tool review.
#
# GENERATED — do not hand-edit. Source:
#   agent-platform/scripts/review/build_condition_tool_guidance.py
#
# Two external neurologists reviewed the tool catalog condition by condition and left 91
# annotations, most carrying a block headed "Revised description (to be inserted)". That text
# is condition-specific, and `ToolMeta.description` is one string per tool shown under every
# condition, so it had nowhere to live: "for MS, brain *and cord* MRI with an MS protocol" is
# wrong in the other nineteen conditions, and putting a condition-specific indication in the
# agent-facing schema would hand the agent the diagnosis it is meant to infer.
#
# This file is that missing place. It is served by the review API next to each condition-tool
# row and rendered in the review app. It is READ ONLY BY `review_api`:
# `tests/test_condition_tool_guidance.py` fails if anything under `neuroagent/tools/`,
# `neuroagent/agents/` or `neuroagent/api/` reads it, because that would be the leak.
#
# Fields per entry:
#   guidance       the reviewer's own revised description, sliced from their annotation
#   rationale      their reasoning, including which elements they removed and why
#   source         the guideline they cite
#   requested_tier the tier they asked for in this condition
#   status         applied | partial | confirm | no_change | open | retired
#   our_response   what we actually did about this specific comment
#   filed_under    the row they annotated, when it differs from the tool that performs the
#                  study — eleven comments describe studies the twelve-tool action space could
#                  not express, so they were filed against whichever row was nearest
#
# reviewer: 1 took the chronic conditions, 2 the acute ones. Reviewer codes are credentials
# and never appear here.
"""


def _block(key: str, text: str, indent: str) -> str:
    if not text:
        return ""
    body = "\n".join(indent + "  " + line if line.strip() else "" for line in text.split("\n"))
    return f"{indent}{key}: |-\n{body}\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    comments: dict[tuple[str, str], tuple[int, str]] = {}
    for path in sorted(glob.glob(REVIEWS)):
        data = json.loads(pathlib.Path(path).read_text())
        number = REVIEWER_NUMBER.get(data["reviewer_code"])
        if number is None:
            # A third reviewer code exists and opened the catalog on 2026-07-10 without
            # annotating anything. Nothing to map, nothing to emit.
            if data.get("field_annotations"):
                raise SystemExit(f"unmapped reviewer code with annotations in {path}")
            continue
        for ann in data.get("field_annotations") or []:
            parts = ann["field_path"].split(":")
            if len(parts) != 3 or parts[0] != "condition_tool":
                continue
            comments[(parts[1], parts[2])] = (number, ann["comment"])

    out: dict[str, dict[str, dict[str, object]]] = {}
    used: set[tuple[str, str]] = set()
    ordered = sorted(SPEC + RETIRED, key=lambda r: r["filed"] != r["tool"])
    for row in ordered:
        cond, filed, tool = row["cond"], row["filed"], row["tool"]  # type: ignore[index]
        key = (cond, filed)
        if key not in comments:
            raise SystemExit(f"spec references an annotation that does not exist: {key}")
        used.add(key)
        number, comment = comments[key]
        if number != row["reviewer"]:
            raise SystemExit(f"{key}: spec says reviewer {row['reviewer']}, data says {number}")
        seg = row.get("seg")
        segment = _slice(comment, *seg) if seg else comment  # type: ignore[misc]
        guidance, rationale, source = _split_guidance(segment)
        if row.get("src_seg"):
            source = _clean(_slice(comment, *row["src_seg"]))  # type: ignore[misc]
            source = re.sub(r"^Sources?:\s*", "", source)
        entry = out.setdefault(cond, {}).setdefault(tool, {})
        for field, value in (("guidance", guidance), ("rationale", rationale), ("source", source)):
            if not value:
                continue
            existing = entry.get(field)
            if not existing:
                entry[field] = value
            elif value not in existing:  # two segments often cite the same guideline
                entry[field] = f"{existing}\n\n{value}"
        entry["reviewer"] = number
        if filed != tool:
            filed_under = entry.setdefault("filed_under", [])
            if filed not in filed_under:
                filed_under.append(filed)  # type: ignore[union-attr]
        if row.get("tier"):
            entry["requested_tier"] = row["tier"]
        entry["status"] = row["status"]
        entry["our_response"] = row["response"]

    missing = sorted(set(comments) - used)
    if missing:
        raise SystemExit(f"{len(missing)} annotations are not accounted for: {missing}")

    lines = [HEADER]
    for cond in sorted(out):
        lines.append(f"\n{cond}:\n")
        for tool in sorted(out[cond]):
            e = out[cond][tool]
            lines.append(f"  {tool}:\n")
            lines.append(f"    reviewer: {e['reviewer']}\n")
            if "filed_under" in e:
                lines.append("    filed_under: ["
                             + ", ".join(sorted(e["filed_under"])) + "]\n")  # type: ignore[arg-type]
            if "requested_tier" in e:
                lines.append(f"    requested_tier: {e['requested_tier']}\n")
            lines.append(f"    status: {e['status']}\n")
            for field in ("guidance", "rationale", "source", "our_response"):
                lines.append(_block(field, str(e.get(field) or ""), "    "))
    text = "".join(lines)
    entries = sum(len(v) for v in out.values())
    print(f"{len(comments)} annotations -> {entries} entries across {len(out)} conditions")
    if args.write:
        OUT.write_text(text)
        print(f"wrote {OUT} ({len(text.splitlines())} lines)")
    else:
        sys.stdout.write(text[:1500])


if __name__ == "__main__":
    main()
