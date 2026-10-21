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
         response="Applied as a conditional requirement: the 3 cases with a negative or "
                  "inconclusive NCCT require LP; the 27 CT-positive cases explicitly avoid it. "
                  "The selected reports and calls contain first-versus-last tube RBC counts, "
                  "protein, glucose and the newly priced spectrophotometric xanthochromia assay; "
                  "OCB, infection PCR, autoimmune antibodies and prion assays are absent."),
    dict(cond="subarachnoid_hemorrhage", filed="order_advanced_imaging",
         tool="order_advanced_imaging", reviewer=2, tier="optional", status="applied",
         response="Applied: TCD is optional in all 30 cases and is the sole routine advanced "
                  "surveillance modality. PET, DaTscan, MIBG, perfusion/spectroscopy MRI, MRA "
                  "and carotid duplex are removed. Three case-specific catheter-DSA actions are "
                  "retained as recommended because CTA is occult/uncertain or definitive "
                  "endovascular anatomy is required; catheter DSA is not a duplicate CTA/MRA."),
    dict(cond="subarachnoid_hemorrhage", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=2, tier="required", status="applied",
         response="Applied. Every case has two explicitly discriminated required actions: "
                  "first-line NCCT with contrast=false/angiography=false, then a distinct CTA "
                  "with contrast=true/angiography=true. The 15 unrelated CT-perfusion outputs "
                  "have been removed from this item, and CTA/DSA routing is no longer crossed."),
    dict(cond="subarachnoid_hemorrhage", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: the required laboratory action in all 30 cases is limited to CBC, "
                  "metabolic panel and coagulation. Thyroid, inflammatory, autoimmune and "
                  "paraneoplastic panels are absent; no sporadic case receives routine genetics."),

    # === ischaemic stroke (reviewer 2) ===
    dict(cond="ischemic_stroke", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=2, tier="required", status="applied",
         response="Applied: all 30 cases have explicitly discriminated first-line NCCT and a "
                  "separate subsequent CTA as 60 required actions. CTA is never represented as "
                  "a substitute for NCCT and its call text states that creatinine must not delay it."),
    dict(cond="ischemic_stroke", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="optional", status="applied",
         response="Applied: no case requires EEG. One case retains it as optional for a witnessed "
                  "tonic-hand seizure-mimic question; the other 29 have no EEG action or authored "
                  "output, and every trace states that EEG must not delay reperfusion."),
    dict(cond="ischemic_stroke", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="optional", status="applied",
         seg=(None, "NEW ITEM OPTIONAL"),
         response="Applied: brain MRI is optional in all 30 cases."),
    dict(cond="ischemic_stroke", filed="analyze_brain_mri", tool="order_advanced_imaging",
         reviewer=2, tier="optional", status="applied",
         seg=("NEW ITEM OPTIONAL", None),
         response="Applied end to end rather than only adding vocabulary: CT_perfusion is optional "
                  "and reachable in the 2 wake-up/extended-window cases where an authored core/"
                  "penumbra report changes selection. Four reports formerly misrouted through "
                  "ordinary head CT were audited; three routine-window/non-selection uses were "
                  "removed. Blanket MRA, TCD and carotid-duplex duplication is also removed."),
    dict(cond="ischemic_stroke", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied in all 30 cases: glucose, CBC, coagulation, creatinine and baseline "
                  "troponin are the acute required set. Case-specific thrombophilia/autoimmune "
                  "panels are demoted to subsequent recommended aetiological work-up. The ground "
                  "truth explicitly encodes every requested do-not-delay rule."),

    # === bacterial meningitis (reviewer 2) ===
    dict(cond="bacterial_meningitis", filed="interpret_labs", tool="order_microbiology",
         reviewer=2, tier="required", status="applied",
         seg=(None, "Item\nLaboratory studies"),
         response="Applied: blood culture with susceptibility is required and reachable in all 30 "
                  "cases. Every action and trajectory states collection before antimicrobials when "
                  "possible, while making explicit that sampling, LP or imaging never delays "
                  "empirical therapy."),
    dict(cond="bacterial_meningitis", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         seg=("Item\nLaboratory studies", None),
         response="Applied: all 30 cases name CBC/differential, CMP, CRP or procalcitonin, paired "
                  "blood glucose, coagulation and HIV. Blood cultures are no longer represented as "
                  "a laboratory-panel result."),
    dict(cond="bacterial_meningitis", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: every LP action explicitly names opening pressure, appearance, total and "
                  "differential cells, RBC, protein, paired glucose, Gram stain, culture with "
                  "susceptibility and relevant PCR, with pre/post-antibiotic timing. Unrelated CSF "
                  "OCB, prion and autoimmune carry-over assays are absent."),
    dict(cond="bacterial_meningitis", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         response="Corrected after re-reading the cases: MRI is absent from the 20 uncomplicated "
                  "initial pathways, recommended only in 1 non-response/hydrocephalus case, and "
                  "required in 9 cases with an authored abscess, ventriculitis, hydrocephalus, "
                  "brainstem, shunt, skull-base or other structural-complication question."),
    dict(cond="bacterial_meningitis", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: electrocardiography is no longer part of this condition's panel and no "
                  "meningitis case orders one."),

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
         reviewer=2, tier="optional", status="applied",
         seg=(None, "Item\nBrain MRI."),
         response="Applied: HEP-ENC-M06 now uses optional abdominal Doppler through "
                  "order_body_imaging to assess the pre-existing TIPS in new post-TIPS overt HE. "
                  "The report was already authored in that case; it was attached to the wrong, "
                  "brain-oriented tool. No blanket abdominal imaging was added: the reviewers' "
                  "trigger remains recurrent/persistent or refractory HE, including a specific "
                  "shunt/TIPS question or failure to recover after 48-72 hours."),
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
         reviewer=2, tier="optional", status="applied",
         response="Applied. We had left it REQUIRED in all 30 cases and put the question back to "
                  "you; that was wrong twice over. First on the facts: the reason we gave — that we "
                  "do not drop an exclusion step before an invasive procedure — was carried over "
                  "from bacterial meningitis, and here the gold standard performs a lumbar puncture "
                  "in 1 of the 30 cases; and your meningitis annotations are on CSF, laboratory, "
                  "MRI and ECG, so the CT there was never contested. Second on method: a first "
                  "attempt assigned tiers per case from a keyword scan, which matched \"seizure\" "
                  "and \"fall\" in all 30 because those words live in the differentials and in "
                  "negated history, and missed HEP-ENC-P05, whose ataxia and ophthalmoparesis are "
                  "Wernicke encephalopathy. All 30 cases were then read in full.\n\n"
                  "Two facts from that reading: **29 of the 30 CT reports are normal** — the only "
                  "positive one is HEP-ENC-P09, a 9 mm chronic subdural with 3 mm midline shift — "
                  "and **no case has a focal deficit except that same P09**; every other "
                  "examination reads \"no focal weakness\" or \"no focal paresis\", and the "
                  "bilateral Babinski signs and asterixis present in most of them are the metabolic "
                  "picture, not focal signs.\n\n"
                  "So the tier is now **optional in 25 of the 30 cases**, as you asked. Five stay "
                  "required, on a textual rule rather than a judgement of ours — the case's own "
                  "text states the CT is mandatory, urgent or necessary, or one of your listed "
                  "triggers appears verbatim in the presentation: P09 (focal right-sided signs; "
                  "\"mandate imaging\"), P06 (\"unresponsive after a witnessed seizure\"), M10 "
                  "and S11 (\"mandatory given coagulopathy and thrombocytopenia\" — your "
                  "\"clinical suspicion of intracranial bleeding\"), and P08 (\"necessary given "
                  "repeated TIA framing\"). P08 is the one of the five that does not match your "
                  "list word for word, and we are flagging it as such. Overruling any of the five "
                  "means reading five sentences. Mandatory CT spend across the condition falls from "
                  "5520 to 920 EUR. The imaging-before-puncture rule is untouched except in "
                  "HEP-ENC-M01, the single case whose gold standard includes a puncture, where it "
                  "is softened from hard to soft so that following your guidance cannot be "
                  "penalised."),

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
         reviewer=2, tier="optional", status="applied",
         seg=("Item\nSpinal and peripheral nerve imaging", None),
         response="Applied: optional contrast spine MRI is now reachable in five cases with a "
                  "specific cord/structural alternative in their own text: post-spinal anaesthesia, "
                  "post-laminectomy, major trauma, leukaemia/infiltration and cervical sensory "
                  "level with new urinary incontinence. Fifteen hidden reports previously sat on "
                  "a brain-oriented tool; the ten generic reports were removed rather than making "
                  "spine MRI routine in GBS. The trigger remains a sensory level, extensor plantar "
                  "response, sphincter involvement, fever/structural concern at onset, or another "
                  "case-specific compressive/myelopathic alternative."),
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
         reviewer=2, tier="unchanged", status="applied",
         response="The epilepsy-oriented protocol and the indication list are applied, and MRI is "
                  "required in 17 cases and absent where the cause is already established. "
                  "MR_venography is now optional in the single pregnancy/PRES-CVST differential "
                  "case, after stabilisation and brain MRI; it is not a blanket status test."),
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
         response="Applied case by case: CSF is optional in 19 cases and recommended in 11 "
                  "equivocal or atypical cases; it is required in none. The panel now includes "
                  "the kappa free-light-chain index accepted by the 2024 criteria, and mass-effect "
                  "cases explicitly defer LP until imaging safety has been assessed."),
    dict(cond="multiple_sclerosis", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="optional", status="applied",
         response="Applied after correcting the first mechanical implementation: OCT is optional "
                  "in 8 optic-neuritis cases and VEP in 14 optic or genuinely equivocal cases, "
                  "rather than both being attached to all 30. No EMG/NCS, RNS, biopsy, autonomic "
                  "test or unrelated evoked-potential action remains."),
    dict(cond="multiple_sclerosis", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="required", status="applied",
         response="Applied: all 30 retain the required baseline mimic-exclusion panel. AQP4-IgG "
                  "and MOG-IgG are targeted to 13 optic-neuritis or atypical/tumefactive cases, "
                  "not used as a fixed universal screen."),
    dict(cond="multiple_sclerosis", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="applied",
         response="Removed end to end: no case orders EEG and no authored EEG result remains."),
    dict(cond="multiple_sclerosis", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed end to end: no case orders ECG and no authored ECG result remains."),

    # === migraine with aura (reviewer 1) ===
    dict(cond="migraine_with_aura", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="optional", status="applied",
         seg=(None, "Migraine with aura is primarily a clinical diagnosis. The true required"),
         response="Applied case by case and corrected beyond the first pass: MRI is absent in 11 "
                  "typical cases, optional in 3 and recommended in 11 red-flag presentations. It "
                  "is required in 5 strong non-routine exceptions: two documented infarcts, "
                  "MELAS with persistent deficit, familial aneurysm evaluation and a witnessed "
                  "seizure. Those scans establish or exclude the complication/alternative, not migraine."),
    dict(cond="migraine_with_aura", filed="analyze_brain_mri", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("Migraine with aura is primarily a clinical diagnosis. The true required", None),
         response="Applied and independently corrected: the structured history/examination is "
                  "required in all 30 cases and now records the actual ICHD-3 rule (at least 3 of "
                  "6 characteristics), full reversibility, attack count, aura modalities and red "
                  "flags. The first implementation incorrectly encoded a 3-of-4 rule."),
    dict(cond="migraine_with_aura", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="applied",
         response="Applied end to end: 29 of 30 cases have neither an EEG action nor an authored "
                  "EEG result. The exception is MIG-AURA-RM11, "
                  "whose diagnosis is hemiplegic migraine *with migralepsy* — a seizure during "
                  "aura, ICHD-3 1.4.4 — so the 24 h video EEG establishes half of the diagnosis "
                  "rather than being routine headache evaluation, and it stays required there. "
                  "That case is the one place to argue with us, and the place to do it is the case "
                  "itself."),
    dict(cond="migraine_with_aura", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed end to end: no migraine case orders an ECG and no authored ECG result remains."),
    dict(cond="migraine_with_aura", filed="order_echocardiogram", tool="order_echocardiogram",
         reviewer=1, tier="remove", status="applied",
         response="Applied to routine migraine evaluation. Three cases order an echocardiogram, "
                  "not about the tier. Three cases order an echocardiogram at required and none is "
                  "a routine migraine: MIG-AURA-P03 is a migrainous infarction whose diagnosis "
                  "rests on secondary causes having been excluded, MIG-AURA-P07 is a cardioembolic "
                  "PCA infarct the case explicitly distinguishes from migrainous infarction, and "
                  "MIG-AURA-P08 is genetically confirmed MELAS, where cardiomyopathy screening is "
                  "standard. In each the echocardiogram is embolic-source or cardiomyopathy "
                  "work-up, so the routine migraine echo your comment targets does not exist in "
                  "the cases. The question is one of composition, the same kind you settled for "
                  "peripheral neuropathy: should a cardioembolic stroke and a confirmed MELAS sit "
                  "under the label 'migraine with aura' at all? Nothing waits on your answer — the "
                  "cases are reviewable as they stand."),
    dict(cond="migraine_with_aura", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="remove", status="applied",
         response="Removed end to end: no migraine case orders CSF analysis and no authored CSF result remains. "
                  "The seizure exception retains EEG, but lacked a specific clinical indication for LP."),
    dict(cond="migraine_with_aura", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied: no case requires blood tests; 4 carry them as optional and 1 as "
                  "recommended, on a secondary-headache suspicion."),

    # === early Alzheimer's disease (reviewer 1) ===
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Applied at pathway level: structural imaging is required in all 30 cases. "
                  "Twenty-nine use MRI; ALZ-EARLY-RS05 uses the requested non-contrast CT "
                  "alternative because severe claustrophobia makes MRI unavailable."),
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("1) structured cognitive", "2) non-contrast"),
         src_seg=("Source:", None),
         response="Applied: a structured cognitive assessment is a required action in all 30 "
                  "cases, scored against the functional criterion, so the 10 mild-cognitive-"
                  "impairment cases are not required to have lost independence. This is one of "
                  "the four mandatory steps you named that had no tool behind them at all."),
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="order_ct_scan",
         reviewer=1, tier="optional", status="applied",
         seg=("2) non-contrast", "3) FDG-PET"),
         src_seg=("Source:", None),
         response="Applied without increasing the dataset: ALZ-EARLY-RS05 now uses non-contrast "
                  "head CT because severe claustrophobia makes MRI unavailable. The report "
                  "states CT's lower sensitivity for microbleeds, subtle vascular disease and "
                  "regional volumetry."),
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="order_advanced_imaging",
         reviewer=1, tier="optional", status="applied",
         seg=("3) FDG-PET", "Suggested diagnostic sequence"),
         src_seg=("Source:", None),
         response="Applied: all subtype studies are optional and occur only after the core "
                  "assessment. Six atypical cases use FDG-PET and one exercises the newly "
                  "priced perfusion-SPECT substitute. Amyloid PET is optional in 8 cases as "
                  "the sole biomarker route, never paired with CSF."),
    dict(cond="alzheimers_early", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="required", status="applied",
         response="Applied in all 30 cases: CBC, CMP, TSH, B12, folate, homocysteine, "
                  "magnesium, ESR and CRP are named and delivered; abnormal case-specific "
                  "values, including functional B12 deficiency, are preserved."),
    dict(cond="alzheimers_early", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="applied",
         response="Removed as routine Alzheimer testing, including the previously exposed reports. "
                  "Two optional case-level exceptions remain for questions other than diagnosing "
                  "Alzheimer disease: RP04 tests for periodic complexes because CJD is active in a "
                  "rapidly progressive dementia, and RP05 records recurrent witnessed unresponsive "
                  "spells to assess seizure. The other 28 cases expose no authored EEG result."),
    dict(cond="alzheimers_early", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed completely from the Alzheimer diagnostic pathway: no case orders one "
                  "and none exposes a case-authored ECG result."),
    dict(cond="alzheimers_early", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="optional", status="applied",
         seg=(None, "Add amyloid PET"),
         response="Applied: CSF Alzheimer biomarkers are optional in 21 cases. RP04 is the sole "
                  "required exception because the same lumbar puncture must answer the independent, "
                  "high-stakes CJD differential with RT-QuIC and 14-3-3; it has no amyloid PET."),
    dict(cond="alzheimers_early", filed="analyze_csf", tool="order_advanced_imaging",
         reviewer=1, tier="optional", status="applied",
         seg=("Add amyloid PET", None),
         response="Applied across actions, stored reports and SFT traces: 8 cases use optional "
                  "amyloid PET as their sole biomarker route, 22 use CSF, and zero cases expose or "
                  "order both. FDG-PET/perfusion SPECT remains a separate optional subtype question."),

    # === frontotemporal dementia (reviewer 1) ===
    dict(cond="ftd", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="required", status="applied",
         response="Applied in all 30 cases: the required baseline names CBC, CMP, TSH, B12, "
                  "folate, ESR and CRP. Infectious, toxic, CK, progranulin and other studies are "
                  "added only where the presentation supplies a question; genetics is not hidden "
                  "inside the blood panel."),
    dict(cond="ftd", filed="order_advanced_imaging", tool="order_advanced_imaging",
         reviewer=1, tier="optional", status="applied",
         response="Applied across actions and authored reports: no FTD case requires or recommends "
                  "advanced imaging. Twenty-nine offer optional FDG-PET and one the requested "
                  "perfusion-SPECT substitute. Amyloid PET remains optional in only 3 cases with "
                  "an active AD differential. P04 has one explicit optional DaTscan exception for "
                  "co-existing Parkinson's disease; it is not presented as an FTD test. Tau PET "
                  "and all vascular imaging modalities are absent."),
    dict(cond="ftd", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="required", status="applied",
         response="Applied: the validated neuropsychological battery is required in all 30 cases. "
                  "Genetic testing is optional in 17 young-onset or familial cases and is never "
                  "required or recommended. EMG/NCS and respiratory testing remain required only "
                  "in P08, whose diagnosis explicitly includes motor neuron disease; they are "
                  "removed from every FTD-only case. Genetics is also optional in 7 selected "
                  "young/familial Alzheimer cases."),
    dict(cond="ftd", filed="order_specialized_test", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("Validated neuropsychological testing must be REQUIRED", "Genetic testing should"),
         src_seg=("Source:", None),
         response="Applied as a separate act: a structured cognitive and behavioural assessment is "
                  "required in all 30 cases, scored against the six Rascovsky features, each "
                  "marked present only where the history describes it."),
    dict(cond="ftd", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=1, tier="optional", status="applied",
         response="Applied without adding cases: S06 uses non-contrast CT because severe "
                  "claustrophobia makes MRI unavailable. M09 separately receives acute non-contrast "
                  "CT in the emergency department before MRI because the immediate question is "
                  "haemorrhage or mass. CT angiography, carotid duplex and transcranial Doppler are "
                  "absent from every FTD case and authored report."),

    # === Parkinson's disease (reviewer 1) ===
    dict(cond="parkinsons", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied case by case: the fixed routine panel was removed. Nine of 30 cases "
                  "retain targeted optional studies for a live thyroid/tremor, Wilson, medication-"
                  "toxicity, metabolic or pretreatment question; the other 21 have no laboratory "
                  "action or authored laboratory report."),
    dict(cond="parkinsons", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="applied",
         response="Removed: no Parkinson case orders an EEG."),
    dict(cond="parkinsons", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed: no Parkinson case orders an ECG."),
    dict(cond="parkinsons", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="optional", status="applied",
         response="Applied end to end: EMG/NCS, repetitive stimulation, biopsies, evoked potentials, "
                  "formal autonomic testing and tilt-table testing are absent from actions and authored "
                  "reports. Neuropsychology remains in 11 cognitively relevant cases and is optional in "
                  "10; PD-RP04 is the documented strong exception because formal neuropsychology is a "
                  "required pre-DBS safety assessment rather than routine PD diagnosis. Polysomnography "
                  "is optional in 11 cases with reported dream enactment. Counselled PD genetics is "
                  "optional only in the 42-year-old young-onset case and one case with an affected "
                  "first-degree relative."),
    dict(cond="parkinsons", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Structural imaging remains required, but is described as exclusion of a secondary or "
                  "atypical parkinsonian syndrome rather than proof of idiopathic PD: MRI in 29 cases and "
                  "the reviewed CT alternative in one."),
    dict(cond="parkinsons", filed="analyze_brain_mri", tool="order_ct_scan",
         reviewer=1, tier="optional", status="applied",
         response="Applied without adding a case: PD-S06 uses non-contrast CT because severe "
                  "claustrophobia makes MRI unavailable; the report explicitly states CT's lower sensitivity."),

    # === amyotrophic lateral sclerosis (reviewer 1) ===
    dict(cond="als", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="required", status="applied",
         response="Applied and corrected case by case: EMG/NCS is the only ALS-specific required "
                  "specialized study in all 30. Respiratory function is recommended in all 30 as "
                  "a post-diagnostic safety/staging baseline, not diagnostic confirmation. An ALS "
                  "gene panel is separately optional/offered after counselling in all 30, consistent "
                  "with the 2023 consensus guideline; it is never embedded in routine labs or required. "
                  "No RNS, biopsy, unrelated evoked potential, autonomic or tilt action remains."),
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
         response="Applied in all 30 as a rule-out rather than confirmatory panel. CBC, CMP, "
                  "calcium, thyroid, B12/folate, CK and inflammatory markers form the baseline; "
                  "anti-GM1, paraprotein, HIV, paraneoplastic and androgen-receptor testing occur "
                  "only in the corresponding phenotype. ALS genetic results were removed from "
                  "laboratory payloads and moved to the counselled genetic-panel action."),
    dict(cond="als", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="optional", status="applied",
         response="Applied after correcting the first blanket implementation: 25 cases have no "
                  "CSF action or authored result. Five atypical cases retain optional, targeted "
                  "CSF for a specific neoplastic, demyelinating/PML, inflammatory-neuropathy, HIV "
                  "or paraprotein mimic; none uses CSF neurofilament as an ALS diagnostic test."),

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
         response="Applied after a case-level re-audit: no NPH case policy requires a standalone "
                  "neuropsychological battery or any other specialized test, and the 58 removed "
                  "specialized-test follow-ups are no longer callable in the NPH cases. The "
                  "required timed gait and brief cognitive comparison is represented by the "
                  "clinical-assessment tool instead."),
    dict(cond="nph", filed="order_specialized_test", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("If Specialized test is kept as REQUIRED", "Neuropsychological testing"),
         src_seg=("Sources:", None),
         response="Applied exactly as written: perform_clinical_assessment"
                  "{gait_and_balance_timed} is required in all 30 cases and its report carries the "
                  "before-and-after comparison, with each case's own timed-up-and-go and 10-metre "
                  "figures. The previous universal >=20% cutoff was not supported by the cited "
                  "guidelines: the cases now state the commonly used >10% TUG criterion and require "
                  "interpretation of absolute and concordant changes. NPH-P08 remains negative "
                  "because it shows no objective improvement."),
    dict(cond="nph", filed="order_advanced_imaging", tool="order_advanced_imaging",
         reviewer=1, tier="remove", status="applied",
         response="Applied: advanced imaging is absent from the NPH panel, all 30 case policies, "
                  "and the callable case follow-ups (60 PET, flow-MRI, DaTscan and other "
                  "advanced-imaging payloads removed). The previous implementation had merely "
                  "relabelled PET as optional, which did not implement a request to remove it."),

    # === temporal lobe epilepsy (reviewer 1) ===
    dict(cond="focal_epilepsy_temporal", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="required", status="applied",
         response="Applied end to end. The previous answer was false: sleep_deprived had been added "
                  "to the vocabulary but no case used it, ambulatory was absent, and 22 cases still "
                  "carried video EEG. The audited cases now contain 23 routine recordings, 5 staged "
                  "sleep-deprived studies, 2 ambulatory studies after non-diagnostic routine/sleep "
                  "recordings, and 10 video studies limited to event capture, PNES or tertiary "
                  "evaluation. RP01 is the single continuous-ICU exception because its presentation "
                  "is non-convulsive status epilepticus, exactly the acute setting you named."),
    dict(cond="focal_epilepsy_temporal", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Applied: dedicated epilepsy-protocol MRI is required in 29 cases. The MRI-negative "
                  "drug-resistant case P04 uses the reviewed non-contrast CT alternative because "
                  "severe claustrophobia makes MRI unavailable; the report states CT's limitations."),
    dict(cond="focal_epilepsy_temporal", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied case by case: 23 cases retain optional targeted tests for acute metabolic "
                  "provocation, antiseizure-drug levels or a concurrent emergency. Seven stable "
                  "tertiary/recurrent cases have no lab action or authored report. Prolactin was "
                  "removed from the routine template."),
    dict(cond="focal_epilepsy_temporal", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="optional", status="applied",
         response="Applied using NICE NG217 rather than the previous arbitrary count: ECG is required "
                  "in 21 first-suspected-seizure or transient-loss-of-consciousness assessments and "
                  "absent from the 9 established/tertiary cases. It is framed as a cardiac-mimic test, "
                  "not an epilepsy test."),
    dict(cond="focal_epilepsy_temporal", filed="order_echocardiogram", tool="order_echocardiogram",
         reviewer=1, tier="remove", status="applied",
         response="Removed from all 30 actions and authored reports. P05 already had a completed "
                  "normal cardiac work-up in its history. RP02 has a genuine separate pulmonary-"
                  "embolism emergency, but generic echo was the wrong substitute: it now orders "
                  "the required chest CT angiogram through body imaging."),
    dict(cond="focal_epilepsy_temporal", filed="order_cardiac_monitoring",
         tool="order_cardiac_monitoring", reviewer=1, tier="remove", status="applied",
         response="Removed from all 30 actions and authored reports. P05's prior Holter was already "
                  "normal, and RP02 requires urgent pulmonary vascular imaging rather than generic "
                  "rhythm monitoring."),

    # === functional neurological disorder (reviewer 1) ===
    dict(cond="functional_neurological_disorder", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier=None, status="applied",
         response="Applied as your second option for this frozen phase: "
                  "the current phase is frozen at 20 conditions and 600 cases, so authoring DLB "
                  "and retiring FND are explicitly deferred. Your fallback option has now been "
                  "applied end to end: the positive functional-sign examination is the sole required "
                  "diagnostic act in all 30 cases; every instrumental action is optional. Video-EEG "
                  "appears in 22 event-capture cases, MRI in 20 explicit red-flag/organic-comorbidity "
                  "cases and targeted labs in 12; no ECG, CSF, neuropsychology or unexecutable null "
                  "action remains. Efficient traces stop after the positive examination. "
                  "The earlier rationale for keeping FND said it was "
                  "the only way to measure diagnostic overuse; that is not true in this benchmark. "
                  "Every current condition has case-level useless-tool penalties, and 16 of the 19 "
                  "non-FND conditions also contain optional actions, so restraint and cost remain "
                  "measurable without FND. The interim FND correction exposed a real defect — the "
                  "old cases encoded diagnosis by exclusion — but it is not a strong reason to "
                  "override your composition recommendation. FND therefore remains a temporary "
                  "member of the frozen dataset, not the final composition choice; DLB is the "
                  "first replacement in the backlog."),
]

