# MIG-AURA-RM11
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance applied through the plan (structured ICHD-3 history required; RM11 keeps EEG for the seizures). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `initial_tool_outputs.clinical_assessment` | Template (class A): the first HPI sentence copied three times, generic red-flag line, placeholder scores, "5 of 6" with a positive aura symptom that the history does not contain. | FIXED: previous attacks, current aura sequence and duration, seizures, ICHD-3 1.2.3 B and 1.2.3.2, medicines, examination, SNNOOP10 flags present and absent; 4 of 6 for this attack (gradual spread not documented, no positive symptom); impression names 1.4.4 conditionally. |
| D | major | `initial_tool_outputs.mri` | The brain MRI carried an MRA finding and "Normal MRA" in the impression (class K); post-gadolinium line in a non-contrast study; "Critically, DWI is NORMAL" and a differential led by "cortical spreading depression". | FIXED: non-contrast technique; one structured finding (left hemispheric cortical swelling, normal DWI/ADC, no SWI signal); vessel text removed; numbered impression with a neutral imaging differential. |
| C | major | `ground_truth.action_criteria` (new `action-mrv`), `followup_outputs[0]` | No venous imaging although she has seizures and cortical oedema on an oestrogen pill (plan class K). | FIXED: required `order_advanced_imaging` `MR_venography`; follow-up: patent sinuses and cortical veins, a hypoplastic left transverse sinus as a normal variant. |
| B | major | `initial_tool_outputs.eeg` | Bilateral slowing with "no hemispheric asymmetry" in a patient with a left hemispheric syndrome and left cortical oedema (plan RM11); empty finding fields. | FIXED: continuous left hemispheric polymorphic slowing, no epileptiform discharges, no lateralised periodic discharges, no electrographic seizures; limitation that it was recorded 4 hours after the last seizure. Criterion accepts `video` or `routine` EEG (plan said video; routine is the usual first EEG after a seizure; see Open questions). |
| C | major | `initial_tool_outputs.labs`, `action-6` | Placeholder lactate "Within reference range" with no units (class L); criterion required all four panels at once and was optional. | FIXED: real values: FBC, renal function, electrolytes, calcium, magnesium, glucose, CRP 2, CK 146, lactate 1.3 mmol/L, beta-hCG negative. Recommended (plan), alternatives `lactate`, `CMP`, `CBC` or `glucose` each alone. |
| C | major | `followup_outputs` (drug check), `action-2` | `{"context": ...}` criterion (unreachable); evidence "TRIPTANS AND ERGOTAMINES CONTRAINDICATED"; output omitted topiramate (contraceptive efficacy, teratogenicity) and offered a desogestrel pill that topiramate weakens. | FIXED: stored check under `Mercilon` in `initial_tool_outputs.drug_interactions` (served for any drug): pill UKMEC 4, topiramate with oral contraception, lamotrigine with ethinylestradiol, triptans, ergots and valproate avoided, IUD as contraception; required with alternatives Mercilon, ethinylestradiol, combined oral contraceptive, topiramate, lamotrigine, verapamil, sumatriptan. |
| D | major | `initial_tool_outputs.literature_search`, `action-1` | Template literature whose text equals the expected evidence (guard leak); literature recommended with an exact query. | FIXED: initial null; one literature follow-up, last: ICHD-3 (1.2.3, 1.2.3.2, 1.4.4), UKMEC 2016, MHRA June 2024 topiramate PPP. Criterion optional `{}`. Guard passes. |
| D | minor | `patient.clinical_history.medications[1].indication` | The indication said contraception, WHO category 4, must be stopped, which hands the agent the management point. | FIXED: "Contraception". Topiramate indication reworded (dash). |
| C | minor | `patient.history_present_illness`, `patient.hpi` | No statement that this was her first seizure, which the differential and the driving advice rest on. | FIXED: "She has not had a seizure before." added (consistent with `pmh` "No prior seizure disorder"). |
| C | minor | `ground_truth.action_criteria` (`action-3`, `-4`, `-5`) | MRI pinned `contrast: false, protocol: stroke`; labels identical to rationales; `[AAN_2000]` and "ICHD-3; NICE CG150 (2025)" citations. | FIXED: MRI `{}`; labels, evidence and rationales from the case; citations cleared or `[ICHD_3]`. |
| A | minor | stop rule, sequence | Max 0, no constraints. | FIXED: stop rule history, MRI, MRV, EEG, drug check, max 1; soft constraints history before MRI and MRI before MRV. |
| C | major | `ground_truth.assessment.required_recommendations` | Test musts ("Genetic panel", "Document seizure with EEG", "Confirm MRI changes reversible"); "Re-evaluate OCP if patient is on combined OCP" although she is; duplicates of the prohibitions; no contraception or pregnancy advice with topiramate. | FIXED: eight musts: diagnosis with exclusions; stop Mercilon (UKMEC 4); class Q canonical topiramate text; prevention review (topiramate under PPP, lamotrigine or verapamil); NSAID with antiemetic; repeat MRI at 4 to 6 weeks as follow-up plan; class J canonical genetics referral; driving and DVLA. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic pill prohibition; "Do not commit to long-term AED on the basis of a single migralepsy seizure" (she had two seizures and already takes topiramate, an antiseizure medicine). | FIXED: triptans and ergots; class I canonical combined hormonal contraception text; valproate in a woman who can become pregnant. The ASM prohibition was deleted (contestable). |
| C | major | `ground_truth.differential` | Familial hemiplegic migraine `moderate` with no family history; autoimmune encephalitis "CSF and antibody panels exclude" and MELAS "normal m.3243A>G" with no such outputs; stroke "MRA normal" (class F). | FIXED: FHM low, focal epilepsy low, CVT very low (MRV), encephalitis low (afebrile, CRP, 12-year stereotyped course), MELAS low (lactate, earlier tests), ischaemic stroke very low (DWI), each with the excluding data from the case. |
| E | minor | `ground_truth.key_clinical_evidence` | Three "July 2026 review" sentences (class D). | FIXED: rebuilt from the case data. |
| E | minor | `ground_truth.red_herrings` | Entries 3 to 5 had empty paths and cited CSF, antibodies, HSV PCR, a 72-hour MRI and an MRV absent from the case (class E). | FIXED: deleted; two red herrings kept with corrected text (two seizures, not one; MRI pattern). |
| C | minor | `ground_truth.avoided_actions` | ECG listed as waste although a 12-lead ECG is standard after a first seizure with loss of awareness (NICE); generic rationales; `[Charles_2017]` on the echo. | FIXED: ECG avoided action deleted (the normal ECG fallback stays); CT, echo and monitoring rationales written for this case; citations cleared. |
| A | minor | `fallback_tool_outputs.literature_search`, `.specialized_test`, `metadata` | Junk fallbacks (class M); stale `case_body_concerns`; em dashes in `difficulty_rationale` and `neurological_exam.mental_status`. | FIXED: both fallbacks null and kinds removed; concerns cleared; dashes replaced; `condition_name` updated. |

