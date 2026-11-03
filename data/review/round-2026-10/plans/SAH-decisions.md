# SAH: decisions on the open questions (24 October 2026)

Andrea, 24 Oct 2026: resolve every open point "nel modo migliore per la qualità del dataset". Each
entry gives the question, the decision, the reason with its source, and what changed where. Sources
checked on 24 Oct 2026: the ESO/EANS/ESMINT 2026 guideline record (UMC Utrecht research portal,
abstract; DOI 10.1093/esj/aakag043), the SAHaRA trial (NEJM 2025;392:1079-1088, doi
10.1056/NEJMoa2410962, via NEJM CME and secondary summaries), the Connolly 2012 DSA recommendation
(quoted Class I, LOE B in a trial protocol citing the guideline); the AHA site refused automated
access, so Hoh 2023 statements are the ones already fixed in the plan (section 1.2), taken from
Reviewer 2's notes and the guideline as cited there. A search for an "AANN 2025" SAH guideline found
none (only the 2010 AANN nursing guideline).

Every case log has a "## Close-out (24 Oct 2026)" section listing each change and its reason.

## Step 1: synonyms and labels

**CENTRAL 3, P02 accepted aneurysmal labels and codes.** Decision: the I60 category entry gets
`except_cases: [SAH-P02]`; the I60.8 entry is scoped to `cases: [SAH-P02]` and carries
perimesencephalic and non-aneurysmal labels only. Reason: the scorer accepts a diagnosis when every
token of any accepted label appears in it, so the generic "subarachnoid hemorrhage" and "SAH" (not
only the aneurysmal labels) would credit "aneurysmal SAH from an AComA aneurysm", the exact error
P02 tests; I60.9 and the location codes would credit it by code. P02 now accepts only I60.8 and
"perimesencephalic subarachnoid hemorrhage/haemorrhage", "perimesencephalic SAH", "perimesencephalic
hemorrhage/haemorrhage", "pretruncal subarachnoid hemorrhage", "non-aneurysmal subarachnoid
hemorrhage/haemorrhage", "nonaneurysmal subarachnoid hemorrhage", "non-aneurysmal SAH",
"angiogram negative subarachnoid hemorrhage".

**Scan of the 29 aneurysmal cases.** Every case accepted I60.8 (ICD-10-CM "other nontraumatic
subarachnoid hemorrhage", the code of the non-aneurysmal entity), a different entity from accepted[0].
Removed from the I60 category codes; `--prune --conditions subarachnoid_hemorrhage` dropped it from
the 29 cases. Kept: the generic labels (a plain "subarachnoid hemorrhage" is under-specified, not
wrong, in an aneurysmal case), I60.9, and the location codes I60.0 to I60.7 (the labels already accept
"aneurysmal SAH" at any location, so a location code adds no wrong answer). Known residue, CENTRAL:
the token matcher still credits "non-aneurysmal SAH" in an aneurysmal case, because "aneurysmal" and
"SAH" are tokens of it; only a scorer change (negation tokens such as "non") can fix that.
`apply_diagnosis_synonyms.py --check --conditions subarachnoid_hemorrhage`: clean.

**Q5, grade ranges in labels (M03 "Hunt-Hess 2-3", S05 "Hunt-Hess 1-2", M08 "Fisher 2-3").** Decision:
one grade each, from the case's own data (ruling 3 allows a label correction once decided; the
condition and the ICD code are unchanged). M03 -> Hunt-Hess 3 (exam: confused, oriented to person and
place only, GCS 14 E4V4M6; Hunt-Hess 3 is drowsiness or confusion). S05 -> Hunt-Hess 2 (alert, GCS 15,
severe headache, marked nuchal rigidity, no deficit). M08 -> Fisher 3: the CT described "moderate"
suprasellar blood; Fisher 1980 grade 3 is a localized clot or layer of 1 mm or more, so the CT finding
now states "layer thicker than 1 mm", the impression and `additional_observations` say Fisher grade 3,
and the NCCT criterion evidence matches. No synonym effect (the generic labels carry the scoring).

**RS12 label** (summary CENTRAL 6): already corrected in the round; nothing keys on the label text.

## Step 2: criteria pack (`dataset-generation/criteria_packs/SAH.md`)

