# Brief: rejected labels and mixed components for scorer v2 (25 Oct 2026)

Scorer v2 (commit 677c7492, `packages/neuroagent-schemas/src/neuroagent_schemas/evaluation.py`
`DiagnosisCriterion`) scores the diagnosis on the label alone:

- an accepted label's tokens must all occur in the asserted part of the answer (denied clauses
  dropped: "non-X", "not X", "no X", "rather than X", "instead of X", "X excluded", "X ruled out",
  "X unlikely", "X criteria not met");
- no `rejected` label may occur there;
- each `required_components` group (list of alternative labels) must be named too.

The ICD code no longer gives credit. Your job: fill `ground_truth.diagnosis.rejected` (and
`required_components` where the case is a mixed diagnosis) for your cases, deciding for dataset
quality (Andrea's standing rule: decide, apply, record why).

## Input
A compact table per case in your group file (scratchpad, path in your prompt): primary label,
short accepted labels, codes, and each differential with candidate labels (its name cut at the
first qualifier, its acronym, the synonym-table labels of its code). Candidates that an accepted
label contains are already dropped. Open the case JSON only when the table leaves the decision
unclear (e.g. whether a differential is in fact a comorbidity in this case).

## Rules
Reject a label when naming it in the primary diagnosis asserts something wrong for this case:
1. a competing diagnosis from the differential, above all the likely and the designed mimics (this
   is what stops hedged answers like "ALS or MS" or "MS vs NMOSD" from scoring);
2. a wrong subtype, stage or variant of the right disease: "PD dementia" / "dementia with Lewy
   bodies" in PD with MCI (PD-RP01, RP04), "secondary progressive" / "primary progressive" in
   RRMS, "mild cognitive impairment" / "MCI" in a dementia-stage case and "dementia" in an MCI
   case, "migrainous infarction" where the case excludes it, a wrong organism in meningitis, a
   wrong grade/entity in glioma ("glioblastoma" in an IDH-mutant astrocytoma).

Do not reject:
- anything true in this case (a concurrent condition, precipitant or cause named in the primary
  label or the key clinical evidence), or anything an accepted label contains;
- generic or fragment candidates ("Cardiac", "primary", "Dementia" alone where dementia-vs-not is
  not the point, "stroke" in a case whose diagnosis is a kind of stroke);
- ambiguous single tokens that may occur in a correct answer for other reasons. Common acronyms of
  the competing disease (MSA, PSP, NMOSD, MOGAD, CIDP, RCVS, DLB, PNES) are fine.

Keep each label short and canonical, lower-case except acronyms; typically 2 to 8 per case.
Write the competing names as a clinician would type them ("multiple system atrophy", "MSA").

Mixed diagnoses: set `required_components` only where the correct answer is two entities that
must both be named (e.g. "concurrent Wernicke encephalopathy and hepatic encephalopathy";
HEP-ENC-P04, coded as Wilson disease). Each component is a list of alternative short labels. The
primary label `accepted[0]` must name every component, and short accepted labels that name only
one entity then stop scoring alone: that is intended.

## Procedure
- Edit through `data/review/round-2026-10/bin/case_io.py` (library `load`/`save`); touch only
  `ground_truth.diagnosis.rejected` and `required_components` of your cases; nothing else.
- Write scratch scripts in your own scratchpad subfolder and run them with `uv run python -I`.
- Guard: `uv run pytest agent-platform/tests/test_case_guards.py -q -k "diagnosis_label and (COND1- or COND2- ...)"`
  must pass (primary label scores, no accepted label names a rejected one).
- Sanity script: for every case, check that `accepted[0]` and each short accepted label still
  match (except where components intentionally block a single-entity label), and that each
  differential's own full name does not match.
- Do not edit the synonym YAML; list class-level rules you would put there in your decisions file.
- Write `data/review/round-2026-10/plans/SCORER-V2-<group>-decisions.md`: one line per case (case,
  rejected labels, components, a short reason for any non-obvious choice) and a short list of
  doubts for the physicians.
- Do not commit. Report under 150 words: cases changed, total labels, components set, doubts.
