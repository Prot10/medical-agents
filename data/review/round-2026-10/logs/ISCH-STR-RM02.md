# ISCH-STR-RM02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 4660dbc9-6c64-413a-a116-11c1316a9e7c | FIXED | Reperfusion frame removed (plan C4.5): the LKW/NIHSS, door-to-needle, pre-IVT BP, glucose-mimic and "secondary prevention plus high-intensity statin" musts and the four tPA prohibitions (NCCT before tPA, INR/platelets, 140/90 floor, large-infarct anticoagulation) are gone; the thrombolysis-checklist criterion `action-7-check-drug-interactions` is now an apixaban check placed right after the CTA. Its output states that apixaban taken within 48 hours contraindicates IV thrombolysis and that INR 1.1 does not measure apixaban activity; the same point is prohibition 2 and key evidence 3. |
| ffd8459c-663e-497f-97eb-615736857ab1 | FIXED | Relabelled as the reviewer ruled: `ground_truth.diagnosis.accepted[0]` "Left internal carotid artery dissection presenting with jaw and facial pain, without completed cerebral infarct", `icd_codes[0]` I77.71 (as RM03). The synonym labels and codes after index 0 were regenerated, not hand-written, by running the logic of `apply_diagnosis_synonyms.py --prune` on this case only (the I63.232 stroke and "moyamoya" synonyms were dropped; the I77.71 entry adds carotid, internal carotid and cervical artery dissection and I63.231); the synonym guard passes. Ketorolac added to apixaban plus aspirin: musts 2 and 3 keep apixaban as the single antithrombotic, stop aspirin and forbid further NSAIDs; the drug check lists the interaction. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness`, `past_medical_history[0]` | "atrial fibrillation (not on anticoagulation)" and "not on anticoagulation due to prior fall-related concern" contradicted the medication list (apixaban restarted 2 days ago). | FIXED: both now say she stopped apixaban months ago over fall concerns and it was restarted 2 days ago. |
| C | major | follow-up `interpret_labs` "Temporal Artery Biopsy" | A biopsy filed as a lab panel (wrong tool) and not indicated once CTA explains the pain. | FIXED: removed (plan). GCA stays in the differential at low with the reasons (no claudication, normal temporal arteries, ESR 34 below the age-adjusted limit of 42, CRP 0.8); a must stops the empirical steroids. |
| C | minor | GCA literature follow-up | Orphan output (no criterion) with a mis-dated EULAR reference. | FIXED: removed (plan C8). |
| C | minor | dissection literature follow-up, `action-6` | Recommended with a label about thrombolysis windows; "Various" authors and an unverifiable Mokri title; summary prescribing treatment. | FIXED: optional, last; Debette and Leys (Lancet Neurol 2009) and Biousse et al. (Stroke 1995) with general findings only. |
| C | major | `ground_truth.assessment` | No antithrombotic decision for AF plus dissection; "Coordinate carotid revascularization" (not indicated: 60% narrowing, no ischaemia); no pain or rate plan; TSH 5.8 unaddressed. | FIXED: eight musts: CTA for the pain, apixaban 5 mg twice daily as single agent (CHA2DS2-VASc at least 3, HAS-BLED 2 falling to 1, no dose-reduction criterion), stop aspirin and NSAIDs, non-NSAID non-codeine analgesia with rate control (AF 105 bpm), admission with telemetry and warning signs, stop empirical steroids, repeat vessel imaging at 3-6 months, CPAP, BP target and TSH recheck. Four case-specific prohibitions. |
| C | minor | `ground_truth.differential` | "Cardioembolic stroke from AF" high and keys mentioning hemiparesis and DWI infarct that the case does not have; "Hemorrhagic stroke" irrelevant. | FIXED: trigeminal neuralgia, GCA (low), ACS (very low; troponin and ECG), dental (very low), ischaemic stroke or TIA (very low; NIHSS 0, no DWI lesion). |
| C | minor | criteria tiers and order | Echo and Holter required in a patient with known AF and no stroke; MRI optional although DWI is what shows there is no infarct; hard NCCT-to-drug-check constraint; stop allowance 0. | FIXED: NCCT, labs, ECG, CTA, drug check (required), MRI (recommended), TTE and monitoring (recommended; monitoring alternatives holter_24h/holter_48h/telemetry, relabelled for rate control), literature (optional). Soft constraints NCCT before CTA, CTA before drug check, echo and monitoring. Stop rule NCCT, labs, ECG, CTA, drug check; `max_additional_actions` 1. |
| D | minor | `initial_tool_outputs.ct` | NCCT template ("does not justify withholding treatment", "Nothing on this study contraindicates intravenous thrombolysis", "clinically implicated territory"); Fazekas 2 on MRI absent on CT. | FIXED: canonical impression with ASPECTS 10 and mild periventricular hypoattenuation. |
| D | minor | `initial_tool_outputs.mri`, labs summary | "confirming chronicity"; unnumbered impression; interpretive lab summary ("subclinical hypothyroidism"). | FIXED: neutral wording, numbered impression, factual summary with reference ranges. |
| B | minor | CTA follow-up | `contrast_used` false; "flame-shaped tapering" (an occlusion sign) with a patent 60% narrowing; stray "; Vessel_wall:" text; impression did not lead with the dissection site. | FIXED: contrast true; tapered narrowing; numbered impression leading with the dissection 2 cm above the bifurcation. |
| D | minor | echo follow-up | "Abnormal values: ... (H)" impression; no `echo_type`. | FIXED: numbered TTE impression; `echo_type` TTE in output and `tool_parameters`; trigger `request_tte_echocardiogram`. |
| D | minor | Holter follow-up | Impression referred to "the patient's known untreated atrial fibrillation" (cross-reference to the history). | FIXED: rhythm and rate only, opening "Recorded on the stroke unit after admission, 24 hours." |
| E | minor | `key_clinical_evidence`, `red_herrings`, citations, `metadata` | Template stroke lines, three "Off-pathway modality" lines, "Tier per the July 2026 clinical review", T1 fat-sat neck MRI never obtained; red herring 2 aimed at "cardioembolic stroke" which no longer exists; free-text guideline string and 2019 keys; difficulty text claiming a completed stroke. | FIXED: six case-specific key evidence lines; red herring 2 retargeted to ESR/CRP and the ED steroids (GCA anchor); one key per source; difficulty description and rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is now what its data show: a left cervical ICA dissection presenting with jaw and face pain, NIHSS 0 and no infarct on DWI, labelled I77.71 as the reviewer ruled, with the whole thrombolysis apparatus removed. The pathway reads NCCT, labs (troponin, ESR, CRP), ECG, CTA (dissection 2 cm above the bifurcation, intramural haematoma, flap, about 60% narrowing), then the drug check, which states that apixaban restarted 2 days ago would contraindicate thrombolysis whatever the INR and that ketorolac on top of apixaban and aspirin is a bleeding hazard; MRI, TTE and rate monitoring follow as recommended steps. Management: apixaban 5 mg twice daily as the single antithrombotic for both AF and the dissection, stop aspirin and NSAIDs, analgesia without NSAIDs or codeine, rate control, observation with telemetry, stop the empirical steroids (GCA unlikely: no claudication, normal temporal arteries, ESR below the age-adjusted limit), repeat vessel imaging at 3-6 months, and CPAP, BP and TSH follow-up. The temporal artery biopsy filed as a lab and the GCA literature output are removed, and the HPI no longer says she is off anticoagulation.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms regenerated for this case with the `--prune` logic of `apply_diagnosis_synonyms.py` (this case only); a central `--prune` run should give the same result. The I63.232 entry of `diagnosis_synonyms.yaml` grants "moyamoya disease" and "moyamoya", which is wrong for I63.232 (carotid occlusion or stenosis) and still affects RM01 and other cases coded I63.232.
- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` (plan section 1.1).
- `fallback_tool_outputs.cardiac_monitoring` describes persistent AF throughout, while the stored Holter shows AF with intervals of sinus rhythm; it is unreachable while the follow-up exists and was left unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- Plan open question 3: RM02 now contains no infarct (as RM03). Confirm that two ISCH-STR cases without a completed infarct are acceptable for the condition.
- MRI made recommended (the plan keeps MRI optional outside RP02): without DWI the "without completed cerebral infarct" part of the label cannot be established, and a silent infarct would change anticoagulation timing.

