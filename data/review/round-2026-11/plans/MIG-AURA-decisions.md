# MIG-AURA: decisions, November 2026 round

Lead decisions for the 63 R1 notes (NB-KSC3-TWUA-QDTM) on the 30 MIG-AURA cases, written 16 Nov
2026. No MIG-AURA case is approved (`work/approved.txt` has none). Each entry gives the note ids, the
decision, the reason and the citation. "Oct" means the October 2026 decisions
(`data/review/round-2026-10/plans/MIG-AURA-decisions.md`) or plan. Sources were checked on 16 Nov 2026
unless they come from the October allow-list (pack section 8).

New sources verified this round:
- `[FSRH_DI_2022]` FSRH CEU Guidance: Drug Interactions with Hormonal Contraception (May 2022),
  https://www.cosrh.org/Common/Uploaded%20files/documents/drug-interactions-with-hormonal-contraception-5may2022.pdf.
  It says to consider topiramate a potential enzyme inducer at any dose. During use of a teratogen
  that is or may be an enzyme inducer it recommends the Cu-IUD, the LNG-IUS or the progestogen-only
  injectable (DMPA), and it does not recommend the progestogen-only pill or the etonogestrel implant.
  NHS topiramate pregnancy prevention programme documents (BSW formulary, Lancashire and South
  Cumbria, 2024-2025) apply it: Cu-IUD, LNG-IUS, or DMPA used with condoms.
- `[MELAS_2026]` Mancuso M, Bellusci M, Carelli V, et al. Diagnostic criteria and management of
  MELAS and stroke-like episodes: consensus-based statements. Eur J Neurol 2026;33(4):e70588,
  doi 10.1111/ene.70588 (ERN-NMD Delphi, 54 statements). Verified: "EEG is an important early
  investigation of acute SLE" (100% agreement); antiseizure medicines are started promptly when
  seizures are suspected during an SLE; and a statement that there are no specific
  contraindications to the standard acute headache drug classes (NSAIDs, triptans, paracetamol).
  The search snippets did not show the exact wording of its valproate statement.
- InterERNs Mitochondrial Working Group consensus on seizures in primary mitochondrial disease
  (Eur J Neurol 2024, abstract checked). Standard antiseizure medicines may be used, with named
  exceptions: valproate in POLG disease, vigabatrin in GABA-transaminase deficiency, and topiramate
  where there is a risk of renal tubular acidosis.
- NICE CG109, Transient loss of consciousness ('blackouts') in over 16s (2010, updated 2023):
  1.1.3 says to record a 12-lead ECG for everyone with TLoC and to take a witness account.
- Powers WJ et al., 2019 AHA/ASA guideline for the early management of acute ischaemic stroke,
  Stroke 2019;50:e344-e418. Brain imaging on arrival, and noninvasive intracranial vessel imaging
  when endovascular therapy is contemplated (Class I).
- NICE NG128, Stroke and TIA in over 16s (2019, updated 2022): urgent specialist assessment of
  suspected TIA. The diagnosis is clinical.

