# MIG-AURA-M03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (structured ICHD-3 history required, MRI for red flags only), applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.history_present_illness`, `patient.hpi` | "the worst headache of his life" is the thunderclap/SAH descriptor, yet the case treats LP as waste and the headache as migrainous; the descriptor contradicted the policy. | FIXED: "a left-sided throbbing headache that built up over about 30 minutes to 9/10, far worse than his usual mild headaches". The structured history records that onset was not thunderclap. |
| B | minor | `patient.chief_complaint` | "right arm weakness during a severe headache ... sent urgently from ED": the weakness preceded the headache, and the HPI says he was referred to clinic 10 days after the ED visit. | FIXED: "right arm weakness and slurred speech followed by severe headache, referred after an emergency visit". |
| D | minor | `patient.clinical_history.medications[0].indication` | "... requires review" hinted at the management. | FIXED: "Started by GP after the emergency department visit for 'possible TIA'". |
| B | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI sentences cut mid-word ("a gradual o..."), copied twice, generic red flags, placeholder modality score; `at_least_two_attacks: true` with no distinction between his visual auras and the single motor attack. | FIXED: structured assessment: previous visual auras (1.2.1 met), index attack with C1-C6 from his data (6 of 6), sporadic-form family line, examination, SNNOOP10 line (motor aura and pattern change present, onset not thunderclap), medicines and vascular risk. New keys `at_least_two_attacks_with_motor_aura` false, `all_criteria_for_hemiplegic_migraine_1_2_3_met` false, `probable_hemiplegic_migraine_met` true. Impression supports probable sporadic hemiplegic migraine and states the red flags. |
| D | major | `initial_tool_outputs.mri.impression` | "Normal MRA intracranial and cervical arteries" inside a brain MRI report (class K); `findings` empty while the impression named three WMH. | FIXED: vessel text removed; structured WMH finding; negatives on DWI, FLAIR/SWI (no subarachnoid blood), flow voids, CADASIL regions. |
| C | major | `ground_truth.action_criteria`, `followup_outputs[0]`, `avoided_actions` | No vessel study for a first motor deficit with vascular risk; MRA was a waste avoided action. | FIXED (class K, plan): new recommended `action-mra` (`order_advanced_imaging` `MR_angiography`) answered by `followup_outputs[0]` (normal intracranial TOF and cervical CE-MRA, no dissection); `avoid-waste-3-order-advanced-imaging` (MRA) deleted. |
| C | major | `followup_outputs` drug block, `action-2` expected evidence, red herrings, musts | "Elevated LDL 148 mg/dL" appears nowhere in the case (PMH: no hyperlipidaemia; no labs) but drove a statin must, the drug output and two red herrings (class E). | FIXED: all LDL text deleted; replaced by a must for GP cardiovascular risk assessment (BP, lipids, HbA1c, QRISK3) and hypertension treatment if above target. |
| A | major | `action-2-check-drug-interactions` | `{"context": ...}` criterion not sendable; output was an aspirin essay unrelated to the triptan question the criterion named; expected evidence called triptans "contraindicated" in capitals. | FIXED (class C): nine triptan `{"drug": ...}` alternatives; follow-up `followup_outputs[1]` (sumatriptan and other triptans: label exclusion in hemiplegic and brainstem aura, ergots, vascular contraindications; his aspirin and paracetamol no interaction; Artto et al. 2007 series as a warning; NSAID plus antiemetic and gepants as alternatives). Required: triptan avoidance changes the acute plan. |
| C | major | `assessment.required_recommendations` | "Brain MRI/MRA required" must duplicated criteria (class J); no decision on the empirical aspirin; preventive and genetics musts vague. | FIXED: musts: stop aspirin and explain to patient and GP; NSAID plus antiemetic at headache onset, no triptans or ergots; diary, prevention if motor aura recurs (verapamil, lamotrigine, flunarizine where licensed); genetics referral (CACNA1A, ATP1A2, SCN1A, PRRT2) if recurrence or an affected relative (class J referral, no vocabulary term); GP cardiovascular risk. |
| C | minor | `assessment.prohibited_recommendations` | Three lines including the ergot-with-triptan boilerplate (class I). | FIXED: one case-specific triptan/ergot avoidance line, plus the canonical class G antiplatelet prohibition (TIA question and aspirin present). |
| C | major | `ground_truth.differential` | TIA "moderate" after normal MRI (class F) with "normal MRI/MRA needed"; seizure "low". | FIXED: TIA low with the clinical features and imaging (and the DWI caveat); cervical dissection added very low (MRA); seizure very low; FHM low (no affected relative; ICD null to avoid echoing the label code); CADASIL very low with MRI regions. |
| B | minor | `ground_truth.red_herrings` | LDL entry (no data), two entries with empty `field_path`; "Normal DWI at 10 days" reasoning. | FIXED: four entries with real paths: HPI TIA concern, aspirin (`medications[0]`), father's stroke and hypertension (`family_history[0]`), WMH (`initial_tool_outputs.mri.findings[0]`). |
| D/E | minor | `key_clinical_evidence` | Two engineering sentences ("Tier per the July 2026 clinical review...", "July 2026 review applied end to end...") (class D); "contraindicated" overstated. | FIXED: deleted; four lines from this case. |
| A | major | `action-1-search-medical-literature`, literature follow-ups | Required literature step in the stop rule; queries as slugs; "Normal DWI is KEY" and patient-specific conclusions; "AAN/HIS guidelines" (no such source). | FIXED: optional, `{}`, last; one follow-up (`followup_outputs[2]`) with ICHD-3 1.2.3 and Russell and Ducros, Lancet Neurol 2011; the triptan block deleted (its content is in the drug check). |
| A | minor | `fallback_tool_outputs.advanced_imaging`, `.specialized_test`, `metadata.fallback_tool_kinds` | "MRA head and neck" and "Neurodiagnostic assessment" junk fallbacks (class M). | FIXED: null; kinds removed. |
| C | minor | `action-3`, `action-4` | Template labels, MRI arguments `{"contrast": false, "protocol": "standard"}`, duplicate/free-text citations. | FIXED: case-specific; MRI `{}`, recommended; one key per source. |
| C | major | `sequence_constraints`, `stop_rule` | None; literature in stop rule, max 0. | FIXED: soft history-before-MRI (MRI-MRA pair not constrained, both recommended); stop rule action-3 and action-2, max 1. Order: history, MRI, MRA, drug check, literature. |
| B | minor | `metadata.difficulty_description`, `difficulty_rationale` | Mentioned the non-existent LDL. | FIXED. |
| E | minor | `avoided_actions[1].rationale` | Em dash. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 42-year-old man with years of typical visual aura had a first attack of right hand tingling spreading over 20-25 minutes, then grip weakness and slurred speech, followed by a migrainous headache; his GP started aspirin for possible TIA. The label (probable sporadic hemiplegic migraine) is unchanged. The headache is no longer described as "the worst of his life" (which would have demanded an SAH work-up the policy calls waste); it now builds over 30 minutes. The structured history separates his typical auras (1.2.1 met) from the single motor attack (hemiplegic migraine criteria met except the second attack). MRI (recommended) shows no infarct and three non-specific WMH; MRA is now a separate recommended study (normal intracranial and cervical arteries) and is no longer listed as waste. The LDL of 148 that appeared only in a drug output and red herrings is gone. The drug check is now a triptan check: triptans and ergots are label-restricted in hemiplegic migraine, so acute treatment is an NSAID with an antiemetic. Musts: stop the aspirin, NSAID plus antiemetic, diary with prevention if motor aura recurs, genetics referral on recurrence or an affected relative, GP cardiovascular risk review. TIA is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Vocabulary: `order_specialized_test` `genetic_panel:hemiplegic_migraine` (CACNA1A, ATP1A2, SCN1A, PRRT2) (plan 5.2); until it exists, genetics is a referral must.
- `diagnosis_synonyms.yaml` G43.109 group: drop "migraine aura" (plan 5.1); this case receives it.
- Criteria pack allow-list: `[AHS_neuroimaging_2020]`, `[AHS_2021]`.
- `condition_tool_guidance.yaml` claims: MRA is now a separate recommended study in M03 (plan 5.5).

