# NPH round plan (November 2026)

Lead plan for NPH-M01..M10, P01..P09 and S01..S11, written 17 Nov 2026.

- Decisions and reasons: `plans/NPH-decisions.md` (D1..D18 below refer to its entries).
- Notes: 36, all from R1 (NB-KSC3-TWUA-QDTM): 21 asking for changes, 15 approvals of the chief
  complaint.
- No NPH case is approved (`work/approved.txt`).

Cases read in full: M03, M08 and P07 (patient, outputs and policy), and P08 (policy, drainage,
evidence, red herrings, metadata). Read in part, through scripted dumps: P05 (history,
differential, evidence), M01 (follow-ups and avoided actions) and M04 and P03 (exam, spine
criterion). The policy of every case was read in `survey.txt`.

Scripts (`/home/aprotani/review-round-2026-11/work/scratch/nph-lead/`):

| file | content |
|---|---|
| `survey_nph.py` / `survey.txt` | every criterion, avoided action, constraint, stop rule, must, prohibition and follow-up trigger of the 30 cases |
| `measure1.py` | antithrombotics, platelets, INR, creatinine and the lab criterion per case |
| `measure2.py` | class counts over all 600 cases (shunt wording, counselling, "awaiting surgery", overstated claims, exercise stress tests, DOAC with a required LP, euthyroid musts, PSP wording, arachnoiditis) |

The MRI contrast scan and the `difficulty_rationale` count check were run inline.

Workers:
- Edit through `case_io` only. Keep every `criterion_id`; new ids are given below.
- After each case, run `perfect_agent.py CASE -v` and `case_io.py check CASE`, and `mri_probe.py`
  if an MRI changed (none planned).
- English in the case's spelling (most NPH ground truth is British: "haematoma", "oesophageal").
  No em dashes in new text. No review-process text in `metadata`.
- After any `rejected` or `accepted[0]` edit (M08, P05), test the answers listed in C8 with
  `DiagnosisCriterion.matches`.
- Update `metadata.revision_reason` (clinical description of the change) and
  `metadata.last_revised` ("2026-11-17").
- Do not touch the chief complaints: 15 of them were approved.

## 1. Governing guidelines and canonical facts

| Key | Source | Governs here |
|---|---|---|
| `[Relkin_2005]` | International iNPH guidelines, Neurosurgery 2005;57(3 Suppl):S4-S16 | Probable iNPH: no antecedent event. **Possible iNPH allows a remote antecedent (mild head trauma, remote haemorrhage, childhood or adolescent meningitis, other conditions) judged unlikely to be causal.** Opening pressure 70 to 245 mmH2O |
| `[Marmarou_2005]` | Neurosurgery 2005;57(3 Suppl):S17-S28 | Tap test sensitivity 26% to 61%, PPV 73% to 100%; extended drainage sensitivity 50% to 100%, PPV 80% to 100%. These are supplementary prognostic tests |
| `[Nakajima_2021]` | Japanese iNPH guideline, 3rd ed., Neurol Med Chir 2021;61:63-97 | DESH, callosal angle, tap protocol, programmable valve (1B). **Shunt complications: obstruction (dysfunction), headache, infection, subdural haematoma from over-drainage; over-drainage is more frequent with LP shunts** |
| `[Halperin_2015]` | AAN practice guideline, Neurology 2015;85:2063-2071 | Shunting "possibly effective" |
| `[ASRA_2025]` | ASRA 5th ed., Reg Anesth Pain Med 2025, doi 10.1136/rapm-2024-105766 | Therapeutic apixaban and rivaroxaban: at least 72 h before a neuraxial puncture; if shorter, a drug-calibrated anti-Xa level may be checked; first dose at least 24 h after; aspirin is not interrupted |
| `[ACCP_2022]` | ACCP perioperative antithrombotic guideline, Chest 2022 | No heparin bridging for a DOAC |
| `[AASLD_2020]` **new** | Northup PG et al., AASLD 2020 practice guidance, Hepatology 2021;73(1):366-413, doi 10.1002/hep.31646 | In cirrhosis (no vitamin K antagonist) the INR does not gauge procedural bleeding risk; no prophylactic plasma before common procedures; individualised approach to severe thrombocytopenia |
| `[Massey_2013]` | Neurology 2013;80:1856-1861 | Midbrain-to-pons ratio below 0.52 is specific for PSP |
| `[Hoglinger_2017]` **new** | MDS PSP criteria, Mov Disord 2017;32(6):853-864, doi 10.1002/mds.26987 | O2 = slow vertical saccades (level 2), which can support PSP without a gaze palsy |
| `[AHA_ACC_perioperative_2024]` **new** | 2024 AHA/ACC multisociety perioperative guideline, Circulation 2024, doi 10.1161/CIR.0000000000001285 | Routine stress testing is not recommended without an independent indication (class 3) |
| `[Tisell_2011]`, `[Williams_2016]`, `[CPIC_tamoxifen_2018]` | as in the pack | unchanged |

