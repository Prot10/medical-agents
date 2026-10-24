# MIG-AURA-M08
Reviewer status: R1 none, R2 none (no reviewer notes for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input applied is the July 2026 tool guidance for `migraine_with_aura` (structured ICHD-3 history required; MRI optional for red flags; CSF, ECG, EEG and routine echo removed) and ROUND_POLICY. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI sentences copied (twice), father's history filed as "aura description", generic SNNOOP10 line, placeholder modality score listing speech, motor and brainstem features she does not have. | FIXED: structured assessment of this patient: four attacks, earlier brief flashes with monocularity unconfirmed, visual then perioral sensory aura in succession, 20-25 min spread, headache timing, medication timeline with no serotonin toxicity features, normal exam, named SNNOOP10 flags (new pattern present, others absent), family history; criteria 6 of 6, 1.2.1 met. |
| D | major | `initial_tool_outputs.mri` | Brain MRI impression reported "Normal MRA" (class K) and "no enhancing lesion" without a contrast sequence. | FIXED: MRA and enhancement text removed; indication and sequences stated; finding made specific (four punctate frontal subcortical foci); impression numbered. |
| A | major | `action-2-check-drug-interactions` | `{"context": ...}` alternative no agent can send (class C); label and rationale generic; expected evidence proposed venlafaxine or amitriptyline without reason; citations `[Holland_2012]` (NSAID guideline) and `AAN_2000` free text. | FIXED: alternatives `{"drug": "sumatriptan"}`, `{"drug": "sertraline"}`; kept required (concrete interaction she asks about, ROUND_POLICY 6); case-specific label, evidence and rationale (FDA 2006 alert against AHS 2010 position paper and Orlova 2018); citation `[AAN_2000]`. |
| C | major | `followup_outputs` drug check | Speculative CSD sentence, "safe at current doses" verdict, no contraindications, no warnings on other serotonergic drugs, NSAID bleeding with SSRI, or tricyclic interaction. | FIXED: rewritten with real interactions (sumatriptan-sertraline with sources and observed incidence; SSRI with NSAID bleeding; sertraline CYP2D6 with amitriptyline), contraindications (MAOI, ergot within 24 h, SmPC vascular list), counselling warnings, topiramate PPP note; summary in report voice. |
| C | major | `followup_outputs` literature (2) | First output speculative and patient-directed (5-HT2A and CSD threshold, "family history supports inherited predisposition"); second wrong ("topiramate: mood stabilising properties", whereas topiramate can cause depression) and prescriptive; unreferenced sources. | FIXED: both deleted; one literature follow-up with real sources (Evans RW et al., Headache 2010;50:1089-1099; Orlova Y et al., JAMA Neurol 2018;75:566-572), general evidence, last in the list. |
| A | major | `action-1-search-medical-literature`, stop rule | Required literature step in the stop rule (ROUND_POLICY 5). | FIXED: optional, `required_arguments: {}`, last; stop rule `[action-3, action-2]`, allowance 1. |
| C | major | `ground_truth.assessment.required_recommendations` | "Brain MRI as a cautious step" (test as must, contradicts the optional MRI tier, class J); "[Holland_2012]" cited for SSRI-triptan; "consider preventive options" without the AHS threshold. | FIXED: five musts: explain 1.2.1 diagnosis; continue sumatriptan with sertraline with counselling and no further serotonergic drugs; triptan at headache onset, under 10 days a month; answer the sertraline question (predisposition predates it, changes agreed with the prescriber); diary, no prevention at about one attack a month (AHS 2021), with sertraline-compatible options and topiramate only under the PPP (class Q). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Ergot prohibition without an ergot (class I); combined pill prohibition not in the canonical wording. | FIXED: ergot line deleted; "Do not stop sumatriptan or call it contraindicated because she takes sertraline" added; canonical UKMEC 4 combined-contraception prohibition (she is 38). |
| C | minor | `ground_truth.differential` | `[Holland_2012]` cited in the serotonin syndrome entry; focal seizure reason imprecise; earlier monocular flashes raise retinal migraine or retinal disease with no entry. | FIXED: serotonin syndrome (Hunter features absent), TIA, retinal migraine or retinal disease (homonymous current attacks, monocularity unconfirmed), focal seizure (phenomenology), IIH; all very low with the excluding features. |
| B | major | `ground_truth.red_herrings` | Two entries with empty `location` and `field_path`; "confirms genetic predisposition" overstated; WMH in the MRI report not addressed. | FIXED: paths `patient.history_present_illness` and `patient.clinical_history.medications`; interpretations without Holland citation; new WMH red herring pointing at `initial_tool_outputs.mri.findings`. |
| D | minor | `ground_truth.key_clinical_evidence` | "July 2026 review applied end to end..." (class D); `[Holland_2012]` misused. | FIXED: deleted; three case pearls (1.2.1 met, predisposition predates sertraline, triptan plus SSRI risk low with counselling). |
| A | minor | citations, MRI criterion | Duplicates and free text ("ICHD-3; NICE CG150 (2025)"); MRI `{"contrast": false, "protocol": "standard"}`. | FIXED: one key per criterion; MRI `required_arguments: {}` with a rationale naming AHS 2020 and Choosing Wisely. |
| A | minor | order, constraints | Literature first; no constraints. | FIXED: history, MRI (optional), drug check, literature; soft constraint history before MRI. |
| C | minor | `avoid-waste-3-order-echocardiogram` | `[Charles_2017]` (pathophysiology review) cited for PFO (class N). | FIXED: rationale names PREMIUM, PRIMA and MIST; citation removed until CENTRAL adds trial keys. |
| B | minor | `patient.hpi`, `patient.history_present_illness` | Sumatriptan "started 6 weeks ago after the first neurology consult" while she now presents to the neurology clinic. | FIXED: "prescribed by her GP 6 weeks ago". |
| E | minor | `metadata.difficulty_rationale` | "new-onset MRI workup" contradicts the optional MRI tier. | FIXED: rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing
38-year-old woman with four typical attacks in 3 months (right-field visual aura spreading over 20-25 minutes with right perioral tingling, then left-sided migrainous headache), starting 2 weeks after sertraline, with a father and sister with migraine and earlier brief visual episodes; normal examination. Diagnosis unchanged (migraine with typical aura, 1.2.1); the structured assessment now documents her own data. The brain MRI stays optional and no longer reports an MRA; its punctate frontal white matter foci are a red herring. The required drug check (sumatriptan or sertraline) now states the real evidence: serotonin syndrome with a triptan and an SSRI is rare (AHS 2010 position paper, Orlova 2018), so both continue with counselling and no other serotonergic drugs; it also covers NSAID bleeding with an SSRI and the sertraline-amitriptyline interaction. Musts no longer order an MRI; prevention is not indicated at about one attack a month; the sertraline question is answered; combined hormonal contraception is prohibited in the canonical UKMEC 4 wording. The incorrect literature (topiramate as mood stabiliser) is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Allow-list: `[AHS_neuroimaging_2020]`, `[AHS_2021]`, `[UKMEC_2016]`, trial keys `[PREMIUM_2017]`, `[PRIMA_2016]`, `[MIST_2008]` (plan 5.3); add the AHS 2010 triptan-SSRI position paper (Evans RW et al., Headache 2010;50:1089-1099) as a key for this case.

## Open questions for Andrea (judgment calls you could not settle)
None. Plan 6 Q6 (triptan with SSRI) is decided as allowed with counselling; the label clause "co-administration acceptable with counselling" already says so and is unchanged.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MIG-AURA. Checked: four attacks and 6 of 6 C characteristics agree across HPI, assessment fields and impression; laterality consistent (right-field visual and right perioral aura, left-sided headache); MRI optional, no MRA, WMH stated in findings and impression and used as a pointed red herring; drug criterion `{"drug": "sumatriptan"}` / `{"drug": "sertraline"}` required (concrete question) and answered by the follow-up through either name; drug output content (Evans 2010 position paper, Orlova 2018 incidence 0.6-2.3/10,000 person-years, NSAID-SSRI bleeding, CYP2D6) is correct and does not repeat the expected evidence (guard passes); musts allow co-prescription with counselling, consistent with the label clause and the prohibition; combined-contraception prohibition canonical (38 F); no preventive at about one attack a month; literature optional and last.
Found: nothing requiring a change. No edit made.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `ground_truth.assessment.required_recommendations[4]`: candesartan was offered to a woman who can become pregnant without the pregnancy caution that M06, P03 and S04 carry (candesartan is fetotoxic). Now "candesartan, only with reliable contraception as it is contraindicated in pregnancy", so the class Q cautions read the same across the condition.

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x2, [AHS_triptan_SSRI_2010] x1, [ICHD_3] x2.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.