## Verification

Adversarial verifier, 23 October 2026. Checked: relabel and ICD (I77.71) against plan and note ffd8459c; synonym list against `diagnosis_synonyms.yaml` (identical to RM03); removal of every reperfusion must and tPA prohibition; the drug check (apixaban within 48 hours, INR does not measure it, ketorolac and aspirin, codeine intolerance); CHA2DS2-VASc and HAS-BLED; GCA age-adjusted ESR ((74 + 10) / 2 = 42); MRI DWI negative; HPI and PMH now consistent with apixaban restarted 2 days ago; differential against the final evidence.

Found and changed:
- Answer leakage in `patient.history_present_illness`: the ED physician's differential named "vascular pathology such as carotid artery dissection", the case's diagnosis. Removed; the sentence now lists temporal arteritis and acute coronary syndrome only.

CENTRAL (added): the I77.71 entry of `diagnosis_synonyms.yaml` appends code I63.231 (cerebral infarction due to occlusion or stenosis of the right carotid artery) to a left ICA dissection explicitly labelled "without completed cerebral infarct" (RM02 and RM03). Remove I63.231 from that entry.

`perfect_agent.py ISCH-STR-RM02 -v` passes; `case_io.py check` clean for the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
I77.71 no longer appends I63.231 (an infarct, on the other side) to a dissection without infarct; list regenerated after the relabel to I77.71.
- codes removed: I63.231
- `case_io.py validate` OK; `perfect_agent.py` passes.
