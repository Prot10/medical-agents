# MS-RR: condition plan for the November 2026 review round

Lead plan, 16 Nov 2026, for the 30 MS-RR cases (M01-M04, P01-P05, RM01-RM04, RP01-RP05, RS01-RS06,
S01-S06). Contract: `data/review/round-2026-10/ROUND_POLICY.md` plus
`/home/aprotani/review-round-2026-11/work/NOVEMBER_ADDENDUM.md`. Decisions with reasons and
citations: `plans/MS-RR-decisions.md` (D1-D20; this plan refers to them). October plan and
decisions stay in force except where D20 lists a revision.

Notes: 118, all R1 (NB-KSC3-TWUA-QDTM), every case `in_progress`; no R2 note. **No MS-RR case is
approved** (`work/approved.txt` has none), so the approved-case restriction does not apply, but
"fix errors, do not churn" does: change only what a note or a class below names.

Helpers (this round): `data/review/round-2026-11/bin/case_io.py` (load/save/check),
`perfect_agent.py CASE -v` (one case per call), `caselog.py`, `mri_probe.py` (only if an MRI is
touched). Python: `uv run python -I` from `/home/aprotani/projects/ma-round11`; scratch in
`/home/aprotani/review-round-2026-11/work/scratch/<label>/`. After every case: `perfect_agent.py
CASE -v`, `case_io.py check CASE`; for every new or changed criterion confirm with a served-answer
probe that its first alternative receives the report carrying its `expected_evidence`.

---

## 1. Governing guidelines and canonical facts

| Topic | Source (verified) | Key |
|---|---|---|
| Diagnosis | Montalban X et al. 2024 revisions of the McDonald criteria. Lancet Neurol 2025;24(10):850-865 | `[McDonald_2024]` |
| MRI protocol | Wattjes MP et al. Lancet Neurol 2021;20(8):653-670 | `[Wattjes_2021]` |
| Relapse, DMT, bladder overview | NICE NG220 (2022; diagnosis amended June 2026), section "Relapse and exacerbation" | `[NICE_NG220]` |
| Bladder (PVR, ISC) | Fowler CJ et al. A UK consensus on the management of the bladder in MS. J Neurol Neurosurg Psychiatry 2009;80(5):470-477 | `[Fowler_2009]` (new key: CENTRAL pack) |
| Steroids before biopsy when lymphoma is possible | Ferreri AJM et al. EHA-ESMO guideline on PCNSL. Ann Oncol 2024;35(6):491-507 | `[EHA_ESMO_PCNSL_2024]` (new key) |
| Tumefactive demyelination | Hardy TA, Chataway J. J Neurol Neurosurg Psychiatry 2013;84(9):1047-1053 | `[Hardy_2013]` |
| NMOSD / MOGAD | Wingerchuk 2015 Neurology 85:177-189; Banwell 2023 Lancet Neurol 22:268-282 | `[Wingerchuk_2015]`, `[Banwell_2023_MOGAD]` |
| Stroke vascular imaging | Kleindorfer DO et al. Stroke 2021;52:e364-e467 | `[AHA_2021_SecPrev]` (new key) |
| MRI dating of infarcts | Allen LM et al. RadioGraphics 2012;32(5):1285-1297 | `[Allen_2012]` (new key) |
| DMT baseline checks | Product labels: ocrelizumab, ofatumumab, dimethyl fumarate, fingolimod, ozanimod, ponesimod, natalizumab, interferon beta | cite as "<drug> prescribing information" in a rationale; not as a bracket key |

Canonical facts added this round (the October F1-F12 stay, with the changes noted):

- **N1 (revises F3).** Lesions in 4-5 regions establish DIS without DIT or CSF **after a typical
  attack** (optic neuritis, partial myelitis, brainstem or cerebellar syndrome, a tumefactive
  attack). In non-specific presentations (episodic vertigo, fatigue, transient paraesthesias:
  P01, P02, P03) DIS is completed by DIT, positive CSF or CVS, as with 2-3 regions [McDonald_2024].
- **N2.** An earlier episode is an "earlier attack" only with objective findings at the time or a
  residual sign on today's exam attributable to it; otherwise it is a "possible earlier attack" and
  is never counted in an attack total. Neither the diagnosis nor a must depends on it (D4).
- **N3 (revises F9).** Before relapse steroids: assess for infection (symptoms, temperature,
  urinalysis with culture sent when there are bladder symptoms); do not wait for a culture unless
  infection is clinically suspected; a negative dipstick does not exclude UTI. Offer treatment for a
  relapse that affects usual tasks as early as possible and within 14 days of onset; beyond 14 days
  it is an individual decision. Oral methylprednisolone 500 mg daily for 5 days is first line; IV
  1 g daily for 3-5 days when oral has failed or is not tolerated, for admission with a severe
  relapse, or for monitoring of a condition such as diabetes [NICE_NG220].
- **N4 (revises F11 screening sentence).** Baseline checks follow the drug: anti-CD20 (ocrelizumab,
  ofatumumab): HBV screening (HBsAg, anti-HBc) and quantitative serum immunoglobulins; live vaccines
  at least 4 weeks and non-live vaccines at least 2 weeks before the first dose. Dimethyl fumarate:
  full blood count with lymphocyte count, liver tests (aminotransferases, alkaline phosphatase,
  bilirubin). Natalizumab: anti-JCV antibody status and index. S1P modulators: ECG, blood count with
  lymphocytes, liver tests, VZV IgG if varicella history or vaccination is not confirmed (vaccinate
  and wait 4 weeks if negative), fundus examination (macular oedema risk higher with diabetes or
  uveitis); first-dose monitoring for every patient on fingolimod, and on ozanimod or ponesimod only
  with the pre-existing cardiac conditions their labels list. Interferon beta: blood count, liver
  tests, thyroid function. Teriflunomide: liver tests, blood count, blood pressure, pregnancy test.
  HIV is already in every mimic panel. HCV is not a universal pre-DMT test.