Scorer fact used in several entries: recommended and optional criteria are credited and never
count as "extra" for the stop rule (`policy_reward.py` lines 138-146, comment "Recommended and
optional criteria are still credited, so they never count as extra"). Only actions that match no
criterion use `max_additional_actions`.

---

## D1. LIT: literature steps rejected (25 notes)
Notes: 2a94bbb7 (M01), 01f7876b (M02), 9664e97f (M03), 9e6fc9af (M04), fca3be91, 8763368b (M05),
b641b8e0 (M06), a6bcf14f (M07), ce7ba35d (M08), af4ad7e1 (P01), bf5d87c0 (P02), 32b921e6 (P03),
fb7dfc9b (P04), 6f780f04 (P05), 26305ba4 (P06), 895b9b5c (P07), 6ee45bc0, 252c9961 (P08),
8d56a61f (P09), 27cd7328 (RM11), 72ca20f5 (S06), b32b7c1a (S07), a36f4096 (S08), 70750e29 (S09),
4929a69f (S11).
Decision: FIXED by class LIT (commit 393c547e). Checked by script: no MIG-AURA case has a string
`search_medical_literature` anywhere, which covers criteria, follow-ups and stored outputs. Workers
re-check their case and add nothing back.
Reason: ROUND_POLICY 5; November addendum item 1.

## D2. PRAISE: approvals of the chief complaint (8 notes)
Notes: a7893337 (S01), 9328b8dc (S02), eed597bc (S03), b33228a7 (S04), f65505f9 (S05),
69bca92e (S08), 96e9ad91 (S09), f6ee93eb (S11).
Decision: NO-ACTION. These are approvals. The chief complaints stay unchanged.

## D3. TOPIRAMATE-CONTRACEPTION: the implant is not adequate with topiramate (6 notes; class)
Notes: 4ed3d3c1 (M04), 16e768ca (M06), e903ea4c (P03), f1d9b692 (RM11), 801e6db7 (S07),
5b8ab438 (S10).
Decision: FIXED. Replace the October class Q text everywhere with this canonical must:
> If topiramate is chosen, start it only under the topiramate pregnancy prevention programme with a
> contraceptive method unaffected by enzyme induction: a copper IUD, a levonorgestrel IUS, or
> medroxyprogesterone acetate injection used with condoms. Topiramate is treated as a potential
> enzyme inducer at any dose, so pills and the etonogestrel implant are not adequate.

Apply the same fact in the other places where the class appears (measured, 9 more fields):
- RM11 PRO[1] ("offer an IUD or an implant").
- P03 initial `drug_interactions.sumatriptan.warnings[2]` ("IUD or implant").
- Drug reports that give the 200 mg/day threshold without the FSRH caution: M04 FU0 warnings[1] and
  FU2 interactions[1]; M06 FU0 warnings[1] and FU1 interactions[2]; P03 initial interactions[4];
  P04 initial interactions[1]; S10 FU0 warnings[0]; RM11 initial interactions[0]. In each, keep the
  pharmacological fact (the evidence is for doses of 200 mg/day or more) and add "FSRH advises
  treating it as a potential enzyme inducer at any dose".

S10 also: the partner's vasectomy (HPI) is relevant to the programme. Add to S10's topiramate must:
"her partner's vasectomy counts only if he is her sole partner and azoospermia was confirmed after
the procedure; otherwise use one of the methods above."
Not changed: the "stop the combined pill and switch to a progestogen-only pill, implant, IUS or
IUD" musts (M01, M02, M04, M06, S07, P03 and others). They concern the aura (UKMEC 2 for the
implant), not topiramate.
Oct conflict: this replaces Oct plan class Q ("IUD or implant preferred"). That text rested on no
interaction source; FSRH 2022 says otherwise, and R1 is right.
Citation: [FSRH_DI_2022]; [MHRA_topiramate_2024].
Cross-condition: across the 600 cases, topiramate and the implant appear together only in
MIG-AURA (24 cases mention topiramate).

