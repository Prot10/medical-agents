# Phase 3 Realism Spec — close the two leak vectors the audit found

The realism sweep cleaned tool-report *impressions*, but the audit found two
answer-leak vectors it could not see. Close both, **conservatively**.

> **AUTHORITY:** `dataset-generation/TOOL_REPORT_STYLE_GUIDE.md`. Decision (locked):
> *within-modality* conclusions are KEPT (EMG "consistent with a motor neuron
> disease"; neuropsych "probable bvFTD"; MRI "acute MCA infarct"); confirmatory
> results (CSF organism, genetics, antibody titres, biopsy histology) are KEPT.
> The leak is the *integrated, cross-modality* answer — never re-derive it.

## Vector A — Kind-1 leakage inside `specialized_test` and imaging free-text

The leak detector SKIPS `specialized_test`, so EMG/NCS/neuropsych/evoked-potential
reports were never swept. Read every `specialized_test` and imaging report
(initial + followup + fallback) in your cases and remove, per the style guide's
three prohibitions:
- **Cross-modality synthesis** — a report citing other tests / genetics / the MRI /
  the exam / "the overall picture" to reach the answer. Delete the citation.
- **Differential-refutation essays** — numbered rebuttals of competing diagnoses
  ("NOT CIDP because (1)… (2)…", "this excludes…", "the MGUS is incidental").
  Collapse to at most one hedged sentence.
- **Management/treatment prescription** — drug/dose/therapy/"start…/admit/refer".
  Keep only a recommendation for a further *diagnostic* step.
KEEP the within-modality electrophysiologic/neuropsychometric conclusion and all
numeric findings.

## Vector B — case-body answer-leakage in HPI / exam (CONSERVATIVE)

Some `patient.history_present_illness` and `neurological_exam` fields pre-state the
answer (e.g. an HPI reading *"BENZODIAZEPINE-RESISTANT SE from isoniazid toxicity"*,
or a record naming the gold diagnosis). The presentation must read like a real
clinician's intake — what the patient reports and what is observed — NOT the
solved case.

**REMOVE only answer-stating editorializing:**
- the final diagnosis / etiology asserted as established ("…from isoniazid toxicity",
  "this is CIDP", "consistent with POEMS syndrome", "diagnostic of X");
- numbered differentials / diagnostic reasoning embedded in the HPI;
- management directives; benchmark meta-commentary ("this case tests…", "the red
  herring is…").

**KEEP every clinical fact — do NOT delete or soften these:**
- symptoms, onset, timeline, severity, progression, associated/negative features;
- past medical history, **medications** (e.g. keep "on isoniazid for latent TB" —
  it's a fact the agent needs; just don't call it *the cause*), allergies, social
  history, review of systems, family history;
- every `neurological_exam` finding and vital sign.

**Worked example.**
- before: *"He presented with benzodiazepine-resistant status epilepticus from
  isoniazid toxicity; he takes isoniazid for latent TB."*
- after: *"He presented with status epilepticus that did not resolve with
  benzodiazepines. He takes isoniazid for latent TB."*
  (kept the refractory-SE fact + the isoniazid medication; removed the "from
  isoniazid toxicity" causal verdict the agent must deduce.)

## Hard constraints
- NEVER change a symptom, timeline, exam finding, lab/vital value, medication, or
  any clinical fact. You are removing *conclusions*, not *data*.
- NEVER change `ground_truth`, the diagnosis, `primary_diagnosis`, or numeric values.
- Preserve each file's unicode convention; coherence must stay 0; schema must validate.
- Touch ONLY your condition's files.

## Self-verification (required, per touched case)
1. `uv run python agent-platform/scripts/validate_ground_truth_coherence.py --case <CASE>.json` → 0
2. schema validates (`NeuroBenchCase.model_validate_json`)
3. HPI/exam no longer names the gold answer: confirm the case's `primary_diagnosis`
   core term / etiology does not appear as a verdict in `history_present_illness`
   or `neurological_exam` (it may legitimately appear as a *fact*, e.g. a known prior
   diagnosis or a medication indication — use judgment).

Report: cases touched; Vector-A fields rewritten; Vector-B HPI/exam phrases removed
(with the fact you preserved); anything flagged instead of fixed.