Canonical facts this round adds:
- A positive tap or drainage test supports shunt consideration but does not decide surgery (D1).
- A normal INR or PT does not show that apixaban or rivaroxaban has cleared. The hold is timed from
  the last dose, and renal function sets the clearance (D6).
- In cirrhosis, platelets of 88 x10^9/L are not severe thrombocytopenia, and the INR is not a
  bleeding-risk measure (D7).

## 2. Classes

### C1 Shunt referral wording (D1). Notes 7f90233f, 8bb5643e, 2cd1748b, 6abe35f0. Cases: all 30

Measured: "Refer to neurosurgery for CSF shunting" is in 30 of 30 NPH cases (P08 in must [1]) and
in no other condition.

Canonical form, keeping the case's own evidence clause verbatim:

> Refer to neurosurgery for shunt eligibility assessment, on the basis of `<the case's existing
> evidence clause: tap-test improvement of n% in TUG at 24 hours, the MRI, normal-pressure CSF,
> ...>`; the `<tap/drainage>` response supports considering a shunt, with a programmable valve if
> one is placed, but does not by itself decide surgery [Nakajima_2021]

Keep the case-specific tails:
- M06: secondary NPH after the subdural haematomas, with a programmable valve because of the risk
  of a recurrent subdural collection with over-drainage.
- M08: "possibly secondary to the pneumococcal meningitis" (C8), and the hepatology input.
- M09: post-traumatic.
- M10: revisit the lumbar decompression only after the shunt response.
- P05: post-SAH.
- S06: "age 80 and stable coronary disease are not by themselves contraindications".

### C2 Counselling on benefit, risks and complications (D2, D3). Same notes plus c5685e22. Cases: all 30

Measured: 26 of 30 cases have no must on risks or complications. 10 have a counselling must (M01,
M03, M05, M07, M09, P01, P02, P03, P04, S02). 8 of those say "expected to improve/reverse" (M03,
M05, M07, M09, P01-P04).

Canonical must, one per case. Rewrite the existing counselling must where there is one, and keep
its case-specific limits. Otherwise add it after the referral:

> Before the decision on surgery, counsel the patient and family on the expected benefit and the
> risks: gait is the symptom most likely to improve`<, case-specific limit>`, and the degree of
> improvement is uncertain; the complications of shunting include shunt obstruction needing
> revision, infection, headache and subdural haematoma from over-drainage [Nakajima_2021]

Case-specific limits, from the existing musts:

| case | limit to keep |
|---|---|
| M01 | memory and the urinary symptoms (partly BPH) less predictable |
| M03 | not the fixed post-stroke right-sided weakness and circumduction |
| M05 | parkinsonian features less likely to improve: the benefit may be limited by the coexisting PD, which keeps its own treatment |
| M07 | not the proximal weakness and distal sensory loss from neuropathy and lumbar stenosis |
| M09 | the note's text: shunting may improve the hydrocephalus-related gait and functional decline, but the degree of recovery is uncertain; the deficits from the diffuse axonal injury may persist; no promise of cognitive recovery |
| P01 | cognition less likely to improve; AD keeps its own treatment; agree the goals of surgery |
| P02 | bradykinesia, rigidity and tremor less likely to improve; PD keeps its own treatment |
| P03 | the spastic myelopathic features will persist and need their own rehabilitation and spinal follow-up |
| P04 | cognition and behaviour less likely to improve; bvFTD keeps its own management (the goals-of-care must stays separate) |
| S02 | urge incontinence possibly mixed with BPH |
| M06 | add "the risk of a recurrent subdural collection is higher after the bilateral haematomas" (new must) |
| M10 | add "the claudicant or radicular symptoms of the lumbar stenosis are not expected to change" (new must) |
| P09 | add "cognition may improve less than gait" (new must) |
| others | no limit clause (new must) |

In copathology cases, write "is more likely to improve A than B", never "is expected to improve".

### C3 Falls must presumes surgery (D4). Own finding. Cases: 28 (all but M07, P05)

Replace "while awaiting surgery" with "while the neurosurgical assessment is pending". Change
nothing else in the falls must.

### C4 Exercise stress testing low-yield (D5). Notes dc2b866b, 89a27997. Cases: all 30

Measured: 29 cases store `request_exercise_stress_test` with no avoided label (P09 stores none). No
NPH criterion credits it. Exercise echo is stored in all 30 and already matches the wildcard waste
entry `avoid-waste-3-order-echocardiogram` (id `avoid-waste-3-...` in every case).

1. Add this entry to `avoided_actions`, after the echocardiogram entry:
   ```json
   {"criterion_id": "avoid-waste-exercise-stress-test", "severity": "waste",
    "alternatives": [{"tool_name": "order_specialized_test", "required_arguments": {"test_type": "exercise_stress_test"}}],
    "rationale": "<He/She> has no cardiac symptom or independent indication for ischaemia testing, and treadmill exercise is unsafe with this gait disorder and stops submaximal and non-diagnostic; cardiac testing belongs to an independent indication or the preoperative assessment, not to the neurological work-up [AHA_ACC_perioperative_2024]",
    "citations": ["[AHA_ACC_perioperative_2024]"]}
   ```
   Adapt "unsafe with this gait disorder" to the case, e.g. "with freezing" where the exam has
   freezing. S06 (stable CAD after CABG): write "no new cardiac symptom", since the CAD is known
   and stable.
2. Append to the rationale of the echocardiogram waste entry: ", and exercise stress
   echocardiography adds nothing: there is no cardiac indication, and treadmill exercise is unsafe
   with this gait disorder [AHA_ACC_perioperative_2024]". Add the key to its `citations`.
3. Keep the stored follow-ups.

### C5 Tier and stop-rule changes (D10, D11)

- P03 `action-spine-mri`: required, and in `required_before_assessment`.
- P08 `action-extended-lumbar-drainage`: recommended, and removed from `required_before_assessment`.
  Must [0], must [1] and red herring [0] change as in D11. The canonical must [0] is in the per-case
  index.

### C6 Pre-LP safety gate on a DOAC (D6). Notes 6687fd88, 444d9998, 664f524a. Cases: M03, M06, S10

Measured: these are the only cases in the 600 with a DOAC or warfarin and a required `analyze_csf`.
Today none gates the tap: labs are optional `{}`, and no constraint involves anticoagulation.

1. `action-3-interpret-labs`:
   - `importance: required`;
   - alternatives `{"panels": ["CBC", "BMP"]}`, `{"panels": ["CBC", "CMP"]}`,
     `{"panels": ["CBC", "creatinine"]}`;
   - label "Renal function and blood count before the lumbar tap on `<apixaban/rivaroxaban>`";
   - rationale one case-specific sentence (clearance of the drug and bleeding risk before a
     large-volume puncture);
   - citations `["[ASRA_2025]"]`;
   - `expected_evidence` only from the CBC and BMP panels (M03: creatinine 1.0 mg/dL, platelets
     204; M06: creatinine 1.1, platelets 188, haemoglobin 13.4; S10: creatinine 0.9, platelets
     208).
   - Check with a probe that each alternative is served the stored CBC and BMP panels.