## D4. TIA-CERTAINTY and ANTITHROMBOTIC musts (M01, M03, P01 notes; class across 10 cases)
Notes: faa8bb3e (M01), 30f0b036 (M03), b37e0b4d (P01). Also the basis for D5 (P02) and D6 (P05).
Measured: the canonical prohibition "Do not start antiplatelet or anticoagulant therapy for presumed
TIA ... and imaging shows no infarct" appears in 7 cases (M01, M03, M05, P01, P09, RS11, S09). Musts
that order antithrombotic withdrawal: M03 REQ0, P01 REQ1, P02 REQ1, P05 REQ1. Text claiming that
imaging excludes or distinguishes TIA: M05 REQ0 ("MRI show no sign of TIA"), P01 REQ0 ("normal
imaging distinguish it from TIA") and P01 accepted[0] ("after TIA exclusion"). Text claiming that
sinus rhythm proves the mechanism: P02 REQ0, P02 action_criteria[3] rationale and P02 PRO0.
Decision (FIXED):
1. Rule: no text may say or imply that MRI, MRA or a normal DWI excludes TIA, or that sinus rhythm
   during an episode excludes cardioembolism. The aura-versus-TIA distinction is clinical (positive
   symptoms, spread over minutes, succession, headache, stereotyped previous attacks). Imaging
   excludes infarction and arterial disease.
2. First-presentation cases (M01, M03, P01, RS11): delete the TIA prohibition and use a conditional
   must instead. Canonical form:
   > Base the antithrombotic decision on the clinical assessment: the episode has the features of
   > migraine aura (<features>), and the MRI excludes an infarct but cannot exclude TIA; no
   > antiplatelet is needed unless the assessment leaves a real suspicion of ischaemia, in which
   > case manage it on the TIA pathway.
   Where aspirin was already started (M03, P01) the must becomes:
   > Review the aspirin started for possible TIA once the cerebrovascular evaluation is complete:
   > stop it if the episodes are judged to be migraine aura and there is no other indication;
   > continue it if a TIA remains a real possibility; explain the decision to the patient and the GP.
   M01 REQ1 drops "so the TIA pathway and antiplatelet therapy are not needed" and states the
   same conditional.
3. Established recurrent-identical-attack cases (M05, P09, S09): keep the prohibition, reworded so
   that it rests on the clinical features and states the DWI limit:
   > Do not start antiplatelet or anticoagulant therapy on the TIA label alone: the stereotyped
   > attacks have the features of migraine aura (<features>); a normal MRI excludes infarction, not
   > TIA, so the decision rests on these features.
4. M05 REQ0, P01 REQ0 and P01 accepted[0]: rewrite per rule 1. P01 label: "after TIA exclusion"
   becomes "TIA judged unlikely on the clinical features" (label change; CENTRAL list, no synonym
   edit needed).
5. Allow cerebrovascular evaluation without requiring it (R1, M01). Add an optional criterion
   `action-vessel-imaging-optional` (alternatives `order_advanced_imaging` `MR_angiography` and
   `carotid_duplex`; the library normal answers) in M01 and M05, the first-episode and new-pattern
   cases without vessel imaging. Optional criteria are credited and never extra. No avoided action
   may match these calls; neither case has one now.
6. P01: MRA goes from recommended to required, with a soft constraint MRI before MRA. The aspirin
   decision R1 asks for needs the cerebrovascular evaluation: a first aura at 52 with isolated
   aphasia is the presentation where TIA must be worked up (NICE NG128; pack section 7). It joins
   the stop rule.
Reason: R1's ruling agrees with the pack's own DWI fact (pack section 1) and with NICE NG128 (the
TIA diagnosis is clinical). A categorical prohibition in a first episode overstates certainty.
Oct conflict: this replaces Oct class G's canonical prohibition for the first-presentation cases.
Oct had already corrected "normal DWI excludes TIA"; the remaining overstatement is the unconditional
wording.
Citation: NICE NG128; [ICHD_3]; [AHS_neuroimaging_2020].

## D5. P02: loop recorder and apixaban (2 notes)
Notes: 316f77a5 (ILR), 5ea76cbc (apixaban).
Decision (both FIXED):
- Remove `action-5-order-cardiac-monitoring` (ILR required) from the criteria, the stop rule and
  sequence constraint [1]. AF is already documented on the GP Holter, and AF stroke risk does not
  depend on AF being present during an episode, so the ILR answers no management question. Add an
  avoided action, waste: `order_cardiac_monitoring` `{"monitor_type": "implantable_loop_recorder"}`,
  rationale "AF is already documented; an implanted recorder adds no information that changes the
  anticoagulation decision, which rests on CHA2DS2-VA". The ILR follow-up stays as stored data for an
  agent who orders it.
- Make brain MRI required, since it is now the discriminating study: silent embolic infarcts would
  make the episodes ischaemic and the score 2. MRA stays recommended. Stop rule: clinical assessment,
  MRI, drug check.
- REQ1 becomes: "Review apixaban with cardiology after the neurological reassessment: if the
  episodes are accepted as migraine aura, CHA2DS2-VA is 0 and ESC 2024 does not recommend
  anticoagulation; if a TIA cannot be confidently excluded the score is 2 and anticoagulation
  continues." REQ0: the clinical features and the MRI without infarct favour aura, and sinus rhythm
  during an episode does not by itself exclude cardioembolism. PRO0 ("loop recorder shows ... sinus
  rhythm") is deleted. accepted[0] drops "nocturnal" and "AF and aphasic episodes temporally
  dissociated on implantable loop recorder" and becomes "Migraine with aphasic aura (ICHD-3 1.2.1)
  co-existing with paroxysmal atrial fibrillation (alcohol-related)". required_components are
  unchanged. Rewrite differential[0], key_clinical_evidence[0,2], red_herrings[0] and the metadata
  `condition_name` / `difficulty_description` (metadata is shown to physicians) without ILR causality.
Oct conflict: Oct Q3 kept "stop apixaban" and the ILR as required. ESC 2024 sets anticoagulation by
CHA2DS2-VA but does not settle whether the episodes are TIAs, and the score depends on that. The
physician's ruling wins (November addendum). Alcohol reduction (Voskoboinik 2020) stays.
Citation: [ESC_AF_2024]; NICE NG128.

## D6. P05: warfarin, INR and the TIA label (2 notes)
Notes: 93326a8a (current INR, bleeding, Hb), 794bf874 (unconditional diagnosis and warfarin stop).
Decision (both FIXED):
- New criterion `action-labs-inr-fbc`, required, alternatives `interpret_labs`
  `{"panels": ["coagulation", "CBC"]}`, `{"panels": ["coagulation"]}` and `{"panels": ["CBC"]}`.
  Store `initial_tool_outputs.labs` with today's values: PT and INR 3.6 (still above range, under
  4.5, so the existing severity must stays valid), aPTT and fibrinogen normal, Hb 124 g/L
  (115-155), platelets 238, WBC 6.4, MCV 88. Set `fallback_tool_outputs.labs` to null; it held the
  old 3.8, and the library answers other assays. Add the criterion to the stop rule. Place it after
  the clinical assessment in the criteria order.
- accepted[0] becomes "Migraine with aphasic aura (ICHD-3 1.2.1), previously labelled TIA;
  supratherapeutic INR with minor bleeding on warfarin". This drops "misdiagnosed" and "warfarin
  should be stopped". The rejected TIA labels stay: the case still scores aura, not TIA, as the
  diagnosis.
- REQ1 is split into: (a) "Withhold warfarin now: INR above range with gum and nose bleeding; no
  bridging"; and (b) "Make the decision not to restart anticoagulation with the referring team
  after reviewing the original rhythm strip: with the attacks attributed to aura and no AF on the
  outside Holter or the 14-day monitor, there is no indication (CHA2DS2-VA 0, ESC 2024), and no
  antiplatelet replacement is needed unless that review finds a real suspicion of ischaemia."
- REQ0: "explain ... and ask the GP and referring team to review the TIA label" instead of
  "so that the TIA label is removed".
- PRO0 becomes: "Do not continue warfarin at the current dose with an above-range INR and mucosal
  bleeding, and do not replace it with an antiplatelet for presumed TIA without new evidence of
  ischaemia."
- REQ2 (management by severity) stays; it now cites today's INR.
- Differential[0] and key_clinical_evidence[2] drop "whatever it shows" and state the conditional.
Citation: Tran HA et al., Med J Aust 2013;198:198-199 (already in the case); [ESC_AF_2024].

## D7. Stop-rule notes (5 notes)
Notes: d33fb521 (M03), fee18a5b (M07), 335b1fbd (S10), 91145af1 (RS11), and the stop-rule part of
f5f97597 (P08).
Decision:
- M03, M07 and S10: ALREADY-FIXED. The MRI, MRA and drug-check criteria the notes name are
  recommended, so they are credited and never count against `max_additional_actions` (scorer fact
  above). A trace with both studies, or with the drug check, has stopping 1.0. No change.
- RS11: FIXED. MRI and MRA are already allowed. The uncredited ECG gets a criterion (D10).
- P08: FIXED by the EEG criterion (D11).

## D8. DX-CERTAINTY: preventive therapy wording (M06 note; class M04)
Note: 1b2dc411 (M06).
Decision: FIXED. M06 accepted[0]: "preventive therapy required" becomes "preventive therapy to be
considered and discussed". M06 REQ2: "Offer prevention" becomes "Discuss prevention, weighing
disability, preference, comorbidity and drug risks". Apply the class to M04 (3 attacks in 4 months):
"preventive therapy indicated" becomes "preventive therapy to be considered", and REQ3 changes in
the same way. AHS 2021 lists brainstem aura and prolonged aura under "consider", not under "offer".
S10 stays "indicated": 2-4 severe attacks a month with MIDAS IV meet the AHS "offer" threshold.
Label changes go on the CENTRAL list; no synonym edit is needed.
Citation: [AHS_2021].

## D9. M08: sertraline causation (1 note)
Note: 034920f8.
Decision: FIXED. accepted[0] becomes "Migraine with visual and somatosensory aura (ICHD-3 1.2.1),
onset after starting sertraline (causal role uncertain); sertraline-sumatriptan co-administration
acceptable with counselling". REQ3 becomes: the temporal association does not establish cause; the
father's and sister's migraine suggest susceptibility; the earlier brief flashes in one eye are too
poorly characterised to count as aura; continuing sertraline is reasonable if the depression is
responding, with any change agreed with her prescriber, while acknowledging that its contribution
is uncertain. Reword key_clinical_evidence[1] and red_herrings[0].correct_interpretation in the
same way.
Citation: [ICHD_3] (an aura is defined by its features, not by a trigger).

## D10. RS11: blackout, ECG and label (2 notes)
Notes: 19601077, 91145af1.
Decision (both FIXED):
- New criterion `action-ecg`, required, `analyze_ecg` `{}`, in the stop rule. Store
  `initial_tool_outputs.ecg`: sinus rhythm 70, PR 162 ms, QRS 92 ms, QTc 416 ms, no pre-excitation,
  no Brugada pattern, no conduction disease. "Normal ECG" is the interpretation. Reason: NICE CG109
  1.1.3 requires a 12-lead ECG for everyone with TLoC, and the Brugada pattern is relevant in an
  East Asian man.
- The clinical assessment's Consciousness finding gets a witness account. Colleague: found
  slumped at his desk, unresponsive to voice; no limb jerking, tongue bite or incontinence seen;
  consciousness returned gradually over about 15-20 minutes in the ambulance. This is consistent
  with the HPI and adds no new diagnosis.
- accepted[0] becomes "Sporadic hemiplegic migraine (ICHD-3 1.2.3.2): two attacks of gradual motor
  and sensory aura followed by headache, with decreased consciousness in the second attack".
  "All secondary causes excluded" goes. key_clinical_evidence[2] becomes "compatible with hemiplegic
  migraine once the witness account and ECG give no other cause".
- EEG and Holter stay unlisted, with no avoided action. They fall within the one extra action
  allowed; R1 says to order them according to findings, not routinely.
- The TIA prohibition becomes the D4 conditional must (first presentation).
Citation: NICE CG109; [ICHD_3].

## D11. P08: MELAS drug rules and EEG (3 notes)
Notes: 64c11ceb (valproate, metformin), 7dd02d6c (triptans), f5f97597 (EEG).
Decision:
- 7dd02d6c FIXED: delete PRO1 (no triptans or ergots after a stroke-like episode). [MELAS_2026]
  states that there are no specific contraindications to the standard acute headache classes,
  triptans included, and an SLE is not an ischaemic stroke, so the label's stroke contraindication
  does not apply. Do not add a must that requires a triptan. The acute plan (if one is written)
  names an NSAID or paracetamol, and a triptan as acceptable. Oct conflict: Oct Q3 kept the
  prohibition on expert opinion only; the 2026 consensus supersedes it.
- 64c11ceb FIXED in part: PRO0 becomes "Do not use valproate: it is contraindicated in POLG disease,
  is best avoided in other mitochondrial disease when alternatives exist (levetiracetam,
  lamotrigine, lacosamide), and she can become pregnant (MHRA)". The prohibition stays for this
  patient, on patient-specific grounds (InterERNs 2024; MHRA valproate). R1's general point is
  applied, but the conclusion for her is unchanged. Metformin leaves the prohibition list. REQ4
  becomes "prefer an agent other than metformin if diabetes develops (risk of lactic acidosis in
  mitochondrial disease)". DECLINED part: removing all valproate restriction. Reason: she is 29 and
  can become pregnant (MHRA 2024 valproate rules apply whatever the mitochondrial question), and a
  safer alternative exists.