Rewritten in line with plan section 1 and the decisions here: Hoh 2023 governs; CT sensitivity per
Perry 2011 (close to 100% within 6 h, falls after 6 h, anemia); LP indication after 6 h or a deficit;
bilirubin about 12 h, persists about two weeks (was "6-12 h", "2-3 weeks"); DSA recommended in every
aneurysmal case and required with a negative CTA; TCD optional, admission baseline; literature
optional and last; drug check tiered per ruling 6; securing "as early as feasible, preferably within
24 hours" (was "24-72h"); hydrocephalus rule (Q1); BP, nimodipine, home-drug, QTc and andexanet facts
from plan 1.2; waste and harm lists; sequence constraints as built; red herrings including the echo
wording rule (Q10) and coital onset. Superseded tiers marked. Allow-list: every key cited in the 30
cases ([Hoh_2023], [Connolly_2012], [Edlow_2008], [Hunt_Hess_1968], [Fisher_1980], [Molyneux_2002],
[Drew_2010], and now [English_2024], [Thompson_2015]) plus [Perry_2011] (title corrected), [Perry_2013]
and [Vergouwen_2026], each with a full reference; [Connolly_2012] marked superseded for management.

## Step 3: generator (`conditions.yaml`, subarachnoid_hemorrhage block)

- `common_followups`: DSA description "gold standard for aneurysm characterization and endovascular
  treatment" (it seeded DSA reports with coiling and Raymond classes, class C3) now asks for a
  diagnostic-only report; TCD "Daily TCD monitoring days 4-14" (it seeded day-4 to day-8 TCDs in
  patients hours from onset, class C2) is now an optional admission baseline; echo description adds
  the wording rule; CTA and telemetry follow-ups added (telemetry 2 to 6 h, never 24 h, class C12).
- `key_findings`: CT "sensitivity >98%" and "CT negative in ~5%" (teaching text that became the "Note:
  CT sensitivity" essays in reports, class C14) replaced by a finding; CSF xanthochromia timing to
  about 12 h and two weeks; labs as values and flags only (the "leukocytosis (stress response)",
  "stress hyperglycemia", "neurogenic" wording the audit found in summaries), potassium and magnesium
  (class C9), type and screen; advanced imaging: DSA in every case, TCD baseline, CTA-negative DSA.
- Differential: RCVS key features (convexity SAH, segmental vasoconstriction), dissection and CVST added.
- `difficulty_variants`: the presentations no longer contain "Hunt-Hess grade 2", "CT shows Fisher
  grade 3 SAH", "LP shows xanthochromia", "CT negative. Considering whether to perform LP" (scored
  results and the grade in the presentation).
- `required_modalities` gains ECG (required in all 30 cases). `test_panel_case_contract`: pass.

## Step 4: review-app guidance

`test_guidance_claims`: the SAH claim "cerebral angiography in 3" failed (30 now). Response for
`order_advanced_imaging` rewritten (DSA in all 30, recommended in 29, required in P02; diagnostic-only
reports; MRA waste after the CTA except the contrast-rash case, and an MRA order returns a matching
report); YAML regenerated with `--write`; claims table now checks DSA in 30, required 1, recommended
29, and LP avoided in the 27 CT-positive cases. All SAH claims pass (remaining failures are ALZ-EARLY).

## Step 5: open questions

**Q1. EVD with GCS 15 (M02, RS12).** Decision: conditional EVD (MUST-EVD-WATCH): "Urgent neurosurgical
review of the early hydrocephalus with intraventricular blood: hourly neurological checks and repeat
CT on any decline in consciousness, with external ventricular drainage if it becomes symptomatic
[Hoh_2023]." Reason: both patients are alert and oriented, GCS 15 (Hunt-Hess 2); the guideline
recommendation, as Reviewer 2 quotes it in note f87e2dd7, is urgent CSF diversion for *acute symptomatic*
hydrocephalus (COR 1, LOE B-NR); early radiological hydrocephalus in an alert patient often settles,
and an EVD before securing carries infection and rebleeding risk. Reviewer 2's substantive point (the
hydrocephalus must have a neurosurgical plan) is kept; the drain is conditional. LP stays
`contraindicated` (IVH and hydrocephalus). M05, M07, P04 (depressed consciousness) keep MUST-EVD-NOW.
Changed: M02 and RS12 musts; M02 `metadata.difficulty_rationale`; pack section 2. Tell R2 at re-review
(it narrows note f87e2dd7).

