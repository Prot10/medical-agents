# MIG-AURA: condition summary, November 2026 round

This is the auditor's summary for the 30 MIG-AURA (`migraine_with_aura`) cases, written 17 Nov 2026.

- Plan: `MIG-AURA.md`. Decisions: `MIG-AURA-decisions.md` (D1-D18). Base: commit 06b74446.
- Audit scripts are in `/home/aprotani/review-round-2026-11/work/scratch/mig-auditor/`:
  - checks: `rulings_cov.py`, `struct.py`, `audit_struct.py`, `grep_fields.py`, `cmp_counts.py`,
    `classes_base.py` (the lead's `classes_mig.py` run on the base worktree), `leak_t0.py`,
    `leak_ddi.py`, `xmod.py`; outputs `leak_t0.txt`, `leak_ddi.txt`, `xmod.txt`, `pa_full.txt`,
    `mri_probe.txt`
  - fixes: `fix_p08_p04.py`, `fix_p09.py`, `fix_ddi_summ.py`, `fix_meta.py`
- There are 63 notes, all from R1 (NB-KSC3-TWUA-QDTM). 30 cases.
- No MIG-AURA case is in `work/approved.txt`, so no approved case was changed.
- All 30 case files differ from 06b74446 (class LIT touched every case). Each one has a log in
  `logs/<CASE>.md` with '## Changes' and '## Verification'.

## 1. Rulings

| status | count |
| --- | --- |
| FIXED | 52 (one of them, 64c11ceb, is partly DECLINED: see below) |
| NO-ACTION | 8 (approvals of the chief complaint: S01 a7893337, S02 9328b8dc, S03 eed597bc, S04 b33228a7, S05 f65505f9, S08 69bca92e, S09 96e9ad91, S11 f6ee93eb) |
| ALREADY-FIXED | 3 (M03 d33fb521, M07 fee18a5b, S10 335b1fbd) |
| DECLINED (in full) | 0 |
| CENTRAL (as primary status) | 0 |
| NEEDS-ANDREA | 0 |

- `rulings_cov.py`: each of the 63 note ids of `notes/MIG-AURA.json` is in exactly one
  `work/rulings/<CASE>.json`, the case it belongs to, with a valid status. None missing,
  duplicated or unknown.
- The 3 ALREADY-FIXED notes all say the stop rule penalises recommended studies (M03 MRI and MRA,
  M07 MRI and MRA, S10 drug check). Those criteria are `recommended`. The scorer credits
  recommended and optional criteria and never counts them as extra (`policy_reward.py`, stopping
  term), so a trace that orders them still scores stopping 1.0 (D7).
- **Partly DECLINED: P08 64c11ceb** (valproate and metformin in MELAS). The general point was
  applied. Metformin is now a preference in the diabetes must. The valproate prohibition now rests
  on reasons specific to this patient: valproate is contraindicated in POLG disease, it is best
  avoided in other mitochondrial disease when alternatives exist (InterERNs 2024), and she is 29
  and can become pregnant (MHRA valproate rules). DECLINED: lifting every valproate restriction for
  her. Reason: the MHRA 2024 valproate pregnancy rules apply whatever the mitochondrial question,
  and safer antiseizure alternatives exist (levetiracetam, lamotrigine, lacosamide).
- **NEEDS-ANDREA**: none. Every point could be decided from the cited guidelines.

## 2. Classes: how they were fixed (field counts at base -> now, all 30 cases)

| class | fix | before | after |
| --- | --- | --- | --- |
| LIT (25 notes; D1) | class LIT, commit 393c547e; checked by script: no `search_medical_literature` criterion, follow-up or stored output left, and `literature_search` null everywhere | 54 fields in 30 cases | 0 |
| TOPI-CONTRA (6 notes; D3) | canonical topiramate must (Cu-IUD, LNG-IUS or DMPA with condoms; pills and the implant not adequate; potential inducer at any dose) in M04, M06, P03, RM11, S07, S10 (S10 adds the vasectomy condition; P03 adds that DMPA is UKMEC 3 after stroke); RM11 PRO1 reworded; drug reports given the FSRH any-dose caution | implant listed as adequate with topiramate: 8 fields in 6 cases; 200 mg threshold without the FSRH caution: 6 fields | 0 / 0 |
| TIA-CERT (3 notes plus class; D4) | categorical TIA prohibition replaced by the conditional must in the first presentations (M01, M03, P01, RS11), reworded on the clinical features and the DWI limit in M05, P09 and S09; M05 REQ0 and P01 REQ0 and label rewritten; optional vessel imaging added in M01 and M05; P01 MRA required | categorical prohibition: 7 cases; text saying imaging excludes or distinguishes TIA: 3 fields | 0 / 0 |
| AF-ANTICOAG (4 notes; D5, D6) | P02: ILR criterion removed and listed as avoided waste, MRI required, apixaban must conditional on the reassessment; P05: INR/CBC labs criterion required with today's result stored, warfarin withheld now, restart decided after review of the original strip | unconditional antithrombotic-stop musts: 4; "sinus rhythm proves not cardioembolic" claims: 2 fields (P02) | 0 / 0 (the 3 remaining "Review aspirin/apixaban" musts are the conditional D4/D5 texts) |
| STOP-RULE (5 notes; D7, D10, D11) | M03, M07, S10 ALREADY-FIXED; RS11 ECG and P08 EEG made criteria | n/a | n/a |
| DX-CERT (7 notes; D8, D9, D10, D12, D13, D15, D6) | label and must wording follow the certainty levels | "preventive therapy required/indicated": 3; "all secondary causes excluded": 2 | 1 (S10, kept: AHS offer threshold) / 1 (P03, kept: four required studies support it) |
| MISSING-CRIT (5 notes) | new criteria: P05 `action-labs-inr-fbc` (req), RS11 `action-ecg` (req), P08 `action-eeg` (rec), RM11 `action-arterial-imaging` (req), M01 and M05 `action-vessel-imaging-optional` (opt) | n/a | all present with the planned tier and stop-rule status (`struct.py`) |
| GENE-SCOPE (2 notes; D16) | P04 and P06 NOTCH3 reports are now targeted familial-variant tests; P04 test recommended and out of the stop rule, P04 MRI required; P06 counselling must added | 2 | 0 |
| MELAS-DRUGS (2 notes; D11) | P08 triptan prohibition deleted; valproate kept on patient grounds; metformin a preference | 2 | 0 |
| IMG-REVIEW (1 note; D14) | P03 MRI criterion and report are now the review of the outside study at day 3 | 1 | 0 |
| ED-PATHWAY (1 note; D15) | RM11 emergency encounter, stroke-protocol CT with CTA, MRA follow-up, CT waste entry deleted, stroke-pathway and seizure-observation musts | 1 | 0 |

The plan's decisions are applied the same way in every case (checked by script and by reading).
The canonical topiramate must text is identical in M04, M06, RM11, S07 and S10. P03 has the
stroke variant, and S10 adds the vasectomy clause. The conditional antithrombotic must has the
same form in M01 and RS11, and the aspirin-review form in M03 and P01. The reworded prohibition
has the same form in M05, P09 and S09. Tiers and stop rules match the plan in every case listed in
section 3 of the plan (`struct.py`).

Structural checks over the 30 cases (`audit_struct.py`) are clean:
- every stop-rule id is a required criterion, and every required criterion is in the stop rule;
- every sequence-constraint id exists;
- no avoided action matches a criterion's call;
- no case has more em dashes than at base.

Some criteria and avoided actions inherited from earlier rounds have empty `citations`. Their
rationale often cites in text. This is not a plan class, so they were left as they are.

### Stragglers found and fixed in this audit (case_io; each logged under '## Verification')

| class | cases | before | after |
| --- | --- | --- | --- |
| Drug-interaction report gives the result of a required study (an initial output, returned by the first drug query of any drug); present at base | P08: `proposed` said "a patient with m.3243A>G mitochondrial disease" and the summary "avoided in this patient" (the required mtDNA result). P09: `proposed` and warnings[0] named "an unruptured intracranial aneurysm" (the required MRA result) | 2 | 0 |
| Drug-check summary applies a label restriction as if the diagnosis were already made (TOOL_REPORT_STYLE_GUIDE: "delete any sentence that uses the drug check to announce or confirm the patient's diagnosis") | M03 and RS11 (hemiplegic migraine), M04 (brainstem aura): the summary now lists the label exclusions together (hemiplegic and brainstem/basilar-type), as contraindications[0] already did. P06 (CADASIL): "if CADASIL is confirmed, ... not first-line" | 4 | 0 |
| Turn-0 medication indication names the diagnosis | P04: "Contraception — appropriate in migraine with aura" became "Contraception" | 1 | 0 |
| Generation-pipeline text in physician-visible metadata (`metadata.case_body_concerns`: "Useless-tool entries dropped ... per authoring guide §1"). No other condition has it, and the workers flagged it for a central sweep | M01-M08, P01, P02, P04, P05, P06, RS11, S01-S11 | 25 | 0 |

Each fix changes no clinical content and no ruling. After the fixes, perfect_agent passes and
test_case_guards passes.

## 3. Blind leak pass

- **Turn 0** (`format_patient_info`, `leak_t0.py`, read case by case). No case names its own new
  diagnosis. Accepted labels appear at turn 0 only in these situations:
  - Known history. S07, S09, S10 and S11 are management cases whose label begins "Established".
    The HPIs of M05, P03 and P07 record years of migraine with aura, but their labels are
    acephalgic aura, migrainous infarction and cardioembolic stroke. P09 and RM11 record a prior
    neurologist's hemiplegic migraine diagnosis, and their labels add the sporadic or probable
    level, the aneurysm, and the seizures with cortical swelling.
  - A relative's diagnosis. P04 and P06: the aunt's or cousin's CADASIL and the familial variant,
    which the targeted test needs. P08: the mother's MELAS (the daughter was never tested). S02,
    S06, P01 and others: relatives with migraine.
  - P04's chief complaint "Migraine with aura; asking whether she should be tested for CADASIL" is
    known history. The scored question is CADASIL.
- **Prior results in the history.** Each one is either a study the case does not score, or an
  earlier study that the scored criterion repeats or extends with different content:
  - M07: A&E CT. S09: MRI 4 years ago. RM11: tests at ages 17 and 22. P09: CT and Holter.
  - P02: the GP Holter with AF (the ILR is now avoided).
  - P05: outside MRI, strip and Holter, and INR 3.8; the new labs criterion returns today's 3.6.
  - P07: inpatient MRI and telemetry; the repeat MRI and the ILR give new content.
  - P03: "told an outside MRI showed a small stroke". The required review supplies the DWI/ADC
    lesion and its location against the aura (D14, the physician's ruling).
- **Stored outputs any query can reach** (`leak_ddi.py`, and every drug-interaction initial,
  follow-up and fallback output read in full).
  - After the fixes above, no output states a criterion's result or asserts the patient's
    undiagnosed condition.
  - What remains is label content listed as rules. Examples: "UKMEC 4 in migraine with aura",
    the triptan label exclusions (hemiplegic, brainstem, after stroke or TIA), and "triptans are
    contraindicated after ischaemic stroke" in P03 and P07, where the stroke is in the history.
  - M04's triptan report still details the brainstem-aura restriction (the ergot line, the AHS
    2021 observational note). It is reached only by a triptan query, and it is the label content
    its own recommended criterion expects.
  - P08's report keeps the mother's variant, as the HPI states it.
  - The 60-character expected-evidence guard passes for all 30 cases.
- **Cross-modality synthesis** (`xmod.py`, every stored report). No report synthesises across
  modalities. Hits read and accepted:
  - Indication lines (P01, P02, P04).
  - Kind 2 statements: the P04 and P06 MRI on the CADASIL pattern, and the P06 genotype
    confirming CADASIL.
  - MRS reporting lactate (P08).
  - "MRI recommended" in the P08 CT.
  - The RM11 stroke-protocol CT carrying its own CTA.
- **Fallbacks.** The abnormal fallbacks (P07 PET, echo and fields; P08 CT, PET, echo and fields;
  P09 DSA; RM11 fields and cognitive screen) are consistent with the case. They are routed by
  their own discriminator: the P09 DSA answers only `cerebral_angiography`.
- **MRI.** `mri_probe.py` over all 30 cases: every stored MRI answers plain and contrast orders.
  None reports gadolinium. Library answers occur only in S01-S11, which store no MRI.

## 4. Approved cases changed

None. No MIG-AURA case is approved.

## 5. Label changes (accepted[0] only; codes and synonym labels unchanged)

| case | from | to |
| --- | --- | --- |
| M03 | Probable sporadic hemiplegic migraine (ICHD-3 1.2.3) ... | ... (ICHD-3 1.5.2) ... (one qualifying motor attack) |
| M04 | ... preventive therapy indicated | ... preventive therapy to be considered (AHS "consider" for brainstem aura) |
| M06 | ... migrainous infarction excluded by normal DWI; preventive therapy required | ... excluded by MRI (normal DWI and FLAIR); preventive therapy to be considered and discussed |
| M08 | ... likely genetically predisposed migraine unmasked by sertraline ... | ... onset after starting sertraline (causal role uncertain) ... |
| P01 | ... after TIA exclusion | ... TIA judged unlikely on the clinical features |
| P02 | ... (alcohol-related, nocturnal); AF and aphasic episodes temporally dissociated on implantable loop recorder | ... co-existing with paroxysmal atrial fibrillation (alcohol-related) |
| P05 | ... misdiagnosed as TIA; warfarin overtreatment ...; warfarin should be stopped | ... previously labelled TIA; supratherapeutic INR with minor bleeding on warfarin |
| P07 | Cardioembolic right PCA-territory ischaemic stroke ... NOT migrainous infarction ... | Ischaemic stroke in the right PCA territory, probably cardioembolic from paroxysmal AF ...; not migrainous infarction (an alternative cause is present) ... |
| P09 | Hemiplegic migraine (probable sporadic, ICHD-3 1.2.3) ... | Sporadic hemiplegic migraine (ICHD-3 1.2.3.2) ... |
| RM11 | Sporadic hemiplegic migraine (ICHD-3 1.2.3) with migraine aura-triggered seizures (migralepsy ...) ... mimics excluded | Probable sporadic hemiplegic migraine (ICHD-3 1.5.2) with seizures during the aura, suspected migraine aura-triggered seizures (ICHD-3 1.4.4), and left hemispheric cortical swelling without infarct; venous thrombosis excluded |
| RS11 | Sporadic hemiplegic migraine (ICHD-3 1.2.3) ...; all secondary causes excluded | Sporadic hemiplegic migraine (ICHD-3 1.2.3.2): ... with decreased consciousness in the second attack |

`apply_diagnosis_synonyms.py --check --conditions migraine_with_aura` shows the synonym lists are
unchanged. Checked with `DiagnosisCriterion.matches`:
- RM11 "Sporadic hemiplegic migraine with migralepsy" scores True and "Focal epilepsy" scores
  False (plan CENTRAL item 4).
- P02 requires both components: aura plus AF scores True, aura alone scores False.
- P05, P08, P09 and M03 short answers score True.

## 6. CENTRAL requests (consolidated)

1. **Criteria pack** `dataset-generation/criteria_packs/MIG-AURA.md` (orchestrator):
   - Section 4, topiramate: replace "(IUD or implant ...)" with the D3 fact (Cu-IUD, LNG-IUS or
     DMPA with condoms; a potential inducer at any dose; pills and the implant are not adequate).
   - Section 4, antithrombotics: add the D4 conditional rule (imaging excludes infarction, not TIA).
   - Section 4, MELAS: triptans are not contraindicated ([MELAS_2026]); valproate is restricted in
     POLG and avoided when alternatives exist; metformin is a preference.
   - Section 2, tier changes: P01 MRA required; P02 MRI required and ILR avoided; P04 MRI required
     and NOTCH3 recommended (targeted); P05 INR/CBC required; P08 EEG recommended; RM11 arterial
     imaging required; RS11 ECG required.
   - Section 3: CT is not waste in an ED presentation within the stroke window (RM11). The RS11
     worker suggests naming HaNDL as the LP indication in sporadic hemiplegic migraine.
   - Section 8: add `[FSRH_DI_2022]` and `[MELAS_2026]`; NICE CG109, NICE NG128 and Powers 2019 as
     text sources.
2. **`condition_tool_guidance.yaml` / `test_guidance_claims.py`** (orchestrator; not edited here).
   The stale MIG-AURA claims, as the test reports them now:
   - "MRI optional 2 recommended 11": the cases say 2 optional, 8 recommended.
   - "MRI required six non-routine exceptions": the cases say 9 (P01, P02, P03, P04, P07, P08, P09,
     RM11, RS11).
   - "MRA required 3 recommended 5": the cases say 5 required (P01, P03, P07, P09, RM11 via
     arterial imaging), 4 recommended.
   - "EEG in exactly 1 case": the cases say 2 (RM11 required, P08 recommended).
   - "labs required only for the P08 mtDNA test": the cases say 2 (adds the P05 coagulation
     panel, a safety INR in an over-anticoagulated patient).
   - "ECG only in P08, recommended": the cases say 2 cases, 1 recommended (P08) and 1 required
     (RS11, NICE CG109 TLoC).
   - "monitor required in exactly 3": the cases say 2 (P03, P07; the P02 ILR was removed, D5).
3. **MockServer CT routing** (`mock_server.py`, code). `order_ct_scan` is not routed by
   `angiography`. In RM11 a plain non-contrast CT order therefore also receives the CTA findings
   of the stroke-protocol report. The arterial-imaging criterion still needs `angiography: true`
   or an MRA, so scoring is right, but the plain order sees a result it did not order. The request
   is a flag discriminator for `order_ct_scan` (`angiography` against a report field such as
   `angiography_performed`), so that the CTA can be stored as its own follow-up. Accepted for now
   per D15, because ED stroke protocols pair CT with CTA.
4. **Synonyms**: none. The label changes above are for the review app's change list only.
5. **Review app display**: none specific to MIG-AURA.

## 7. Check results (after the audit fixes)

| check | result |
| --- | --- |
| `perfect_agent.py <id>` for each of the 30 cases (one call each) | 30/30 pass; no warnings in the full output |
| `pytest test_case_guards.py -k "MIG-AURA-"` | 240 passed |
| `apply_diagnosis_synonyms.py --check --conditions migraine_with_aura` | would change 0 of 600 cases |
| `pytest test_panel_case_contract.py test_red_herring_paths_resolve.py` | 4 passed |
| `case_io.py check` on the 7 cases with clinical-text audit edits | schema OK, synonym guard OK, no test failure names these cases (2 failures elsewhere in the suite, other conditions or central claims) |
| `pytest test_guidance_claims.py` | fails on the 7 stale MIG-AURA claims listed in section 6.2 (maintained centrally) |
| `mri_probe.py` on all 30 | no defect (library answers only where no MRI is stored) |

Residual items for the physicians at re-review (from the plan, unchanged):
- P02 and P05: the antithrombotic musts now depend on the reassessment.
- P08: the exact valproate wording of [MELAS_2026] was not visible; the prohibition does not
  depend on it.