- f5f97597 FIXED: new criterion `action-eeg`, recommended, alternatives `analyze_eeg` with
  `eeg_type` `routine`, `ambulatory` and `video`. Add a routine EEG follow-up (right
  parieto-occipital slowing, no epileptiform discharges or electrographic seizures, the same
  findings as the stored ambulatory and video records; trigger `request_routine_eeg`) so a routine
  order is not answered by the library normal. Rationale: confusion with the episode 10 days ago
  and still "slightly slow to respond"; [MELAS_2026] (EEG an important early investigation in an
  SLE). It is not in the stop rule and is not required (the episode is not acute now).
- The MELAS key: add `[MELAS_2026]` to the pack (CENTRAL) or cite it in rationale text.

## D12. P07: certainty of the cardioembolic mechanism (1 note)
Note: a219ebf2.
Decision: FIXED. accepted[0] becomes "Ischaemic stroke in the right PCA territory, probably
cardioembolic from paroxysmal AF found on an implantable loop recorder, occurring during a migraine
episode; not migrainous infarction (an alternative cause is present); switch aspirin to DOAC".
REQ0 becomes: migrainous infarction is not diagnosed because AF provides a probable alternative
mechanism (ICHD-3 1.4.3 criterion D), and the aetiology is probable rather than proven. The DOAC
must stays (AF with stroke, CHA2DS2-VA 2, regardless of causality). The synonym scoping from Oct
section 1 is untouched (labels and codes keep I63.4).
Citation: [ICHD_3]; [ESC_AF_2024].

