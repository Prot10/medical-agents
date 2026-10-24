# ISCH-STR-RM01
Reviewer status: R1 none, R2 in_progress | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| ef70fcc1-21c8-42f2-b3af-ab0442f7007c | FIXED | CTA follow-up `output.impression` rewritten around the carotid finding: "1. Dissection of the left internal carotid artery from the C2 level to the skull base: intimal flap, crescentic mural haematoma and greater than 70% luminal stenosis, extending into the petrous segment. 2. Irregular calibre of the left M1 ... without occlusion ... 3. No right carotid or vertebrobasilar dissection; no intracranial aneurysm." Also `contrast_used` set true (plan C11) and "subtle beading pattern" dropped from the M1 finding (beading suggests FMD or vasculitis, which the case does not intend). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.additional`, musts, key evidence | NIHSS 3 not derivable. Recount: facial palsy 1 (subtle lower facial weakness on smiling), best language 1 (word-finding pauses), arm 0 (no drift; grip 4/5 is not an NIHSS item), dysarthria 0 (the slurring had resolved) = 2. | FIXED: "NIHSS score: 2 (facial palsy 1, best language 1)", noting the hand deficit the scale misses; pre-stroke mRS 0 added; 2 used in the LKW must, decision must and key evidence. |
| C | major | `ground_truth.assessment.required_recommendations` | No reperfusion decision; template door-to-needle and BP musts with no decision; template "high-intensity statin per mechanism" (LDL 108, no atherosclerosis); "Recognize neck/face/eye pain" (she has neck tenderness, no face or eye pain); 140/90 prohibition (plan C5). | FIXED: decision must: IV thrombolysis given (about 2 h, glucose, INR, platelets normal; extracranial dissection not a contraindication; seizure at onset does not make the deficit postictal when vessel imaging shows the mechanism; dominant-hand deficit prevents return to her laboratory work, so disabling); no thrombectomy (no LVO, NIHSS below 6). Door-to-needle and BP 185/110 then 180/105 musts kept because IVT is given. Statin must removed. Antithrombotic must for at least 3 months after 24 h and a scan without haemorrhage, repeat vessel imaging at 3-6 months. Hemodynamic precaution (avoid hypotension, greater than 70% stenosis, border-zone infarct) in the stroke-unit must. Seizure must (prolonged EEG if recurrent; ASM only for confirmed recurrent seizures). Sport restriction must. |
| C | major | drug-check follow-up, `action-9` | Output proposed warfarin or DOAC and ignored levothyroxine and asthma; the alternative "aspirin 325 or aspirin + clopidogrel per CADISS" misstates CADISS. | FIXED (plan C7, required): aspirin checked against the actual list: combined OCP is MEC category 4 after ischaemic stroke (contraindications field), oestrogen raises levothyroxine needs (recheck TSH 6-8 weeks after stopping), asthma and aspirin-exacerbated respiratory disease, no antithrombotic within 24 h of IVT; alternatives clopidogrel, anticoagulation, non-oestrogen contraception. Placed after echo and monitoring (it informs secondary prevention). |
| B | major | `initial_tool_outputs.mri` | FLAIR "hyperintense ... subacute" for an infarct of today's episode 2 hours before arrival (plan C12); report described post-contrast sequences while the criterion orders a non-contrast stroke protocol. | FIXED: frontoparietal lesion acute with faint FLAIR change less conspicuous than DWI; contrast statements replaced (no mass lesion; normal sinus flow voids); impression names the MCA-ACA border-zone infarct and the temporally distinct late subacute pallidal infarct. |
| B | minor | `initial_tool_outputs.ct` | NCCT template management text ("does not justify withholding treatment", "Nothing on this study contraindicates intravenous thrombolysis", "clinically implicated territory"); the 2-week-old pallidal infarct seen on MRI was absent on CT. | FIXED: template removed; finding of an 8 mm subacute hypodensity in the left globus pallidus; numbered impression with ASPECTS 10. |
| A | minor | `initial_tool_outputs.labs` | "Exclusion studies" panel with leaking `clinical_significance`; TSH summary interpretive ("suboptimal thyroid replacement"). | FIXED: panel removed (plan C9); summary factual. |
| C | major | follow-ups and criterion `action-6-interpret-labs` | Hypercoagulability panel (with a weakly positive lupus anticoagulant), an orphan autoimmune panel and a "connective tissue screening" filed as `interpret_labs` (physical signs, an echo aortic root and a genetic panel as lab rows). Thrombophilia testing is not indicated in a traumatic dissection (plan C9). | FIXED: all three follow-ups and the criterion removed. The clinical connective tissue findings moved to the exam (normal habitus, no skin hyperextensibility or atrophic scars, Beighton 3/9) and key evidence; the aortic root (2.8 cm) moved to the TTE. `difficulty_description` no longer cites the lupus anticoagulant. |
| D | minor | echo follow-up | "All values within normal limits." as impression; LAVI without unit; no `echo_type`. | FIXED: real normal TTE report (plan C11); `echo_type` TTE in output and `tool_parameters`, trigger `request_tte_echocardiogram`. |
| A | minor | Holter follow-up | Impression concluded "No arrhythmic source for cardioembolism"; not timed after admission (plan C2). | FIXED: opens "Recorded on the stroke unit after admission, 24 hours."; rhythm description only. |
| C | minor | criteria tiers and order | Literature recommended (wrong label about thrombolysis windows); drug check placed and phrased as a thrombolysis checklist; echo and Holter required (plan 3.1: recommended here); hard NCCT-to-drug-check constraint; stop rule allowance 0. | FIXED: order NCCT, labs, ECG, CTA, MRI (optional), EEG (optional, kept for the seizure question), TTE, monitoring (recommended, alternatives holter_24h/holter_48h/telemetry), drug check (required), literature (optional, last). Soft constraints NCCT before CTA, CTA before echo and monitoring. Stop rule: NCCT, labs, ECG, CTA, drug check; `max_additional_actions` 1. |
| C | minor | literature follow-up | Unverifiable "Debette S, Leys D ... 2022"; Biller 2014 statement (on manipulative therapy) cited for connective-tissue screening. | FIXED: CADISS (2015), TREAT-CAD (Engelter 2021), Debette and Leys (Lancet Neurol 2009); general summary only. |
| C | minor | `ground_truth.differential`, `red_herrings` | Cardioembolic left low after normal TTE and Holter; red herrings not tied to case values. | FIXED: cardioembolic very low; seizure entry explains seizure or limb-shaking as a manifestation of the dissection; red herrings name the EEG pattern and TSH 5.8. |
| E | minor | `key_clinical_evidence`, citations, `metadata.case_body_concerns` | Generic template lines (thrombectomy pathway, TOAST, three "Off-pathway modality" lines, "Tier per the July 2026 clinical review", "T1 fat-saturated MRI of the neck" which the case never obtains); free-text guideline string and `[AHA_ASA_2019]`/`[AHA_ASA_2014]` duplicates; stale "no output" concern. | FIXED: key evidence rebuilt from case data; one key per source; concern deleted. |
| B | minor | `initial_tool_outputs.ecg.interpretation` | "No evidence of structural heart disease" (an ECG cannot say so). | FIXED: rhythm and intervals only. |

## Changes, in one paragraph a physician can read before re-reviewing

The CTA impression now leads with the left ICA dissection (flap, mural haematoma, over 70% stenosis C2 to skull base) and is flagged as contrast-enhanced. NIHSS is recounted to 2 (face 1, language 1), with the dominant-hand weakness that the scale misses stated beside it. The case now decides reperfusion: IV thrombolysis is given at about 2 hours because the hand deficit prevents her return to laboratory work (disabling) and neither the extracranial dissection nor the tonic posturing at onset contraindicates it; thrombectomy is not indicated. Management: stroke unit with telemetry and avoidance of hypotension, antithrombotic therapy for at least 3 months starting after 24 hours and a clean scan (aspirin or anticoagulation, CADISS and TREAT-CAD), repeat vessel imaging, stop the combined pill (MEC 4) with TSH recheck, EEG and antiseizure treatment only for recurrent episodes, and sport restriction. The thrombophilia, autoimmune and "connective tissue" lab follow-ups are gone (the clinical connective tissue findings are in the exam), the MRI FLAIR now matches a 2-hour-old infarct alongside the 2-week-old pallidal infarct, which the CT now also shows, and the NCCT, echo and Holter reports are plain reports.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonym list contains "moyamoya disease" and "moyamoya" (and "lacunar stroke", "cardioembolic stroke"), which are wrong for a carotid dissection; fix in `diagnosis_synonyms.yaml`.
- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` (plan section 1.1).
- `EchoReport` drops the `echo_type` field (see ISCH-STR-P05 log); echo follow-ups route by trigger only.