2. A new sequence constraint `action-3-interpret-labs` before `action-4-analyze-csf`, `hard`, with
   reason "Renal function and the blood count must be known, and the `<drug>` hold confirmed, before
   a large-volume lumbar puncture in an anticoagulated patient [ASRA_2025]".
3. Add `action-3-interpret-labs` to `required_before_assessment`.
4. Replace the DOAC must with:
   > Before the lumbar tap, confirm that the last dose of `<apixaban 5 mg twice daily / rivaroxaban
   > 20 mg daily>` was taken at least 72 hours earlier, check renal function and the blood count,
   > and review bleeding risk; a normal INR or PT does not show that `<drug>` has cleared, reduced
   > renal clearance prolongs the interval, and if the interval is shorter the tap is postponed or
   > a `<drug>`-calibrated anti-Xa level is checked [ASRA_2025]. Restart it no sooner than 24
   > hours after the tap, without heparin bridging, weighing the interruption against the stroke
   > risk of atrial fibrillation`< (CHA2DS2-VASc n, prior stroke)>` [ASRA_2025] [ACCP_2022]
5. Keep the prohibition "Do not perform the lumbar tap while `<drug>` is active ...".
6. In M03, the lab interpretation lists "INR" as normal. That is data and stays. No text may
   present it as evidence of drug clearance.

### C7 Cirrhosis bleeding-risk review (D7). Note 7c5ef56c. Case: M08

`action-3-interpret-labs`:
- required, both alternatives kept;
- label "Platelet count, coagulation and bleeding-risk review before the lumbar tap in cirrhosis";
- citations `["[AASLD_2020]"]`;
- `expected_evidence` "Platelets 88 x10^9/L, INR 1.4 and prothrombin time 15.6 s".

Also:
- A hard constraint labs before CSF, reason "Platelets, coagulation and the clinical bleeding risk
  of cirrhosis with varices must be reviewed before a large-volume lumbar puncture
  [AASLD_2020]".
- Add the criterion to the stop rule.
- New must, after the referral: "Before the lumbar tap, review the platelet count (88 x10^9/L),
  the INR (1.4) and the clinical bleeding risk (Child-Pugh B cirrhosis, varices on propranolol); no
  routine platelet or plasma correction is needed, and the INR does not measure procedural bleeding
  risk in cirrhosis [AASLD_2020]".
- Prohibition [3] becomes "Do not transfuse platelets or plasma routinely before the lumbar tap: a
  platelet count of 88 x10^9/L is not severe thrombocytopenia, and an INR of 1.4 does not measure
  procedural bleeding risk in cirrhosis [AASLD_2020]".
- The key-evidence line on the thresholds is reworded the same way (no "INR 1.5 or less").

### C8 Remote antecedent: accept the idiopathic reading (D8, D9). Notes 730a2ee7 (M08), f6b2546c (P05)

**M08:**
- `accepted[0]` becomes "Normal pressure hydrocephalus, possibly secondary to prior meningitis".
  `icd_codes[0]` stays G91.0. Log it as a label change.
- Remove "idiopathic normal pressure hydrocephalus" and "iNPH" from `rejected`.
- The differential's iNPH entry becomes `moderate`: "Possible iNPH: the pneumococcal meningitis was
  8 years before onset with full recovery, so a causal link is possible but not shown
  [Relkin_2005]".
- Key evidence [0] becomes: "Communicating hydrocephalus after a remote meningitis may be secondary
  NPH or possible iNPH: arachnoiditis is not demonstrated and the meningitis was 8 years before
  onset; both readings are investigated and shunted by the same route [Relkin_2005]".
- Referral as C1. Grep the case for "arachnoiditis" and "post-meningitic" and reword every claim
  of a proven mechanism.

**P05:**
- `accepted[0]` stays. Remove the idiopathic labels from `rejected`.
- The differential's iNPH entry becomes `moderate`: "the decline began about 2.5 years after a
  good recovery, with no documented interval ventricular enlargement, which also fits possible
  iNPH".