## D13. P09: sporadic, not probable (1 note)
Note: befb9ef9.
Decision: FIXED. accepted[0]: "Hemiplegic migraine (probable sporadic, ICHD-3 1.2.3)" becomes
"Sporadic hemiplegic migraine (ICHD-3 1.2.3.2)"; the rest of the label stays. The data show five
attacks of motor and speech aura and no affected first- or second-degree relative. P09 has a
`hemiplegic_migraine` gene-panel criterion (optional); that stays optional.
Class: M03 "Probable sporadic hemiplegic migraine (ICHD-3 1.2.3)" is a single motor attack, so
"probable" is right but the code is wrong. Change the code reference to "(ICHD-3 1.5.2)". RM11:
D15.
Citation: [ICHD_3] 1.2.3.2 and 1.5.2.

## D14. P03: review of the outside MRI (2 notes; e903ea4c is D3)
Note: 19136208.
Decision: FIXED. The criterion stays required, because ICHD-3 1.4.3 needs imaging of the infarct in
the relevant area and `analyze_brain_mri` is the only route. Label and rationale become "Review the
outside brain MRI (DWI/ADC, 3 days after the attack) to confirm the infarct and its location
against the aura; repeat only if the images are inadequate". The stored MRI output becomes the
formal neuroradiology review of the imported outside study: a 4 mm focus of restricted diffusion
with low ADC in the right occipital cortex, acute infarct, no other lesion, no haemorrhage. It is
no longer a new 4-week scan. expected_evidence follows. This also removes the contradiction in the
rationale ("outside report not available, so repeated" versus "images imported"). The HPI line "The
outside report is not with her today" stays: the images are obtained, the report is not. Run
`mri_probe.py`.
The label clause "all secondary causes excluded" stays in P03. Four required studies (MRA,
30-day monitor, bubble echo, antiphospholipid panel) support it, unlike RS11.
Citation: [ICHD_3] 1.4.3.