## Open questions for Andrea (judgment calls you could not settle)

- Thrombolysis rests on calling an NIHSS 2 dominant-hand deficit disabling because it prevents her return to work (the AHA/ASA definition includes return to work). If R2 judges it non-disabling, the decision becomes no thrombolysis with immediate antiplatelet therapy, and the door-to-needle, BP and 24-hour-delay musts and prohibitions 2 and 3 change accordingly.
- The plan's index gives NIHSS 3; the recount from the exam is 2. If R2 counts the resolved slurring or the hand weakness, the decision does not change.

## Verification

Adversarial verifier, 23 October 2026. Checked: the CTA impression note (ef70fcc1), `contrast_used`, NIHSS 2 recount, removal of the thrombophilia, autoimmune and connective-tissue follow-ups, echo and Holter reports, the drug check against the medication list, the MRI FLAIR wording against a 2-hour LKW, the CT pallidal finding the worker added, and every reperfusion statement.

Found and changed (major):
- The worker's decision to give IV thrombolysis ignored the case's own prior ischaemic stroke: the episode 2 weeks ago is an infarct (subacute left pallidal infarct on the NCCT the worker added and on MRI, and key evidence item 3 calls it "from the episode 2 weeks ago"). IV thrombolysis within 3 months of a prior ischaemic stroke may be harmful, and today's deficit is mild (NIHSS 2) and was already improving per the HPI. Changed to no thrombolysis:
  - `required_recommendations[3]`: decision now "do not give" with those reasons; the dissection and the tonic onset are stated as not being the reason; thrombectomy unchanged.
  - Former `required_recommendations[4]` (door-to-needle, pre- and post-IVT BP) removed.
  - Antithrombotic must (now `[5]`): start at once after CT excludes haemorrhage, instead of after 24 hours post-IVT.
  - `prohibited_recommendations[1]` ("Do not withhold IV thrombolysis ...") replaced by "Do not give IV thrombolysis" with the prior-stroke reason; `[2]` (no antithrombotic within 24 h of IVT) replaced by the canonical C5 no-reperfusion BP text (BP 128/74).
  - `key_clinical_evidence[1]` ("not a contraindication") and `[3]` (disabling, thrombolysis indicated) rewritten to match; `metadata.difficulty_description` no longer says the deficit is disabling.
  - Drug-check follow-up warning about the 24-hour post-IVT delay replaced by "Start only once brain imaging has excluded intracranial haemorrhage."; criterion `action-9-check-drug-interactions` expected evidence drops the post-IVT clause.

The worker's open question on "disabling" is superseded by this. Open question for Andrea: the class of the AHA/ASA 2026 recommendation on IVT after an ischaemic stroke within 3 months should be confirmed against the guideline text (the 2019 guideline rated it potentially harmful); the case text states "may be harmful" without a class.

`perfect_agent.py ISCH-STR-RM01 -v` passes; `case_io.py check` clean for the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
"moyamoya" (I63.232) is now scoped to P02; dissection labels scoped to this case.
- labels removed: "embolic stroke", "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke", "moyamoya disease", "moyamoya"
- labels added: "carotid artery dissection", "internal carotid artery dissection", "cervical artery dissection"
- codes removed: I63.4, I63.5, I63.3, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.23
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Must added: atorvastatin 80 mg for LDL 108 mg/dL (AHA/ASA 2021 COR 1, SPARCL), paired with non-oestrogen contraception (decision OQ4g). The no-IVT decision for the ischaemic stroke 2 weeks earlier is kept (decision OQ2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
