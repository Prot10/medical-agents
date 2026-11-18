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
         response="Applied: TCD is optional in all 30 cases, as an admission baseline, and is the "
                  "sole routine advanced surveillance modality. PET, DaTscan, MIBG, "
                  "perfusion/spectroscopy MRI and carotid duplex are scored as waste; MRA is waste "
                  "after the CTA, except in the patient with a prior contrast rash, and an MRA "
                  "order now returns a report that matches the case. Since the October 2026 "
                  "review catheter DSA with 3D rotational angiography is in all 30 cases, after "
                  "the CTA and before securing: recommended in the 29 aneurysmal cases, where the "
                  "CTA has already shown the aneurysm, and required in the perimesencephalic "
                  "case, where it is the study that excludes one. Every DSA report is diagnostic "
                  "only (anatomy, neck, dome-to-neck ratio, branches), never a treatment result; "
                  "catheter DSA is not a duplicate CTA/MRA."),
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
         response="Applied: all 30 cases have an explicitly discriminated first-line NCCT, and 29 a "
                  "separate subsequent CTA, as 59 required actions; in the pregnant ISCH-STR-RP02 "
                  "an MRI with MR angiography replaces the CTA. CTA is never represented as a "
                  "substitute for NCCT and its call text states that creatinine must not delay it."),
    dict(cond="ischemic_stroke", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="optional", status="applied",
         response="Applied: no case requires EEG. One case retains it as optional for a witnessed "
                  "tonic-hand seizure-mimic question; the other 29 have no EEG action or authored "
                  "output, and every trace states that EEG must not delay reperfusion."),
    dict(cond="ischemic_stroke", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="optional", status="applied",
         seg=(None, "NEW ITEM OPTIONAL"),
         response="Applied: brain MRI is optional in 23 cases. It is recommended in 6 where it "
                  "answers a question the CT cannot (fat-saturated T1 for dissection in M04, P01, "
                  "RM03 and RM04, DWI in RM02, small vessel disease in RP05) and required in 1, "
                  "RP02, where it replaces the CTA in pregnancy."),
    dict(cond="ischemic_stroke", filed="analyze_brain_mri", tool="order_advanced_imaging",
         reviewer=2, tier="optional", status="applied",
         seg=("NEW ITEM OPTIONAL", None),
         response="Applied end to end rather than only adding vocabulary: CT_perfusion is reachable "
                  "in the 5 wake-up/extended-window cases where an authored core/penumbra report "
                  "changes selection, recommended in 4 and required in 1 (P04, where it selects "
                  "thrombectomy at 8 hours). Four reports formerly misrouted through ordinary head "
                  "CT were audited; three routine-window/non-selection uses were removed. Blanket "
                  "MRA, TCD and carotid-duplex duplication is also removed: the only separate "
                  "vascular study left is an optional MRA in RP02, if it was not acquired with "
                  "the brain MRI."),
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
                  "cases; EDTA whole-blood meningococcal PCR is recommended in BACT-MEN-S05, whose "
                  "lumbar puncture is deferred, and an ulcer swab in RS01. Every action and trajectory states collection before antimicrobials when "
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
                  "susceptibility and relevant PCR, with pre/post-antibiotic timing. The LP is "
                  "required in 29 cases; in 1, BACT-MEN-S05 (rapidly spreading purpura with an "
                  "uncorrected coagulopathy), it is optional and deferred (NICE NG240; WHO 2025), "
                  "and blood cultures and blood PCR carry the organism. Unrelated CSF OCB, prion "
                  "and autoimmune carry-over assays are absent."),
    dict(cond="bacterial_meningitis", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         response="Corrected after re-reading the cases: MRI is absent from the 18 uncomplicated "
                  "initial pathways, recommended in 2 (hydrocephalus in advanced HIV; "
                  "complications in an immunosuppressed patient), and required in 10 cases with an "
                  "authored abscess, ventriculitis, hydrocephalus, brainstem, shunt, skull-base or "
                  "other structural-complication question."),
    dict(cond="bacterial_meningitis", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: electrocardiography is no longer part of this condition's panel and no "
                  "meningitis case orders one."),

    # === hepatic encephalopathy (reviewer 2) ===
    dict(cond="hepatic_encephalopathy", filed="interpret_labs", tool="order_microbiology",
         reviewer=2, tier="required", status="applied",
         seg=(None, "Item\nLaboratory studies."),
         response="Applied, and tiered case by case in the October 2026 review: blood and urine "
                  "cultures are required in the 12 cases with a suspected infection and "
                  "recommended in 16 as a screen for an occult precipitant (afebrile, normal white "
                  "cell count, no focal source; EASL 2022); in the covert-HE case P07 both are "
                  "optional, and P08 has optional blood cultures only. Diagnostic paracentesis is "
                  "required in the 21 with ascites, and C. difficile stool testing is recommended "
                  "in 2. Before this there was no tool able to sample anything outside the CNS."),
    dict(cond="hepatic_encephalopathy", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         seg=("Item\nLaboratory studies.", None),
         response="Applied: ammonia, electrolytes, renal and liver function, CRP, TSH and zinc "
                  "are named; autoimmune, paraneoplastic and genetic panels are out."),
    dict(cond="hepatic_encephalopathy", filed="analyze_brain_mri", tool="order_body_imaging",
         reviewer=2, tier="optional", status="applied",
         seg=(None, "Item\nBrain MRI."),
         response="Applied: HEP-ENC-M06 now uses abdominal Doppler through order_body_imaging, "
                  "required since the October 2026 review, to assess the pre-existing TIPS in new "
                  "post-TIPS overt HE. The report was already authored in that case; it was "
                  "attached to the wrong, brain-oriented tool. Abdominal ultrasound is also "
                  "required in S05 (obstruction, collection, portal vein) and contrast abdominal "
                  "imaging of the splenorenal shunt recommended in P08; a chest radiograph is "
                  "recommended in 4 cases as part of the infection screen. No blanket abdominal imaging was added: the reviewers' "
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
         response="Applied: EEG is recommended in 24 cases and absent in 5. It is required in 1, "
                  "HEP-ENC-P06, unresponsive after a witnessed seizure, where non-convulsive status "
                  "must be excluded."),
    dict(cond="hepatic_encephalopathy", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=2, tier="optional", status="applied",
         response="Applied. We had left it REQUIRED in all 30 cases and put the question back to "
                  "you; that was wrong twice over. First on the facts: the reason we gave — that we "
                  "do not drop an exclusion step before an invasive procedure — was carried over "
                  "from bacterial meningitis, and here no gold standard performs a lumbar puncture "
                  "(the one in HEP-ENC-M01 was removed in the October 2026 review); and your meningitis annotations are on CSF, laboratory, "
                  "MRI and ECG, so the CT there was never contested. Second on method: a first "
                  "attempt assigned tiers per case from a keyword scan, which matched \"seizure\" "
                  "and \"fall\" in all 30 because those words live in the differentials and in "
                  "negated history, and missed HEP-ENC-P05, whose ataxia and ophthalmoparesis are "
                  "Wernicke encephalopathy. All 30 cases were then read in full.\n\n"
                  "Two facts from that reading: **28 of the 30 CT reports show no acute "
                  "abnormality** — the exceptions are HEP-ENC-P09, a 9 mm chronic subdural with 3 "
                  "mm midline shift, and P04, bilateral symmetric putaminal hypodensity — and **no "
                  "case has a lateralised deficit except that same P09**; every other "
                  "examination reads \"no focal weakness\" or \"no focal paresis\", and the "
                  "bilateral Babinski signs and asterixis present in most of them are the metabolic "
                  "picture, not focal signs.\n\n"
                  "So the tier is now **optional in 24 of the 30 cases**, as you asked. Six stay "
                  "required, on a textual rule rather than a judgement of ours — the case's own "
                  "text states the CT is mandatory, urgent or necessary, or one of your listed "
                  "triggers appears in the presentation: P09 (focal right-sided signs; "
                  "\"mandate imaging\"), P06 (\"unresponsive after a witnessed seizure\"), M10 "
                  "and S11 (\"mandatory given coagulopathy and thrombocytopenia\" — your "
                  "\"clinical suspicion of intracranial bleeding\"), S06 (found down in coma "
                  "with nobody to exclude a fall, INR 3.4 and platelets 48: possible head trauma, "
                  "added in the October 2026 review), and P08 (\"necessary given repeated TIA "
                  "framing\"). P08 is the one of the six that does not match your list word for "
                  "word, and we are flagging it as such. Overruling any of the six means reading "
                  "six sentences. Mandatory CT spend across the condition falls from 5520 to 1104 "
                  "EUR. No case now has an imaging-before-puncture rule: HEP-ENC-M01, the single "
                  "case whose gold standard included a puncture, lost the puncture in the October "
                  "2026 review."),

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
                  "also found a cervical-cord glioblastoma being imaged by a brain MRI. Since the "
                  "November 2026 round every case stores the plain MRI and the gadolinium study as "
                  "separate reports, and the required MRI in all 30 orders the gadolinium tumour "
                  "protocol, so a report describing enhancement no longer appears under a "
                  "\"contrast used: none\" header."),
    dict(cond="brain_tumor_glioma", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="unchanged", status="applied",
         seg=(None, "Item\nAdvanced imaging"),
         response="Applied: no case requires EEG for the tumour itself."),
    dict(cond="brain_tumor_glioma", filed="analyze_eeg", tool="order_advanced_imaging",
         reviewer=2, tier="optional", status="applied",
         seg=("Item\nAdvanced imaging", None),
         response="Applied: amino_acid_PET was added with the tracers EANO names, and perfusion "
                  "MRI plus MR spectroscopy are recommended actions in 29 of the 30 cases. In the "
                  "intramedullary cervical glioblastoma (GLIO-HG-RM02) both are optional, because "
                  "spinal cord perfusion and spectroscopy are not validated for grading. FDG-PET is "
                  "not among them, per your note. Since the November 2026 round functional MRI is "
                  "also recommended in S05, where the hand motor area lies about 9 mm from the "
                  "enhancing margin in a patient with right-sided weakness, so motor mapping plans "
                  "the resection margin (EANO 2021)."),
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
         response="Applied: contrast spine MRI is reachable in eight cases, each with a specific "
                  "cord or structural alternative in its own text, and is never routine in GBS. It "
                  "is recommended in six (post-laminectomy pain and weakness, quadriparesis after a "
                  "fall, a cervical sensory level with urinary incontinence, an apparent thoracic "
                  "sensory level, urinary retention at onset with metastatic cancer, and known "
                  "cervical stenosis with asymmetric hand symptoms) and optional in two, where the "
                  "red flag is weak (recent spinal anaesthesia; leukaemia with negative CSF "
                  "cytology). Fifteen hidden reports previously sat on a brain-oriented tool; the "
                  "generic ones were removed. The trigger remains a sensory level, extensor "
                  "plantar response, sphincter involvement, fever or a structural concern at onset, "
                  "or another case-specific compressive or myelopathic alternative."),
    dict(cond="guillain_barre", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: required in 29 cases and recommended in one, where the puncture has "
                  "to wait for an interval after apixaban in a patient on dual antiplatelet therapy "
                  "after a coronary stent; 14-3-3/RT-QuIC are gone from this condition."),
    dict(cond="guillain_barre", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied. The anti-GQ1b point also caught a routing defect elsewhere: a "
                  "myasthenia case was being served a Miller-Fisher ganglioside panel because the "
                  "matcher treated the token 'anti' as identifying an antibody."),
    dict(cond="guillain_barre", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: brain MRI is waste wherever nothing in the case raises a central "
                  "question, and is a criterion in 8 cases that do: recommended in seven (Miller "
                  "Fisher syndrome and an anti-GQ1b ptosis case against a brainstem lesion, two "
                  "pharyngeal-cervical-brachial cases, bifacial weakness, a wake-up asymmetric "
                  "deficit in atrial fibrillation, and ophthalmoplegia with nystagmus and a "
                  "cervicomedullary signal) and required in one with fever, neck stiffness and "
                  "encephalopathy at onset. The October 2026 review round added these after the "
                  "physician notes on unexcluded mimics. The sweep this comment started moved 63 "
                  "spine studies out of the brain-MRI tool across the whole dataset."),
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
         response="Applied, and revised in the November 2026 round. Repetitive nerve stimulation "
                  "now follows ABN 2025: neurophysiology is mandatory when the antibodies are "
                  "negative, while with unequivocal AChR or MuSK antibodies the diagnosis is "
                  "serological and RNS is good practice that changes neither the diagnosis nor "
                  "management. RNS is therefore recommended in the 18 seropositive new diagnoses "
                  "(in the 2 ocular cases, RS11 and S05, as RNS or single-fibre EMG) and required "
                  "in 9: the 3 seronegative or LRP4 cases (P01, P04, RP14), the 2 Lambert-Eaton "
                  "cases (P02, RM13) and 4 where the nerve conduction or needle study answers a "
                  "named alternative (a low-positive AChR titre with a possible Sjogren neuropathy "
                  "in M02, a GBS relapse in RM12, bulbar-onset ALS in RP12, neck extensor myopathy "
                  "or ALS behind the head drop in RS16). This reverses the October 2026 tier, which "
                  "required it in 27 cases. The three known-myasthenia exacerbation or crisis cases "
                  "(M04, RM14, RM15) list it as waste, since it delays treatment. Single-fibre EMG "
                  "is ordered in 26 cases: required in the 3 seronegative or LRP4 cases, "
                  "recommended in 5 (M02 and RM11, where RNS is equivocal or borderline, RS14, a "
                  "MuSK-positive case where a limb study may be normal, and the 2 ocular cases as "
                  "the RNS alternative), and optional in 18 where serology or RNS is already "
                  "diagnostic. It is waste in the 3 crisis cases and in P02, where RNS with "
                  "positive VGCC antibodies has already made the diagnosis. emg_single_fiber "
                  "already existed and was one of the values the stale catalog hid from you."),
    dict(cond="myasthenia_gravis", filed="order_specialized_test", tool="order_body_imaging",
         reviewer=2, tier="required", status="applied",
         seg=("Item\nMediastinal (thymic) imaging", None),
         response="Applied: thymic imaging (mediastinum_CT with contrast, chest CT or mediastinal "
                  "MRI accepted) is a required action in every new diagnosis, 27 cases, including "
                  "the two Lambert-Eaton cases, whose required tumour search is a chest CT that a "
                  "mediastinal CT also satisfies. It is optional in the three known-myasthenia "
                  "exacerbation or crisis cases, whose histories document earlier thymic imaging "
                  "or a thymectomy and whose deterioration has an explained precipitant. Before "
                  "order_body_imaging existed the agent could image only the brain, so the thymus "
                  "was unreachable."),
    dict(cond="myasthenia_gravis", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: no case orders a brain MRI as a first-line study. It is an action "
                  "in 6 cases, each for a question the case itself raises: required in one (P03, "
                  "new ptosis and diplopia in multiple sclerosis on natalizumab, with gadolinium, "
                  "to exclude a relapse and PML), recommended in one (RS14, a MuSK-positive bulbar "
                  "case with PSP-like signs, raised from optional in the November 2026 round), and "
                  "optional in 4: small-cell lung cancer staging in a Lambert-Eaton case (P02), a "
                  "stroke question with antiphospholipid syndrome (RP14), a brainstem small-vessel "
                  "differential (RS12) and, as brain or cervical spine MRI, a cervical myelopathy "
                  "behind a head drop (RS16). The last three were added in the November 2026 round "
                  "as optional criteria for scans the cases already stored, rather than as waste "
                  "labels. A brain MRI is waste in 20 cases where "
                  "nothing raises a central question."),
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
         response="Applied: a transthoracic echocardiogram is required in all 30 cases. In "
                  "SYNC-CARD-P03, a Brugada syndrome, it was recommended until your November 2026 "
                  "note: the type 1 pattern there is fever-induced, and an induced pattern needs "
                  "no other heart disease before Brugada syndrome is diagnosed (ESC 2022), so the "
                  "echocardiogram that excludes structural disease is now required. Exercise "
                  "echocardiography was added as its own study (exercise_echo, priced) because one "
                  "case had been modelling a provoked outflow gradient as a treadmill stress test, "
                  "a different study at a different price. It is required in 2 cases, as the "
                  "provoked gradient in the hypertrophic cardiomyopathy (P02) and as an accepted "
                  "alternative to the exercise test in CPVT (RP03), and recommended in 4 as the "
                  "same alternative: the November 2026 round added a recommended exercise test for "
                  "syncope on exertion with intermittent AV block (M01, M02, RM03) and accepts the "
                  "exercise echo for it there and in the exercise-induced ventricular tachycardia "
                  "of P01."),
    dict(cond="syncope_cardiac", filed="order_echocardiogram", tool="order_advanced_imaging",
         reviewer=2, tier="optional", status="applied",
         seg=("Item\nAdvanced cardiac imaging", None),
         response="Applied. Half of this was already satisfied — cardiac MRI existed — and the "
                  "rest was added and priced: coronary CTA, coronary angiography, cardiac FDG-PET, "
                  "chest CT angiography. After the October 2026 round cardiac MRI is in 21 of 30 "
                  "cases: required in 4 (the two arrhythmogenic cardiomyopathies, the hypertrophic "
                  "cardiomyopathy and the right ventricular outflow mass), recommended in 8 (mostly "
                  "AV block before 60 without a clear cause, ESC 2021 pacing IIa) and optional in 9; "
                  "cardiac FDG-PET is required in the one sarcoid case. Coronary CTA or angiography is "
                  "recommended only where ischaemia is a real question (P01, and since the November "
                  "2026 round RM03 and RS05), and is waste or, with an eGFR of 27, harm where "
                  "nothing points to ischaemia. Your prediction that "
                  "offering brain MRI and no cardiac imaging is 'the arrangement most likely to "
                  "produce the wrong imaging choice' was already true in the data: one case was "
                  "requesting a CT pulmonary angiogram through the head-CT tool."),
    dict(cond="syncope_cardiac", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="optional", status="applied",
         response="Applied, and the numbers were worse than the comment assumed: TSH was in the "
                  "required panel of 29 of 30 cases and BNP of 27. After the October 2026 round "
                  "the step is required in 10 cases and recommended in 20, and a required panel "
                  "names only the assay that changes management: electrolytes and magnesium where "
                  "an arrhythmia or the QT may be electrolyte driven, ESR, CRP and ASO in the "
                  "rheumatic case, troponin, BNP and beta-hCG in the pulmonary embolism, the "
                  "paraneoplastic panel in the anti-Hu case, calcium in the sarcoid case. TSH is "
                  "named in one case (sick sinus syndrome, recommended) and BNP in one. The hard "
                  "sequence rule requiring labs before monitoring is gone from every case, or an "
                  "agent that correctly skipped the panel took a violation."),
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
         response="The epilepsy-oriented protocol and the indication list are applied: MRI is "
                  "required in 14 cases (new-onset, unexplained or refractory status, or "
                  "suspected encephalitis, autoimmune disease or tumour), recommended in 6 and "
                  "optional in 7, mostly where the cause is already established, and absent in the 3 "
                  "toxic cases (organophosphate, isoniazid, tricyclic). "
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
         response="Applied case by case: CSF (oligoclonal bands or the kappa free-light-chain "
                  "index accepted by the 2024 criteria, with paired serum) is optional in 20 cases "
                  "and recommended in 8 (the three migraine-lesion puzzles, three tumefactive "
                  "cases for cytology and flow cytometry, and the two patients over 50 with "
                  "vascular risk); it is required in none. In the two tumefactive cases with "
                  "midline shift or a posterior fossa mass, lumbar puncture is a contraindicated "
                  "action, and every CSF criterion follows the brain MRI."),
    dict(cond="multiple_sclerosis", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="optional", status="applied",
         response="Applied after correcting the first mechanical implementation: OCT is optional "
                  "in 14 cases with current or earlier optic neuritis and VEP in 18 cases where "
                  "the optic nerve counts as a region or a documented optic neuropathy needs a "
                  "result, rather than both being attached to all 30; neither is required or "
                  "recommended. Acute optic neuritis shows no OCT thinning in the first weeks. No "
                  "EMG/NCS, RNS, autonomic test or unrelated evoked-potential action remains."),
    dict(cond="multiple_sclerosis", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="required", status="applied",
         response="Applied: all 30 retain the required baseline mimic-exclusion panel (CBC, B12, "
                  "thyroid, HIV). AQP4-IgG and MOG-IgG by cell-based assay are a separate order "
                  "in 25 cases, not a universal screen: required in 8 with a red flag (severe "
                  "optic neuritis, tumefactive lesion, onset at 50 or later), recommended in 7 with "
                  "a feature suggestive of NMOSD or MOGAD (optic neuritis and myelitis in one attack, "
                  "optic disc swelling, painful tonic spasms) and optional in 10 typical "
                  "presentations; 5 cases have no criterion. The November 2026 round made the test "
                  "targeted: before, it was recommended whenever optic neuritis or myelitis was in "
                  "the history (17 cases). Their results are returned only to an "
                  "order that names the assay, not to the first-line panel."),
    dict(cond="multiple_sclerosis", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="applied",
         response="Removed as a diagnostic step: no case has an EEG criterion, and EEG is a "
                  "wasteful action in 28 cases. In the two cases where an EEG is clinically "
                  "reasonable (a first seizure with a tumefactive lesion, and post-operative "
                  "coma) it is neither scored nor penalised, and their EEG report fits the case."),
    dict(cond="multiple_sclerosis", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed as a diagnostic step: no case has an ECG criterion. An agent that "
                  "orders one receives a baseline tracing consistent with the patient (normal, or "
                  "borderline voltage LVH in the hypertensive patient); it is penalised as waste "
                  "in one case."),

    # === migraine with aura (reviewer 1) ===
    dict(cond="migraine_with_aura", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="optional", status="applied",
         seg=(None, "Migraine with aura is primarily a clinical diagnosis. The true required"),
         response="Applied case by case and corrected beyond the first pass: MRI is absent in 11 "
                  "typical cases, optional in 2 and recommended in 8 red-flag presentations. It "
                  "is required in 9 non-routine exceptions: a first aphasic aura at 52 (P01), an "
                  "aphasic aura with atrial fibrillation, where silent infarcts would change the "
                  "anticoagulation decision (P02), two documented infarcts (P03, P07), a family "
                  "history of CADASIL (P04), MELAS with persistent deficit (P08), familial aneurysm "
                  "evaluation (P09), a witnessed seizure (RM11) and sporadic hemiplegic migraine "
                  "with impaired consciousness (RS11). P02, P04 and RS11 moved from recommended to "
                  "required in the November 2026 round. Those scans establish or exclude the "
                  "complication or alternative, not migraine. Vessel imaging is its own study and "
                  "no brain MRI report describes vessels. MR angiography appears in 12 cases: "
                  "required in 5 (P01, P03, P07, P09 and RM11, where CT angiography is accepted in "
                  "the 3-hour emergency presentation), recommended in 4, and optional in 3 (M01, "
                  "M05 and P05, as MRA or carotid duplex), because a normal MRI excludes infarction "
                  "but not TIA, as your November 2026 notes asked. P01's MRA and RM11's arterial "
                  "imaging became required in that round. MR venography appears in 1 case (the "
                  "seizure case, on a combined pill)."),
    dict(cond="migraine_with_aura", filed="analyze_brain_mri", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("Migraine with aura is primarily a clinical diagnosis. The true required", None),
         response="Applied and independently corrected: the structured history/examination is "
                  "required in all 30 cases and now records the actual ICHD-3 rule (at least 3 of "
                  "6 characteristics), full reversibility, attack count, aura modalities and red "
                  "flags. The first implementation incorrectly encoded a 3-of-4 rule."),
    dict(cond="migraine_with_aura", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="applied",
         response="Applied end to end: 28 of 30 cases have no EEG action, and an EEG ordered in "
                  "them is answered with a normal report. There are two exceptions. "
                  "MIG-AURA-RM11's diagnosis is probable sporadic hemiplegic migraine with "
                  "suspected migraine aura-triggered seizures (a seizure during aura, ICHD-3 "
                  "1.4.4), so the EEG (video preferred, routine accepted) answers half of the "
                  "diagnosis rather than being routine headache evaluation, and it stays required "
                  "there. In MIG-AURA-P08, genetically confirmed MELAS, still slightly slow to "
                  "respond 10 days after a stroke-like episode with confusion, an EEG (routine, "
                  "ambulatory or video) is recommended since the November 2026 round, as an early "
                  "investigation of a stroke-like episode, not as headache work-up. Those two cases "
                  "are the places to argue with us, and the place to do it is the case itself."),
    dict(cond="migraine_with_aura", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Applied to migraine evaluation: 28 of 30 cases have no ECG action, and neither "
                  "exception is headache work-up. In MIG-AURA-P08, genetically confirmed MELAS, an "
                  "ECG is recommended (not required) to screen for pre-excitation and conduction "
                  "disease, part of the Mitochondrial Medicine Society care standards. In "
                  "MIG-AURA-RS11 the second attack included a period of unresponsiveness, so a "
                  "12-lead ECG is required since the November 2026 round: NICE CG109 asks for one "
                  "in everyone with transient loss of consciousness."),
    dict(cond="migraine_with_aura", filed="order_echocardiogram", tool="order_echocardiogram",
         reviewer=1, tier="remove", status="applied",
         response="Applied to routine migraine evaluation. Three cases order an echocardiogram, "
                  "all at required, and none is a routine migraine: MIG-AURA-P03 is a migrainous infarction whose diagnosis "
                  "rests on secondary causes having been excluded, MIG-AURA-P07 is a probably cardioembolic "
                  "PCA infarct the case explicitly distinguishes from migrainous infarction, and "
                  "MIG-AURA-P08 is genetically confirmed MELAS, where cardiomyopathy screening is "
                  "standard. In each the echocardiogram is embolic-source or cardiomyopathy "
                  "work-up, so the routine migraine echo your comment targets does not exist in "
                  "the cases. On composition we decided (24 October 2026) to keep the cardioembolic "
                  "stroke, CADASIL and MELAS cases under this condition as mimic cases with their own "
                  "labels and codes, as other conditions do: each tests not calling migraine with "
                  "aura when the work-up shows another cause. Tell us if you would rather see them "
                  "moved."),
    dict(cond="migraine_with_aura", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="remove", status="applied",
         response="Removed end to end: no migraine case has a CSF analysis action, and a CSF order "
                  "is answered with a normal stored report. The seizure exception retains EEG, but "
                  "lacked a specific clinical indication for LP. Since the November 2026 round a "
                  "lumbar puncture is no longer scored as waste in MIG-AURA-RS11: ICHD-3 notes that "
                  "an LP may be needed in sporadic hemiplegic migraine to exclude HaNDL, which is now "
                  "in that case's differential."),
    dict(cond="migraine_with_aura", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied: no case requires routine blood tests. Five carry a targeted panel as "
                  "recommended (ESR and CRP in a first aura after 50, antiphospholipid antibodies "
                  "in the two infarct cases, lactate in the hemiplegic migraine and MELAS cases). "
                  "Two laboratory orders are required, and neither is routine: MIG-AURA-P08's "
                  "m.3243A>G test, which can be requested as a laboratory panel or as a genetic "
                  "test and confirms MELAS, and, since your November 2026 note, today's INR and "
                  "blood count in MIG-AURA-P05, a patient on warfarin with an above-range INR and "
                  "gum and nose bleeding."),

    # === early Alzheimer's disease (reviewer 1) ===
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Applied at pathway level: structural imaging is required in all 30 cases. "
                  "Twenty-nine use MRI; ALZ-EARLY-RS05 uses the requested non-contrast CT "
                  "alternative because severe claustrophobia makes MRI unavailable. The MRI criterion "
                  "is a non-contrast dementia protocol; only RS06 adds an optional gadolinium study, "
                  "since the November 2026 round, to characterize the incidental extra-axial lesion "
                  "its non-contrast study shows."),
    dict(cond="alzheimers_early", filed="analyze_brain_mri", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("1) structured cognitive", "2) non-contrast"),
         src_seg=("Source:", None),
         response="Applied: a structured cognitive assessment is a required action in all 30 "
                  "cases, scored against the functional criterion, so the 6 mild-cognitive-"
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
                  "assessment. Since the November 2026 round FDG-PET is a conditional test for a "
                  "subtype question that would change management: the optional FDG-PET step remains "
                  "only in P03, a frontal-variant presentation with a paternal behavioural dementia, "
                  "where behavioural-variant FTD is the suspected alternative, and it accepts "
                  "perfusion SPECT as the substitute. It was removed from P01, P02, RM04, RP01, RP02 "
                  "and RP03, where the syndrome, the MRI and the amyloid biomarkers settle the "
                  "diagnosis, and FDG-PET is waste in the 22 amnestic cases with conclusive amyloid "
                  "biomarkers. Perfusion SPECT is waste in the other 29 cases, because it substitutes "
                  "for FDG-PET only where FDG-PET is unavailable. Every case still authors its own "
                  "FDG-PET report, so an unanticipated order never returns a library normal scan. "
                  "Amyloid PET is an alternative to CSF within one optional amyloid-status step in "
                  "29 cases (one conclusive test is enough)."),
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
                  "spells to assess seizure. In the other 28 cases EEG is no criterion; an "
                  "unindicated order returns a normal report."),
    dict(cond="alzheimers_early", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Removed from the Alzheimer diagnostic pathway: no case requires or recommends "
                  "an ECG. Two cases (P04, RP02) carry an optional baseline ECG before donepezil "
                  "because the patient takes escitalopram (QT prolongation); elsewhere an ECG is "
                  "an avoided or unscored step and returns a normal report."),
    dict(cond="alzheimers_early", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="optional", status="applied",
         seg=(None, "Add amyloid PET"),
         response="Applied: CSF Alzheimer biomarkers are optional in 29 cases, as one of two "
                  "alternatives (with amyloid PET) of a single amyloid-status step. RP04 is the sole "
                  "required exception because the same lumbar puncture must answer the independent, "
                  "high-stakes CJD differential with RT-QuIC and 14-3-3; there amyloid PET is not a "
                  "criterion, and since the November 2026 round ordering it is waste, because the "
                  "lumbar puncture already establishes amyloid status."),
    dict(cond="alzheimers_early", filed="analyze_csf", tool="order_advanced_imaging",
         reviewer=1, tier="optional", status="applied",
         seg=("Add amyloid PET", None),
         response="Applied, following your ruling that PET is an alternative to CSF: in 29 cases "
                  "one optional amyloid-status step accepts either CSF biomarkers or amyloid PET, "
                  "one conclusive test is enough, and both return a concordant case-authored "
                  "result. A second amyloid test is not required, and since the November 2026 round "
                  "it counts as an unjustified extra action once the required work-up is done, except "
                  "in M01 and M03, where a borderline CSF result leaves room for the other test. "
                  "FDG-PET (or perfusion SPECT in its place) remains a separate subtype question, "
                  "credited only in P03."),

    # === frontotemporal dementia (reviewer 1) ===
    dict(cond="ftd", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="required", status="applied",
         response="Applied in all 30 cases: the required baseline names CBC, CMP, TSH, B12, "
                  "folate, ESR and CRP. Infectious, toxic, CK, progranulin and other studies are "
                  "added only where the presentation supplies a question; genetics is not hidden "
                  "inside the blood panel. Lithium (M05) and valproate with ammonia (P01) are "
                  "checked as blood levels, not as drug-interaction checks."),
    dict(cond="ftd", filed="order_advanced_imaging", tool="order_advanced_imaging",
         reviewer=1, tier="optional", status="confirm",
         response="Applied with one departure we ask you to rule on. No FTD case requires advanced "
                  "imaging. FDG-PET, with perfusion SPECT accepted as the alternative, is optional "
                  "in 26 cases and recommended in 4 (P01, P02, P05, P07): their MRI is normal or "
                  "equivocal, so without functional imaging they meet only possible bvFTD although "
                  "the clinical picture is probable. Recommended is credited, never required. If "
                  "you would rather keep it optional there, tell us and those cases will be "
                  "relabelled possible bvFTD. Every case authors concordant FDG-PET and SPECT "
                  "results. Amyloid PET, with CSF AD markers as the alternative, is optional in 4 "
                  "cases with an active AD differential. No FTD case credits a DaTscan: the optional "
                  "DaTscan in P04 was removed in the November 2026 round, so ordering one is now waste "
                  "in all 30 cases; in P04 because the parkinsonism is clinically established and levodopa-responsive "
                  "and the scan cannot separate Parkinson's disease from FTD-associated "
                  "parkinsonism. Tau PET and all vascular imaging modalities are absent."),
    dict(cond="ftd", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="required", status="applied",
         response="Applied: the validated neuropsychological battery is required in all 30 cases. "
                  "Genetic testing (C9orf72, GRN, MAPT) is optional in 27 cases, every bvFTD case "
                  "with onset before 65 except the known GRN carrier, and is never required or "
                  "recommended; genetic counselling is a must only with onset before 55, a "
                  "suggestive family history or motor neuron disease. In P08, whose diagnosis "
                  "includes motor neuron disease, EMG/NCS is required and respiratory testing is "
                  "recommended as staging; both are absent from every FTD-only case. The two "
                  "primary progressive aphasia cases (S11, S12) recommend a speech and language "
                  "evaluation. Since the November 2026 round an ALS gene panel is waste in the 7 "
                  "cases with no sign of motor neuron disease that store one, because the FTD panel "
                  "already tests C9orf72. It is accepted as an alternative within the optional "
                  "genetics step in M02, whose brother died of ALS, and in P08. Genetics is also optional in 7 "
                  "selected young/familial Alzheimer cases."),
    dict(cond="ftd", filed="order_specialized_test", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("Validated neuropsychological testing must be REQUIRED", "Genetic testing should"),
         src_seg=("Source:", None),
         response="Applied as a separate act: a structured cognitive and behavioural assessment is "
                  "required in all 30 cases, scored against the six Rascovsky features in the 28 "
                  "behavioural-variant cases and against the Gorno-Tempini features in the 2 "
                  "primary progressive aphasia cases, each feature marked present only where the "
                  "history describes it. The bedside screen scores are part of this result, not "
                  "of the examination."),
    dict(cond="ftd", filed="order_ct_scan", tool="order_ct_scan",
         reviewer=1, tier="optional", status="applied",
         response="Applied without adding cases: S06 uses non-contrast CT because severe "
                  "claustrophobia makes MRI unavailable. In M09 an emergency-department non-contrast "
                  "CT is optional, acceptable but not required: it was required until the November "
                  "2026 round, but nothing in the history (no trauma, headache, focal sign, fever or "
                  "sudden change) calls for an emergency scan, and MRI remains the required study. "
                  "CT angiography, carotid duplex and transcranial Doppler are "
                  "absent from every FTD case and authored report."),

    # === Parkinson's disease (reviewer 1) ===
    dict(cond="parkinsons", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied case by case: the fixed routine panel was removed. Nine of 30 cases "
                  "keep a targeted laboratory study for a question the case raises: required only "
                  "in RM05 (thyroid function on levothyroxine, with new slowing and a TSH 6 months "
                  "old; raised from recommended in the November 2026 round), recommended in RM02 "
                  "(valproate level and ammonia) and RS01 (lithium level), and optional in the "
                  "other 6. One of those 6 is P04's Wilson screen (ceruloplasmin and serum and "
                  "24-hour urinary copper), which your November 2026 note moved from required to "
                  "optional: the presentation at 42 is typical and the slit-lamp shows no "
                  "Kayser-Fleischer rings. The other 21 have no laboratory action; where a stored "
                  "result exists (for example HbA1c in a diabetic patient), it is there only so "
                  "that an order is answered consistently with the case. Counselled genetics is "
                  "under specialised tests."),
    dict(cond="parkinsons", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="remove", status="applied",
         response="Removed: no Parkinson case orders an EEG, and it is listed as waste in 28; the "
                  "DLB and PSP mimic cases (P02, P03) do not penalise it, since posterior slowing "
                  "is a supportive DLB biomarker."),
    dict(cond="parkinsons", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="remove", status="applied",
         response="Applied, with three exceptions your November 2026 notes settled. 27 cases have "
                  "no ECG criterion, and 17 list the ECG as waste. In RP01, a man with recurrent "
                  "syncope and known Wolff-Parkinson-White, the 12-lead ECG is now required (the "
                  "2018 ESC syncope guideline asks for one in every syncope), a 24-hour Holter and "
                  "an electrophysiology study for accessory-pathway risk stratification are "
                  "recommended (2019 ESC SVT guideline; a Holter that captured no syncope does not "
                  "exclude an arrhythmia), and echocardiography is optional. P01 (recurrent falls "
                  "and near-syncope with neurogenic orthostatic hypotension, midodrine or droxidopa "
                  "planned) and P02 (two falls with loss of consciousness, before a cholinesterase "
                  "inhibitor) now have a recommended baseline ECG with a stored tracing."),
    dict(cond="parkinsons", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="optional", status="applied",
         response="Applied end to end: EMG/NCS, repetitive stimulation, biopsies and evoked "
                  "potentials are absent from every action and authored report; formal autonomic "
                  "and tilt-table testing are never a criterion and are listed as waste in all 30 "
                  "(P01 and RP03 store their reports only so that an order is answered "
                  "consistently with the case). Neuropsychology is selected in 11 cases: optional "
                  "in 10 where cognition is clinically relevant, and required in RP04 as the "
                  "pre-DBS assessment. Polysomnography is optional in 14 cases with reported dream "
                  "enactment not yet confirmed and recommended in one (M05, violent episodes with "
                  "obstructive sleep apnoea as the RBD mimic). Counselled PD genetics is optional "
                  "only in the 42-year-old young-onset case and one case with an affected "
                  "first-degree relative. The cardiac electrophysiology study recommended in RP01 "
                  "is described under the ECG answer."),
    dict(cond="parkinsons", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Structural imaging is described as exclusion of a secondary or atypical "
                  "parkinsonian syndrome rather than proof of idiopathic PD. Your November 2026 "
                  "notes made it optional in clinically typical PD (NICE NG71: structural MRI is "
                  "not used to diagnose PD), and we applied that to all 15 typical cases: MRI is "
                  "optional in 14 and the CT alternative in S06, so 14 cases have no required test "
                  "and are answered by a clinical diagnosis. MRI stays required in the other 15, "
                  "each for a written reason: near-symmetric gait-onset parkinsonism in older "
                  "diabetic patients (M01, M02, M03), MSA or PSP features (P01, P03, RP03), early "
                  "orthostatic hypotension (RP01, RP02), a dementia work-up (P02), onset at 42 "
                  "(P04), new episodic oculomotor and speech symptoms (RM01), encephalitis 18 "
                  "months earlier (RM02), pre-DBS planning (RP04), a prior TIA with white-matter "
                  "disease (RP05) and a ventriculoperitoneal shunt (RS02)."),
    dict(cond="parkinsons", filed="analyze_brain_mri", tool="order_ct_scan",
         reviewer=1, tier="optional", status="applied",
         response="Applied without adding a case: PD-S06 uses non-contrast CT because severe "
                  "claustrophobia makes MRI unavailable; the report explicitly states CT's lower "
                  "sensitivity. Since the November 2026 round the CT is optional there, as MRI is "
                  "in the other clinically typical cases, to be considered only if structural "
                  "imaging becomes indicated."),

    # === amyotrophic lateral sclerosis (reviewer 1) ===
    dict(cond="als", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="required", status="applied",
         response="Applied and corrected case by case: EMG/NCS is required in all 30. "
                  "Respiratory function is recommended in 28 as a post-diagnostic safety/staging "
                  "baseline, not diagnostic confirmation, and optional in the 2 carrier cases that "
                  "do not meet ALS criteria (P02, P08). An ALS gene panel is optional/offered after "
                  "counselling in 26, consistent with the 2023 consensus guideline, and required in "
                  "the 4 familial cases whose label or counselling rests on the result (P02, P08, "
                  "P09, S10); it always follows EMG and is never embedded in routine labs. No RNS, "
                  "biopsy, unrelated evoked potential, autonomic or tilt action remains."),
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
                  "list rather than a generic structural read. NPH-P06 is the one case whose MRI "
                  "criterion asks for gadolinium; since the November 2026 round its plain MRI and "
                  "its gadolinium study are separate reports, so each order receives its own "
                  "study."),
    dict(cond="nph", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied for diagnosis: no blood test is required to diagnose NPH. Blood tests "
                  "are optional and targeted in 23 cases and recommended in the 3 with a "
                  "case-specific mimic (thyroid in NPH-M04 and S08, vitamin B12 with methylmalonic "
                  "acid on metformin in M07). Your November 2026 notes made a pre-tap safety check "
                  "required in 4 cases, as a procedural prerequisite rather than a diagnostic test: "
                  "renal function and blood count before the lumbar tap on apixaban (M03, S10) or "
                  "rivaroxaban (M06), and the platelet count, coagulation and bleeding-risk review "
                  "in cirrhosis (M08, previously recommended). In each the labs must come before "
                  "the tap."),
    dict(cond="nph", filed="analyze_csf", tool="analyze_csf",
         reviewer=1, tier="required", status="applied",
         response="Applied: required in all 30, as the large-volume tap with opening pressure."),
    dict(cond="nph", filed="order_specialized_test", tool="order_specialized_test",
         reviewer=1, tier="remove", status="applied",
         response="Applied after a case-level re-audit: no NPH case requires or recommends a "
                  "neuropsychological battery or any other specialized test, and the battery is "
                  "avoided as waste in 29 cases. The one exception is NPH-P09, a cognitive-"
                  "predominant case with a prior Alzheimer diagnosis, where the battery is optional "
                  "and its authored subcortical-frontal profile lets the agent test that label. "
                  "The timed gait and brief cognitive screen are done with the clinical-assessment "
                  "tool instead."),
    dict(cond="nph", filed="order_specialized_test", tool="perform_clinical_assessment",
         reviewer=1, tier="required", status="applied",
         seg=("If Specialized test is kept as REQUIRED", "Neuropsychological testing"),
         src_seg=("Sources:", None),
         response="Applied: perform_clinical_assessment{gait_and_balance_timed} is required in "
                  "all 30 cases as the baseline before the tap, and a second, post-tap reassessment "
                  "(timing post_intervention) is required in all 30, after the tap. The baseline "
                  "report no longer contains the post-tap result; the tap report and the "
                  "reassessment give each case's own timed-up-and-go and 10-metre figures at 2 to 4 "
                  "and 24 hours, and the baseline and post-tap orders are each answered by their own "
                  "report. The previous universal >=20% cutoff was not supported by "
                  "the cited guidelines: the cases describe a 10% TUG improvement as a commonly used "
                  "threshold, not a guideline cut-off, and interpret absolute and concordant "
                  "changes. NPH-P08 keeps a single tap with no objective improvement. Extended lumbar "
                  "drainage (source lumbar_drain) improves gait there, because one negative tap does "
                  "not exclude a shunt response; since your November 2026 notes it is recommended "
                  "rather than required, as a supplementary prognostic test (Marmarou 2005), and "
                  "another specialist assessment is an acceptable next step."),
    dict(cond="nph", filed="order_advanced_imaging", tool="order_advanced_imaging",
         reviewer=1, tier="remove", status="applied",
         response="Applied: advanced imaging is absent from the NPH panel and from all 30 case "
                  "policies, and is avoided as waste in all 30 (60 PET, flow-MRI, DaTscan and other "
                  "advanced-imaging payloads removed). Five reports are authored back in four "
                  "copathology cases (DaTscan in NPH-M05 and P02, amyloid and FDG PET in P01, FDG "
                  "PET in P04), only so that an agent who orders one anyway receives the patient's "
                  "real result instead of a contradicting normal; ordering them still counts as "
                  "waste. The previous implementation had merely relabelled PET as optional, which "
                  "did not implement a request to remove it."),

    # === temporal lobe epilepsy (reviewer 1) ===
    dict(cond="focal_epilepsy_temporal", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier="required", status="applied",
         response="Applied end to end in the October 2026 round and adjusted in the November 2026 "
                  "round. The pathway is staged: 24 routine recordings (required in 22; optional in "
                  "RP01, where continuous EEG is the required study; recommended in RP02, where the "
                  "ambulatory recording is the decisive study, November 2026 round), 5 sleep-deprived "
                  "studies, all recommended after a non-diagnostic or equivocal routine EEG, and 2 "
                  "ambulatory studies (recommended in M03, required in RP02, where they capture the "
                  "events). Video-EEG appears in 11 cases and is required only in 7: event capture "
                  "against panic or PNES (P01, P03), the LGI1 encephalitis (P02) and presurgical "
                  "evaluation (P04, RP04, RS01, RS04). It is recommended in M05, RP05, P05 and RP03. "
                  "P05 moved from required to recommended in the November 2026 round: the routine EEG "
                  "and the MRI already secure the diagnosis and the cardiac work-up was normal, so "
                  "event capture only closes any remaining syncope doubt. RP03 gained it in the same "
                  "round, because its stored 72-hour study captured nine seizures while the routine "
                  "EEG showed no epileptiform discharges. RP01 is the single continuous-ICU recording, required, because its "
                  "presentation is nonconvulsive status epilepticus, the acute setting you named."),
    dict(cond="focal_epilepsy_temporal", filed="analyze_brain_mri", tool="analyze_brain_mri",
         reviewer=1, tier="required", status="applied",
         response="Applied: brain MRI is required in 29 cases, as the dedicated epilepsy protocol in "
                  "26; RP01 (encephalitis after skull-base cancer) and RP03 (a growing metastasis) "
                  "require contrast MRI, and P02 (LGI1 encephalitis) any MRI. Gadolinium is added "
                  "only when a lesion, infection or tumor is suspected: since the November 2026 round "
                  "every first MRI report is a non-contrast study, and a post-gadolinium study is "
                  "recommended in M04 and RM04 (a possible tumor before surgical planning) and RM03 "
                  "(possible Sturge-Weber syndrome); in the pregnant patient (RS02) gadolinium is a "
                  "harmful action. P04 has no MRI criterion: her earlier 1.5T epilepsy-protocol MRI "
                  "was normal, she could not tolerate the 3T study and declined anesthesia, so CT is "
                  "optional there and her presurgical work-up rests on video-EEG and FDG-PET. CT is "
                  "required only after the head injury in RM03 and recommended in RM01 (shunt) and "
                  "RP05 (skull-base defect). Two optional CT steps were added in the November 2026 "
                  "round: in RP01, CT or MRI before the lumbar puncture to exclude mass effect, so "
                  "that CSF and acyclovir are not delayed for MRI, and in RS02, a non-contrast CT to "
                  "confirm the calcified granulomas, which may be deferred until after delivery."),
    dict(cond="focal_epilepsy_temporal", filed="interpret_labs", tool="interpret_labs",
         reviewer=1, tier="optional", status="applied",
         response="Applied: 26 cases have a laboratory criterion, optional in 15. It is required only "
                  "where the result is the case question (P02 serum LGI1 antibodies and sodium, RM03 "
                  "the phenytoin level after a fall with head injury, RS02 the eclampsia screen at 33 "
                  "weeks) and recommended in 17 with a named indication (an antiseizure medication "
                  "level after a breakthrough seizure, renal function before acyclovir, glucose on "
                  "metformin). The November 2026 round added two of these: a pregnancy test "
                  "(beta-hCG) in 10 women of childbearing potential whose pregnancy status is not "
                  "established and who start or switch an antiseizure medication or present with a "
                  "first convulsion (M01, M02, P01, RM02, RP05, RS03, RS04, S02, S04, S06), and serum "
                  "and urine osmolality with urine sodium for the hyponatremia on carbamazepine in "
                  "P02. Four cases have no laboratory criterion. The earlier claim that prolactin had "
                  "left the template was not true at the time; it is now: only P05 keeps a level. It "
                  "was drawn 22 minutes after a witnessed convulsion, outside the 10 to 20 minute "
                  "window, so since the November 2026 round it is read as at most supportive and no "
                  "longer as evidence against a psychogenic event."),
    dict(cond="focal_epilepsy_temporal", filed="analyze_ecg", tool="analyze_ecg",
         reviewer=1, tier="optional", status="applied",
         response="Applied as you asked. The previous answer (ECG required in 21 cases) did the "
                  "opposite. The ECG is now optional in 20 cases, so ordering it is credited and never "
                  "waste, and it is required in none. P05 was the last required ECG; it became "
                  "optional in the November 2026 round, because a normal 12-lead ECG, Holter, "
                  "echocardiogram and tilt test were done in the past three months, so a repeat is "
                  "acceptable but not mandatory. It is recommended in RP02 as part of the pulmonary "
                  "embolism assessment. The 9 established or tertiary cases have no ECG criterion."),
    dict(cond="focal_epilepsy_temporal", filed="order_echocardiogram", tool="order_echocardiogram",
         reviewer=1, tier="remove", status="applied",
         response="Removed from all 30 action lists: no case has an echocardiography criterion, and "
                  "ordering one is waste in 29 cases, each with its own rationale. P05 is the "
                  "exception: it already had a normal cardiac work-up in its history, and a repeat "
                  "study is neither scored nor penalised. In RM02 and RP02 only a transesophageal "
                  "study is waste (added in the November 2026 round, as low yield); a transthoracic "
                  "study is left to clinical need there, and RP02's pulmonary embolism is assessed "
                  "with the required chest CT angiogram. Stored fallback reports are normal studies, "
                  "so an agent that orders an echocardiogram anyway gets a coherent result."),
    dict(cond="focal_epilepsy_temporal", filed="order_cardiac_monitoring",
         tool="order_cardiac_monitoring", reviewer=1, tier="remove", status="applied",
         response="Removed from all 30 action lists: no case has a rhythm-monitoring criterion, and "
                  "ordering it is waste in 28 cases. P05's earlier Holter was already normal, and "
                  "RP02 needs pulmonary vascular imaging rather than rhythm monitoring."),

    # === functional neurological disorder (reviewer 1) ===
    dict(cond="functional_neurological_disorder", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=1, tier=None, status="applied",
         response="Applied as your second option, as agreed in August 2026 and confirmed on 24 "
                  "October 2026: FND stays in the frozen 20-condition dataset, and dementia with "
                  "Lewy bodies remains a deferred same-size replacement. The examination of positive "
                  "functional signs is required in all 30 cases. Your November 2026 notes changed "
                  "the rest: a test that a guideline makes necessary is now required rather than "
                  "optional, while the waste labels still measure over-testing. Video-EEG appears "
                  "in 18 paroxysmal cases and is optional in none. It is required in 7 where no "
                  "clinician has seen a habitual event or the bedside semiology cannot separate "
                  "the events from an epileptic seizure type (M04, M06, P01, RP01, S05, S06, S11), "
                  "because without the recording the diagnosis stays at the ILAE possible level, "
                  "and recommended in the 11 where a clinician witnessed a typical event (AAN "
                  "2025). A 12-lead ECG is required in 12 cases whose events include apparent loss "
                  "of responsiveness with no ECG on record (NICE CG109), recommended in 3 (RP01 "
                  "and RS03, where an earlier ECG is likely but not documented, and RP02, on "
                  "ondansetron with low potassium and magnesium), optional in P08 and scored as "
                  "waste in 10 cases without loss of responsiveness. Brain MRI is required in 8 "
                  "cases: a new focal deficit within 7 days (M05, P08, S05, S06, S10, RS04; in P08, "
                  "three hours after an insulin bolus, MRI or non-contrast CT), new symptoms on "
                  "natalizumab with a JC virus index of 2.8 (M09, with gadolinium) and complete "
                  "bilateral visual loss (RS02, MRI or CT). It is recommended for 4 subacute "
                  "questions (M03, P07, RM02, RP03), optional in 8 and waste in 2. Spine MRI is "
                  "required for the acute paraplegia in S07 and optional in 2 cases. Named assays "
                  "are required in 5 cases (glucose after insulin in P08, sodium and osmolality "
                  "with polydipsia in RM01 and RM03, electrolytes and thiamine before refeeding in "
                  "RP02 and RS01), recommended in 4 (lupus markers in M05, inflammatory markers in "
                  "RP03, thyroid function for the new tremor in S02, electrolytes and thiamine with "
                  "hazardous alcohol use in S09) and optional in 4. A neuropsychological battery is "
                  "optional in all 30 cases. The medicine review is required in 5 cases as a "
                  "management act, not a diagnostic one: a drug started for the events is to be "
                  "tapered (levetiracetam in M02, carbamazepine, phenytoin and diazepam in RP01, "
                  "levetiracetam and diazepam in RP03), or a drug on the list worsens the picture "
                  "(desmopressin with polydipsia in RM03, metoclopramide above its weight-based "
                  "maximum in RS01). It is recommended in 8 and optional in 15. Four cases were "
                  "rewritten as new phenotypes after your near-duplicate notes: S02 functional "
                  "tremor, S03 functional gait disorder, S04 functional fixed dystonia and RS02 "
                  "record-derived functional visual loss, where visual evoked potentials and OCT "
                  "are recommended. EMG/NCS and somatosensory evoked potentials are scored as waste "
                  "in all 30 cases. Efficient traces stop once the examination and the required "
                  "safety tests are done."),
]

