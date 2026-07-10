# NeuroBench v5 — Clinician-Adjudication Flag List

Items the automated/agent passes deliberately did **not** auto-fix because they
require clinical judgment or change clinical meaning. Compiled from the field-by-field
audit (`data/review/audit/{CONDITION}.md`) and the Phase-3 realism pass. The
mechanical/architectural fixes (followup-union bug, doubled units, answer-leakage)
are already applied; this is the residue for the human review round.

Priority key: **[BLOCKER]** internally impossible / wrong gold action · **[MAJOR]**
likely error or high-stakes call · **[REVIEW]** confirm-intended.

## 1. Laterality (imaging ↔ exam ↔ reasoning consistency)
A recurring, clinically serious class — left/right must agree across the case.
- **[BLOCKER] ISCH-STR-S01** — left-MCA imaging + global aphasia but **left-body** deficits (a left-MCA stroke cannot cause left hemiplegia). Internally impossible.
- **[MAJOR] ISCH-STR-S03, S04** — "right gaze deviation" in left-MCA strokes with right hemiparesis; cortical gaze should deviate **left** (toward the lesion). (S02 is the correctly-lateralized template.)
- **[MAJOR] PD-RM02, RM03, RS01, S02** — DaTscan striatal deficit on the **same** side as the worse clinical signs; the dopaminergic deficit should be **contralateral**. RS01/S02 even contradict their own "contralateral" wording.
- **[MAJOR] FTD-M06** — MRI/FDG left-hemisphere predominant, but CBS exam + neuropsych describe **left-hand** cortical signs (→ right hemisphere).
- **[REVIEW] FEPI-TEMP-RM01** — left-sided hemiparesis with a left-hemisphere lesion; contralateral mapping expected.

## 2. Gold-answer / criteria calls
- **[MAJOR] PD-RP02** — gold = idiopathic PD over a near-complete MSA-P picture (symmetric DaTscan, poor levodopa response, early dysautonomia, axial rigidity); sister cases call MSA on similar data.
- **[MAJOR] PD-RS03** — gold = idiopathic PD despite rapid course, early falls, Pisa syndrome, early dysautonomia.
- **[MAJOR] GLIO-HG-RP03** — IDH-mutant WHO grade-2 (low-grade) tumor sitting in the high-grade set, with GBM/Stupp-templated ground_truth that contradicts it.
- **[MAJOR] HEP-ENC-M05** — case premise (zinc *excess* precipitating HE via arginase inhibition) is the opposite of standard teaching (zinc is usually *supplemented* in HE).
- **[MAJOR] GBS-RM13** — differential entry contradicts the case (says ammonia/encephalopathy "absent" though the case has baseline hepatic encephalopathy + ammonia 68); also a 6-week course justified as "within the 4-week GBS range".
- **[REVIEW] NPH-M07** — gold iNPH despite Evans 0.30 (pack needs >0.3) and callosal angle 91° (needs <90°); rests on the tap response.
- **[REVIEW] NPH-P04** — iNPH + bvFTD copathology with a sub-threshold tap (18%) and dominant bvFTD FDG-PET; confirm NPH isn't over-called.
- **[REVIEW] SE-M02** — levetiracetam called "subtherapeutic" in the gold/red-herring, but the lab value is therapeutic.

## 3. Copy-paste / template contamination (wrong facts bled between cases)
- **[MAJOR] GLIO-HG-M02** — drug-interaction warning asserts pregnancy/perimenopausal status + age "52" for a **47-yo male** (from M01).
- **[MAJOR] NMDAR-ENC M05, P02, P03, RP01, RP02, RP03, RS03** — 7 **male** cases carry "ovarian teratoma / women of reproductive age" boilerplate in `key_reasoning_points`.
- **[MAJOR] PD-P01, RP01, RP02, RS04** — phantom metoclopramide cited in ground_truth that the case body explicitly denies.
- **[MAJOR] SAH-M06, M08** — `critical_actions` mandate emergent EVD "given acute hydrocephalus" while their own CTs say **no hydrocephalus**.
- **[MAJOR] NPH-P07** — `red_herrings` names "breast cancer" in a **prostate-cancer** patient (from P06).
- **[REVIEW] BACT-MEN-M01, M02, M03; FEPI-TEMP-M03** — fabricated penicillin/childhood-rash allergy in drug-interaction text contradicting `patient.allergies`.
- **[REVIEW] HEP-ENC-M07** — fabricated "bariatric history" + wrong BMI appearing nowhere else.

## 4. `analyze_csf` listed harmful while CSF is the populated/critical test
- **[MAJOR] SAH-M02, M05, M07, P04, RS12** — `analyze_csf` in `harmful_tools` (raised-ICP/anticoagulation), yet an LP result is populated as initial data.
- **[MAJOR] BACT-MEN-P02, P03** — `analyze_csf` in `harmful_tools` but CSF is the confirmatory test, and P03 also mandates serial therapeutic LPs as a critical action.

## 5. `consult_medical_specialist` tiering (dataset-wide)
Marked `required` widely vs the criteria packs' `recommended`; also absent from the
documented 12-tool roster (CLAUDE.md). Needs a single dataset-wide ruling.

## 6. "R"-subtype taxonomy mismatch (dataset-wide, documentation)
The criteria packs define the "R" subtype as a non-disease mimic, but most R-cases are
real-seeded **confirmed** cases of the index disease (verified in ALS, SAH, FND,
ALZ-EARLY, MS-RR, GBS, MIG-AURA, NMDAR-ENC). Reconcile the pack docs vs. composition.

## 7. Mimic prefixing — confirm intended
PD-P01/P02/P03/RP03 (atypical parkinsonism), GLIO-HG-P02 (PCNSL), NMDAR-ENC-RP01
(seronegative AE), FND-P09 (SREAT), several MIG-AURA (CADASIL/MELAS/AF-stroke/aneurysm).
These carry the index-condition prefix but a different gold diagnosis — confirm the
prefixing convention and that per-condition metrics handle them.

## 8. Lab `is_abnormal` / unit-scale judgment calls (not mechanically fixed)
- **[REVIEW]** Borderline `is_abnormal` flags (B12 218 in range 200-900; just-outside HEP-ENC glucose/Hb/platelets/K). NOTE: PD UPDRS-III "0-132" entries use `reference_range` as the *scale* — those flags are correct, do not "fix".
- **[REVIEW]** Unit-scale typos flagged but not blanket-changed: TSH `mIU/mL` (vs `mIU/L`/`µIU/mL`) in GBS-RP11/RP13; verify intended units.

## 9. Other notable single-case flags
- **[MAJOR] SYNC-CARD-RM01** — brain MRI shows a normal brainstem, contradicting the gold reasoning that brainstem signal identifies the anti-Hu encephalitis.
- **[MAJOR] SYNC-CARD-RM02** — same Holter event given both 12 s and 4.8 s pause durations.
- **[MAJOR] FTD-M06** — GRN `c.1477+1G>A` labelled "frameshift" but is a splice-site variant (FTD-P02 handles GRN naming correctly).
- **[REVIEW] FTD-P02/P04** — two required `order_specialized_test` calls (neuropsych + genetic panel) but the mock server resolves to one output slot; genetics delivered via `interpret_labs`. (Mock-server limitation, logged.)
- **[REVIEW] FND-M03** — TOMM 52/50: impossible score on a 50-item test.

## Note for maintainers (infrastructure, not clinical)
The mock server resolves `order_specialized_test` / `order_advanced_imaging` to a single
output slot regardless of `test_type`/`modality` — a case needing two distinct tests of
the same tool can only return one. Consider keying those outputs by `test_type`.