## Open questions for Andrea (judgment calls you could not settle)

None. The HPI headache wording was changed because the original thunderclap descriptor would make the case's CSF "waste" entry and the migraine label clinically indefensible; the alternative (adding an SAH work-up) would turn the case into a different one.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the HPI headache-onset change against the CSF waste entry, the chief complaint, structured-history keys versus the HPI (visual auras for 1.2.1, one motor attack for probable 1.2.3), MRI and new MRA outputs (no vessel text left in the brain MRI), removal of all LDL text, triptan drug-check content (label exclusion, Artto et al. 2007 exists and reports 76 patients), literature source (Russell and Ducros, Lancet Neurol 2011), musts (aspirin stop consistent with the antiplatelet prohibition; genetics as referral), differential, red-herring paths, sequence direction, stop rule, BMI 27.7 consistent with demographics. Every log claim holds. No reviewer notes exist for this case.

Found and fixed:
- `assessment.prohibited_recommendations[1]`: the canonical class G text claimed "previous identical attacks"; the motor attack is his first (his earlier attacks were visual only). Rewritten to the features this attack has (sensory march over 20-25 minutes, motor and speech symptoms in succession, migrainous headache, background of typical visual aura).

`perfect_agent.py -v` ok, `case_io.py check` clean for the case, guard tests pass.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x2, [ICHD_3] x1.
- synonyms re-derived: the generic migraine-with-aura labels ("migraine with aura", "migraine with typical aura", "classic migraine", "migraine aura") and codes G43.1, G43.109, G43.119, G43.909 removed, because hemiplegic migraine is the subtype the case scores (triptan avoidance, genetics) and typical aura excludes motor aura; hemiplegic labels and G43.4, G43.419 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Discriminators and vocabulary (24 Oct 2026)

Genetic panel decision: not wired as a criterion. One motor attack at 42 makes this probable HM; the must already ties gene testing to a second attack or an affected relative, so ordering the panel now is not indicated. No case data changed.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-1-search-medical-literature` label: "Search the literature on sporadic hemiplegic migraine (optional)" -> "Search the literature on sporadic hemiplegic migraine"