**Q2. DSA tier.** Decision: required in P02, recommended in the 29 aneurysmal cases. Reason: DSA with
3D rotational angiography is indicated for aneurysm detection except when a noninvasive angiogram has
already shown the aneurysm (Connolly 2012, Class I, LOE B). In the 29 the CTA shows the aneurysm, so
DSA refines anatomy before securing (recommended, and often done in the same session as coiling); in
P02 the CTA is negative and the non-aneurysmal label rests on the DSA. Changed: P02 DSA criterion
`required` and in `required_before_assessment`; pack; guidance claims. perfect_agent: pass.

**Q3. P02 nimodipine after a negative DSA.** Decision: start it while an aneurysm is not excluded;
after a negative DSA with a perimesencephalic pattern it can be stopped. Reason: the nimodipine
evidence (Hoh 2023, COR 1, LOE A) is in aneurysmal SAH; delayed cerebral ischemia is rare after
perimesencephalic hemorrhage; the wording permits, it does not forbid, completing 21 days, so a
physician can check it. Changed: P02 nimodipine must.

**Q4. ESO 2026 and AANN 2025 references.** ESO: verified, Vergouwen MDI et al., Eur Stroke J
2026;11(5):aakag043, doi 10.1093/esj/aakag043 (expert consensus: treat within 24 h after ictus when the
most dedicated team is available); allow-listed as `[Vergouwen_2026]`, not added to case text (the
window is already carried by `[Hoh_2023]`; adding it would only churn approved cases). AANN 2025: no
such guideline found; not allow-listed, cited nowhere.

**Q5. Grade-range labels.** See step 1.

**Q6. Approval status of P04, P06, P07, RS11, S02, S03, S05.** Decision: treat as approved. Reason:
PATTERNS.md records 21 SAH approvals by Reviewer 2; the notes file lists 14 approved and 9
needs-changes cases with notes, and these 7 are the only other cases, so 14 + 7 = 21. All were changed
for logged real errors; they go back to re-review like the others. No change.

**Q7. RP11 lymphocytes 4.4 and natalizumab wording.** Decision: confirmed. Natalizumab blocks
alpha-4 integrin-mediated lymphocyte trafficking and raises circulating lymphocytes, so a high count
(4.4 x10^9/L against 1.0-4.0) is the expected effect, and the earlier "0.8, low-normal due to
natalizumab" was wrong physiology. Deferring the next infusion's timing to the MS neurologist is
correct (no interaction with nimodipine; a short delay is acceptable). No change.

**Q8. Hunt-Hess grade in the patient block.** Decision: removed everywhere it appeared (exam
`additional` in 27 cases, plus the RS11 HPI "Hunt-Hess Grade 2 on arrival"). Reason: Hunt-Hess is a
scale for SAH, so writing it in the presentation names the diagnosis before any study (in the
CT-negative P01 and P06 it was the answer itself) and does the grading the agent is assessed on
(TOOL_REPORT_STYLE_GUIDE, ruling on the patient block). The descriptive exam (mental status, GCS,
meningism, deficits) stays and supports the grade. The grade stays in labels and ground truth. Changed:
27 cases (all except P02, P03, P05, which had none); this closes the RS11 FLAGGED finding.

**Q9. P08 field ECG in the HPI.** Decision: keep. Reason: the prehospital 12-lead (T-wave inversions
V1-V4, catheterization considered) is the premise of the case's STEMI red herring and a different study
from the scored in-hospital ECG (V1-V5, QTc 532 ms, which the HPI does not state). No change.

**Q10. Echo wording.** Decision: an echo reports the LVEF and the wall-motion pattern. With apical
hypo- or akinesis and basal hyperkinesis it may say "apical ballooning pattern ... consistent with
stress (Takotsubo) cardiomyopathy" (Kind 2, standard echo language); with only mild apical hypokinesis
and a preserved EF it does not use the Takotsubo label (it does not meet the pattern); diagnostic
labels graded "classic", "severe", "moderate", "mild" or "borderline Takotsubo" in findings or
`wall_motion`, and "cardiology consultation" advice (management, ruling 4), are removed. The audit
template "echocardiogram showing apical ballooning confirms etiology" was still in 9 red herrings: an
echo does not confirm etiology, so each now states the case's own pattern and LVEF. Changed: echo
reports in M02, M04, M05, M07, P04, P05, P06, RM11, RS11, RS12, S02, S06, S09, S10 (with the echo
criterion evidence in P05, P06, S09, S10; P05 and P06 "EF mildly reduced" at 54% and 52% now
"low-normal"); red herrings in M01, M02, M05, M07, RS11, RS12, S02, S06, S08.

