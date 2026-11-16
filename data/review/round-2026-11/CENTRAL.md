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
