# NPH: November 2026 decisions

Lead decisions for the 36 R1 notes (NB-KSC3-TWUA-QDTM) on the 30 NPH cases, written 17 Nov 2026.
There are no R2 notes and no approved NPH cases (`work/approved.txt` has no NPH line). The plan
(`plans/NPH.md`) applies these decisions case by case; D-numbers are referenced there.

Sources verified on 17 Nov 2026 (web search; no case text was searched):
- Relkin N et al., Diagnosing idiopathic normal-pressure hydrocephalus, Neurosurgery
  2005;57(3 Suppl):S4-S16 (`[Relkin_2005]`), Table 2.1 as reproduced by the Hydrocephalus
  Association (hydroassoc.org, "INPH Guidelines, Part II"). **Probable** iNPH needs no antecedent
  event (head trauma, intracerebral haemorrhage, meningitis, other known cause of secondary
  hydrocephalus). **Possible** iNPH explicitly allows symptoms that follow remote events such as
  mild head trauma, a remote haemorrhage, or childhood and adolescent meningitis, "or other
  conditions" judged by the clinician. I could not confirm the exact closing words ("not likely to
  be causally related") from the search, so the cases paraphrase and do not quote them.
- Kopp SL et al., ASRA evidence-based guidelines, 5th edition, Reg Anesth Pain Med 2025, doi
  10.1136/rapm-2024-105766 (`[ASRA_2025]`), through the Guideline Central summary: high-dose
  (therapeutic) apixaban and rivaroxaban are stopped at least 72 hours before a neuraxial puncture;
  a drug-specific (apixaban or rivaroxaban calibrated anti-Xa) level may be checked if the
  interval is shorter (IIC). The ASA ACE sample question treats apixaban 5 mg twice daily for AF as
  the high-dose regimen. The renal-function-dependent intervals were not readable in the summary, so
  the cases say only that reduced renal clearance prolongs the interval and give no CrCl cut-off.
- Douketis JD et al., ACCP perioperative antithrombotic guideline, Chest 2022 (`[ACCP_2022]`):
  no heparin bridging during DOAC interruption (unchanged from October).
- Nakajima M et al., Japanese iNPH guideline, 3rd edition, Neurol Med Chir (Tokyo)
  2021;61:63-97, PMC7905302 (`[Nakajima_2021]`), section on shunt complications: shunt
  dysfunction from obstruction, headache, shunt infection and subdural haematoma associated with
  over-drainage; over-drainage complications are more common with LP than VP shunts; programmable
  valves recommended for safety.
- Northup PG et al., AASLD 2020 practice guidance, Vascular liver disorders, portal vein
  thrombosis and procedural bleeding in patients with liver disease, Hepatology 2021;73(1):366-413,
  doi 10.1002/hep.31646 (new key `[AASLD_2020]`): the INR should not be used to gauge procedural
  bleeding risk in cirrhosis in patients not on a vitamin K antagonist; no prophylactic plasma
  before common procedures; an individualised approach to severe thrombocytopenia; correct
  modifiable risk factors before procedures. I did not verify how the guidance classifies lumbar
  puncture, so the cases do not state a procedure-risk class.
- Höglinger GU et al., MDS clinical diagnostic criteria for PSP, Mov Disord 2017;32(6):853-864,
  doi 10.1002/mds.26987 (new key `[Hoglinger_2017]`): O1 vertical supranuclear gaze palsy (level 1),
  O2 slow velocity of vertical saccades, vertical more than horizontal (level 2), O3 square-wave
  jerks or eyelid apraxia (level 3). Slowed vertical saccades are a core feature that can support
  PSP without a gaze palsy.
- 2024 AHA/ACC/ACS/ASNC/HRS/SCA/SCCT/SCMR/SVM guideline for perioperative cardiovascular
  management for noncardiac surgery, Circulation 2024, doi 10.1161/CIR.0000000000001285 (new key
  `[AHA_ACC_perioperative_2024]`), section 4.3: routine stress testing is not recommended in
  low-risk patients or those with adequate functional capacity (class 3, no benefit); stress
  testing only where it would be appropriate independently of the planned surgery. The author list
  was not verified, so the key cites the guideline by title and DOI.

## D1. Shunt referral wording (notes 7f90233f, 8bb5643e, 2cd1748b, 6abe35f0; class in all 30)