SPEC += [
    # === anti-NMDA receptor encephalitis (reviewer 2) ===
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_brain_mri",
         tool="order_body_imaging", reviewer=2, tier="required", status="applied",
         seg=(None, "Item:\nBrain MRI"),
         response="Applied after correcting the first over-broad implementation. Tumour screening "
                  "is required in all 30 cases but not as blanket CAP CT: all 23 women receive "
                  "pelvic/abdominal ultrasound, 4 younger men receive targeted testicular "
                  "ultrasound, and 3 older men with an oncologic context receive CAP CT. Existing "
                  "pelvic/testicular reports were moved out of the laboratory payload."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_brain_mri",
         tool="analyze_brain_mri", reviewer=2, tier="unchanged", status="applied",
         seg=("Item:\nBrain MRI", None),
         response="Applied: the MRI stays required in all 30 cases and its role in the ground "
                  "truth is exclusion of alternatives, not confirmation."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied in all 30 cases: CBC, metabolic/coagulation, thyroid function and "
                  "antibodies, inflammatory markers, autoimmune/paraneoplastic antibodies and a "
                  "separately priced serum IgG anti-GluN1 cell-based assay are named. Serum is "
                  "explicitly read with CSF, never alone; there are no paediatric cases requiring "
                  "selected genetic/metabolic testing."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied in all 30 cases: basic CSF, OCB/IgG index, HSV PCR and the CSF "
                  "anti-GluN1 assay are one reachable required order. Six initially unreachable "
                  "or pending antibody results were reconciled with the authored confirmatory "
                  "reports; the seronegative case remains negative rather than being forced positive."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: a routine EEG is required in all 30 cases and explicitly assesses "
                  "extreme delta brush without calling it pathognomonic. Continuous ICU EEG is a "
                  "recommended escalation in the 13 cases with severe encephalopathy or "
                  "electrographic seizures, rather than a blanket order in all 30."),
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