## Changes, in one paragraph a physician can read before re-reviewing

A 26-year-old woman with sporadic hemiplegic migraine since 14, on topiramate 75 mg twice daily and the combined pill Mercilon, presents with right visual blurring, left headache, dysphasia and right hemiparesis, then two focal seizures within the hour. The pathway: structured history (known 1.2.3.2, this attack 4 of 6, seizures fitting 1.4.4 if nothing else explains them); brain MRI (left hemispheric cortical swelling across territories, normal diffusion; the MRA text is gone); MR venography (new, required, normal); EEG (now left hemispheric slowing to match her right-sided syndrome, no epileptiform discharges); blood tests (recommended, real values, lactate 1.3 mmol/L); the drug check (required: stop the pill, topiramate weakens oral contraception and is teratogenic, triptans, ergots and valproate avoided); optional literature. Musts: the diagnosis; stop Mercilon; topiramate only with an IUD or implant under the pregnancy prevention programme; review prevention (lamotrigine or verapamil as alternatives); NSAID with antiemetic; repeat MRI to confirm resolution; genetics referral (CACNA1A, ATP1A2, SCN1A, PRRT2); driving advice. Familial hemiplegic migraine is now low, and the red herrings that cited CSF, antibodies and a 72-hour MRI not in the case are gone. ECG is no longer penalised.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Vocabulary (plan 5.2): `genetic_panel:hemiplegic_migraine` (CACNA1A, ATP1A2, SCN1A, PRRT2); until it exists the test stays a referral must.
- Citation keys `[UKMEC_2016]` and `[MHRA_topiramate_2024]` (plan 5.3); cited by name until they exist.
- Guidance claims (plan 5.5): RM11 gains MRV; ECG is no longer an avoided action here.
- Label (added by the verifier): `diagnosis.accepted[0]` says "migralepsy (single seizure during aura)" while the case has two seizures; reword to "migraine aura-triggered seizures (ICHD-3 1.4.4)" centrally.

## Open questions for Andrea (judgment calls you could not settle)