- **N5.** UK consensus: test for UTI, measure the post-void residual; ISC for a residual over
  100 mL, antimuscarinic (or mirabegron) when the residual is low [Fowler_2009]. A single bladder
  scan is repeated before ISC is taught, through the continence or urology team.
- **N6 (revises F10 and pack 1.9).** With a tumefactive lesion and lymphoma possible: avoid
  corticosteroids before tissue whenever clinically possible; with clinical deterioration, urgent
  biopsy before steroids is preferred, and steroids are not withheld when waiting is unsafe
  (herniation, falling consciousness, respiratory compromise) [EHA_ESMO_PCNSL_2024]. A negative CSF
  cytology and flow cytometry lower but do not exclude lymphoma.
- **N7.** Targeted AQP4-IgG/MOG-IgG CBA (D14): required with a red flag; recommended with a
  suggestive feature (simultaneous optic neuritis and myelitis, optic disc swelling, painful tonic
  spasms); optional otherwise. A negative CBA lowers, never absolutely excludes, NMOSD or MOGAD.
- **N8.** Normal ADC about one week after onset and gadolinium enhancement do not by themselves
  exclude a subacute infarct; DWI can be falsely negative in the posterior circulation [Allen_2012].

---

## 2. Classes

Counts are measured on the 16 Nov working tree (`work/scratch/msrr-lead/measure.py`, `dmt.py`,
`xcond.py`). "x-cond" is the count across all 600 cases.

### C1. LIT (D1)
Notes: one "no" per case on the literature follow-up (30) plus RP02 26f64ab1 (criterion). Cases
measured: 0 of 30 have any literature criterion, follow-up or stored literature output. Fix: none
(FIXED by class LIT, commit 393c547e). Workers confirm in the log; never add one back.

### C2. MRI-CONTRAST (D2)
Notes: one per case (30) on `initial_tool_outputs.mri`. Measured: 30 of 30 plain initial
(`contrast_used: false`, no gadolinium text) plus `request_contrast_mri` follow-up
(`contrast_used: true`), MRI criterion `{contrast: true, protocol: ms}`. Fix: none (FIXED by class
MRI-CONTRAST, commit 71517e55).

### C3. Four regions need no DIT only after a typical attack (D3)
Notes: P03 62865b19. Cases: P01 (KCE[2]), P02 (KCE[2]), P03 (must[0], KCE[2]). Fix: replace the
"with four regions DIT is not required" clause. Canonical KCE: "DIT: simultaneous gadolinium-enhancing
and non-enhancing lesions (<sites>). The presentation is non-specific, so the four-region rule does
not apply and DIS is completed by DIT." Canonical must (P03): "State MS by the 2024 McDonald
criteria: DIS in four regions (periventricular, juxtacortical, infratentorial, spinal cord) completed,
because the presentation is non-specific, by DIT from the enhancing and non-enhancing lesions; explain
that absent CSF oligoclonal bands do not exclude MS." P01/P02 must[0] already name DIT: keep, but drop
the RR demand per C4. Not elsewhere (27 typical presentations keep the four-region wording). x-cond: the
rule is MS-specific.

### C4. Uncertain earlier episodes (D4)
Notes: M04 b0c42fef, P01 8396c5dc, P02 4fc5612f, RS04 c2cb2aec. Rule N2. Measured instances to fix:
- M01: must[2] "three attacks in 14 months" (counts the hand tingling attributed to carpal tunnel;
  the left optic neuritis with residual RAPD/pallor is an objective earlier attack): "the current
  myelitis after a left optic neuritis 8 months ago, a possible earlier sensory episode, enhancing
  brain and cord lesions". KCE[1]: "Earlier attack: ... left optic neuritis ...; possible earlier
  episode: two weeks of right hand tingling 14 months ago".
- M03: KCE[1] "Prior attack" for the untested hand episode: "Possible earlier attack: ...".
- M04: must[1] (canonical below), must[3] "two attacks in 8 months" -> "the current severe optic
  neuritis, a possible earlier sensory episode, lesions in five regions"; KCE[1] "Prior attack" ->
  "Possible earlier attack ...; the non-enhancing C5-C6 lesion could explain it".
  Canonical M04 must[1]: "Explain that MS is established now by the 2024 McDonald criteria (lesions in
  five regions after a typical optic neuritis), so this is not a clinically isolated syndrome awaiting
  a second attack; the right arm and trunk tingling 8 months ago is a possible earlier attack, and the
  diagnosis does not depend on it."
- P01: must[0] -> "State MS by the 2024 McDonald criteria (a relapsing course is likely but the
  earlier vertigo episodes and the hand clumsiness are possible, not confirmed, attacks), naming the
  regions ... completed by DIT ..."; must[2] "recurrent attacks over 18 months" -> "recurrent episodes
  of uncertain significance over 18 months"; KCE[0] "Attacks:" -> "Episodes of uncertain attack
  status:".
- P02: must[2] exact physician text: "two distinct vertigo episodes over 8 months, with intermittent
  sensory symptoms of uncertain relapse significance" replaces "three attacks in 8 months"; KCE[0]
  "Attacks:" -> "Episodes:" with the tingling "of uncertain relapse significance".
- RS04: must[2] "two attacks in 3 months" -> "the current abducens palsy with an enhancing pontine
  lesion, a possible earlier sensory episode, DIS and DIT on MRI". Check RS04 KCE and must[0] for the
  same count.
- RM01, RM02: KCE[0] "(earlier attack)" for a subjective numbness episode -> "(possible earlier
  attack)"; check must[0] ("with the right-hand episode two years ago as an ...") likewise.
- Everyone else: check each "two attacks" / "prior attack" against N2; RS02, RS03, RS05, RS06, S01,
  S02, S05, P04, P05, RM04 cite a residual sign or a documented optic neuritis and stay if the
  residual is in the exam (RS05, RS06: confirm a residual sign exists; if not, "possible").
- Diagnosis scoring needs no change (accepted includes "multiple sclerosis", "MS").

