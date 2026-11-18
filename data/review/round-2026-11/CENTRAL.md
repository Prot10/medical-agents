# November 2026 round: CENTRAL requests (changes outside the case files)

Each item: file, change, the cases or notes that need it. Condition-specific items are added from
`plans/<COND>-summary.md` at the end of the round.

## Review app display (web-review/src/components/cases/CaseDetail.tsx, `RenderValue`)
1. Null renders as "none" (line ~585). Physicians read "contrast used: none" and "clinical
   significance: none" as data. Render null as "not stated" (or omit the key). Notes: the
   MRI-CONTRAST notes (all now fixed in the data) and every "significance none" note
   (ALZ-EARLY, FEPI-TEMP: ruled CENTRAL + the clinical point fixed in the case). 2865 abnormal
   lab rows in 450 cases have a null `clinical_significance`; none says "none".
2. Object keys render in stored order, alphabetical after `case_io.save`, so `abnormal`,
   `is_abnormal`, `result` print above `test`: a reader pairs a value or flag with the neighbouring
   row (ALZ-EARLY neuropsych flag notes, MG "label and value shifted by one row"). Render label
   keys first (`test`, `name`, `parameter`, `measurement`, `domain`), then value, unit, range,
   flag, significance.
3. Stop rules and sequence constraints show only the tool name of a criterion; show the
   criterion's discriminating argument (test_type, study, modality, panels) next to it (MG notes).

## Tests
4. Guard: a stored brain MRI whose text reports gadolinium content states `contrast_used: true`,
   and a case storing one also stores a plain study (plans/MRI-CONTRAST-decisions.md).
5. Guard: no case stores a `literature_search` output and no criterion uses
   `search_medical_literature` (class LIT), or drop the tool from the catalogue.

## From the condition rounds (details and case lists in plans/<COND>-summary.md)
6. Vocabulary (`costs.yaml`, `fallback_library.yaml` normal, `review_api/services/tool_io.py`
   mirror, `TOOL_PARAMETER_VOCABULARY.md`):
   - `perform_clinical_assessment` `swallow_assessment` (CPT 92610): MG musts in 15 cases ask for
     a swallow assessment no criterion can order yet (interim: must only; MG notes ruled CENTRAL).
   - `interpret_labs` `clustered_MuSK_cell_based`: MG P01, RP14, P04.
   - `order_body_imaging` `breast_mammography` (CPT 77067), optionally `breast_MRI`: NMDAR-ENC RM03,
     RS02 (Abboud 2021 tumour screen).
   - optional `analyze_csf` `neuronal_surface_tissue_assay`: NMDAR-ENC RP01.
7. Review app (web-review CaseDetail.tsx): show stored follow-ups that match no criterion in a
   separate "answered on request" block (ALZ-EARLY, VASC-DEM notes: reviewers read them as pathway
   steps; 2417 such follow-ups in 496 cases); label a second alternative "alternative to step N".
8. Schemas (`evaluation.py` StopRule): an optional `rationale` shown in the app ("actions that match
   an optimal action never count against the allowance"): ALZ-EARLY, VASC-DEM, FND stop-rule notes.
9. Criteria packs (`dataset-generation/criteria_packs/<COND>.md`) and `conditions.yaml` template
   musts for the 13 conditions: update tiers, canonical musts and citation allow-lists to the
   November decisions (each summary lists the sections and new citation keys; some keys were
   recalled, not re-verified: FEPI-TEMP lists four to check).
10. `build_condition_tool_guidance.py --write`: its input (`data/review/tool_reviews/`) is not in
    this worktree, so condition_tool_guidance.yaml was patched with the builder's row order; re-run
    it where the input exists and check the diff is empty.
11. Guard: a stored invasive or harmful study (biopsy, catheter angiography, electrophysiology
    study, levodopa challenge, TEE) that no criterion orders carries an avoided action. Unlabelled
    biopsy reports remain in SE (6 cases) and TEE in GBS (1) and SE (3), conditions without
    November notes (not changed this round).
12. Neuropsychology percentile convention: VASC-DEM now uses the AACN 2020 labels (R1's VASC
    notes); ALZ-EARLY keeps flags that match each row's stated range (44 R1 notes). A dataset-wide
    convention is for R1 to choose at re-review.
