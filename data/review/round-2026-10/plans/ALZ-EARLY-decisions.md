# ALZ-EARLY: decisions on the open questions (24 Oct 2026)

Andrea ruled on 24 Oct 2026: "per i punti aperti, risolvili nel modo migliore per la qualità del
dataset". Every item below is decided and, where it needed a change, applied. Per-case detail is in
each case log under "Close-out (24 Oct 2026)".

Sources checked on 24 Oct 2026: Rabinovici GD et al., Updated appropriate use criteria for amyloid
and tau PET, Alzheimers Dement 2025;21(1):e14338 (doi 10.1002/alz.14338) and J Nucl Med
2025;66(Suppl 2):S5-S31; Dubois B et al., IWG recommendation, JAMA Neurol 2024, doi
10.1001/jamaneurol.2024.3770; ADA, 13. Older Adults: Standards of Care in Diabetes-2026, Diabetes
Care 2026;49(Suppl 1):S277-S296 (Table 13.2: A1C below 8.0% for complex/intermediate health,
including mild to moderate cognitive impairment); Blumenthal RS et al., 2026 ACC/AHA multisociety
guideline on the management of dyslipidemia, Circulation 2026;153(17):e1154-e1276 (retires the
2018 cholesterol guideline); NICE NG239 (2024), vitamin B12 deficiency (180-350 ng/L
indeterminate, consider MMA); AHA/ASA 2021 secondary stroke prevention (no newer edition found).
The other pack references were checked against their published bibliographic data.

## 1. Diagnosis synonyms (`diagnosis_synonyms.yaml`, ALZ-EARLY entries)

Entries are selected by the case's primary code only, so the summary's "per code over every code"
description no longer held; the remaining defect was the labels and codes those entries grant.

| entry | before | after | reason |
| --- | --- | --- | --- |
| `G30` | 5 labels incl. "alzheimer dementia", "dementia due to alzheimer"; codes G30.0, G30.1, G30.8, G30.9, F00 | disease names only ("alzheimer disease" x3 spellings); code G30.9 | G30.0 (onset under 65) and G30.1 (65 or later) name different variants and must not grant each other |
| `G30+dementia` (new) | | "alzheimer dementia", "dementia due to alzheimer", F00; `except_cases: [ALZ-EARLY-P02]` | P02 (lvPPA) is staged without dementia-level loss of function |
| `G30.0` | "posterior cortical atrophy", "benson syndrome", "early onset alzheimer" | "early onset alzheimer" | PCA labels were granted to lvPPA, frontal, familial and amnestic cases |
| `G30.1` (new) | | "late onset alzheimer" | |
| `G30.0+pca` (new) | | PCA labels, G30.8; P01, RP01, RP02, RP03 | the four PCA cases |
| `G30.0+lvppa` (new) | | lvPPA labels, G30.8; P02 | |
| `G30.0+frontal` (new) | | frontal-variant labels, G30.8; P03 | |
| `G31.84` | MCI labels plus "alzheimer disease", "alzheimer's disease"; codes G30.0, G30.1, G30.9 | MCI labels only, no extra codes | every "mild dementia due to Alzheimer disease" answer contains the tokens of "alzheimer disease", so an overcall of an MCI case scored as correct |

Applied with `apply_diagnosis_synonyms.py --prune --conditions alzheimers_early` (30 cases).
This settles the CENTRAL_PENDING item "ALZ-EARLY prune diffs predate the batch-1 synonym change":
`--check` and `--check --prune` are both clean for the condition. The restaged cases (RM01, RM02,
RM03, RS06) lost their MCI labels; the amnestic late-onset cases lost PCA, Benson and early-onset
labels and G30.0.

Limitation (CENTRAL, scorer): a dementia case still accepts an MCI answer ("mild cognitive
impairment due to Alzheimer's disease" contains "alzheimer's disease"). Requiring the token
"dementia" would reject the plain clinical answer "Alzheimer's disease", which is correct for a
dementia case. The fix needs a scorer feature (per-case rejected tokens, e.g. an answer containing
"mild cognitive impairment" or "MCI" does not match a dementia case).

## 2. Label change (ruling 3)

- **RM04** (summary CENTRAL 2): `accepted[0]` "... (amnestic, predominantly amnestic single-domain
  with naming involvement)" -> "Mild cognitive impairment due to Alzheimer's disease (amnestic
  multi-domain, with naming involvement)"; G31.84 unchanged. The battery shows memory plus naming
  (BNT 7th percentile) and semantic fluency (14th) impairment: amnestic multi-domain MCI (Albert
  2011). The label contradicted the case's own impression; scoring is unchanged.

## 3. Open questions (summary section 5)

