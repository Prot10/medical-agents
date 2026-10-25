# ISCH-STR-RS03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 8b0515f8-94d2-402a-8839-c4edfd7746fd | FIXED | Fetal-type right PCA stated in `initial_tool_outputs.mri` (new "Circle of Willis" signal entry in `findings[1]`, `impression` item 3) and in the CTA (`followup_outputs[0].output.additional_observations[4]`, `impression` item 2). MRI lesion extended: `findings[0].location`/`borders` now "right medial occipital and inferior parietal lobe in the right PCA territory and the posterior MCA-PCA border zone, extending into the subjacent posterior corona radiata", and the impression names it. `key_clinical_evidence[4]` explains the embolic route through the ICA and the hemiparesis. |
| 3fea7d10-8433-4f09-9eda-2619da7a4293 | FIXED | `followup_outputs[0].output.impression` (CTA) is a numbered list opening with "Near-complete occlusion of the right PCA P2 segment with minimal residual distal flow, likely embolic". `contrast_used` set true (C11). |
| d703ff12-fc6e-4eec-8db9-3696f32098c5 | FIXED | The conditional "If LVO present, consider mechanical thrombectomy" must is replaced by the decision must (`required_recommendations[1]`): isolated P2 occlusion is a medium vessel occlusion with no graded thrombectomy indication, NIHSS 8 does not meet the basilar criteria, thrombectomy not indicated; the surgical-recency clause the reviewer liked is kept ("recent surgery would not in itself have been a contraindication to thrombectomy"). `key_clinical_evidence[3]` adds ESCAPE-MeVO and DISTAL. |
| 16f5be33-8615-45ee-bdc9-eea4046acf3c | FIXED | Decision must and first prohibition state no IVT: 10 hours 45 minutes from LKW, FLAIR positive (DWI-FLAIR limb closed), and for the perfusion limb (sleep midpoint about 02:45, 6 hours before arrival, not an EVT candidate) a 3-week-old oesophagogastric anastomosis after GI cancer resection makes systemic thrombolysis high risk. The "on the cusp" prohibition is deleted; `key_clinical_evidence[2]` says day 21 is a week beyond the 14-day rule and that the rule is not the reason. Door-to-needle and pre-IVT BP musts removed. HPI gives the sleep onset (about 22:30) and the 07:00 assessment so the sleep midpoint is computable; the HPI "10.5 hours prior to symptom recognition" (wrong: 22:00 to 07:30 is 9.5 h) became "10 hours 45 minutes before arrival". |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.additional`, `.mental_status`, `.cranial_nerves`, `.motor`, `.coordination` | NIHSS 8 not derivable (C13): "No pronator drift" with a weak left arm and leg scores 0 on motor items, gaze not documented, 1b ambiguous ("not to date"), ataxia ambiguous. | FIXED: exam states age right but month wrong (1b 1), full eye movements (gaze 0), left arm drift before 10 s and leg drift before 5 s without touching the bed (1 each), past-pointing in proportion to weakness (ataxia 0), no aphasia or dysarthria; itemised "NIHSS 8 (LOC questions 1, visual fields 2, left arm 1, left leg 1, sensory 1, extinction and inattention 2)". Total unchanged. |
| B | major | `patient.clinical_history.past_medical_history[0]` | "Esophagectomy with cervical esophagostomy, pyloroplasty" is internally contradictory (a pyloroplasty implies a gastric conduit and an anastomosis, an oesophagostomy means none) and conflicts with pantoprazole "for surgical anastomotic protection". | FIXED: "cervical esophagogastric anastomosis ... feeding-jejunostomy placement". |
| D | major | `initial_tool_outputs.ct` | NCCT template management text ("does not justify withholding treatment", "Nothing on this study contraindicates intravenous thrombolysis...", "the clinically suspected event"); a head CT describing "post-surgical appearances of the recent thoracic procedure" (C11). A completely normal CT also sat poorly beside an MRI whose FLAIR is already positive. | FIXED: finding of subtle loss of grey-white differentiation in the right medial occipital cortex without established hypodensity; observation "No extra-axial collection and no pneumocephalus"; impression "1. No acute intracranial haemorrhage. 2. Subtle loss of grey-white differentiation ... which may represent early ischaemic change; no established infarct and no mass lesion." |
| B | major | `initial_tool_outputs.mri` | Impression asserted "Chronic small vessel ischemic changes" absent from the findings (C11); post-contrast T1 and "no enhancing lesions, no leptomeningeal enhancement" in a report served for the non-contrast stroke-protocol criterion; FLAIR phrased as an age estimate; T1 hypointensity strong for an infarct of under 12 hours. | FIXED: unsupported line removed; non-contrast report (no mass, no vasogenic oedema, SWI without haemorrhage); FLAIR "matching the DWI lesion (no DWI-FLAIR mismatch)"; T1 mildly hypointense; numbered impression. |
| B | major | `followup_outputs[0]` (CTA) `contrast_used` | false for a CT angiogram (C11). | FIXED: true. |
| B | minor | `followup_outputs[1]` (TTE) | Identical numbers to RS01 (LVEF 52, LAVI 40, concentric LVH, mild-to-moderate MR: template carry-over); "Abnormal values ... (H)" impression flagging LVEF 52 high; no `echo_type` (C11). | FIXED: case-specific TTE (LAVI 46 mL/m2, mild concentric LVH, LVEF 57 percent, mild MR, no vegetation, intact septum, trace effusion, appendage not seen); numbered impression; `tool_parameters.echo_type` TTE. |
| D | minor | `followup_outputs[2]` (Holter) | Impression judged "suboptimal rate control" (management); no admission timing (C2); heart-rate range average only. | FIXED: opens "Recorded on the stroke unit after admission, 24 hours."; min 58 and max 138 from the stored events; `tool_parameters.monitor_type` holter_24h; criterion alternatives holter_24h, holter_48h, telemetry; recommended (AF known). |
| C | major | `followup_outputs[3]` (drug check), criterion `action-7-check-drug-interactions` | Criterion was an IVT checklist ("Confirm absence of contraindications to IV thrombolysis") while the output reviewed apixaban; output suggested "enoxaparin bridge", "consult surgery" and an albumin claim, missing the dose rule (C7). | FIXED: apixaban 5 mg twice daily against his list (stop prophylactic enoxaparin without overlap; no interaction with metoprolol, amlodipine, metformin, atorvastatin, pantoprazole); contraindication field names the 3-week-old anastomosis after cancer resection; warnings on timing, dose-reduction criteria, haemoglobin, prophylactic enoxaparin not barring IVT, sulfonamide allergy irrelevant. Trigger `check_apixaban_enoxaparin_postoperative`; criterion required (plan C7), `drug` apixaban, placed after echo and monitoring. |
| B | minor | removed `followup_outputs` hypercoagulability panel | Orphan thrombophilia panel received by no criterion; not indicated in AF cardioembolism (C9). | FIXED: deleted. |
| C | major | `followup_outputs[4]` (literature), criterion `action-6-search-medical-literature` | Recommended literature step (ruling 5); two misattributed references (Dearborn 2014 is "Stroke and cancer: a complicated relationship", J Neurol Transl Neurosci, not Current Atherosclerosis Reports; Mashour 2011 is "Perioperative stroke and associated mortality after noncardiac, nonneurologic surgery"); superseded AHA 2019 entry; summary carried the 14-day rule and a DOAC choice. | FIXED: Navi 2017 (JACC), Mashour 2011 and Dearborn 2014 with correct titles and general findings; general summary. Criterion optional, last, `required_arguments` {}; trigger `search_stroke_cancer_perioperative`. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts (generic LKW, NCCT first, door-to-needle and pre-IVT BP in a patient who cannot be thrombolysed, glucose, prolonged monitoring for paroxysmal AF in known AF, "per mechanism") (C2, C4, C6); no rate control for AF at 104 bpm (C14). | FIXED: LKW/NIHSS, decision, stroke unit telemetry, swallow screen (aspiration pneumonia after oesophagectomy), rate control by metoprolol up-titration, apixaban 5 mg twice daily with CHA2DS2-VASc 5 and HAS-BLED 3 on day 6 to 7 with surgical agreement and enoxaparin stopped without bridging, prophylactic enoxaparin until then, TTE with TEE deferred, atorvastatin 80 mg for LDL 128 with diabetes and plaque. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | 140/90 prohibition (C5); generic IVT prohibitions in a case without IVT; TEE prohibition phrased as tool syntax ("Avoid order_echocardiogram with echo_type=TEE"). | FIXED: case-specific no-IVT prohibition; canonical COR 3 No Benefit BP prohibition (BP 162/88); anticoagulation timing rewritten to ELAN with no bridging; TEE prohibition in clinical words; delirium red-herring prohibition added. |
| C | minor | `ground_truth.avoided_actions` | TEE after oesophagectomy was prohibited in the musts but not scored. | FIXED: `avoid-harm-1-order-echocardiogram-tee` (severity harm, `echo_type` TEE) added; the three waste entries recited with the 2026 key. |
| C | major | `ground_truth.differential` | Brain metastasis, raised by the referring team in the HPI, absent (ruling 7); cancer-associated stroke absent; entries without the excluding data. | FIXED: brain metastasis very low (abrupt onset, arterial-territory diffusion restriction, matching occlusion, no mass); cancer-associated stroke low (resected tumour, single territory, no vegetation); septic embolism very low (afebrile, WBC 9.8, no vegetation); large artery low with the CTA data. |
| E | minor | `ground_truth.key_clinical_evidence` | Three "Off-pathway modality" engineering lines, the July 2026 tier line, a normal-sinus-rhythm pearl in known AF, a DAWN/DEFUSE pearl (C17). | FIXED: case-specific pearls (window, both wake-up limbs, 14-day rule, MeVO, fetal PCA, rate); TOAST, perioperative-risk, anticoagulation-restart, PCA-presentation and AHA/ASA 2026 sequencing lines kept. |
| A | minor | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule` | CTA after echo, Holter, literature and drug check (C1); labels identical to rationales; `[AHA_ASA_2019]`, doubled keys and free-text citations; echo and Holter required; hard NCCT-to-drug-check constraint; allowance 0. | FIXED: order NCCT, labs, ECG, CTA, MRI (optional), echo and monitoring (recommended), drug check (required), literature (optional); ids kept; distinct labels and rationales; keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]`; soft NCCT before CTA, CTA before echo, CTA before monitoring; stop rule NCCT, labs, ECG, CTA, drug check; `max_additional_actions` 1. |
| E | minor | `initial_tool_outputs.labs.abnormal_values_summary`; `metadata.difficulty_description`, `.difficulty_rationale` | Interpretive flags ("malnutrition", "suboptimally controlled diabetes"); difficulty text began "Straightforward" for a `diagnostic_puzzle` case and named a "TEE contraindication" and "tPA timing constraints". | FIXED: factual flags (values unchanged); difficulty text describes the reperfusion decision and the fetal PCA anatomy. |

## Changes, in one paragraph a physician can read before re-reviewing

The story is unchanged: a 67-year-old man 3 weeks after oesophagectomy for adenocarcinoma, with atrial fibrillation off apixaban since surgery, last known well at 22:00 and found at the 07:00 assessment with a right PCA infarct from a P2 occlusion, arriving at 08:45. The surgical history now names the cervical oesophagogastric anastomosis that his pyloroplasty and pantoprazole imply. The exam is itemised so that it sums to NIHSS 8. The CTA and MRI now state the fetal-type right PCA, the MRI lesion extends into the posterior corona radiata to explain the mild left hemiparesis, and the CTA impression opens with the P2 occlusion (contrast recorded). The CT shows only subtle early change and no management text; the MRI drops the unsupported small vessel line and the gadolinium sequences. The work-up reads NCCT, labs, ECG, CTA, then TTE, monitoring, the apixaban interaction check and an optional literature search; the orphan thrombophilia panel is gone. The musts state the decision: no thrombolysis (window passed, FLAIR positive, and for the perfusion limb the fresh anastomosis after GI cancer surgery; the 14-day rule is explicitly not the reason), no thrombectomy (P2 is a medium vessel occlusion, NIHSS 8). They add stroke unit telemetry, a swallow screen, rate control, apixaban 5 mg twice daily on day 6 to 7 agreed with the surgeons with enoxaparin stopped and no bridging, TTE with TEE deferred (now also a scored harmful action), and atorvastatin 80 mg.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms appended to `accepted` include "lacunar stroke" and "lacunar infarct" for a cardioembolic PCA infarct (plan section 5.3 owner).
- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` (plan section 5.1).
- Generator (plan section 5.5): CTA `contrast_used` false and impression omitting the occlusion; echo template numbers copied across cases (this TTE was identical to RS01's).
- `perfect_agent.py -v` prints "?" for the initially served NCCT and labs in this case as in every ISCH case checked; the check passes.

## Open questions for Andrea (judgment calls you could not settle)

- Infarct size for anticoagulation timing: a 5.2 cm lesion spanning the PCA cortical territory and the adjacent MCA border zone is between the ELAN "moderate" and "major" categories. The must chooses day 6 to 7, which the fresh anastomosis also favours; a reviewer may prefer within 48 hours.
- CHA2DS2-VASc 5 does not count the mild carotid and basilar plaque as vascular disease (strict definition); counting it gives 6. HAS-BLED 3 counts the anaemia as bleeding predisposition and not the acute BP of 162/88.
- The no-IVT reason for the perfusion limb (fresh oesophagogastric anastomosis after GI cancer resection) is a clinical judgement from the plan; the guideline lists structural GI malignancy and recent GI bleeding among the situations where IVT may be harmful, but I did not quote a section number from memory.
- TEE added as a scored harmful action (`severity` harm). If you prefer it only as a prohibition, drop the avoided action.

## Verification
Adversarial verifier, 23 October 2026. Read the log, the diff and the whole final case (large rewrite).
- Notes: 8b0515f8 (fetal-type right PCA in MRI and CTA impressions, lesion extended into the posterior corona radiata), 3fea7d10 (CTA impression opens with the P2 occlusion, contrast true), d703ff12 (MeVO, NIHSS 8 below basilar threshold, EVT not indicated), 16f5be33 (no IVT on window, FLAIR and the anastomosis; "on the cusp" and the door-to-needle and pre-IVT BP musts gone) all FIXED as logged. No note missing.
- NIHSS 8 recounted (1b 1, visual 2, arm 1, leg 1, sensory 1, extinction 2 in two modalities; gaze 0, ataxia 0); consistent everywhere. Times: LKW 22:00, sleep 22:30, found 07:00, arrival 08:45 give 10 h 45 min and a sleep midpoint of about 02:45 (6 hours), as stated. CHA2DS2-VASc 5 and HAS-BLED 3 follow from the record; apixaban full dose is right (age 67, creatinine 1.2, weight to be recorded). TEE harm avoided action agrees with the must and the TTE criterion. Navi 2017, Mashour 2011 and Dearborn 2014 are correctly titled. Anion gap 14, Hct about 3 x Hb.
- Minor, not changed: triage HR 102 and ECG rate 104 are both arrival values; the must quotes the ECG. Found nothing that needed changing; perfect_agent and case_io check clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.5, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.43
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TTE" to the stored echocardiogram report (the schema now keeps the field and the MockServer routes TTE/TEE/bubble orders by it; the value was only in `tool_parameters`).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Minor non-specific finding.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 73 -> 59 kg, height 174 -> 174 cm, BMI 24.1 -> 19.5 (the prompt shows height, weight and BMI).
- Why: rule 3: exam 'Cachexia noted with recent 20-lb weight loss' with stored BMI 24.1; BMI lowered to 19.5 (59 kg, about 68 kg before the loss); the apixaban note 'at most one [criterion] can apply' still holds.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

Lead follow-up (25 Oct 2026): weight 59 -> 61 kg (BMI 20.1). At 59 kg the case sat just under the
apixaban 60 kg dose-reduction threshold; with age 67 and creatinine 1.2 mg/dL only one criterion
would be met, so 5 mg twice daily was already right, but 61 kg removes the ambiguity while keeping
the post-oesophagectomy cachexia.