Decision: FIXED as a class in all 30 cases. The referral must becomes "Refer to neurosurgery for
shunt eligibility assessment ...", and a positive tap supports shunt consideration but does not
decide surgery. Reason: a tap or drainage response is a prognostic test, with a PPV of 73% to 100%
and limited sensitivity [Marmarou_2005]. The AAN grades shunting only "possibly effective"
[Halperin_2015]. Surgery is a shared decision taken after neurosurgical assessment and counselling,
and the complications are real [Nakajima_2021]. Measured: "for CSF shunting" is in 30 of 30 NPH
musts and in no other condition (31 neurosurgery-referral musts in 600 cases; the other is
ISCH-STR-P02, an unrelated referral). The programmable valve stays as a conditional clause ("if a
shunt is placed"), because it is a grade 1B recommendation [Nakajima_2021] and not a reason to
operate. M06 keeps its own reason for a programmable valve (risk of a recurrent subdural collection
with over-drainage). Conflicts with October C11 (canonical "Refer to neurosurgery for CSF
shunting"), which was written without physician input. The physician's ruling wins, and no
guideline says the opposite.

## D2. Pre-shunt counselling on benefit, risks and complications (same notes; class in all 30)

Decision: FIXED in all 30. Every case has one counselling must naming (a) the expected benefit
(gait most likely to improve), the case's own limits on it, and the uncertainty of the degree, and
(b) the procedural risks and complications: shunt obstruction needing revision, infection, headache
and subdural haematoma from over-drainage [Nakajima_2021]. Where a counselling must already exists
(M01, M03, M05, M07, M09, P01, P02, P03, P04, S02), rewrite it into this form and keep its
case-specific content. Otherwise add one. Measured: 26 of 30 cases have no must mentioning risk or
complication, and only 10 have a counselling must at all. Reason: notes M01, M02, M04 and M05 make
counselling mandatory, and "one note is a class". The complications list is the guideline's own.

## D3. Overstated benefit (note c5685e22; class in 8 cases)

Decision: FIXED. M09 takes the note's wording: shunting "may improve the hydrocephalus-related gait
and functional decline, but the degree of recovery is uncertain", and the deficits from the
diffuse axonal injury may persist, with no promise of cognitive recovery. The same class ("shunting
is expected to improve/reverse ...") is in M03, M05, M07, P01, P02, P03 and P04. These become "is
more likely to improve A than B, and the degree of improvement is uncertain", merged with D2.
Measured: 8 NPH musts. The only hit in the other 570 cases, ALZ-EARLY-M04, quotes a patient's
belief, not a claim, so it is not the class. Reason: shunt response is probabilistic
[Halperin_2015] [Marmarou_2005].

## D4. "While awaiting surgery" in the falls must (own finding, class of D1; 28 cases)

Decision: FIXED. "while awaiting surgery" becomes "while the neurosurgical assessment is pending" in
the 28 cases that have it (all but M07 and P05). Reason: the phrase presumes the operation that D1
says is not automatic. No other text changes.

## D5. Exercise stress testing is low-yield (notes dc2b866b, 89a27997; class in 29 + echo 30)

Decision for dc2b866b: FIXED as a class. Add the avoided action
`avoid-waste-exercise-stress-test` (severity `waste`), alternative
`order_specialized_test {"test_type": "exercise_stress_test"}`, to the 29 cases that store the
`request_exercise_stress_test` follow-up (all but P09). Add it to P09 too, so the label is uniform;
there it matches the library answer, which is harmless. The rationale says there is no cardiac
symptom or independent indication for ischaemia testing, treadmill exercise is unsafe with this
gait disorder and comes out submaximal and non-diagnostic, and cardiac testing belongs to an
independent indication or the anaesthetic preoperative assessment, not the neurological work-up
[AHA_ACC_perioperative_2024]. No criterion credits the test in any NPH case, so nothing conflicts.
Severity is `waste`, not `harm`: the note says "low-yield", and the stored report shows a test
stopped safely with a harness. The stored follow-up stays: it prevents a contradicting library
normal.

Decision for 89a27997: ALREADY-FIXED for the scoring. `avoid-waste-3-order-echocardiogram` is a
wildcard over `order_echocardiogram`, so the exercise echo already counts as waste and no criterion
credits it. Because the note asks for an explicit classification, FIXED for the wording in all 30:
the echo waste rationale gains a clause naming exercise stress echocardiography, with the same
reason and citation.

Elsewhere: 5 cases in other conditions store an exercise stress test with no label (BACT-MEN-RS03,
GBS-RS16, SYNC-CARD-P02, SYNC-CARD-RM01, SYNC-CARD-S06), and 5 SYNC-CARD cases credit one (where it
can be indicated). This is reported to the orchestrator, not acted on here.

## D6. Pre-LP safety gate on a DOAC (notes 6687fd88 M03, 444d9998 M06, 664f524a S10)

Decision: FIXED, in two parts. These are the only 3 cases among all 600 with a DOAC or warfarin and
a required `analyze_csf` (measured).
1. **Tool-level gate.** The labs criterion `action-3-interpret-labs` (id kept) becomes
   **required**, with alternatives `{"panels": ["CBC", "BMP"]}`, `{"panels": ["CBC", "CMP"]}` and
   `{"panels": ["CBC", "creatinine"]}`. It gets the label "Renal function and blood count before
   the lumbar tap on <apixaban/rivaroxaban>", a **hard** sequence constraint labs before CSF, and a
   place in `stop_rule.required_before_assessment`. Reason: confirming the hold itself is history
   (time of last dose), which no tool represents. Renal function sets DOAC clearance and the
   platelet count sets bleeding risk, so these are the orderable parts of "assess renal function
   and bleeding risk" (note 6687fd88). A hard constraint is right because a large-volume puncture
   on an anticoagulated patient whose clearance and platelets are unknown is the unsafe order
   ROUND_POLICY means. A DOAC level is not required: with a 72-hour hold, ASRA needs none.
2. **Must.** The DOAC must gets the canonical text in the plan (section 2, C6). It covers the last
   dose at least 72 hours before the tap; renal function and blood count checked; and that a normal
   INR or PT does not show the drug has cleared. If the interval is shorter, the tap is postponed
   or a drug-calibrated anti-Xa level is checked [ASRA_2025]. The restart rules stay unchanged
   (restart no sooner than 24 h, no heparin bridging, weighed against CHA2DS2-VASc)
   [ASRA_2025] [ACCP_2022]. The existing prohibition "Do not perform the lumbar tap while
   <drug> is active" stays.

Conflicts with October: the October lab tiers ("26 optional, 4 recommended, none required") and
the pack's "exactly two sequence constraints". October reasoned from Reviewer 1's July ruling that
labs are optional because "blood tests do not diagnose NPH". That ruling concerned diagnostic labs.
A procedural-safety prerequisite is a different question, and the same reviewer now asks for it.
The physician wins, and no guideline is against it. S10's note asks for a hard constraint
"requiring confirmation that apixaban has been withheld". The hard constraint on the safety labs
plus the must is the closest checkable form, so the ruling is FIXED, with the limit stated in the
log: the hold time itself is asserted in the must, not by a tool.

## D7. Cirrhosis bleeding-risk review before the tap (note 7c5ef56c, M08)

Decision: FIXED.
- `action-3-interpret-labs` becomes **required**. Keep both alternatives (CBC + coagulation, with or
  without ammonia). Add a **hard** constraint labs before CSF and put the criterion in the stop
  rule.
- Relabel the criterion "Platelet count, coagulation and bleeding-risk review before the lumbar
  tap in cirrhosis". Its citation `[Relkin_2005]` is wrong for this purpose (ruling 8) and becomes
  `[AASLD_2020]`. Its `expected_evidence` cites only CBC and coagulation (platelets 88, INR 1.4, PT
  15.6 s), not the ammonia, which the second alternative does not order (SKILL_NOTES, lab
  payloads).
- Add a must: "Before the lumbar tap, review the platelet count (88 x10^9/L), the INR (1.4) and the
  clinical bleeding risk (Child-Pugh B cirrhosis, varices on propranolol); no routine platelet or
  plasma correction is needed, and the INR does not measure procedural bleeding risk in cirrhosis
  [AASLD_2020]".
- Prohibition 3 and the key-evidence line cite "usual thresholds (platelets 50 or more, INR 1.5 or
  less)" without a source. The INR threshold contradicts AASLD 2020. Reword both: "Do not
  transfuse platelets or plasma routinely before the lumbar tap: a platelet count of 88 x10^9/L is
  not severe thrombocytopenia, and an INR of 1.4 does not measure procedural bleeding risk in
  cirrhosis [AASLD_2020]".

This revises October's F9 ("platelets 50 or more and INR 1.5 or less are the usual thresholds") for
the INR part: in cirrhosis, the current hepatology guidance says not to use the INR.

## D8. M08 diagnosis label and the idiopathic alternative (note 730a2ee7)

Decision: FIXED (a label change, CENTRAL for the synonyms).
- `accepted[0]` "Secondary normal pressure hydrocephalus, post-meningitic arachnoiditis" becomes
  "Normal pressure hydrocephalus, possibly secondary to prior meningitis". `icd_codes[0]` G91.0
  stays (communicating hydrocephalus).
- "idiopathic normal pressure hydrocephalus" and "iNPH" leave `diagnosis.rejected` (case data).
- CENTRAL: the `G91.0+meningitic` entry accepts "normal pressure hydrocephalus", "NPH",
  "idiopathic normal pressure hydrocephalus" and "iNPH", with code G91.2.
- The differential's iNPH entry goes from `low` to `moderate`, with key_features saying the
  meningitis was 8 years before onset with full recovery, so a causal link is possible but not
  shown.
- Every "arachnoiditis" claim goes (key evidence [0]). The referral must names "normal pressure
  hydrocephalus, possibly secondary to the pneumococcal meningitis".

Reason: arachnoiditis is not demonstrated (no imaging or CSF sign of it). Relkin 2005 reserves the
antecedent exclusion for **probable** iNPH. **Possible** iNPH allows a remote antecedent judged
unlikely to be causal, and an adult meningitis 8 years before onset, with full recovery, is such a
judgement call.

Conflict with October section 1 ("an antecedent excludes iNPH", bare NPH labels removed from the
secondary cases): re-examined. The October premise is right for probable iNPH only. The guideline
itself provides the possible category, so the physician's ruling wins. The October rule stays for
M06 (SDH evacuation 14 months before onset) and M09 (severe TBI 8 months before): there the
antecedent is recent and plainly causal, and no note asks otherwise.

## D9. P05: post-SAH preferred, iNPH acceptable (note f6b2546c)

Decision: FIXED (CENTRAL for the synonyms).
- `accepted[0]` stays. "idiopathic normal pressure hydrocephalus" and "iNPH" leave `rejected`.
- CENTRAL: the `G91.0+sah` entry accepts the bare and idiopathic NPH labels and G91.2.
- The differential's iNPH entry goes to `moderate`, saying the decline began about 2.5 years after
  a good recovery with no documented interval ventricular enlargement.
- Prohibition 1 ("Do not label the hydrocephalus idiopathic ...") contradicts the ruling. It is
  replaced by: "Do not dismiss the remote aneurysmal SAH with intraventricular extension: it is the
  most likely cause of the communicating hydrocephalus, although a decline that began about 2.5
  years after a good recovery also fits possible iNPH [Relkin_2005]".
- Key evidence [0] is reworded to the same effect.

Reason and the conflict with October: as D8. A Fisher 4 SAH with IVH is a strong antecedent, so the
preferred label stays secondary, as the note says. Accepting iNPH follows Relkin's possible
category for a remote haemorrhage.

## D10. P03 cervical spine MRI required (notes 3e7e8482, 3cc428d0)

Decision: FIXED.
- `action-spine-mri` goes from recommended to **required** and is added to
  `required_before_assessment`.
- No sequence constraint is added: the order relative to the tap does not matter for safety.

Reason: a progressive gait and bladder decline with bilateral Babinski and Hoffmann signs, 3+
lower-limb reflexes and spasticity after a C3-C6 fusion is a red flag for recurrent or
adjacent-segment compression. That is a treatable alternative, and the stop rule must not let an
agent close the case before addressing it.

Conflict with October C14 (recommended): October set the tier before any physician input. The
ruling wins.

M04 is not in the class: its exam has no upper motor neuron sign ("No hyperreflexia ... No
Babinski ... no myelopathy signs"), so its spine MRI stays recommended (measured: P03 is the only
NPH case with a spine criterion and bilateral UMN signs).

## D11. P08 extended drainage recommended, not required (notes 6eedd7f8, 9ea36124, ff859687)

Decision: FIXED.
- `action-extended-lumbar-drainage` goes from required to **recommended**. Its id leaves
  `required_before_assessment`, and the soft tap-before-drainage constraint stays.
- Must [0] becomes the note's wording: "After a single tap test without objective improvement,
  consider extended lumbar drainage (about 10 mL/hour, 300 to 500 mL over 72 hours, with daily timed
  gait measures) or another appropriate specialist assessment, because a negative tap test does not
  exclude shunt-responsive iNPH (tap sensitivity 26% to 61%, drainage 50% to 100%)
  [Marmarou_2005]".
- Must [1] becomes the D1 referral form. It rests on the full syndrome, the DESH MRI and the
  normal-pressure CSF, and adds the drainage response only if the drainage was done.
- Red herring [0]'s "extended lumbar drainage is the next test" becomes "extended drainage or
  another specialist assessment can be considered".

Reason: Marmarou 2005 presents drainage as a supplementary prognostic test, not a mandatory one. A
DESH MRI has a high PPV [Nakajima_2021], so a shunt-eligibility referral after a negative tap is
reasonable when the evidence is compelling. The options in note ff859687 are kept as options.

Conflict with October (drainage required once `lumbar_drain` landed): the ruling wins.

## D12. P07 PSP prohibition (note 1af93709)

Decision: FIXED. Prohibition [1] becomes: "Do not keep PSP as the working diagnosis on the mild
slowing of upward saccades and the falls: slowed vertical saccades can support PSP
[Hoglinger_2017], but here the slowing is mild, upward only, with normal downward saccades and full
range, the falls are forward, the midbrain-to-pons ratio is 0.55 [Massey_2013], and the DESH MRI
and the 32% tap response support iNPH".

The same implication is in red herring [0] ("Without a vertical supranuclear gaze palsy or midbrain
atrophy ... the PSP label is not supported"). It becomes: "The only eye finding is mild, nonspecific
upward-saccade slowing; with a midbrain-to-pons ratio of 0.55, DESH and a 32% tap response, PSP is
less likely and iNPH is the diagnosis".

Unchanged: the differential's PSP entry (low, with reasons) and red herring [1] carry no such
implication.

This is consistent with October's flag to the physicians (MDS-PSP O2). The reviewer keeps iNPH, so
no label change follows.

## D13. Thyroid confirmation as a must (note 49b4998b; class M04)

Decision: FIXED in S08 and M04 (measured: the only two NPH musts that demand a lab result).
- S08 must [1] becomes "Continue levothyroxine 75 mcg daily unchanged". M04 must [2] becomes
  "Continue levothyroxine 100 mcg daily unchanged".
- The labs criteria stay **recommended**, as the note asks.
- The S08 prohibition "Do not attribute ... to hypothyroidism when thyroid function is normal on
  replacement" stays: it is conditional and requires no result.

Kept: M07's "Replace vitamin B12 and recheck MMA" is a treatment of an abnormal result the
recommended labs find, and the cobalamin deficiency is a real contributor to gait and cognition. It
is not "confirm a normal value", and no note objects to it. NO-ACTION, recorded so that a worker
does not extend D13 to it.

## D14. P06 contrast (note b4648379)

Decision: ALREADY-FIXED by class MRI-CONTRAST (`plans/MRI-CONTRAST-decisions.md`).
- The initial MRI is the plain study (`contrast_used: false`, no gadolinium text).
- The follow-up `request_contrast_mri` is the gadolinium study (`contrast_used: true`, with "No
  leptomeningeal, ependymal or parenchymal enhancement").
- The required MRI criterion asks for `{"contrast": true}`.

`mri_probe.py NPH-P06` (17 Nov) serves the contrast report to the criterion. No other NPH MRI states
gadolinium content with `contrast_used` not true (scan of initial, follow-up and fallback MRIs).

## D15. Approvals of the chief complaint (15 notes)

Decision: NO-ACTION. These notes say "tutto ok" (all fine), "bene così" (fine as it is), "ottimo"
(excellent), "bene" (good), "ok", "okok" or "niente da segnalare" (nothing to report):
f9899f54 (M07), 8c33ff13 (M10), d61c8272 (P01), ccbaf98b (P02), ee99bd6b (P04), 70c405eb (P09),
52729570 (S01), 01c52d0d (S02), 0cec7b8c (S03), 46348ed9 (S04), cb213a41 (S05), 9d68c312 (S06),
bdd1a3d0 (S07), 03abb2d3 (S09), 272fa1bf (S11). The chief complaints are not touched.

## D16. Stale tier counts in `metadata.difficulty_rationale` (own finding, 30 of 30)

Decision: FIXED. Every case's rationale still counts the post-tap reassessment as recommended, which
it has been required since October. P08 also counts the drainage as recommended. After the edits,
each worker recounts the tiers from `action_criteria` and rewrites the counts. `metadata` is shown
to physicians.

## D17. Diagnosis certainty wording of the iNPH labels (considered, no change)

The iNPH labels do not say "probable". The round rule asks for certainty wording, but it also
forbids changing `accepted[0]` without a reviewer ruling, and no note asks for it. NO-ACTION; listed
as an open question for the next review.

## D18. New citation keys

`[AASLD_2020]`, `[Hoglinger_2017]` and `[AHA_ACC_perioperative_2024]` (sources above) are used in
the cases. The NPH criteria pack's allow-list needs them, and its tiers need updating (post-tap
required; labs required as a pre-tap safety check in M03, M06, M08 and S10; P03 spine MRI
required; P08 drainage recommended; shunt-eligibility referral wording). This is a CENTRAL request
for the pack and for the review-app guidance responses (`condition_tool_guidance.yaml`, generated
by `build_condition_tool_guidance.py`). No test checks case citations against the pack (grep of
`agent-platform/tests`).