1. **Q1, NIA-AA 2018 or AA 2024.** Decision: labels follow the clinical criteria (McKhann 2011,
   Albert 2011); reports name the measured profile and say "A+T+" only when amyloid and p-tau are
   both abnormal. Reason: AA 2024 is a biological framework that the IWG 2024 explicitly disputes as
   a clinical definition; in symptomatic patients, which all 30 are, both agree, and the clinical
   criteria are what decides MCI versus dementia, the skill the condition scores. M01 and M03 keep
   "intermediate likelihood": amyloid is decreased or borderline, p-tau within range, and MRI
   neuronal injury borderline for age (MTA 1-2), which is Albert 2011 intermediate likelihood. Pack
   section 1 records it; `[AA_2024]` and `[IWG_2024]` added to the allow-list.
2. **Q2, RM03 and RS06 restaged without a reviewer note.** Confirmed. RM03: wife took over the
   finances after unpaid bills, medication reminders, lost twice while driving. RS06: daughter took
   over the medicines after miscounting despite a pill organiser; alterations work given up. Both are
   interference with usual activities (McKhann 2011) and meet the round's functional rule, the same
   rule Reviewer 1 applied to RM01 and RM02.
3. **Q3, CSF and amyloid PET counterparts authored in all 30.** Accepted. Without them a correct
   alternative returned the library's normal result, contradicting the case; one criterion with two
   concordant alternatives is what Reviewer 1 asked for. Physicians see them at re-review.
4. **Q4, FDG-PET authored only in 13 cases.** Decision: author it everywhere. Added an FDG-PET
   follow-up (no criterion) to the 17 cases without one (M01-M05, P04, RM01-RM03, RP04, RP05,
   RS01-RS06): each a case-specific Alzheimer-type pattern matching the MRI severity and laterality,
   MCI cases mild, focal defects at known lacunes, no cingulate island sign where DLB is weighed
   (RM03, RP05), no patchy cortical or thalamic defect in the CJD question (RP04), metabolically
   normal cortex under the RS06 meningioma. Reason: the library's normal FDG in a case with
   hippocampal atrophy and positive amyloid is internally inconsistent data an agent can receive.
   Probed: FDG and amyloid PET orders each return their own report in either order; perfect agent
   30/30. No criterion or tier changed.
5. **Q5, RS06 MRI with contrast.** Keep both `contrast` false and true. The agent cannot know the
   meningioma before the MRI and contrast is not part of the dementia protocol, so requiring it
   would penalise standard care; contrast is clinically reasonable once the lesion is seen, and the
   contrast report is served only to a contrast order.
6. **Q6, normal liver tests added to six CMPs and copied normal values varied.** Accepted: a CMP
   order must return a CMP; the values are normal and nothing scored depends on them.

## 4. Auditor flags

7. **RS04 hip flexors 4+/5 and hyporeflexia attributed to sarcopenia.** No change. Symmetric mild
   proximal weakness with reduced bulk, BMI 19.8, no sensory signs, reduced ankle reflexes at 79
   (common after 75), normal B12, homocysteine, TSH and electrolytes; the nutrition must covers it.
8. **Near-duplicates (summary CENTRAL 8).** RP01/RP02: kept (the RP02 worker showed different
   source reports and traps). RS03/RS04 were twins at the surface (both "Mrs. Tanaka", retired
   seamstress from a garment factory, Japanese, with a daughter): RS04 renamed Mori, now a retired
   florist, and its failed complex task an ikebana arrangement. S02/S03/S04 were all retired postal
   workers: S03 now a retired hospital pharmacy technician, S04 a retired city bus driver. HPI text
   similarity between any two ALZ-EARLY cases is below 0.3 (difflib); clinical content unchanged.
9. **B12 300-350 pg/mL without MMA** (own check against NICE NG239, which calls 180-350 ng/L
   indeterminate): no change. Every case reports homocysteine, a functional marker, and it is
   normal in these cases; the MMA criterion stays at the plan's about-300 pg/mL threshold. The
   repeated 310 pg/mL value (7 cases) is plausible and kept, as in ALS (decision 25).
10. **Superseded citations.** `[ADA_older_adults_2025]` -> `[ADA_older_adults_2026]` in M05, RP04,
    RP05 (same target); `[AHA_ACC_cholesterol_2018]` -> `[ACC_AHA_dyslipidemia_2026]` in RP01.
    `[Appropriate_Use_Amyloid_PET]` (122 uses) now points to the 2025 AUC, which supersedes Johnson
    2013; every statement cited with it holds under both, so no case text changed.

## 5. Criteria pack, generator and guidance