## D15. RM11: emergency pathway, label certainty and history (3 notes; f1d9b692 is D3)
Notes: 1ea8561d, 0efba9dd.
Decision 1ea8561d (FIXED):
- `encounter_type` becomes `emergency` (3-hour ED presentation).
- New criterion `action-arterial-imaging`, required, alternatives `order_advanced_imaging`
  `MR_angiography` and `order_ct_scan` `{"angiography": true}`. Store an MRA follow-up (normal
  intracranial and cervical arteries, no occlusion, stenosis or dissection). Move the CT to
  `initial_tool_outputs.ct` as a stroke-protocol report: non-contrast CT (no haemorrhage, no
  established infarct, subtle left hemispheric sulcal effacement) plus `angiography_findings` (no
  large-vessel occlusion). CT is not routed by `angiography`, so one report answers both orders.
  Soft constraint: MRI before arterial imaging is not added (either order is acceptable in the ED).
  Add the criterion to the stop rule.
- Delete avoided_actions[0] (head CT waste). Emergency CT is standard in a 3-hour persistent deficit.
- New musts: (a) "Manage as suspected acute stroke until imaging decides: urgent stroke-team
  assessment within the treatment window; reperfusion is not indicated once MRI shows no restricted
  diffusion and arterial imaging no occlusion"; (b) "Admit for neurological and seizure observation;
  treat a seizure lasting over 5 minutes or recurrent seizures with a benzodiazepine and then a
  second-line agent per the status epilepticus protocol, and decide on an antiseizure medicine
  according to recurrence and the EEG (lamotrigine would also serve as the preventive)".