- Prohibition [1] becomes the D9 text.
- Key evidence [0] is reworded: post-SAH communicating hydrocephalus is the preferred reading,
  possible iNPH is acceptable [Relkin_2005].

Until CENTRAL C-SYN lands, an "iNPH" answer simply does not match in these two cases; it is no
longer vetoed.

Test with `DiagnosisCriterion.matches` after the edit:
- "Normal pressure hydrocephalus after pneumococcal meningitis" (M08): should match.
- "Secondary NPH after SAH" (P05): should match.
- "Idiopathic normal pressure hydrocephalus": should not be vetoed (it should match once C-SYN
  lands).
- "Hepatic encephalopathy" (M08): should not match.

### C9 PSP wording (D12). Note 1af93709. Case: P07

Prohibition [1] and red herring [0]: the D12 texts. Nothing else in P07 changes.

### C10 Musts that demand a lab confirmation (D13). Note 49b4998b. Cases: S08, M04

- S08 must [1] becomes "Continue levothyroxine 75 mcg daily unchanged". M04 must [2] becomes
  "Continue levothyroxine 100 mcg daily unchanged".
- The lab criteria stay recommended.
- M07's B12 must stays (D13).

### C11 MRI contrast (D14). Note b4648379. Case: P06. ALREADY-FIXED; no NPH MRI elsewhere has the defect

### C12 Stale `difficulty_rationale` tier counts (D16). Own finding. Cases: all 30

After the edits, recount required, recommended and optional from `action_criteria` and correct the
sentence. Every case currently says "3 required ... 1 recommended" (or similar) while the post-tap
reassessment is required.

### C13 Approvals (D15). 15 notes. NO-ACTION

## 3. Per-case index (all 30; none approved)

Every case gets C1, C2, C3 (unless stated), C4 and C12. The rows below give the notes and anything
specific. "Musts" refers to the current indexes in `survey.txt`.

### NPH-M01
- 7f90233f-8fee-40c4-99d8-cb0f0b741f8d FIXED: C1 on must [0]; C2 by rewriting must [2] (BPH limit) with the risks.
- dc2b866b-98e3-446a-91d5-2d7dbbe2d5d8 FIXED: C4 new avoided entry (the exam has freezing at initiation).
- 89a27997-a823-4886-8463-64e9ae327d6c ALREADY-FIXED (the echo waste wildcard covers the exercise echo); wording FIXED by the C4
  rationale clause.
- Class: C3 on must [1]; C12.

### NPH-M02
- 8bb5643e-93d0-4aaf-b6e3-5eb0350fc63d FIXED: C1 on must [0]; C2 new counselling must (no limit clause).
- Class: C3, C4, C12.

### NPH-M03
- 6687fd88-bd7f-4d34-9df8-392fb9751726 FIXED: C6. Labs required with the CBC+BMP alternatives, a hard labs-before-CSF
  constraint, the stop rule, and the DOAC must [1] in the canonical form (CHA2DS2-VASc 4, prior
  stroke). Prohibition [2] kept.
- Class: C1 on must [0]; C2 rewriting must [3] (post-stroke limit, "expected to" removed); C3 on
  must [2]; C4; C12.

### NPH-M04
- 2cd1748b-b135-4197-9b61-1543654686af FIXED: C1 on must [0]; C2 new counselling must (no limit clause; the gabapentin must
  stays).
- Class C10: must [2] becomes "Continue levothyroxine 100 mcg daily unchanged". Labs stay
  recommended. The spine MRI stays recommended (no UMN signs, D10).
- Class: C3 on must [3]; C4; C12.

### NPH-M05
- 6abe35f0-c07b-4d51-8f0d-a3d964b35adf FIXED: C1 on must [0]; C2 rewriting must [1] with the PD-limited benefit, the
  uncertainty and the risks.
- Class: C3 on must [3]; C4; C12.

### NPH-M06
- 444d9998-c126-4f97-a98a-613aa1a58952 FIXED: C6 with rivaroxaban 20 mg daily. Labs required, hard constraint, stop rule, must
  [1] canonical. Prohibition [1] kept.
