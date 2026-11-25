# Physician feedback, 21-22 November 2026

Two tasks asked of both reviewers after the 18 Nov deploy (`deploy.sh --keep-cases`): the
re-check of 20 corrected cases (review set `recheck-2026-11`) and a full review of one condition
already reviewed by the other physician (the same-condition comparison). R1 = NB-KSC, R2 = NB-87M.

Snapshot: VPS backup taken 2026-11-25T10:39Z (649 annotation files). Copies:
`~/Backups/neurobench-review-backups/manual/review-data-2026-11-25T1039Z.tar.gz`, the same tarball
and readable notes in `notes/` (gitignored: reviewer text stays off git), and the full annotation
tree mirrored into the local `data/review/annotations/`. Re-export with
`python3 -I data/review/feedback-2026-11/bin/export_notes.py <snapshot>/annotations data/review/feedback-2026-11/notes`.
No annotation file changed after 22 Nov 19:57 UTC. 94 items are not in any round's ledger
(54 full review, 40 re-check, by `round-2026-11/bin/new_notes_since.py`).

## Re-check (20 corrected cases)

The physicians split the set instead of each doing all 20, so no re-check case has two reviews.
FEPI-TEMP-M02 was opened by both; R2 left it `pending` with no notes.

| | Cases | Approved | Needs changes | Not submitted |
|---|---|---|---|---|
| R1 | ALS, ALZ-EARLY, FEPI-TEMP, FND, FTD, MIG-AURA, MS-RR, NPH, PD, VASC-DEM | 7 | 0 | 3 (ALS-P05, MIG-AURA-P06, MS-RR-RS05, 2 errors each) |
| R2 | BACT-MEN, GBS, GLIO-HG, HEP-ENC, ISCH-STR, MG, NMDAR-ENC, SAH, SE, SYNC-CARD | 0 | 10 | 0 |

R2's ten verdicts by dimension (needs_revision): stopping 8, diagnosis 5, actions 2, assessment 2,
scenario 2, sequencing 1, avoided actions 0. On the 86 verdicts of 3-15 Nov the weak dimensions
were assessment (48) and actions (33); after the corrections they are 2 and 2 out of 10. Most R2
notes are now `issue`, one per case, and narrow (a citation, a missing ICD code, a GCS item).

Three groups explain most of the remaining notes:

1. **Stop rule display (central, review app).** 6 of R2's notes (SAH-M01, HEP-ENC-P05,
   SYNC-CARD-M02, MG-S03, BACT-MEN-M03, GLIO-HG-S05) read "Further actions allowed after that: N"
   as a cap on all later actions, so recommended actions placed after the required set look
   impossible. In the reward (`policy_reward.py`, stopping) recommended and optional criteria
   never count as extra; N only tolerates unjustified actions. The app text causes the reading.
   The same box shows tool names only, so two criteria with one tool appear as
   `interpret_labs / interpret_labs` (R1, ALS-P05) or two `order_ct_scan` (R1, five ISCH-STR
   notes ask to tell non-contrast CT from CTA).
2. **"First order" MRI display (central, review app).** R1 (ALS-P05, MS-RR-RS05) reads the
   non-contrast initial MRI, labelled "First order of this tool", as the answer to the required
   contrast MRI. The MockServer serves the contrast follow-up to a `contrast: true` order
   (perfect-agent check `-v`, 25 Nov), so the data are right and the label is wrong.
3. **Case content.** Missing ICD codes for a named component (HEP-ENC-P05 Wernicke,
   SYNC-CARD-M02 bifascicular block), GCS/FVC arithmetic (SE-M07, GBS-RM12), SE-M07 classified
   as NCSE although myoclonus is visible (ILAE 2015: myoclonic SE), SAH-M01 blood-pressure must
   vs ESO 2026, NMDAR-ENC-P01 and ISCH-STR-RP02 a required test left recommended, MIG-AURA-P06
   MRI to required, MS-RR-RS05 McDonald 2024 wording, BACT-MEN-M03 NICE duration.

## Same-condition full review: ISCH-STR

R1 reviewed ISCH-STR, the condition R2 reviewed in September (23 needs_changes, 5 approved,
97 notes, all ruled in the October round). R1 opened 21 of 30 cases on 22 Nov in 80 minutes
(about 4 minutes each), wrote 54 notes (all `error`, in English), submitted none and gave no
policy verdict. RS03-RS05 and S01-S06 were not opened; RS02 was opened with no notes.
The cases R1 saw are the October-corrected version (hash 88bd8dc0), not what R2 saw.

Classes in R1's notes (cases):

| Class | Cases | Relation to R2 / October round |
|---|---|---|
| Stop rule mixes the acute reperfusion decision with the etiological work-up (drug-interaction check, echo, NOTCH3, antiphospholipid panel required before the assessment) | 13 | New. R2 never raised it. It questions what the stop rule means, not one case. |
| Dysphagia screening missing from the musts | 9 | New class. |
| Wake-up stroke: extended-window imaging should be required | M01, M02, M03, P05 | R2 raised it on M01 (06456aa6); October added CTP as recommended. R1 wants it required. |
| NIHSS: visual extinction scored on item 3 and item 11 | M02, M03, RP04 | October open question 1. R1 now agrees with R2 (item 11 only). |
| Over-strict IVT prohibitions vs AHA/ASA 2026 (moyamoya, prior infarct, intradural dissection, apixaban) | P02, RM01, RM04, RM02 | October open questions 2-3: R1 answers RM01 and RM04 (individualize), RP04 (aPTT 46 s: do not give IVT). |
| LDL < 70 target in non-atherosclerotic stroke | P05, RM01, RM04, RP03 | New, copied across cases. |
| Dissection without infarct filed under ischemic stroke | RM02, RM03 | New. Condition assignment. |
| Others: DAPT after IVT, CTP volumes, CHA2DS2-VASc 7 vs 6, pregnancy CTA, TTP prophylaxis, endocarditis antibiotics | single cases | ISCH-STR-RP02: both physicians (R2 in the re-check, R1 here) touch the TTP handling and the CT-vs-MRI first study. |