SPEC += [
    # === anti-NMDA receptor encephalitis (reviewer 2) ===
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_brain_mri",
         tool="order_body_imaging", reviewer=2, tier="required", status="applied",
         seg=(None, "Item:\nBrain MRI"),
         response="Applied after correcting the first over-broad implementation. Tumour screening "
                  "is required in all 30 cases but not as blanket CAP CT: the 21 women aged 12-44 "
                  "receive pelvic/abdominal ultrasound, the 4 men under 45 receive targeted "
                  "testicular ultrasound, and the 5 patients aged 45 or older (2 women, 3 men), "
                  "whose tumours are mostly carcinomas, receive contrast CAP CT. Existing "
                  "pelvic/testicular reports were moved out of the laboratory payload. Since the "
                  "November 2026 round pelvic MRI is accepted in place of the ultrasound in 20 of "
                  "the 21 women (in M03 it is the separate recommended characterisation step), and "
                  "9 cases with a negative first study have a recommended second-line screen, as "
                  "Abboud 2021 describes: pelvic MRI (M02, P05), pelvic MRI and CAP CT (RM01, "
                  "RS04), CAP CT (M05), chest CT (RS03), pelvic ultrasound (RS02) and whole-body "
                  "FDG-PET (RM03, RP01)."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_brain_mri",
         tool="analyze_brain_mri", reviewer=2, tier="unchanged", status="applied",
         seg=("Item:\nBrain MRI", None),
         response="Applied: the MRI stays required in all 30 cases and its role in the ground "
                  "truth is exclusion of alternatives, not confirmation. It orders the gadolinium "
                  "study, and since the November 2026 round the plain and gadolinium studies are "
                  "separate reports, each answering its own order. Two further imaging "
                  "criteria answer your November 2026 notes: MR angiography is recommended in RP01 "
                  "to exclude a stroke before steroids, and a brain FDG-PET is optional in P04, "
                  "which stores an abnormal one, as Abboud 2021 allows when suspicion is high and "
                  "the other studies are uninformative."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="interpret_labs", tool="interpret_labs",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied in all 30 cases: CBC, metabolic/coagulation, thyroid function and "
                  "antibodies, inflammatory markers, autoimmune/paraneoplastic antibodies and a "
                  "separately priced serum IgG anti-GluN1 cell-based assay are named. Serum is "
                  "explicitly read with CSF, never alone; there are no paediatric cases requiring "
                  "selected genetic/metabolic testing. Your November 2026 notes added three "
                  "recommended case-specific tests: MOG antibodies in RM01 (an overlap question), "
                  "serum ACE in RS04 (neurosarcoidosis in the differential) and, in RS02, urine "
                  "and blood cultures, because that patient has fever, a CRP of 50 and a "
                  "catheter."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_csf", tool="analyze_csf",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied in all 30 cases: basic CSF, OCB/IgG index, HSV PCR and the CSF "
                  "anti-GluN1 assay are one reachable required order, and the CSF report carries "
                  "the final CSF titre (no result is left pending). The one case first written as "
                  "seronegative sat in this condition with anti-NMDAR answers scored correct, so "
                  "it was rewritten as CSF-positive and serum-negative, the pattern in which the "
                  "serum assay must be read with the CSF. Since the November 2026 round CSF flow "
                  "cytometry is recommended in RS04, against a haematological malignancy behind "
                  "the meningoencephalitis pattern."),
    dict(cond="autoimmune_encephalitis_nmdar", filed="analyze_eeg", tool="analyze_eeg",
         reviewer=2, tier="unchanged", status="applied",
         response="Applied: a routine EEG is required in all 30 cases and explicitly assesses "
                  "extreme delta brush without calling it pathognomonic. Continuous ICU EEG is a "
                  "recommended escalation in 29 cases (fluctuating consciousness, seizures, "
                  "behavioural arrests or rhythmic activity), never required; the one case "
                  "without seizures or epileptiform activity on either EEG has no cEEG "
                  "criterion."),
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