- Class: C1 on must [0], keeping the SDH and programmable-valve reason; C2 new counselling must
  (recurrent subdural collection risk); C3 on must [2]; C4; C12.
- Secondary label and rejected iNPH unchanged (D8).

### NPH-M07
- f9899f54-b8ea-4c43-a466-72bf9a41157c NO-ACTION (approval).
- Class: C1 on must [0]; C2 rewriting must [2] (neuropathy and stenosis limit, "expected to"
  removed); C4; C12. There is no falls must "awaiting surgery" (no C3). The B12 must stays.

### NPH-M08
- 730a2ee7-95c9-4064-96ab-5323001426f1 FIXED (label change; CENTRAL C-SYN): C8. New `accepted[0]`, rejected cleaned,
  differential iNPH moderate, key evidence [0] reworded, every "arachnoiditis" removed.
- 7c5ef56c-b1ee-4d52-97c1-063d5104c8d1 FIXED: C7. Labs required, hard constraint, stop rule, citation `[AASLD_2020]`, evidence
  trimmed, new bleeding-risk must, prohibition [3] and the threshold key evidence reworded.
- Class: C1 on must [0] ("possibly secondary to the pneumococcal meningitis", hepatology input
  kept); C2 new counselling must; C3 on must [2]; C4; C12.

### NPH-M09
- c5685e22-da01-4f6c-aa6a-b797c788b10e FIXED: C2 rewriting must [2] with the note's wording plus the risks.
- Class: C1 on must [0] (post-traumatic kept); C3 on must [3]; C4; C12. Secondary label unchanged.

### NPH-M10
- 8c33ff13-943f-40c6-bbea-5205b6ef2695 NO-ACTION (approval).
- Class: C1 on must [0] (keep the lumbar-decompression tail); C2 new counselling must (stenosis
  symptoms not expected to change); C3 on must [2]; C4; C12.

### NPH-P01
- d61c8272-d96c-4cb0-a377-607d928ca24f NO-ACTION (approval).
- Class: C1 on must [0]; C2 rewriting must [1] (cognition limit, goals of surgery kept); C3 on must
  [3]; C4; C12.

### NPH-P02
- ccbaf98b-801f-4d0e-9672-116469836f25 NO-ACTION (approval).
- Class: C1 on must [0]; C2 rewriting must [1]; C3 on must [4]; C4; C12.

### NPH-P03
- 3e7e8482-29f2-4ef9-9006-979fd6f8f6cb FIXED: C5. `action-spine-mri` becomes required.
- 3cc428d0-0e34-4f5c-8f4f-6353cab137c1 FIXED: C5. `action-spine-mri` is added to `required_before_assessment`.
- Class: C1 on must [0]; C2 rewriting must [1]; C3 on must [3]; C4; C12.

### NPH-P04
- ee99bd6b-c9bb-4b84-9c84-90006b259410 NO-ACTION (approval).
- Class: C1 on must [0]; C2 rewriting must [1] (the goals-of-care must [2] stays); C3 on must [4];
  C4; C12.

### NPH-P05
- f6b2546c-31e2-403e-aaf0-88f5b730e3c8 FIXED (CENTRAL C-SYN): C8. Rejected cleaned, differential iNPH moderate, prohibition
  [1] replaced, key evidence [0] reworded.
- Class: C1 on must [0] (post-SAH kept); C2 new counselling must; C4; C12. No "awaiting surgery"
  (no C3).

### NPH-P06
- b4648379-d962-45e4-9195-1f65792bda98 ALREADY-FIXED: class MRI-CONTRAST (plain initial MRI, gadolinium follow-up
  `request_contrast_mri`, criterion `{"contrast": true}`, verified with `mri_probe.py`).
- Class: C1 on must [0]; C2 new counselling must; C3 on must [3]; C4; C12.

