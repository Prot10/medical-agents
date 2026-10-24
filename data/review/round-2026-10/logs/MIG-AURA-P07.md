# MIG-AURA-P07
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance applied through the plan (structured ICHD-3 history required; echo kept here as embolic-source work-up). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.chief_complaint` | "right eye visual field now has permanent defect" while the deficit is a left homonymous hemianopia (plan P07). | FIXED: "the left visual field defect has not recovered". |
| D | major | `patient.history_present_illness`, `patient.hpi` | HPI gave the infarct size (3.5 x 2.5 cm), DWI/ADC detail and the outside report's "embolic occlusion" differential while brain MRI is a required criterion. | FIXED: HPI keeps only that the inpatient MRI showed an acute right occipital infarct (the basis of the label she arrives with); size and the radiology quote removed. Added that inpatient telemetry and a 24-hour Holter showed sinus rhythm (the history behind "no AF"). |
| A | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI fragments (one truncated with "..."), generic red flags, placeholder scores, impression mentioning MELAS. | FIXED: habitual attacks (12 years, shimmering crescent spreading over minutes, 20-30 min, about monthly; 5 of 6) separated from the index attack (typical onset, deficit persisting 6 weeks); medicines, vascular risk, examination and red flags; impression: fits ICHD-3 1.4.3 only if no other cause (criterion D). |
| D | major | `initial_tool_outputs.mri` | Impression reported the original MRA ("possible right PCA occlusion, now recanalised") (class K); DWI "established restriction... T2 shine-through" at 6 weeks. | FIXED: MRA text removed; DWI no restriction with ADC increased; technique, comparison, no other-territory infarct, no haemorrhagic transformation; numbered impression. |
| C | major | `ground_truth.action_criteria` (new `action-mra`), `followup_outputs[0]` | No vessel imaging although the label turns on stroke mechanism (plan class K: MRA required). | FIXED: `order_advanced_imaging` `MR_angiography` required; follow-up: normal intracranial and cervical MRA, right PCA patent. |
| B | major | `followup_outputs[1]`, `action-7` | Criterion asked `bubble_study` while the output was a TOE (plan P07). | FIXED: TTE with agitated saline chosen (first-line study in a young stroke); output `echo_type: bubble_study`, structurally normal heart, normal LA, no valve disease (relevant to DOAC eligibility), small PFO with Valsalva, no atrial septal aneurysm. Trigger renamed. |
| D | major | `followup_outputs[3]` (ILR) | Event note "confirms paroxysmal AF as cardioembolic source" (diagnostic conclusion in a monitor report); `findings` empty. | FIXED: report-voice event, findings and numbered impression (43 min AF on day 17); duration stated as the first 30-day download. Trigger renamed `request_implantable_loop_recorder_30d` so a 30-day monitor order also reaches it. |
| B | major | `followup_outputs[2]` (new) | Without it, a 24-hour Holter, 48-hour Holter, telemetry or 14-day monitor order was answered with the ILR report (AF on day 17), an impossible result for a short recording that would also hand the diagnosis to a cheap study. | FIXED: added a short-recording follow-up (sinus rhythm, no AF) matched by those monitor types, placed before the ILR in the pathway. Checked: holter_24h, holter_48h, telemetry and 14d get it; ILR and 30d get the ILR report. |
| C | major | `initial_tool_outputs.labs`, `action-5` | Placeholder labs ("Within reference range", no units) (class L); the antiphospholipid panel named in the criterion was not answered; no renal function or blood count although a DOAC is the plan. | FIXED: real values: lupus anticoagulant (dRVVT and SCT ratios) negative, aCL and anti-beta2GPI IgG/IgM below 20, FBC, creatinine 68 umol/L, PT/APTT, glucose, HbA1c, lipids. Criterion `recommended` with alternatives `antiphospholipid` or `lupus_anticoagulant` (plan said optional; see Open questions). |
| C | major | `initial_tool_outputs.drug_interactions`, `action-2` | Criterion used `{"context": ...}` (unreachable); the initial "general" block was empty with a summary equal to the expected evidence (guard leak); a follow-up DOAC check gave CHA2DS2-VASc rules. | FIXED: one stored check under `apixaban` (served for any drug): DOAC with aspirin, NSAIDs, paracetamol, CYP3A4/P-gp drugs; DOACs unsuitable in APS, mechanical valve or mitral stenosis, pregnancy; triptans contraindicated after stroke; apixaban dose-reduction rule; renal and FBC monitoring. Alternatives apixaban, rivaroxaban, edoxaban, dabigatran, aspirin. The follow-up DOAC block was deleted. Guard now passes. |
| C | major | `followup_outputs` (literature) | Literature stated migrainous infarction as "1.4.1" (it is 1.4.3) with an invented "<10 mm" size rule; invented Broderick 2007 paper; Sanna 2014 misquoted ("30-day ILR... 12-15%"); a rehabilitation search with a wrong "automatic DVLA Category I revocation" statement. | FIXED: one literature follow-up, last: ICHD-3 1.4.3 criteria (including D) and CRYSTAL AF (8.9% at 6 months, 12.4% at 12 months vs 1.4% and 2.0%). The rehabilitation search was deleted; the driving advice is now a must. |
| C | major | `ground_truth.action_criteria` | Literature required with an exact query; MRI pinned `contrast: false, protocol: stroke`; ILR and echo labels identical to rationales with `[AAN_2000]`; no constraints; stop rule with literature, max 0. | FIXED: literature optional `{}` last; MRI `{}`; ILR alternatives ILR or `event_monitor_30d`; order history, MRI, MRA, labs, echo, ILR, drug check, literature; soft constraints history before MRI, MRI before MRA, echo and monitoring; stop rule: the six required criteria, max 1. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts terse ("Switch from aspirin to DOAC", "Initiate migraine preventive therapy"); no dose or timing; no contraception or pregnancy advice on a DOAC; DVLA vague. | FIXED: seven musts: revised diagnosis with ICHD-3 1.4.3 D; DOAC now, stop aspirin, CHA2DS2-VA 2 (ESC 2024), apixaban 5 mg twice daily with the dose-reduction check, no further delay at 6 weeks; no triptans or ergots, paracetamol plus antiemetic, avoid regular NSAIDs; discuss prevention (AHS 2021: acute treatments contraindicated); contraception without oestrogen, copper IUD or LNG-IUS, no pregnancy on a DOAC; visual rehabilitation and occupational health; no driving and DVLA notification. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | No prohibition of the aspirin-plus-DOAC combination or of PFO closure, although the echo shows a PFO. | FIXED: aspirin alone or added to the DOAC prohibited; PFO closure prohibited (AF explains the stroke). Triptan and combined contraception prohibitions kept. |
| C | major | `ground_truth.differential` | Migrainous infarction left `moderate` after the AF finding (class F); APS entry cited a "weakly positive aCL" that no output contains. | FIXED: migrainous infarction low (criterion D fails; code G43.609); PFO paradoxical embolism low (small shunt, no ASA, AF stronger); dissection/vasculopathy very low (normal MRA); APS very low (negative panel). |
| E | minor | `ground_truth.key_clinical_evidence` | Three "Tier per the July 2026 clinical review" / "July 2026 review" sentences (class D). | FIXED: deleted; key evidence rebuilt from the case data. |
| E | minor | `ground_truth.red_herrings` | Entries 2 and 3 had empty `field_path`; entry 3 cited a weakly positive aCL absent from the data (class E). | FIXED: three red herrings: the migrainous infarction label, the typical aura at onset (both HPI), and the small PFO (`followup_outputs[1].output.impression`). |
| A | minor | `fallback_tool_outputs.advanced_imaging`, `.specialized_test` | Junk fallbacks (class M). | FIXED: null; kinds removed from `metadata.fallback_tool_kinds`. EEG, CT and CSF normal fallbacks kept (they match avoided actions). Avoided-action rationales rewritten for this case. `metadata.condition_name` em dash replaced. |

## Changes, in one paragraph a physician can read before re-reviewing

A 41-year-old woman with 12 years of typical visual aura had an infarct during an attack, was labelled migrainous infarction and now has a persistent dense left homonymous hemianopia. The chief complaint now says left visual field. The HPI no longer gives the infarct size or the outside report's differential. The pathway is: structured history (habitual aura 5 of 6; the index attack fits migrainous infarction only if criterion D holds), brain MRI (established 3.5 x 2.5 cm right PCA infarct, no other territory; the MRA text is gone), MR angiography (new, required, normal), blood tests (recommended: negative antiphospholipid panel, normal renal function and blood count before anticoagulation), TTE with bubble study (structurally normal heart, small PFO without septal aneurysm), loop recorder (43 minutes of paroxysmal AF on day 17), the DOAC interaction check (required) and an optional literature search with ICHD-3 1.4.3 and CRYSTAL AF. A short Holter or 14-day monitor ordered by an agent now returns sinus rhythm, not the loop-recorder result. Musts: revised diagnosis; apixaban 5 mg twice daily now with aspirin stopped (CHA2DS2-VA 2, ESC 2024); no triptans or ergots and NSAIDs avoided on the DOAC; discuss prevention; contraception without oestrogen and no pregnancy on a DOAC; visual rehabilitation and work support; no driving and DVLA notification. Prohibitions add aspirin plus DOAC and PFO closure. Migrainous infarction is now low in the differential, with PFO, dissection and APS low or very low on the stored results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.1): the I63 group appended to this case accepts "lacunar stroke", "lacunar infarct" and plain "stroke", which credit a wrong mechanism; restrict to cardioembolic and ischaemic stroke labels.
- Citation keys (plan 5.3): `[ESC_AF_2024]`, `[AHA_ASA_2021_secondary]`, `[AHS_2021]`, `[UKMEC_2016]`; also a key for CRYSTAL AF (Sanna T et al., NEJM 2014;370:2478-2486). Cited by name in text until they exist.
- MockServer: `order_cardiac_monitoring` has no discriminator, so any monitor order is served the first matching stored recording. This case needed a second (short-recording) follow-up so a 24-hour Holter does not return the loop-recorder AF. Consider a duration-aware rule centrally (a stored ILR should not answer a 24-hour order).
- Guidance claims (plan 5.5): P07 gains MRA and keeps echo.

## Open questions for Andrea (judgment calls you could not settle)

- Labs tier: the plan table says labs optional for P07. I made them recommended because antiphospholipid syndrome is a stroke mechanism in a young woman and makes a DOAC unsuitable, and renal function and a blood count are needed before choosing and dosing the DOAC. Decision made; recorded for the lead.
- Composition (plan section 6.1): cardioembolic stroke case under MIG-AURA, kept as a mimic case with its own label per the plan default.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MIG-AURA. Checked: chief complaint, exam, MRI (right PCA) and hemianopia (left) laterality agree; CHA2DS2-VA 2 for the stroke in a 41-year-old woman (ESC 2024) supports a DOAC; apixaban dose-reduction criteria and creatinine 68 umol/L agree; UKMEC after stroke (CHC 4, LNG-IUS 2, copper IUD 1) agrees with the contraception must; CRYSTAL AF figures (8.9% vs 1.4% at 6 months, 12.4% vs 2.0% at 12 months) are correct; MRA, bubble TTE and ILR criteria, outputs and triggers agree; the short-recording follow-up keeps a 24-hour Holter from returning the ILR result; antiphospholipid values are real and negative; the labs tier change to recommended is clinically justified and logged; differential, red herrings (`followup_outputs[1]` is the echo) and key evidence match the outputs; the PFO-closure and aspirin-plus-DOAC prohibitions do not conflict with any must.
Found and fixed: the PFO entry in `ground_truth.differential` said "no venous thrombosis" although no venous study is in the case; now "no known venous thrombosis and no Valsalva at onset".
Noted, not changed: the short-recording follow-up is a 24-hour Holter report that also answers a 14-day monitor order (the MockServer has no duration discriminator; already under CENTRAL in this log). perfect_agent and case_io check clean; leak guard passes.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `ground_truth.assessment.required_recommendations[3]`: candesartan was offered to a woman who can become pregnant without the pregnancy caution that M06, P03 and S04 carry (candesartan is fetotoxic). Added "(only with reliable contraception, as it is contraindicated in pregnancy)", so the class Q cautions read the same across the condition.

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x2.
- synonyms: generic stroke labels, "embolic stroke" (would credit paradoxical embolism through the small PFO), "lacunar stroke", "lacunar infarct", plain "stroke" and "PCA territory infarct" (would credit migrainous infarction) removed; mechanism labels kept or added (cardioembolic stroke/infarct/infarction, atrial fibrillation stroke/infarct); codes now I63.4, I63.43, I63.431 (I63.432 is the left PCA; I63.5, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89 and I63.9 name other or unspecified mechanisms).
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