- `dataset-generation/criteria_packs/ALZ-EARLY.md` rewritten to the plan: per-case ICD rule
  (G31.84, G30.0, G30.1 by onset), functional staging rule, biomarker wording (Q1), workup order and
  tiers (one amyloid criterion with two alternatives, FDG authored everywhere, drug check only in
  dementia, ECG only with a QT drug, no literature), the three soft sequence constraints and the stop
  rule, pitfalls (AChEI in MCI, donepezil pharmacology, sedatives, subclinical hypothyroidism, B12,
  microbleeds, NPH, contrast, CT). Allow-list: every key cited in the 30 cases with a full
  reference, plus `[AA_2024]`, `[IWG_2024]`, `[NICE_NG239]`, `[CLARITY_AD_2023]`,
  `[Lecanemab_AUR_2023]`; superseded: `[ADA_older_adults_2025]`, `[AHA_ACC_cholesterol_2018]`,
  alias `[McKeith_2017_DLB]`.
- `conditions.yaml` (alzheimers_early block): MMSE scores removed from the two difficulty
  presentations (the cognitive screen is a scored step) and the moderate one made unambiguously MCI
  by the functional rule; BMP -> CMP; TSH line no longer calls a normal TSH proof against
  "hypothyroid dementia" and names subclinical hypothyroidism; low-normal B12 prompts MMA; CSF
  findings name Abeta40 and the routine-panel-only rule; FDG and amyloid PET follow-up descriptions
  no longer state results; MMA follow-up added; header comment for the round. No literature, consult
  or MCI drug-check follow-ups existed to remove.
- Guidance claims: `build_condition_tool_guidance.py` ALZ responses updated (6 MCI cases, not 10;
  CSF and amyloid PET as alternatives in 29; FDG in 7 with RP03's SPECT substitute and FDG authored
  everywhere; ECG optional in P04 and RP02 only; EEG and ECG elsewhere answered by normal reports);
  YAML regenerated with `--write`; claim table: CSF 29, amyloid PET 29, FDG 7, new ECG (0 required
  or recommended, 2 optional) and MCI-count claims. `test_guidance_claims.py` and
  `test_condition_tool_guidance.py` pass.

## Files changed

- Cases: all 30 (synonym re-expansion); content in RM04 (label), 17 FDG cases (above), M05, RP01,
  RP04, RP05 (citations), RS04, S03, S04 (diversity). Logs: all 30, "Close-out (24 Oct 2026)".
- `agent-platform/config/policies/diagnosis_synonyms.yaml` (G30, G31.84 entries and new scoped
  entries), `dataset-generation/criteria_packs/ALZ-EARLY.md`, `dataset-generation/config/conditions.yaml`
  (ALZ block), `agent-platform/scripts/review/build_condition_tool_guidance.py` (ALZ responses),
  `agent-platform/config/review/condition_tool_guidance.yaml` (regenerated),
  `agent-platform/tests/test_guidance_claims.py` (ALZ rows).

## Checks

`perfect_agent.py` 30/30; `case_io.py check` on all 30: schema and synonym guard OK, no test failure
names an ALZ-EARLY case; `test_case_guards.py -k ALZ-EARLY-` 60 passed;
`apply_diagnosis_synonyms.py --check --conditions alzheimers_early` clean (also with `--prune`);
guidance claim tests pass.

## Still for Andrea or the physicians

Nothing blocks. For re-review: the restagings of RM03 and RS06 (no reviewer has seen them), the
CSF, amyloid PET and FDG-PET results authored this round, and two scoring changes (MCI cases no
longer accept a bare "Alzheimer disease" or G30 codes; G30.0 and G30.1 cases no longer accept each
other's code).

## CENTRAL (not made here; owners elsewhere)

1. **Scorer**: per-case rejected tokens so a dementia case does not accept an MCI answer (section 1).
2. **Vocabulary**: a speech and language assessment term for PPA cases (P02), e.g.
   `perform_clinical_assessment` assessment_type `language_assessment` (naming, repetition,
   single-word comprehension, motor speech and grammar; Gorno-Tempini 2011); today the content sits
   in the neuropsych battery. The `not_completed` fallback kind used by RS05, if kinds are
   enumerated centrally.
3. **Library** (`fallback_library.yaml`): amyloid PET, CSF and FDG-PET defaults are normal, so any
   condition's AD-type case that does not author them gets a contradicting result (ALZ-EARLY now
   authors all three); confirm the MR spectroscopy and DaTscan defaults are normal and
   non-contributory; the drug-check default says "no interaction" for any drug.
4. **Harness**: `check_drug_interactions` serves the single stored follow-up (donepezil) for any
   drug (memantine, rivastigmine); add a drug discriminator to the MockServer matcher.
5. **perfect_agent.py**: a mode that exercises every alternative of each criterion and flags library
   answers.
6. **Citation alias dataset-wide**: PD-P01, PD-P02, PD-P03, PD-RP03 cite `[McKeith_2017_DLB]`;
   ALZ-EARLY uses `[DLB_2017]`; harmonise in the PD pack and cases when PD runs.