### C5. Drug-specific pre-DMT checks (D5)
Notes: 25 (list in D5). Cases: all 30 (measured; P03 and P05 without a note). Canonical must,
completed per case with the drug its DMT must or drug-check output favours (N4):
"Before starting disease-modifying therapy, complete the baseline checks the chosen drug requires:
for <favoured drug/class>, <its checks from N4>; for another drug, its own label checks (for example
<one or two alternatives the case discusses>). Review vaccination history and give any live vaccine at
least 4 weeks before a drug that precludes it."
Per case favoured drug (measured, `dmt.py`): DMF in M01, M02, M03, P01, P02, RM03, RS04, S01;
ocrelizumab or anti-CD20 in M04 (or DMF), P05 (serology already stored: keep "use the completed
serology", add immunoglobulins), RP04, RS01, RS02, RS03, S03, S04; natalizumab in RM04, RS05, RS06
(anti-JCV index; RS06 also lists anti-CD20 alternatives); interferon beta in RP01; class lists without
one drug in P03, P04, RM01, RM02, RP02, RP03, RP05, S02, S05, S06 (write the anti-CD20 and S1P lines,
plus anti-JCV where natalizumab is named). Keep RP05's diabetes and RS01's age infection-risk wording.
Also fix drug-check outputs that state the universal list as a rule: P03 ("Before anti-CD20 or S1P
modulator therapy: HBsAg, anti-HBc, HCV, HIV and VZV IgG ..."), P04 (same), P05 ("Anti-CD20 antibodies
and cladribine: ..." -> split: anti-CD20 HBV and immunoglobulins; cladribine HBV, HCV, HIV, VZV, TB
per its label). x-cond: 30, all MS-RR.

### C6. Infection assessment before steroids (D6)
Notes: P04 bc2383f3, P05 222ff635, RM04 42b55638, RP05 ae3e77f6, RS02 55123805, RS03 414f3aaa, S03
b2269e22, S04 2f73da0e, M01 8d31a900 (part). Cases (13): M01, M02, M03, P04, P05, RM04, RP05, RS02,
RS03, S02, S03, S04, S06. Canonical clause (replaces "after a urine dipstick (and culture) excludes
infection", "Exclude urinary tract infection (urinalysis and culture) before steroids", "Check
urinalysis to exclude ..."): "after assessing for infection (symptoms, temperature, urinalysis with a
urine culture sent given her/his bladder symptoms), without waiting for the culture result unless
infection is suspected; a negative dipstick does not exclude a urinary infection". Keep each case's
other clauses (PPI with NSAID, glucose monitoring, potassium on thiazide). RS01, RS05, RS06, RM03 say
only "after excluding infection" with no urine gate: leave. x-cond: 12-13, all MS-RR.

### C7. Relapse beyond 14 days (D7)
Notes: M01 8d31a900. Cases (onset more than 14 days before assessment, measured from chief complaint
and HPI): M01 6 weeks, M02 3 weeks, P04 16 days, P05 3 weeks, RM04 3 weeks, RP04 6 weeks, RP05 3
weeks. Canonical opening of the steroid must: "Decide on high-dose methylprednisolone individually:
the relapse began <N> weeks ago, beyond the 14 days within which NICE advises treatment, so weigh
whether the deficit is still worsening or disabling, current activity on MRI (<the enhancing
symptomatic lesion>) and <her/his> preference; if treated, oral 500 mg daily for 5 days, or IV 1 g
daily for 3-5 days <when the case's reason applies: severe relapse needing admission, monitoring of
diabetes>, after assessing for infection (C6)". Keep plasma exchange only for a severe relapse that
does not respond. Cases within 14 days keep "Offer/Treat" wording (with C6 where applicable).

### C8. Post-void residual and ISC (D8)
Notes: S02 d39dab89, S03 572f1efc, S04 5ddb7080. Cases (12): M01, M02, M03, P04, P05, RM04, RS02,
RS03, S02, S03, S04, S06. Canonical must: "Measure the post-void residual by bladder scan, repeated if
raised: offer an antimuscarinic or mirabegron for the urgency if it is low <M01: mindful of the
additive anticholinergic effect of dicyclomine>; if a raised residual (over about 100 mL) is
confirmed, arrange intermittent self-catheterisation teaching through the continence or urology team."
Keep case-specific additions.

### C9. S1P first-dose monitoring (D9)
Notes: RS06 31eb1284, RP05 99088fd7 (part). Cases: RS06 (drug-check warning "Fingolimod and other S1P
modulators require a baseline ECG and first-dose monitoring for bradyarrhythmia") -> "S1P modulators
need a baseline ECG; first-dose heart-rate monitoring is required for every patient starting
fingolimod and, for ozanimod or ponesimod, for patients with the pre-existing cardiac conditions their
labels list". RP05 prohibition[3] -> "Do not start an S1P modulator without a baseline ECG,
confirmation that his sleep apnoea is treated, first-dose heart-rate monitoring where the drug's
label requires it (always with fingolimod) and an eye examination for macular oedema, which diabetes
makes more likely". RS02, RS03, RS05 say it of fingolimod only: correct, leave. x-cond: 1.

### C10. Tumefactive steroid decision (D10)
Notes: RP01 25994494, RP02 64579059, RP03 b3996cce. Cases: RM01, RM02, RP01 (cytology gate), RP02,
RP03 (tissue gate).
- C10a, canonical steroid must for RM01, RM02, RP01: "After CSF has been taken (cytology, flow
  cytometry, oligoclonal bands), decide corticosteroids with neurosurgery and neuro-oncology: a
  negative cytology and flow cytometry do not exclude lymphoma; if the imaging, CSF and other lesions
  make demyelination secure, give IV methylprednisolone 1 g daily for 3-5 days <case clauses>; if
  neoplastic suspicion remains, obtain a stereotactic biopsy before corticosteroids, unless
  deterioration makes waiting unsafe." Canonical prohibition (replaces "Do not give/start
  corticosteroids before CSF cytology and flow cytometry ..."): "Do not give corticosteroids before CSF
  has been taken and the lymphoma question has been weighed, and do not treat a negative CSF cytology as
  excluding lymphoma: steroids can make it non-diagnostic." RM02's "and MR spectroscopy favours
  demyelination" may stay as one input, not a gate. Keep the repeat-MRI musts.
- RM02 and RP01 have no biopsy criterion: check what `obtain_tissue_diagnosis {procedure:
  stereotactic_biopsy}` returns (the library answers "Non-diagnostic brain tissue ... no demyelinating
  pathology", which contradicts these patients). Store a case fallback tissue report of the dominant
  lesion with the October G2 histology (active demyelination, CD68 macrophages with myelin debris,
  perivascular T cells, preserved axons; CD20 reactive B cells only, IDH1 negative; impression = the
  histology only), so a biopsy order is answered coherently without being scored. Probe it.
- RP02: `action-biopsy` recommended -> **required**, add to `required_before_assessment`;
  must[1] -> "Withhold corticosteroids until a neurosurgical stereotactic biopsy of the left parietal
  lesion has been obtained, because steroids can make lymphoma non-diagnostic; if she deteriorates
  before tissue can be taken (falling consciousness, signs of herniation), do not delay treatment:
  give corticosteroids after neurosurgical discussion and accept the diagnostic cost." Prohibition[1]
  -> "Do not start corticosteroids before tissue has been obtained unless deterioration makes waiting
  unsafe". Criterion label "Stereotactic biopsy of the left parietal lesion before corticosteroids"
  stays; rationale says why it is required (LP contraindicated, imaging indeterminate).
- RP03: must[2] -> "Decide urgently with neurosurgery and neuro-oncology: an urgent stereotactic biopsy
  of the accessible right temporal lesion before corticosteroids is preferred because steroids can
  make lymphoma non-diagnostic, but if she deteriorates before tissue can be taken (falling GCS,
  hydrocephalus, respiratory compromise), start corticosteroids without waiting; dexamethasone or
  diversion for hydrocephalus after neurosurgical review." Must[3] "Once histology shows
  demyelination ..." -> "Once tissue is obtained, or earlier if deterioration forces treatment, give IV
  methylprednisolone ...". Prohibition[2] -> "Do not start corticosteroids before the biopsy decision
  has been made with neurosurgery, unless deterioration makes waiting unsafe". Biopsy stays
  recommended.
x-cond: cytology gate 4 (MS-RR 3, NPH 1, out of scope), steroid-before-tissue prohibition 5 (MS-RR).

### C11. Pre-LP safety with a tumefactive lesion (D11)
Notes: RM01 7a15f67e, RM02 aac7f149. Cases: RM01, RM02, RP01 (tumefactive with a CSF criterion).
Fix: sequence constraint `action-1-analyze-brain-mri` -> `action-5-analyze-csf` severity `hard`, reason
"With a tumefactive lesion, lumbar puncture only after the MRI has shown no midline shift, no
effacement of the basal cisterns or fourth ventricle and no tonsillar descent", citations
`["[Hardy_2013]"]` or none. New must: "Before lumbar puncture, document from the MRI and the
examination that the <size> lesion causes no midline shift, basal cistern or fourth-ventricle
effacement, that there is no papilloedema and that consciousness is stable; proceed only then, and do
not perform the LP if any of these is present." CSF criterion rationale may add one clause on this.
The 25 non-tumefactive cases keep the soft constraint.

### C12. RP03 reversible postoperative causes (D12)
Note: RP03 f273dd7b. New must (place after must[0]): "Exclude reversible causes of the postoperative
unresponsiveness at once: capillary glucose (glibenclamide), arterial blood gas for hypoxia and
hypercapnia, residual anaesthetic, opioid or neuromuscular-blocking drug effect from the anaesthetic
record (with reversal where appropriate), sodium, and an acute vascular event on the diffusion and
gadolinium MRI." New criterion `action-abg`, **required**, `interpret_labs` `{panels: ["ABG"]}`, label
"Arterial blood gas", rationale (GCS 8 after general anaesthesia: ventilation and oxygenation must be
known), citations none or `[NICE_NG220]`-free; stored `interpret_labs` follow-up (trigger
`request_arterial_blood_gas`, panel name "ABG") with values that exclude a gas-exchange cause (e.g. pH
7.39, pCO2 42 mmHg, pO2 96 mmHg on 2 L/min, HCO3 25, lactate 1.4), plain interpretation; add to
`required_before_assessment`, place after labs. Probe: an `ABG` order gets it, the first-line panel
order does not. Prohibition[1] -> "Do not attribute the unresponsiveness and quadriparesis to residual
anaesthesia once glucose, gas exchange and drug effects have been checked and the MRI shows the
brainstem lesion".

### C13. OCB references with no LP (D13)
Note: RP03 7f4a6c46. RP03 differential NMOSD: delete "The absent oligoclonal bands do not count against
NMOSD, so the CBA result carries the exclusion."; MOGAD: delete "and absent bands". Check KCE, red
herrings and musts for any other OCB or CSF-result reference (none measured). RP02: none measured.

### C14. AQP4/MOG targeting (D14)
Notes: S06 9b6ac8b8, S06 aa109b3c, S05 35951e23. Tier table (N7):

| Tier | Cases |
|---|---|
| required (unchanged) | M04, RM01, RM02, RP01, RP02, RP03, RP05, RS01 |
| recommended (unchanged) | M03, P04, RM04, S02, S03, S04, S05 |
| recommended -> **optional** | M01, M02, P05, RP04, RS02, RS03, RS05, RS06, S01, S06 |
| none (unchanged; stored negative follow-up kept) | P01, P02, P03, RM03, RS04 |

Canonical rationale, recommended: "<the suggestive feature> can occur in NMOSD or MOGAD; a targeted
cell-based assay lowers, but does not exclude, those diagnoses." Optional: "<typical presentation>
without a red flag or a feature suggestive of NMOSD or MOGAD: the assay is optional; a negative result
lowers but does not exclude them." Delete "settles it/them before DMT", "exclude NMOSD and MOGAD before
DMT" in every criterion rationale (measured: RS05, RS06, S01-S06). Delete prohibition "Do not start a
DMT before NMOSD and MOGAD are excluded; ..." in S05 and S06. S06 prohibition[0] -> "Do not diagnose
NMOSD from the cord lesion: it spans one segment and is eccentric, with brain lesions typical of MS".
Keep P04 prohibition[1] and M04/P04 ELISA prohibitions. Differential entries that cite a negative CBA
stay `low` with their other features; none says "excluded" (RP03 fixed by C13). Stop rules: unchanged
(optional and recommended are not in them). No change to the stored assay follow-ups.

### C15. P05 natalizumab and platform prohibitions (D15)
Note: P05 36c0f924. Delete prohibition[2]; prohibition[3] -> "Do not start natalizumab without an
explicit PML benefit-risk discussion: her anti-JCV index of 2.84 is in the high-risk range (above 1.5)".
Must[3] keeps "preferring an anti-CD20 antibody ... over natalizumab given the anti-JCV index of 2.84"
but its "three attacks in 18 months" is checked against N2.

### C16. RS01 vascular assessment (D16)
Note: RS01 ca5f6a94. Add criterion `action-vascular-imaging`, **required**, `order_advanced_imaging`
`{modality: MR_angiography}`, label "MR angiography of the head and neck", rationale "Sudden onset on
waking at 61 with hypertension and dyslipidaemia: the vertebrobasilar circulation must be imaged before
the pontine deficit is attributed to demyelination", citations `[AHA_2021_SecPrev]`; stored follow-up
(`order_advanced_imaging`, `modality: MR_angiography`, trigger `request_mr_angiography`) reporting
normal intracranial and cervical arteries with a patent basilar and both vertebral arteries, no
stenosis, occlusion or dissection (impression only that); place after the spine MRI; add to
`required_before_assessment`. Differential "Pontine lacunar infarct" key_features -> "For: age 61,
hypertension, dyslipidaemia, sudden onset on waking. Against: patent vertebrobasilar arteries on MRA,
multiple lesions of different ages in periventricular, juxtacortical and cerebellar sites, a C5-C6
cord lesion and CSF-restricted oligoclonal bands. Normal ADC at one week and enhancement do not by
themselves exclude a subacute infarct." (cite [Allen_2012] in a rationale if needed). KCE[3] -> the
same point (patent vertebrobasilar arteries plus the multifocal pattern; ADC not used alone). Delete
avoided `avoid-waste-3-order-echocardiogram` and `avoid-waste-4-order-cardiac-monitoring` (normal
fallbacks stay). Red herring wording "stop after a vascular work-up" -> "stop at a lacunar-infarct
diagnosis". Prohibition[1] stays. max_additional_actions stays 2.

### C17. Head CT wording and RM04 hypercalcaemia (D17)
Note: RM04 0f34eee4. Class: avoided `order_ct_scan` rationales that say "CT" without "head" (18 of 27:
P03, P04, P05, RM03, RM04, RP01, RS01-RS06, S01-S06): first word(s) "CT" -> "Head CT" (wording only).
RM04: rationale "A head CT does not show demyelinating lesions; the MS-protocol MRI answers the
neurological question"; add optional `action-chest-ct` (`order_body_imaging` `{study: chest_CT}`,
label "Chest CT for the PTH-independent hypercalcaemia", citations none) with a stored normal chest CT
follow-up (no hilar or mediastinal lymphadenopathy, no perilymphatic nodules, no mass); place after
OCT, before the drug check; probe that `chest_CT` is answered by it and nothing else changes. New must:
"Investigate the PTH-independent hypercalcaemia separately (chest imaging, PTH-related peptide and
1,25-dihydroxyvitamin D, with endocrinology), since sarcoidosis and malignancy are not excluded by the
neurological work-up." Differential neurosarcoidosis keeps "low".

### C18. Ancestry (D18)
Note: S03 d26941cf. DECLINED: S03 `patient.demographics.ethnicity` = "African American"; no field of
S03 mentions East Asian descent. No change.

---

## 3. Per-case index (all 30)

Legend: ruling for each note id; "Class" = class findings to apply in a case even without a note. No
case is approved.

**MS-RR-M01**
- 3c36ea1f-302e-43f4-8244-a01ce0e615e4 FIXED (C1, class LIT 393c547e; none left).
- d314b506-c37c-4e83-94cf-c2b7aa1dadce FIXED (C2, class MRI-CONTRAST 71517e55).
- 8d31a900-599b-422c-baf5-ceb86ba49b43 FIXED: must[1] rewritten per C7 (6 weeks) with C6 infection
  clause.
- 9aac7870-94d2-4225-a0fa-d80f9a4e44da FIXED: must[3] per C5 (DMF: CBC with lymphocytes, liver tests).
- Class: C4 (must[2], KCE[1]), C8 (must[4]), C14 AQP4 recommended -> optional.

**MS-RR-M02**
- 5d684e76-8ca7-4b5f-8a9e-2719ca145f05 FIXED (C1).
- 8fd691d8-4396-4aee-95d7-5410960c74ee FIXED (C2).
- f67f4b40-2aeb-4761-bb1c-4d7175e8605a FIXED: must[3] per C5 (DMF).
- Class: C6 + C7 (must[1], 3 weeks), C8 (must[4]), C14 -> optional; C4 check KCE[1] (documented
  optic neuritis with RAPD/pallor: stays "earlier attack").

**MS-RR-M03**
- 98a5a8bf-0564-424a-b3e0-eb977ea9aec8 FIXED (C1).
- 1c8c3cec-b50a-46a0-aeb9-50075977cfe1 FIXED (C2).
- 93f50957-994c-4fc5-bc22-464f0cefbb1a FIXED: must[3] per C5 (DMF).
- Class: C4 (KCE[1] -> possible earlier attack), C6 (must[1], 2 weeks: within window), C8 (must[4]);
  C14 stays recommended (current right colour desaturation with myelitis).

**MS-RR-M04**
- 363fdf51-23df-478f-852a-d7ea35edd9ff FIXED (C1).
- 163a39be-9fa2-47b0-9e05-c876a2fcdd0e FIXED (C2).
- 4fd4a20e-b413-4a62-ae50-1eb387be001c FIXED: must[4] per C5 (ocrelizumab or DMF lines).
- b0c42fef-e1e0-4f34-ab2c-7fb5137d1e91 FIXED: must[1] canonical text in C4; KCE[1] and must[3] per C4.
- Class: C14 required (unchanged).

**MS-RR-P01**
- 5d2b6ecb-b9eb-4a71-ba6c-c7cf9c96dc46 FIXED (C1).
- 038773d3-7dcf-4158-9858-b44a7fdc322e FIXED (C2).
- 8396c5dc-557a-47c1-8033-9ffff16eb820 FIXED: must[0] and KCE[0] per C4 (MS, RR not demanded; episodes
  possible attacks); diagnosis scoring already accepts "multiple sclerosis" (no synonym change).
- 08a37986-9f3d-44fd-a6f8-0f624f5dac49 FIXED: must[3] per C5 (DMF).
- Class: C3 (KCE[2]); C4 must[2].

**MS-RR-P02**
- 50c224da-d57e-4a33-9244-76fce24d0da9 FIXED (C1).
- 44d2787c-f683-4ee6-9c8c-8c06aa26d6eb FIXED (C2).
- b3e864f0-d5f4-4143-80d2-5630d8adf00f FIXED: must[3] per C5 (DMF).
- 4fc5612f-9672-418d-9fbc-87202bf77af0 FIXED: must[2] with the physician's exact phrase (C4); KCE[0].
- Class: C3 (KCE[2]); must[0] drop the RR demand per C4.

**MS-RR-P03**
- 63fd1103-5243-4e07-9053-9f4e6f4fc35a FIXED (C1).
- 30374b22-bb3d-4b96-9e84-bb1cca0e2905 FIXED (C2).
- 62865b19-0fd0-4d1f-9541-0b4177aa7349 FIXED: must[0] canonical text in C3; KCE[2] per C3.
- Class: C5 (must[3], no note; class lists); drug-check output universal screening sentence (C5).

**MS-RR-P04**
- cf79fc34-e0a8-4630-8851-bd846872f907 FIXED (C1).
- 2c3e8c48-8a6c-462d-a979-2b25a7c68e44 FIXED (C2).
- bc2383f3-55db-4e75-bb4f-590cb8b75dbf FIXED: must[1] per C6 and C7 (16 days; disabling 20/80 optic
  neuritis with myelitis: treatment remains reasonable, written as an individual decision).
- Class: C5 (must[4], class lists + anti-JCV; drug output sentence), C8 (must[2]), C14 recommended
  (simultaneous ON and myelitis), prohibition[1] kept.

**MS-RR-P05**
- 3d3a5404-7c84-4aab-a698-011394cfc7f3 FIXED (C1).
- d79462a1-3b9f-454a-abb4-768d5a1e9169 FIXED (C2).
- 222ff635-aab6-492c-8bc1-cc0854e752e4 FIXED: must[1] per C6 and C7 (3 weeks).
- 36c0f924-41e5-47f1-b744-ed8b59f85e24 FIXED: C15 (delete prohibition[2], reword [3]).
- Class: C5 (no note; anti-CD20 with stored serology, add immunoglobulins; drug output cladribine
  split), C8 (must[2]), C14 -> optional, C4 check must[3] count.

**MS-RR-RM01**
- d4b7cca1-381c-49b1-9f76-042b2e50f85d FIXED (C1).
- d7aadfb2-a8fb-423f-af38-808111daad48 FIXED (C2).
- 7a15f67e-ff2e-42ec-8bad-58d55fd34aea FIXED: C11 (hard constraint + pre-LP must).
- Class: C10a (must[2], prohibition[1]), C5 (must[5]), C4 (KCE[0], must[0] "earlier attack").

**MS-RR-RM02**
- 53481544-a074-4440-b75c-4b93b585c9f1 FIXED (C1).
- bbe19a4a-71b4-42dc-a831-8ef38b995ed3 FIXED (C2).
- aac7f149-e134-4800-aacb-be2c01b4d2a4 FIXED: C11.
- Class: C10a (must[1], prohibition[1]; biopsy fallback tissue report), C5 (must[5]), C4 (KCE[0],
  must[0]).

**MS-RR-RM03**
- 871beb4f-0c54-4160-8ecd-c8781106c9e9 FIXED (C1).
- f977f1a8-ff4d-48fb-aeed-bdcee9ee1459 FIXED (C2).
- d5d8ad08-df4a-4aaf-87fa-837ebd2f2a48 FIXED: must[4] per C5 (DMF: CBC with lymphocytes, liver tests;
  renal function and urinalysis may stay only as "per local label" or go; HBV/HCV/VZV out).
- Class: C17 CT wording.

**MS-RR-RM04**
- ae3e2c68-775e-4c68-a96b-700fe4199544 FIXED (C1).
- 4ba826e1-ba6a-4004-be96-23094222319e FIXED (C2).
- 42b55638-8b44-4f32-8aaf-b5b55248dd99 FIXED: must[1] per C6 and C7 (3 weeks).
- 0f34eee4-8a1c-432a-8dbb-d06c321e7c6a FIXED: C17 (head CT rationale, optional chest CT criterion
  with stored report, hypercalcaemia must).
- 7667e073-57b7-436a-b5e0-bd86638de1d4 FIXED: must[5] per C5 (natalizumab: anti-JCV status and index;
  alternatives' checks).
- Class: C8 (must[2]); C14 recommended (painful tonic spasms); must[0] "two earlier right optic
  neuritis episodes are prior attacks" stays (residual RAPD, pallor).

**MS-RR-RP01**
- df7f1041-fb9b-4788-8a36-d7208c4c325e FIXED (C1).
- f0066d39-69d5-4a4b-be6e-1194e9fa084a FIXED (C2).
- 25994494-23bc-4858-94f5-6c0e93f22c2c FIXED: C10a (must[1], prohibition[1]; biopsy fallback tissue
  report). Note anchored on must[0]; must[0] itself unchanged.
- af8dc3ff-758e-4fcc-a510-4f227d416012 FIXED: must[4] per C5 (interferon beta: blood count, liver
  tests, thyroid function; plus alternatives).
- Class: C11 (hard constraint + pre-LP must), C17 wording.

**MS-RR-RP02**
- af14ba3e-b955-4912-b20a-1149d674de45 FIXED (C1).
- 82bf0764-9f9c-4fee-aa93-0321ac192323 FIXED (C2).
- 26f64ab1-f140-4102-95bc-3dc912091ea5 FIXED (C1; the literature criterion is gone).
- 64579059-6d6e-4f38-a256-edf064b2165c FIXED: C10 RP02 (biopsy required + stop rule; must[1] and
  prohibition[1] allow treatment on deterioration).
- c1fa2929-feb9-41b4-9466-3214672a88de FIXED: must[5] per C5 (class lists).

**MS-RR-RP03**
- 0b10d18c-6dff-4218-92a9-7507df825654 FIXED (C1).
- 5ac01e02-d1bc-41c2-b327-35f04cdb8b48 FIXED (C2).
- f273dd7b-d41f-400c-9404-172e2a7ee86a FIXED: C12 (new must, required `action-abg` with stored ABG,
  stop rule, prohibition[1]). Note anchored on must[0]; must[0] unchanged.
- b3996cce-a127-4bc0-8754-eeef721d5c0a FIXED: C10 RP03 (must[2], must[3], prohibition[2]).
- 7f4a6c46-8999-456d-a37a-ef2c86dc1e57 FIXED: C13.
- 5303a100-0e7e-459f-bf1e-b0b7a1ac63b3 FIXED: must[6] per C5 (class lists).

**MS-RR-RP04**
- 6ab3508a-c6a9-45a5-911e-3f1df57c431e FIXED (C1).
- ed9bc1cc-1c97-4877-8031-6409cdc25ee2 FIXED (C2).
- 9b069b39-441b-478f-92e6-4db924528514 FIXED: must[3] per C5 (ocrelizumab: HBV and immunoglobulins,
  as the physician says).
- Class: C7 (steroid must, 6 weeks), C14 -> optional.

**MS-RR-RP05**
- 4f862a4d-3004-496a-9dd5-79020ebfba8f FIXED (C1).
- 6dbe45a8-9e06-41a1-9de3-5c1883a34c7c FIXED (C2).
- ae3e77f6-b3d3-44b7-8060-84931adfedb2 FIXED: must[1] per C6 and C7 (3 weeks; keep glucose and
  potassium clauses).
- 99088fd7-f9d2-4f04-8b6d-022007ea22d1 FIXED: must[4] per C5 (class lists, keep diabetes infection
  risk) and prohibition[3] per C9.
- Class: C14 required (unchanged).

**MS-RR-RS01**
- 130a223d-80e8-4778-8b9e-eae1cfc611aa FIXED (C1).
- 85934a28-b27a-460b-9acb-42d38c2d0538 FIXED (C2).
- ca5f6a94-8025-44e8-85dc-bb37d02a4606 FIXED: C16 (required MRA criterion + stored report + stop
  rule; differential, KCE, red herring; echo and monitoring waste labels deleted).
- 57aa1800-199f-460e-8cea-7c938dbdb2f1 FIXED: must[4] per C5 (ocrelizumab: HBV and immunoglobulins;
  keep the age-related infection-risk point in must[3]).
- Class: C17 wording.

**MS-RR-RS02**
- 73fb67cf-9f81-4cf8-9582-8bac67a753d1 FIXED (C1).
- a4cc567e-357e-41d9-ad3f-5105eb1f2546 FIXED (C2).
- 55123805-904b-4eff-9495-7de35705bc93 FIXED: must[1] per C6 (10 days: within window).
- 5d08d9ce-1dc6-40e7-9ac2-df6f0ab0c7f3 FIXED: must[5] per C5 (ocrelizumab).
- Class: C8 (must[2]), C14 -> optional, C17 wording; C4 check (residual pallor: stays).

**MS-RR-RS03**
- 8b35361b-5011-445a-9a24-ca957034736d FIXED (C1).
- 05fc7082-d1aa-403f-b40e-1a279b93358a FIXED (C2).
- 414f3aaa-465f-4f4b-bb4c-94499f462099 FIXED: must[1] per C6 (4 days).
- 3a28a3e0-9014-45f5-9d79-952c7b48da51 FIXED: must[5] per C5 (ocrelizumab).
- Class: C8 (must[2]), C14 -> optional, C17 wording; C4 check (residual paraparesis: stays).

**MS-RR-RS04**
- b5ef007c-03c7-49e2-8075-ca4e7bff52ad FIXED (C1).
- d23ff70b-7062-4be0-8d50-f2d91e8c0ee8 FIXED (C2).
- c2cb2aec-10a9-4e74-9789-43e9048b0e62 FIXED: must[2] per C4; check must[0] and KCE for the count.
- d196fb36-1832-4728-abee-c65b48b0686d FIXED: must[3] per C5 (DMF: CBC with lymphocytes, liver tests).
- Class: C17 wording.

**MS-RR-RS05**
- 3039f409-6e75-4eca-a118-fefa531aadf2 FIXED (C1; "np" read as "no").
- 02f9bb04-b849-47e6-8f0c-3a78e493a16c FIXED (C2).
- 8d8410b0-4d9a-45c4-ba10-517682cebc72 FIXED: must[4] per C5 (natalizumab: anti-JCV; no universal
  HBV/HCV/VZV).
- Class: C14 -> optional (rationale "before DMT" deleted), C17 wording, C4 check must[0]/must[3]
  "two attacks" (residual sign needed).

**MS-RR-RS06**
- e7e97eea-6649-4396-9b02-ce139af1a922 FIXED (C1).
- e20a2dcb-fd16-41a5-bec4-feae705cd3cb FIXED (C2).
- 43400e82-e5f4-4990-bbed-6b4d729a9712 FIXED: must[5] per C5 (natalizumab anti-JCV; anti-CD20 HBV and
  immunoglobulins; S1P VZV immunity, ECG).
- 31eb1284-86db-4ee3-b891-33b5eff70a22 FIXED: C9 (drug-check warning rewritten).
- Class: C14 -> optional, C17 wording, C4 check must[0] "two attacks".

**MS-RR-S01**
- ea2f16a2-e4b4-4cb5-a730-b2957fe6728b FIXED (C1).
- cb6ba1af-b29e-42a4-ba2a-b39ff8fcd9d0 FIXED (C2).
- 09a248b7-1b75-4cc2-b726-9c8185842fd5 FIXED: must[3] per C5 (DMF: CBC with lymphocytes and liver
  function, as the physician says).
- Class: C14 -> optional, C17 wording.

**MS-RR-S02**
- 8ad157e1-edde-42c2-8fdb-3dc4d122af6e FIXED (C1).
- 3e6f650b-2d74-4724-bbef-6d1ae412ccf8 FIXED (C2).
- d39dab89-51a7-48c5-bf91-74f295aaf180 FIXED: must[4] per C8.
- 3d927c95-306d-4928-b224-0d08a7a3cf3c FIXED: must[3] per C5 (class lists).
- Class: C6 (must[1], 14 days: within window), C14 recommended (rationale "targeted"), C17 wording.

**MS-RR-S03**
- c71a0068-7b59-4c96-a9dd-86d17f8aa6d1 FIXED (C1).
- 7f298746-b004-4a21-a345-ab737c8f617e FIXED (C2).
- d26941cf-3b60-4a59-95af-7cc2b6d3a5e6 DECLINED (C18: the patient is African American; the note
  describes another patient).
- b2269e22-08ff-4bad-bdbc-d0cd5398bd47 FIXED: must[1] per C6.
- 572f1efc-98f3-4de6-bfc3-5996951e0819 FIXED: must[4] per C8.
- e5700afc-2bc1-4fdf-bc23-30027340fb0a FIXED: must[3] per C5 (ocrelizumab: HBV and immunoglobulins).
- Class: C14 recommended (rationale "targeted"; ancestry clause may stay), C17 wording.

**MS-RR-S04**
- cc2af8db-7b22-4139-bb02-07819245c6ca FIXED (C1).
- 84d4820f-3067-45bc-8a03-96465db13c7c FIXED (C2).
- 2f73da0e-b01c-41cc-a2e0-0434c9ccd0d7 FIXED: must[1] per C6.
- 5ddb7080-92d3-483d-bf72-87f4b7ed8a64 FIXED: must[4] per C8.
- 1d31027a-cd2e-434c-ae4c-29ed6c9ad4e9 FIXED: must[3] per C5 (ocrelizumab: HBV and immunoglobulins).
- Class: C14 recommended (rationale "targeted"), C17 wording.

**MS-RR-S05**
- fa1f7b44-81f5-4d0e-8934-6d6abe61f740 FIXED (C1).
- afe3b540-cda4-4e22-8685-14f929df29e1 FIXED (C2).
- f3f11452-9da6-42bf-9230-8feaf8d2da8b FIXED: must[3] per C5 (class lists).
- 35951e23-bc55-4ff8-a1f1-5167071092f5 FIXED: C14 (delete prohibition[1]; rationale "targeted";
  AQP4 stays recommended for the disc swelling; differential[1] wording already non-absolute).
- Class: C17 wording.

**MS-RR-S06**
- 940c4226-b02c-480b-89f7-c8d7613d9c03 FIXED (C1).
- ed6f0d3b-9112-4b8f-b38e-59945341e1cf FIXED (C2).
- 9b6ac8b8-1765-4da2-84e7-a5c1f080a8c5 FIXED: C14 (action-aqp4-mog-cba recommended -> optional).
- aa109b3c-5e68-4df4-864e-da2f7b57f580 FIXED: C14 (prohibition[1] deleted, prohibition[0] reworded,
  rationale "before DMT" deleted).
- b2ed8a7b-9c12-445d-957b-2b9d9656d7af FIXED: must[3] per C5 (class lists).
- Class: C6 (must[1], 12 days: within window), C8 (must[4]), C17 wording.

---

## 4. CENTRAL requests

1. **Criteria pack** `dataset-generation/criteria_packs/MS-RR.md` (orchestrator, after the cases
   land): 1.3 add "after a typical attack; in non-specific presentations and RIS, DIS is completed by
   DIT, CSF or CVS" (D3); 1.9 replace the steroid gate with N6 (D10); section 2 AQP4/MOG tier lists
   per D14 (8 required, 7 recommended, 10 optional, 5 none), RP02 biopsy required, RS01 MRA required,
   RP03 ABG required, RM04 chest CT optional, hard MRI-before-CSF in RM01/RM02/RP01; section 3 "head
   CT"; section 4 drop "natalizumab with anti-JCV index above 1.5" as a prohibition (now benefit-risk);
   section 8 musts per N3, N4, N5 and C7; section 9 allow-list add `[Fowler_2009]`,
   `[EHA_ESMO_PCNSL_2024]`, `[AHA_2021_SecPrev]`, `[Allen_2012]` with the references of section 1.
2. **`agent-platform/config/review/condition_tool_guidance.yaml`** `multiple_sclerosis.interpret_labs`
   `our_response`: "required in 8 ... and recommended in 17 with optic neuritis or myelitis" becomes
   "required in 8 with a red flag, recommended in 7 with a feature suggestive of NMOSD or MOGAD
   (simultaneous optic neuritis and myelitis, disc swelling, painful tonic spasms), optional in 10";
   `order_specialized_test` unaffected; regenerate with `build_condition_tool_guidance.py`.
   `test_guidance_claims.py` MS claims (AQP4 counts, CT/echo avoided counts: echo and monitoring waste
   now 29 instead of 30) are maintained centrally.
3. No synonym, vocabulary (`ABG`, `MR_angiography`, `chest_CT`, `stereotactic_biopsy` all exist),
   library, MockServer or review-app change is needed for any MS-RR note.

## 5. Open questions

None that need information only Andrea has. For the physicians at re-review: the AQP4/MOG tier
change (10 cases recommended -> optional) applies R1's S05/S06 ruling across the condition; RS01 now
requires vascular imaging; RP02 now requires the biopsy; RP03 requires a blood gas.

<!-- PLAN COMPLETE -->