Agreement cannot be measured as planned: R1 did not submit verdicts, the two reviews saw different
versions, and R2's ISCH-STR notes are mostly case comments (85 of 97) while R1's are field notes. Two R1 notes on
ISCH-STR-P01 repeat the ISCH-STR-M05 text word for word, including a clopidogrel-omeprazole
interaction although P01 has no omeprazole, so some notes were templated.

## Agreement on ISCH-STR (computed 25 Nov)

`bin/agreement.py` on the 20 cases where R1 left notes (RS02 has none). Every note of both
reviewers on them (R1 54, R2 73 from September) was given one policy dimension and a short issue
label, and pairs raising the same problem on the same case were matched, by a subagent reading
the notes (`notes/ischstr_classified.json`, gitignored; spot-checked). Caveat for every number:
the two reviews saw different versions (R2 the September cases, R1 the October-corrected ones,
where all 73 R2 notes had been ruled FIXED), so this measures agreement on what is wrong across
two rounds, not two independent reads of one case.

| Level | Agreement | Cohen kappa | Gwet AC1 | PABAK |
|---|---|---|---|---|
| Case verdict (needs changes vs approved; unsubmitted cases with an `error` count as needs changes) | 19/20 = 0.95 | 0.00 | 0.95 | 0.90 |
| Case x dimension, pooled (140) | 0.66 | 0.24 | 0.40 | 0.33 |
| Issue (same problem, same case) | 13 matches; Dice 0.21 | | | |

Kappa is 0 on the verdict because R1 flags every case (prevalence paradox); AC1 and PABAK are
the meaningful figures there. Per dimension the reviewers look at different things: R2 flags
scenario plausibility (NIHSS, labs, history) in 17/20 cases and R1 in 4; R1 flags the stop rule in
12/20 and R2 in 1; both flag the assessment (musts, treatment decisions) in 13/20. Actions
(kappa 0.43) and avoided actions (0.64) agree best; scenario and stopping do not agree (AC1 -0.50
and 0.02).

Of the 13 matched issues, about 6 have R1 objecting to the October fix of R2's note (RNF213
testing, IVT in moyamoya, apixaban, intradural V4, CTA in pregnancy, CHA2DS2-VASc), so the
reviewers agree on where the problem is but not on the answer. The other 7 (extended-window
imaging in M01/M02, etiological work-up gating the acute decision, echo before EVT, dissection
without infarct filed under ISCH-STR, antiphospholipid panel) agree on both. R1's dysphagia
(10 cases), LDL target (5) and airway notes have no R2 counterpart.

## Case-level metric from the annotations (Andrea's rule, 25 Nov)

Rule: a case with annotations has not passed. `bin/case_agreement.py` gives each reviewer, per
case: FAIL (at least one field note or case comment, whatever the severity or status), PASS (no
annotation and the case decided, `approved` or `needs_changes`), NOT REVIEWED (no annotation, not
decided: opened only, excluded). Agreement statistics on the 2x2 table: observed agreement, Cohen's
kappa, Gwet's AC1, PABAK, specific agreement on FAIL and on PASS.

Result on the current data (snapshot 25 Nov):

- 29 cases were opened by both. 8 drop out as NOT REVIEWED: R2 opened ALS-M01, ALS-M08,
  ALZ-EARLY-M01, FEPI-TEMP-M01, MIG-AURA-M01, NPH-M01, VASC-DEM-M01 for 0-30 seconds without
  notes (the first case of a condition list), R1 opened ISCH-STR-RS02 last and stopped, and in the
  re-check R2 opened FEPI-TEMP-M02 without notes.
- 20 pairs remain, all ISCH-STR, all FAIL for both: agreement 1.00, specific agreement on FAIL
  1.00, kappa undefined (no case passes), AC1 1.00, PABAK 1.00. (RS01, `approved` by R2 with 6
  comments, is a FAIL under the rule.)
- The number says nothing yet: the two reviews are of different cases (R2 on 22-26 Sep, R1 on
  22 Nov; all 30 ISCH-STR files changed in between, 14 commits of the October round), and nothing
  can pass for R1 in the full review: R1 has 320 FAIL and 0 PASS there (it never decides a case
  without notes), while in the re-check R1 passed 7 of 10. R2 passes 94 of 299 full-review cases
  and 0 of 10 re-check cases.

What a valid measure needs: both reviewers on the same frozen version, every case decided (an
`approved` click when there is nothing to note, or the case cannot pass), and a set where passing
is possible. The re-check set meets the first and the last: each physician did 10 of the 20 frozen
copies in `data/review/sets/recheck-2026-11/`, so each doing the other's 10 gives 20 pairs on the
same version. A finer level is the same rule per section of the case, read deterministically from
`field_path` (patient and tool reports, diagnosis and differential, action criteria, avoided
actions, sequence, stop rule, assessment); it needs field notes rather than case comments (R2's
482 case comments, mostly before November, carry no path).