**Q11. Left unchanged by the audit.**
- "Late presentation (>24 h) ... xanthochromia persists for weeks" pearl (M08, P01, P03): removed. It
  gave a 24-hour threshold where the evidence is 6 hours (Perry 2011) and "weeks" where bilirubin
  persists about two weeks, and it duplicates the canonical CT and LP pearls (P01, P03); in the
  CT-positive M08 it was carry-over (the sentinel-headache pearl carries M08's lesson).
- No home-drug must for sertraline (M03) or rosuvastatin (M07): confirmed. Both are continued
  (abrupt SSRI withdrawal; no reason to stop a statin), the drug checks state it, and a must is
  reserved for drugs whose handling changes acute management.
- P04 exam note "clonazepam may artificially lower GCS": kept as the intended distractor; it is a
  plausible bedside note and the red herring scores the reasoning (grade attributed to the
  hemorrhage until proven otherwise).

## Auditor flags (summary CENTRAL 9 and 10, decided here because they are case data)

**CENTRAL 9, `fallback_tool_outputs.cardiac_monitoring` a normal 24 h Holter in all 30.** Decision:
replaced in all 30 by a copy of the case's own telemetry follow-up. Reason: a 24-hour recording
cannot exist at assessment time, and a Holter order in the acute setting is answered by the telemetry
the patient is on; the copy guarantees the same rhythm (M07 AF). Simulated a `holter_24h` order in
M01, P02, S07, P01, M05: telemetry served.

**CENTRAL 10, off-pathway MRI and MRA returning normal studies.** Decision, per case:
- MRA: every case now stores an MR angiography follow-up (S07 already had one): the DSA's aneurysm
  site and size, 0.2 mm smaller as time-of-flight reads it, the second aneurysm in M05 and S05,
  negative in P02. MRA stays a `waste` avoided action after the CTA. Simulated: served.
- Brain MRI: the 25 cases without an MRI follow-up get a `fallback_tool_outputs.mri` built from their
  own CT findings (FLAIR hyperintensity and SWI susceptibility in the same spaces, intraventricular
  blood and enlarged ventricles where the CT has them, P07's empty sella and flattened globes, no
  restricted diffusion). Simulated: served.
- CT perfusion and the other library defaults (for example an off-pathway `order_ct_scan` variant)
  are library text: left to CENTRAL.

## Leak and guards

`test_case_guards -k SAH-`: 60 passed (the 7 SAH leak failures in CENTRAL_PENDING were fixed during
the round). `perfect_agent.py`: 30/30. `case_io.py check` on all 30: schema OK, synonym guard OK, no
failure names an SAH case.

## Cases changed in the close-out

All 30 (synonym prune of I60.8 in 29 and the P02 labels; telemetry fallback in 30; MRA follow-up in
29; MRI fallback in 25), plus: Hunt-Hess removal in 27; M03, S05, M08 labels; M02, RS12 EVD; P02 DSA
and nimodipine; P06 and RM11 citation keys; echo and red-herring edits as in Q10; M08, P01, P03 pearl.

## Still needing Andrea or the physicians

Nothing needs information only Andrea has. For Reviewer 2 at re-review: Q1 (conditional EVD in M02 and
RS12 narrows note f87e2dd7), Q2 (P02 DSA required), Q5 (three labels now name one grade), Q8 (grade
removed from the presentation of 19 approved or probably approved cases), Q10 (echo wording).

## CENTRAL

1. **Scorer** (`DiagnosisCriterion.matches`): negation-aware matching. "non-aneurysmal SAH" contains
   every token of "aneurysmal subarachnoid hemorrhage" and of "SAH", so it scores as correct in the 29
   aneurysmal cases. A token such as "non" (or "nonaneurysmal") in the submission that is absent from
   the label should block the match.
2. **Fallback library**: SAH-aware or non-asserting defaults for CT perfusion and for any imaging
   variant the case does not store (the case-level MRI and MRA are now done for SAH).
3. **Vocabulary**: no new term needed (`cerebral_angiography`, `MR_angiography`,
   `transcranial_doppler`, `magnesium`, `xanthochromia_spectrophotometry` are priced).
4. Carried from the summary: review UI to show initial outputs and follow-ups in criterion order;
   `perfect_agent.py` to check that `required_arguments` keys exist in the tool schema (P06 MRI
   `sequences`); review app to flag note text duplicated across cases (M06 note copied from M05).