- The EEG (required) already covers non-convulsive status.
Decision 0efba9dd (FIXED): the HPI records the earlier attacks as headache with arm weakness
only. Do not add historical aura features. Correct clinical_assessment findings[4] to: "previous
attacks: motor weakness with headache documented; accompanying visual, sensory or speech symptoms
not recorded. Current attack: motor with visual and speech aura (1.2.3 B met in this attack). No
affected relative." Fix the impression to match. accepted[0] becomes "Probable sporadic hemiplegic
migraine (ICHD-3 1.5.2) with seizures during the aura, suspected migraine aura-triggered seizures
(ICHD-3 1.4.4), and left hemispheric cortical swelling without infarct; venous thrombosis excluded".
REQ0 uses the same certainty and adds "confirm with the clinical course and the repeat MRI". The
rejected label "focal epilepsy" stays. The answer must not be focal epilepsy, but the differential
entry for focal epilepsy moves to `low` with "not excluded by an EEG showing focal slowing only;
reassess on follow-up". PMH "Sporadic hemiplegic migraine, diagnosed at age 22" stays as recorded
history.
Oct conflict: Oct section 1 added migralepsy to the label. It is kept but qualified ("suspected"),
as R1 asks, because ICHD-3 1.4.4 criterion C (not better accounted for) is not yet met.
Citation: Powers 2019 AHA/ASA; [ICHD_3] 1.2.3, 1.4.4, 1.5.2; NICE CG137 / ESO status epilepticus
practice (benzodiazepine first line).

## D16. P04 and P06: scope of NOTCH3 testing (2 notes)
Notes: 95362414 (P04), 7e1924c9 (P06).
Decision P04 (FIXED):
- The NOTCH3 output becomes a targeted test of the familial variant: "Targeted Sanger analysis of
  NOTCH3 exon 4 for the familial variant c.457C>T p.(Arg153Cys): not detected". No exon 2-24
  sequencing and no CNV analysis.
- `action-5-order-specialized-test` goes from required to recommended (offered after counselling;
  she may decline) and leaves the stop rule.
- Brain MRI review goes from recommended to required and joins the stop rule. The family CADASIL
  history is a red flag, and the MRI pattern (no anterior temporal or external capsule involvement)
  is the non-invasive answer.
- REQ0 stays (counselling, option not to test). REQ1 and REQ2 are made conditional: the MRI shows
  no CADASIL pattern; if she chooses testing, absence of the familial variant excludes CADASIL in her
  and her children.
- The label stays: the stored targeted result supports "CADASIL excluded by NOTCH3 testing".
Decision P06 (FIXED): the output becomes targeted testing for the familial c.544C>T p.(Arg182Cys)
(detected, heterozygous, pathogenic). It no longer says "Sanger sequencing of exons 2-24". The
criterion label becomes "Targeted NOTCH3 testing for the familial variant, after pre-test
counselling and consent"; the tier stays required (he is symptomatic). Add a must: "Discuss the test
with him before it is sent (pre-test counselling and consent), including what a result means for his
three children".
Vocabulary: `genetic_panel:CADASIL` serves both. No new term is needed (R1's request is about
scope, not a new test).
Citation: [EAN_CADASIL_2020]; VASCERN CADASIL 2023 (pack).

## D17. Other own findings (no note; real defects in scope)
- M01 and M03 differential[0] already say "a normal DWI does not exclude TIA". No change.
- M01 metadata.difficulty_description "first episode requires TIA exclusion": reword to "first
  episode: TIA must be considered". RS11 metadata.condition_name "TIA and epilepsy exclusion" is
  acceptable.
- No other class from the notes exists outside MIG-AURA, except that the 200 mg topiramate
  threshold could appear in other conditions' drug reports. Measured: no non-MIG case links
  topiramate to the implant.

## D18. Declined items, summarised
- 64c11ceb: the general removal of the valproate restriction is DECLINED for this patient (D11).
- No note is declined outright.