### NPH-P07
- 1af93709-617c-4d8c-bb04-8ccdcd99d487 FIXED: C9. Prohibition [1] and red herring [0] reworded with `[Hoglinger_2017]`.
- Class: C1 on must [0]; C2 new counselling must; C3 on must [1]; C4; C12.

### NPH-P08
- 6eedd7f8-b3b7-4765-a83b-507525828a4d FIXED: drainage criterion becomes recommended (soft tap-before-drainage constraint
  kept).
- 9ea36124-a383-4f2a-824d-e20ccfb5625b FIXED: drainage removed from `required_before_assessment`. Must [1] allows the referral
  on the syndrome, DESH and normal-pressure CSF.
- ff859687-b531-41b4-9962-05b271c739bb FIXED: must [0] becomes "After a single tap test without objective improvement, consider
  extended lumbar drainage (about 10 mL/hour, 300 to 500 mL over 72 hours, with daily timed gait
  measures) or another appropriate specialist assessment, because a negative tap test does not
  exclude shunt-responsive iNPH (tap sensitivity 26% to 61%, drainage 50% to 100%)
  [Marmarou_2005]". Red herring [0] is reworded the same way.
- Class: C1 on must [1]: "Refer to neurosurgery for shunt eligibility assessment, on the basis of
  the full syndrome, the DESH-pattern MRI and normal-pressure CSF, together with the extended
  drainage response (TUG 31 to 19 s, 39%, on day 3) if drainage was performed ... [Nakajima_2021]".
  Also C2 new counselling must; C3 on must [2]; C4; C12 (the drainage is now recommended).

### NPH-P09
- 70c405eb-1025-4ca0-bafc-4ad82c5a0496 NO-ACTION (approval).
- Class: C1 on must [0]; C2 new counselling must (cognition may improve less than gait); C3 on must
  [2]; C4 avoided entry only (no stored exercise follow-up; the entry matches the library answer);
  the echo rationale clause; C12.

### NPH-S01
- 52729570-14b0-4f56-a662-1dbc62b4517d NO-ACTION (approval).
- Class: C1 on must [0]; C2 new; C3 on must [1]; C4; C12.

### NPH-S02
- 01c52d0d-49f5-48c2-bdd7-c4880d4b17e2 NO-ACTION (approval).
- Class: C1 on must [0]; C2 rewriting must [1] (BPH limit); C3 on must [2]; C4; C12.

### NPH-S03
- 0cec7b8c-1b4d-4fa6-9317-61933185a17c NO-ACTION (approval).
- Class: C1 on must [0]; C2 new; C3 on must [1]; C4; C12.

### NPH-S04
- 46348ed9-c172-497e-992f-aa5fb619c71e NO-ACTION (approval).
- Class: C1 on must [0]; C2 new; C3 on must [1]; C4 (freezing in the history); C12.

### NPH-S05
- cb213a41-c7e8-42e7-9b34-4927c3222fd5 NO-ACTION (approval).
- Class: C1 on must [0]; C2 new; C3 on must [1] (the osteoporosis clause stays); C4; C12.