- `diagnosis.accepted[0]` says "single seizure during aura", but the HPI (unchanged source data) has two seizures. The label is frozen; please reword it centrally or confirm.
- EEG: I accept `routine` as well as `video` (plan said video). A routine EEG is the usual first study after a seizure; say if only video should count.
- CSF: no criterion and no avoided action. With cortical oedema, confusion and seizures some would do a lumbar puncture to exclude encephalitis; I left it neutral because she is afebrile, CRP is normal and the attack is stereotyped over 12 years.
- ECG: avoided action deleted rather than adding a recommended ECG criterion (NICE first-seizure guidance); add one if the panel wants it scored.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MIG-AURA. Checked: right-sided syndrome, left cortical swelling on MRI and left hemispheric EEG slowing now agree; the MRV criterion, follow-up and trigger agree; labs have real values (lactate 1.3 mmol/L, beta-hCG negative) and `is_abnormal` matches the ranges; topiramate 75 mg twice daily is 150 mg/day as the must says; lamotrigine-ethinylestradiol and topiramate-oral contraception interactions are correct; the canonical class Q must and the MHRA 2024 PPP text agree; the differential no longer cites outputs that do not exist; stop rule and MRI-before-MRV constraint are consistent.
Found and fixed:
- `initial_tool_outputs.drug_interactions.Mercilon.warnings[1]` was factually wrong: it called the copper IUD a progestogen-only method and put all progestogen-only methods at UKMEC 1 in migraine with aura. Now: copper IUD UKMEC 1; LNG-IUD, implant, desogestrel pill and injectable UKMEC 2.
- `initial_tool_outputs.mri.additional_observations[1]` said "Normal flow voids in the dural venous sinuses on T2": venous-patency text in a brain MRI report (class K), which partly answers the required MRV question. Removed; the line is now "No haemorrhage or microbleed."
- `ground_truth.assessment.prohibited_recommendations[1]` (canonical pill text) offered "a progestogen-only method", which contradicts the must that topiramate needs an IUD or implant because it weakens oral methods. Now "offer an IUD or an implant, since topiramate weakens oral methods".
- `initial_tool_outputs.clinical_assessment.findings` (Seizures) said the seizures came "within the hour after the aura began", but the visual aura began about 3 hours earlier; the HPI places them within the hour after the speech and motor aura. Reworded to "During the speech and motor aura, within the hour after it began".
- MELAS differential claimed "no hearing loss" with no hearing assessment in the case; now "no hearing loss or short stature recorded".
Still open (already in this log): `accepted[0]` says "single seizure" while the HPI has two; the label is frozen, so it belongs under CENTRAL as well as Andrea's questions. perfect_agent and case_io check clean; leak guard passes.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- No case edit. Decision on the open label question: `accepted[0]` says "single seizure during aura" while ten fields of the case, consistently, record two focal seizures within the hour (HPI, structured history, EEG limitation, red herring, musts, key evidence). The data stay as they are: two aura-triggered seizures are still ICHD-3 1.4.4, the source story has two, and rewriting ten fields to one seizure would be churn to fit a descriptive clause. The label clause is a wording error in a field this round may not edit (ROUND_POLICY 3), so it stays under CENTRAL: reword to "migraine aura-triggered seizures (ICHD-3 1.4.4)". It is no longer an open question for Andrea: nothing in it needs information only Andrea has.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- UKMEC 2016 -> UKMEC 2025 citation text x1.
- UKMEC 2016 -> UKMEC 2025 citation text x1.
- accepted[0]: 'single seizure during aura' -> 'migraine aura-triggered seizures' (the case records two aura-triggered seizures).
- synonyms re-derived: the generic migraine-with-aura labels ("migraine with aura", "migraine with typical aura", "classic migraine", "migraine aura") and codes G43.1, G43.109, G43.119, G43.909 removed, because hemiplegic migraine is the subtype the case scores (triptan avoidance, genetics) and typical aura excludes motor aura; hemiplegic labels and G43.4, G43.419 kept.
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Discriminators and vocabulary (24 Oct 2026)

Wiring (`genetic_panel:hemiplegic_migraine`): new recommended criterion `action-hm-genetic-panel` after the blood tests, with the follow-up `request_hemiplegic_migraine_gene_panel` (no pathogenic variant in CACNA1A, ATP1A2, SCN1A or PRRT2; a negative panel does not exclude HM) and a soft constraint brain MRI before the panel. Tier: sporadic, but onset at 14 with seizure-complicated attacks is the highest-yield profile for a de novo CACNA1A/ATP1A2 variant (Di Stefano 2020, JNNP); the result informs counselling, not today's management, so recommended rather than required. The genetics referral must is now genetic counselling about the panel (the test itself is the criterion).

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.
- Action-5-analyze-eeg alternatives reordered routine first (the stored EEG is the routine one).

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-1-search-medical-literature` label: "Optional: literature on hemiplegic migraine with seizures, contraception and topiramate" -> "Literature on hemiplegic migraine with seizures, contraception and topiramate"