### NPH-S06
- 9d68c312-0fa6-42ca-88b0-11dbee6eb4b0 NO-ACTION (approval).
- Class: C1 on must [0] (age and CAD clause kept); C2 new; C3 on must [2]; C4 ("no new cardiac
  symptom"; stable CAD after CABG); C12.

### NPH-S07
- bdd1a3d0-3335-4775-bc4a-5f81f8c29e4f NO-ACTION (approval).
- Class: C1 on must [0]; C2 new; C3 on must [2]; C4; C12.

### NPH-S08
- 49b4998b-e3ea-4a6f-bce3-d4e6bf8a481c FIXED: C10. Must [1] becomes "Continue levothyroxine 75 mcg daily unchanged". Labs stay
  recommended.
- Class: C1 on must [0]; C2 new; C3 on must [2]; C4; C12.

### NPH-S09
- 03abb2d3-2b2a-4b22-b362-e2f9085b5d5b NO-ACTION (approval).
- Class: C1 on must [0]; C2 new; C3 on must [2]; C4; C12.

### NPH-S10
- 664f524a-a314-4e87-8cc9-11444260f667 FIXED: C6 with apixaban 5 mg twice daily. The hard constraint labs before CSF is the
  checkable gate; the must asserts the 72-hour hold (CHA2DS2-VASc 4). Prohibition [2] kept. Log the
  limit: the time of the last dose is history, not a tool result.
- Class: C1 on must [0]; C2 new; C3 on must [2]; C4; C12.

### NPH-S11
- 272fa1bf-9808-4a91-bb03-6bc76fb3d266 NO-ACTION (approval).
- Class: C1 on must [0]; C2 new; C3 on must [1]; C4; C12.

## 4. CENTRAL requests

- **C-SYN (`diagnosis_synonyms.yaml`).** Add to the scoped entries `G91.0+meningitic` (NPH-M08)
  and `G91.0+sah` (NPH-P05) the labels "normal pressure hydrocephalus", "NPH", "idiopathic normal
  pressure hydrocephalus" and "iNPH", and the code G91.2. Then re-apply with
  `apply_diagnosis_synonyms.py --prune --conditions nph` and `--check`. Update the comment above
  the G91 block: "possible iNPH (Relkin 2005) allows a remote antecedent judged not causal; M08 and
  P05 accept both readings, November 2026 physician ruling". Also: M08 `accepted[0]` changed to
  "Normal pressure hydrocephalus, possibly secondary to prior meningitis" (label change).
- **C-PACK (`dataset-generation/criteria_packs/NPH.md`).**
  - Add `[AASLD_2020]`, `[Hoglinger_2017]` and `[AHA_ACC_perioperative_2024]` to the allow-list
    (references in section 1).
  - Update the tiers: post-tap reassessment required in all 30; labs required as a pre-tap safety
    check in M03, M06, M08 and S10, with a hard labs-before-CSF constraint; P03 spine MRI required;
    P08 drainage recommended.
  - Change the referral must to "shunt eligibility assessment" with counselling on risks and
    complications.
  - Add `exercise_stress_test` to the waste list.
  - Replace "INR 1.5 or less" with the AASLD statement.
  - Section 1: secondary versus possible iNPH (M08, P05).
- **C-GUIDE (`build_condition_tool_guidance.py` and `condition_tool_guidance.yaml`, NPH).**
  - `interpret_labs` our_response: labs are optional in 23, recommended in 3 (M04, M07, S08) and
    required in 4 (M03, M06, S10 renal function and blood count; M08
    platelets and coagulation) as pre-tap safety checks, never as NPH diagnostics. Recount after
    the edits.
  - `perform_clinical_assessment` our_response: "extended lumbar drainage (source lumbar_drain,
    required there)" becomes "recommended there".
  - `test_guidance_claims` is maintained centrally.
- **C-XCOND (information for the orchestrator).** Exercise stress tests stored with no avoided
  label in BACT-MEN-RS03, GBS-RS16, SYNC-CARD-P02, SYNC-CARD-RM01 and SYNC-CARD-S06 (measured).
  Their leads should decide whether the test is waste there; SYNC-CARD credits it in five other
  cases.
- **C-UI (display, from the addendum).** Nothing NPH-specific: no NPH note is a row-shift or
  null-significance display note.

## 5. Open questions

- None needs information that only Andrea has.
- For the next physician review:
  - **Certainty wording of the iNPH labels (D17).** With a positive tap and normal-pressure CSF,
    most cases meet "probable iNPH" [Nakajima_2021], but the labels do not say so. A change needs
    a reviewer ruling on `accepted[0]`.
  - **M06 and M09.** The idiopathic reading stays rejected there, because the antecedent is recent
    and plainly causal (D8). A reviewer may say otherwise.
  - **Other low-yield stored follow-ups (unlabelled).** The levodopa challenge (all 30), EMG/NCS,
    SSEP, speech-language, olfactory test and polysomnography are stored in some cases but are not
    waste-labelled. No note raised them, and some can be justified (levodopa challenge in M05 and
    P02, SSEP in P03). Left as is.

<!-- PLAN COMPLETE -->
