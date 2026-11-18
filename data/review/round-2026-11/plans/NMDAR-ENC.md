# NMDAR-ENC: lead plan, November 2026 round (17 Nov 2026)

**Workers.** Read `ROUND_POLICY.md`, `NOVEMBER_ADDENDUM.md` and `NMDAR-ENC-decisions.md` (D1-D35),
then this plan. Apply the classes in section 2 (canonical texts verbatim, with `<...>` slots filled
from the case), then the case items in section 3.

**Note set.** 35 notes, all from R2 (NB-87MF-FBTV-TPWE). 24 are policy verdicts with comments, 11
are plain approvals and 5 are case comments.

**Approved cases** (`approved.txt`): P03, P07, P08, RM02, S01, S02, S03, S04, S06, S09, S10. They
carry the same template musts the physician ruled wrong (PLEX 5-7, 10-14 days, the 72 h rule) and
are changed only for those class defects. Say so in each log.

**Checks after editing:**
- `perfect_agent.py CASE -v`
- `case_io.py check CASE`
- `mri_probe.py CASE` (only if the MRI was touched)
- `served()` on every new or changed body-imaging, lab and microbiology order. CAP CT stored as a
  follow-up also answers `chest_CT` orders (SKILL_NOTES), so check both.

---

## 1. Governing guidelines and canonical facts

- **Which source governs:**
  - Graus 2016 governs the diagnosis.
  - Abboud 2021 (JNNP 2021;92:757-768) governs acute management, tumour screening and escalation.
    R2 cites it in every note.
  - ESCMID 2016 governs empirical bacterial cover, with NICE NG240 for cephalosporin use in a
    penicillin allergy.
  - Spasovski 2014 governs hyponatraemia, Lejuste 2016 neuroleptic intolerance, ASCO irAE 2021 RP02
    and Armangue 2018 the post-HSV cases.
- **Verified 17 Nov 2026:**
  - Graus 2016: "CSF HSV PCR can be negative if done too early (eg, within 24 h), and this test
    should be repeated if the clinical suspicion remains high".
  - Abboud 2021:
    - PLEX 5-10 sessions every other day;
    - add IVIG or PLEX if there is no improvement by the end of the initial steroid cycle;
    - IVIG first in agitated patients and in bleeding disorders;
    - PLEX first in severe hyponatraemia, high thromboembolic or cancer risk, or brain or spinal
      demyelination;
    - IVIG may worsen hyponatraemia by volume expansion;
    - second line after 2-4 weeks without response;
    - before the CSF is analysed, CNS-dose aciclovir plus standard bacterial meningitis cover.
  - ESCMID 2016: Listeria cover above 50; vancomycin where there is pneumococcal resistance.
- **Taken from R2's reading of Abboud** (not contradicted by any verified passage):
  - methylprednisolone 1 g/day for 3-7 days;
  - IVIG 2 g/kg over 2-5 days;
  - cyclophosphamide 600-1000 mg/m²;
  - box 1 item 9 (combined start for severe presentations);
  - box 1 item 13 (bridging with an oral prednisone taper, or monthly IVIG or methylprednisolone).
- **In-text sources in musts.** Musts are plain strings. A must whose rule comes from a specific
  source ends with a short parenthetical: "(Graus 2016)", "(Abboud 2021)", "(Spasovski 2014)",
  "(Lejuste 2016)", "(ESCMID 2016)", "(ASCO 2021)". The physician asked for missing sources (M01:
  "three missing sources").
- **Spelling.** Keep each case's spelling convention (acyclovir/aciclovir, tumor/tumour, m2/m²). No
  em dashes in new text. Units follow the case (mEq/L or mmol/L).

## 2. Classes

Counts are measured over all 30 NMDAR-ENC cases with scripts in
`/home/aprotani/review-round-2026-11/work/scratch/nmdar-lead/` (`measure.py`, `measure2.py`,
`factors.py`, `musts.py`). Where cheap, they are also counted over all 600 cases.

### K1 MRI contrast header: ALREADY-FIXED (D1)
- **Notes:** S03 7907651d, S04 0d6e3601, S06 1d9f3e58, S09 f0dd0c07, S10 18186d99, plus the MRI
  sub-point of the verdicts of P01, P06, RP01, RP02, RP03, RS01, RS03, RS04 and M05.
- **Measured** with `mri_probe.py`, all 30 cases: the plain order gets `contrast_used=False` with no
  gadolinium text; the `{contrast: true}` criterion gets `contrast_used=True` with gadolinium text.
- **Done:** class MRI-CONTRAST (commit 71517e55). No edit. Log the ruling as "ALREADY-FIXED (class
  MRI-CONTRAST, commit 71517e55; mri_probe clean)".

### K2 Must 1, aciclovir and empirical bacterial cover: all 30 (D2, D3)
- **Notes:** every verdict with comments.
- **Measured:**
  - 28 of 30 musts carry the "within 72 hours" clause (P03 and RP03 are the post-HSV restart
    texts). The clause appears in no other condition.
  - 0 of 30 have bacterial cover, except RP02 (ceftriaxone for aspiration, must 8).

**Canonical text (non-post-HSV cases):**

> "Start IV <aciclovir|acyclovir> 10 mg/kg every 8 hours at presentation<, renal clause><, with
> hydration and without NSAIDs (hold <drug>)>, with empirical bacterial meningitis cover (<regimen>)
> until the CSF cell count, Gram stain and culture exclude bacterial infection (Abboud 2021, ESCMID
> 2016); stop <aciclovir> once CSF HSV PCR is negative and the antibody diagnosis is established.
> HSV PCR can be negative if done too early (for example within 24 hours of onset) and is repeated
> if clinical suspicion of HSV encephalitis remains high (Graus 2016)."

**Early-LP cases** (RS03, onset 1-2 days before the LP; RP02, about 24 hours): replace the last
sentence with:

> "The LP was within <interval> of onset, when HSV PCR can be falsely negative (Graus 2016): continue
> <aciclovir> and repeat the HSV PCR on a second CSF sample before stopping it."

RP02 adds: "HSV encephalitis is less likely (afebrile, normal medial temporal lobes), but
high-dose steroids are starting."

**Post-HSV cases** (P03, RP03): keep the restart text and add the cover clause "<...>, with
empirical bacterial meningitis cover (<regimen>) until the CSF Gram stain and culture are negative".
Then: "HSV PCR can be negative if done too early (for example within 24 hours of onset) (Graus
2016); repeat it if the relapse remains clinically suspected." RP03's physician question is answered
by the clause itself: the cover applies until the CSF results return, and the normal procalcitonin
makes it short.

**Regimens** (D3; check each case's allergy list again):

| case group | regimen |
| --- | --- |
| No beta-lactam allergy, under 50, not immunosuppressed: M03, M04, M05, P01, P02, P03, P05, P06, P07, P08, RM01, RM02, RS01, RS03, RS04, S01, S03, S06, S10 | ceftriaxone 2 g IV every 12 hours with vancomycin |
| Non-severe penicillin or amoxicillin rash, under 50: M02, P04, S04, S09 | ceftriaxone 2 g IV every 12 hours with vancomycin (a cephalosporin is acceptable after a non-severe penicillin rash) |
| Cephalosporin hives: M01, S02 | meropenem 2 g IV every 8 hours with vancomycin (a non-cephalosporin regimen) |
| 50 or older, no penicillin allergy: RP01 | ceftriaxone with vancomycin and amoxicillin 2 g IV every 4 hours for Listeria |
| RS02 (age 50, recent high-dose steroids, valproate) | ceftriaxone with vancomycin and amoxicillin 2 g IV every 4 hours; no carbapenem (it sharply lowers valproate levels) |
| 50 or older with a penicillin rash: RM03, RP03 | ceftriaxone with vancomycin and co-trimoxazole for Listeria |
| RP02 | "the ceftriaxone of must 8 is also the meningitis cover until the CSF culture is negative, with co-trimoxazole for Listeria (renally adjusted; monitor potassium on lisinopril)" |

**Renal clause** (RP02 only): "adjusted to every 12 hours for his creatinine clearance of about 46
mL/min (Cockcroft-Gault)" (D19).

**NSAID hold:** keep it where present (P06, RS01, RS03). Add "hold ibuprofen while IV <aciclovir>
and high-dose steroids are given" in RM01 and RM02 (on ibuprofen, no hold yet).

### K3 Must 2, first-line immunotherapy: all 30 (D4, D5, D6)
- **Notes:** every verdict with comments.
- **Measured:**
  - 30 of 30 musts say "1 g daily for 5 days" (RP02: "3 to 5 days");
  - 29 say "5 to 7 exchanges" in the musts;
  - 8 also say it in a drug-interaction output (`alternatives`): P04, RM03, RP01, RP02, RS01, RS03,
    RS04, S01;
  - 28 offer "IVIG ... or plasma exchange" without a trade-off.
  - Elsewhere in the dataset, "5 to 7 exchanges" is found only in MS-RR (1 case).

**Canonical combined text:**

> "Start first-line immunotherapy once infection is reasonably excluded on the CSF results, without
> waiting for the antibody result: IV methylprednisolone 1 g daily for 3 to 7 days, combined from
> the start with IVIG (2 g/kg over 2 to 5 days) or plasma exchange (5 to 10 sessions every other
> day), because the presentation is severe (<reasons>) (Abboud 2021). <Agent sentence><; case
> cautions kept: glucose, potassium, IgA, etc.>."

**Canonical sequential text** (P01, P04, RM03, RP01):

> "<Timing sentence>: IV methylprednisolone 1 g daily for 3 to 7 days, adding <agent, dose> if there
> is no clinical improvement by the end of the steroid course; combined therapy from the start is
> reserved for severe presentations, and this one is <mild|ward-level> (Abboud 2021). <Agent
> sentence>."

**Agent sentence:**

> "<Preferred> is preferred here (<factors for it>); <factors for the other> favour <other>, which
> remains the alternative<, precaution>."

**Precautions:**
- IVIG with Na below 135: "monitor sodium, as IVIG can worsen hyponatraemia".
- IVIG with a thrombotic factor: "with hydration, a slow infusion rate and VTE prophylaxis<, and
  the oestrogen contraceptive stopped>".
- PLEX: "with central venous access and haemodynamic monitoring<; give <drug> after each exchange>".

**Per-case decision table** (from `factors.py` and the exam; Na in the case's units):

| case | start | reason for combined, or tier | preferred | for preferred / for the other |
| --- | --- | --- | --- | --- |
| M01 | combined | profound hyponatraemia with seizures, HDU | PLEX | Na 122, COC, teratoma / agitation (benzodiazepines; secure the line) |
| M02 | combined | five Graus groups with seizures and heart-rate lability | IVIG | agitation, no PLEX factor / none (Na 136) |
| M03 | combined | seizures, heart-rate lability with diaphoresis, agitation under restraint | IVIG | agitation under restraint / teratoma, COC: stop the COC, VTE prophylaxis, Na 131 |
| M04 | combined | combative agitation, seizure, mutism | IVIG | agitation / Na 129, 3.8 cm teratoma: monitor sodium; PLEX if sodium falls |
| M05 | combined | GCS 12 with recurrent seizures | PLEX | Na 128, no agitation or dysautonomia / none |
| P01 | sequential, mild | n/a | PLEX | teratoma, COC (thrombosis flagged in the DDI step) / mild agitation |
| P02 | combined | ICU: GCS 12, seizures, dysautonomia | IVIG | agitation, dysautonomia / testicular tumour: Na 131 |
| P03 | combined | autonomic instability with seizures | IVIG | agitation, dysautonomia / none: Na 133 |
| P04 | sequential, mild | n/a | PLEX | teratoma / none |
| P05 | combined | catatonia with food refusal, subclinical seizures, ICU | IVIG | agitation / no tumour or hyponatraemia: Na 131 |
| P06 | combined | dysautonomia and seizures, ICU | IVIG | dysautonomia / teratoma: Na 134 |
| P07 | combined | ICU: dysautonomia, electrographic seizures | IVIG | agitation, dysautonomia / teratoma |
| P08 | combined | ICU: dysautonomia, recurrent seizures | IVIG | dysautonomia, agitation / teratoma: Na 130 |
| RM01 | combined | combative agitation, dysautonomia, seizures | IVIG | agitation, dysautonomia / none: Na 131 |
| RM02 | combined | ICU: GCS 12, central hypoventilation | IVIG | agitation / teratoma, COC: VTE prophylaxis and COC review (must 9); Na 131 |
| RM03 | sequential, ward | n/a | IVIG | orthostatic hypotension argues against PLEX volume shifts / Na 128, age 62, ex-smoker: slow infusion, hydration, VTE prophylaxis, check osmolality before treating a sodium fall |
| RP01 | sequential, ward; after vascular imaging | n/a | PLEX | age 61, diabetes, hypertension, LVH (IVIG thrombotic risk) / none |
| RP02 | steroids, adding IVIG or PLEX for severity (keep) | ICU: GCS 7 | PLEX | active lung cancer, age 76, IVIG AKI risk with lisinopril in CKD / dysautonomia, agitation: hold lisinopril, haemodynamic monitoring |
| RP03 | combined | ICU: dysautonomia, seizures | IVIG | agitation, dysautonomia / coronary disease: slow infusion and hydration (kept), VTE prophylaxis, Na 131 |
| RS01 | combined | ICU: hypoventilation, dysautonomia, seizures, catatonia | IVIG | agitation, dysautonomia / COC, immobility, teratoma: COC stopped and VTE prophylaxis (must 9), Na 131 |
| RS02 | IVIG or PLEX now plus repeat steroids (keep the structure) | failure of 3 days of steroid | PLEX | possible demyelination of the tracts, COVID-19, immobility, D-dimer 0.72 / agitation, dysautonomia: give valproate after each exchange, time enoxaparin around the catheter; if IVIG, monitor Na 131 |
| RS03 | combined | ICU: GCS 9, hypoventilation, recurrent seizures | IVIG | agitation, dysautonomia, no PLEX factor / none: Na 134 |
| RS04 | combined | bilateral optic neuritis threatening vision, plus seizures | PLEX | demyelination (optic neuritis) / agitation, dysautonomia: levetiracetam after each exchange |
| S01 | combined | dysautonomia with seizures | IVIG | agitation, dysautonomia / COC, teratoma: COC stopped and VTE prophylaxis (must 9), Na 133 |
| S02 | combined | ICU | IVIG | agitation, dysautonomia / teratoma: glucose monitoring kept |
| S03 | combined | ICU | IVIG | agitation, dysautonomia / teratoma, COC (held, must 9) |
| S04 | combined | ICU | IVIG | agitation, dysautonomia / teratoma: Na 133 |
| S06 | combined | ICU | IVIG | dysautonomia / Na 126, teratoma: monitor sodium (must 9) |
| S09 | combined | ICU | IVIG | marked dysautonomia (HR 138, BP 172/108) / Na 124, teratomas: close sodium monitoring with must 9; record the divergence |
| S10 | combined | step-down with dysautonomia | IVIG | dysautonomia, agitation / Na 127, teratoma: monitor sodium |

**Timing sentence:**
- P01: "Start first-line immunotherapy once infection is excluded on the basic CSF results, without
  waiting for the antibody result, because the Graus 2016 criteria for possible autoimmune
  encephalitis are met (subacute psychiatric and cognitive change with seizures, alternatives
  reasonably excluded) and autoimmune encephalitis is highly suspected (Abboud 2021)".
- P04: "Start first-line immunotherapy now that the CSF anti-GluN1 result establishes definite
  anti-NMDAR encephalitis; before it, neither the possible nor the probable Graus 2016 criteria were
  met".
- RM03: "... without waiting for the antibody result, because the Graus 2016 criteria for possible
  autoimmune encephalitis are met (memory deficit, seizures, CSF pleocytosis, MRI)".
- RP01: "Once vascular imaging has excluded a stroke and infection is excluded on the CSF, start
  first-line immunotherapy: the Graus 2016 criteria for possible autoimmune encephalitis are met
  through the new focal deficit (aphasia), and the CSF anti-GluN1 result is positive".

**Drug-interaction outputs:** replace "Plasma exchange (5 to 7 exchanges)" with "Plasma exchange (5
to 10 sessions every other day)" in the 8 cases. Leave `proposed` as it is (D4).

### K4 Bridging must: 29 cases (D7)
- **Notes:** M01, M02, M05, P01, P02.
- **Measured:** 29 cases have no bridging must. RP02 has the oral taper; P07's "taper quetiapine"
  is not bridging.
- **Insert after must 2:**

> "After the acute course, bridge with a gradual oral prednisone taper, or monthly IVIG or IV
> methylprednisolone, while recovery or second-line therapy takes effect (Abboud 2021)."

- RS02: write "After the acute course" as "After this second course".

### K5 Escalation must: all 30 (D8)
- **Measured:** "10 to 14 days" in 30 of 30 (this condition only); a cyclophosphamide dose in 0.
- **Canonical text:**

> "If there is no clinical or radiological improvement 2 to 4 weeks after completion of first-line
> therapy, escalate to rituximab (375 mg/m² weekly for 4 doses or 1000 mg twice 2 weeks apart, after
> hepatitis B screening) and/or IV cyclophosphamide 600 to 1000 mg/m² monthly<; discuss fertility
> preservation before cyclophosphamide> (Abboud 2021)."

- P02 and RP02 add "deciding at the earlier end of this window given the severity". P02 keeps
  "(sperm cryopreservation)".

### K6 Sourced rules: hyponatraemia and benzodiazepines (D9, D10)
- **Hyponatraemia.** "no more than 10 mEq/L (or mmol/L) in 24 hours" appears in M01, M04, M05,
  RM03, S06, S09 and S10. Replace it with "correcting slowly, by no more than 10 <unit> in the first
  24 hours (Spasovski 2014), to avoid osmotic demyelination". M05 adds "fluid restriction is usually
  sufficient" (Abboud).
- **Benzodiazepines.** Every agitation must ("benzodiazepines (lorazepam) first ...") ends with
  "(Lejuste 2016)". That is all cases except RP01 and RP02.

### K7 Tumour screen beyond the first study, and the tumour musts (D11, D12, D13)
- **Measured.** By demography and result:
  - Women 18-44 with a negative ultrasound: M02, P05, RM01, RS04. None has a pelvic MRI follow-up.
  - Men under 45 with a negative scrotal ultrasound: M05, RS03 (P03 is post-HSV). None has a CAP or
    chest CT follow-up.
  - Age 45 or older with a negative CAP CT: RM03, RP01, RS02 (RP03 is post-HSV, RP02 has known lung
    cancer). RM03 and RP01 have no whole-body PET follow-up; RS02 has no pelvic ultrasound.
  - 20 women aged 12-44 have only `pelvis_abdomen_ultrasound` in the required tumour criterion.
    Pelvic MRI follow-ups exist in 16 of them (all except M02, P05, RM01, RS04).
- **A. OR alternative (D13).** Add `{study: pelvis_abdomen_MRI}` to `action-5-order-body-imaging` in
  20 cases: M01, M02, M04, P01, P04, P05, P06, P07, P08, RM01, RM02, RS01, RS04, S01, S02, S03, S04,
  S06, S09, S10. Not M03.
  - Before adding it, check with `served()` that the pelvic MRI order returns a report consistent
    with the ultrasound: same side, size within 2 mm, teratoma features or normal ovaries.
  - Add "or pelvic MRI" to the label.
- **B. New recommended criteria (D11).** Each gets a new id and a follow-up placed after the
  existing diagnostic follow-ups and before the drug-interaction step. Every report is normal
  unless stated otherwise.

| case | new criterion id | alternatives | stored report |
| --- | --- | --- | --- |
| M02, P05, RM01, RS04 | `pelvic-mri-tumour-screen` | `{study: pelvis_abdomen_MRI}` | normal ovaries and uterus, no adnexal lesion, no fat-containing lesion |
| RM01, RS04, M05 | `cap-ct-tumour-screen` | `{study: chest_abdomen_pelvis_CT, contrast: true}` | no thoracic, abdominal or pelvic mass or lymphadenopathy. RS04 adds "no hilar or mediastinal lymphadenopathy" |
| RS03 | `chest-ct-aspiration-gct` | `{study: chest_CT}`, `{study: chest_abdomen_pelvis_CT, contrast: true}` | one contrast CAP CT: dependent right lower lobe consolidation consistent with aspiration; no mediastinal or retroperitoneal mass or lymphadenopathy |
| RM03, RP01 | `whole-body-pet-tumour-screen` | `{modality: whole_body_FDG_PET}` | no hypermetabolic lesion suggesting malignancy |
| RS02 | `pelvic-ultrasound-screen` | `{study: pelvis_abdomen_ultrasound}` | postmenopausal uterus and ovaries, no adnexal mass |

- **C. Tumour must, canonical texts:**
  - Women 18-44, negative ultrasound:

    > "Pelvic ultrasound shows no tumour; in an adult woman a negative ultrasound does not end the
    > screen: obtain pelvic MRI now<, and contrast CT of the chest, abdomen and pelvis>, and
    > continue tumour surveillance during follow-up (Abboud 2021)."

  - M05 and RS03:

    > "Scrotal ultrasound shows no testicular tumour; a negative scrotal ultrasound does not exclude
    > an extragonadal germ cell tumour, so obtain contrast CT of the chest, abdomen and pelvis
    > (Abboud 2021)<; RS03: it also assesses the aspiration>."

  - RM03, RP01:

    > "Contrast CT of the chest, abdomen and pelvis shows no tumour; at <age> and a former smoker,
    > obtain whole-body FDG-PET now, and repeat screening during follow-up if the course is
    > refractory or relapsing (Abboud 2021)."

  - RS02:

    > "Contrast CT of the chest, abdomen and pelvis shows no tumour; add a pelvic ultrasound now,
    > and repeat screening if the course is refractory (Abboud 2021)."

  - The mammography part for RM03 and RS02 waits for CENTRAL 1. Do not write a mammography must
    until a criterion can order it.
- **D.** Update the tumour bullet of `key_clinical_evidence` and the criterion `expected_evidence`
  to match the new results.

### K8 Teratoma resection criterion: DECLINED (D14)
- Note: M01, "teratoma removal" sub-point.
- Rationale: ROUND_POLICY rule 4 (treatment is never a tool call). Must 3 carries the removal. The
  stored `order_resection` follow-ups (16 cases) stay without a criterion.

### K9 CSF/serum glucose pairing: M01, P01, S01, S02, S03, S04 (D21)
- Notes: S03 7907651d, S04 0d6e3601.
- **Measured:** the CSF report's paired serum glucose differs from the labs glucose in 6 NMDAR
  cases. The same pairing check finds 7 MS-RR cases and ALZ-EARLY-P02.
- **Fix:** in `glucose_ratio` and the CSF interpretation, set the serum value to the labs value and
  recompute the ratio:

| case | serum glucose | ratio |
| --- | --- | --- |
| M01 | 95 | 0.67 |
| P01 | 100 | 0.58 |
| S01 | 106 | 0.58 |
| S02 | 114 | 0.58 |
| S03 | 104 | 0.58 |
| S04 | 96 | 0.67 |

### K10 Calculated versus measured osmolality: RP01, RS01
- Note: RP01, scenario sub-point.
- **Measured:** calculated minus measured is 6 in RP01 (284 vs 278) and 4 in RS01 (272 vs 268).
  All other cases are within 2.
- **Fix:** RP01 measured osmolality becomes 286, RS01 becomes 274. Change the lab row, the
  interpretation and any summary.

### K11 Lateralisation discordance: M03, M04 (D23)
- **Measured** (side counts of the MRI, EEG, cEEG and PET impressions, 30 cases): a unilateral
  opposite-side discordance exists only in M03 (MRI and PET right, EEG left) and M04 (MRI left, EEG
  and PET right).
- **Fix:** add a key-clinical-evidence bullet, in the D23 text with the case's sides. No report
  changes.

### K12 Template post-intervention cognitive screen: P01, P04, RP01 (D24)
- **Measured:** one identical output in all 30 cases, and nowhere else in the dataset. It
  contradicts the baseline in P01 (MoCA 23, near-oriented), P04 (mild, independent) and RP01
  (aphasia, not disorientation).
- **Fix:** impression "Repeat bedside screen during the admission: findings unchanged from the
  baseline screen (<baseline deficits>)". The findings rows mirror the baseline. Report no
  improvement or worsening attributable to treatment.

### K13 Performance status versus gait: P06, P08, RM03 (D25)
- Note: P06.
- **Fix:** the activity row becomes "walks with supervision; up and about less than half of waking
  hours". Keep ECOG 3 and Karnofsky 40; the self-care row is consistent. The P06 gait report (10 m
  in 12 s, unassisted tandem) and the exam stay.

### K14 Denied fever but febrile on arrival: M01, RS04 (D27)
- **Measured:** an HPI denial of fever with a temperature of 38.0 C or more occurs only in these two.
- **Fix:** append to the HPI sentence "...; she is febrile (<T> C) on arrival, a new fever". Mirror
  it in `patient.hpi` if present.

### K15 Diagnostic certainty before the antibody: P01, P04, RP01 (D15, D17)
- **P01 `prohibited_recommendations[1]`:**

> "Do not delay immunotherapy for the antibody result once the Graus 2016 criteria for possible
> autoimmune encephalitis are met and infection is excluded on the basic CSF results."

- **P04:**

> "Do not delay immunotherapy now that the CSF anti-GluN1 result is positive, for example while
> awaiting repeat testing, serum confirmation or the teratoma operation."

- **RP01:** a confirmatory tissue-based assay in the CSF antibody result (section 3).

### K16 Supportive musts from the case's own steps (D18, D19, D30, D32, D33)
- RM01, RM02: ibuprofen hold (K2).
- RP01, RP03 (aspirin with high-dose steroids): "Give gastric protection with a proton pump
  inhibitor while aspirin and high-dose steroids are given."
- RP02: Pneumocystis prophylaxis with glucose and sodium monitoring.
- P02: a hyponatraemia monitoring must.
- RS02, RS04: drug dosing after each exchange (in must 2).

### K17 Harmful tests served without an avoided action: RP03 (D20)
- Two `harm` avoided actions: coronary angiography and coronary CTA.
- Scan of the 30 cases: no other cardiac or invasive study is served without an indication.
  RP02's chest CTA, mediastinal CT and chest X-ray belong to its aspiration and lung-cancer context.

### K18 Case-specific report fixes
- RS03 blood gas and FiO2 (D22).
- RP02 creatinine and Babinski sign (D19).
- P06 EEG linked to the clinical events (D26).
- RP03 PET sentence (D35).
- RP01 MRA and the CSF tissue-based assay (D17, D18).
- RM01 MOG/AQP4 and ANA (D30).
- RS02 cultures (D28).
- RS04 sarcoid screen (D29).
- P04 FDG-PET optional (D16).

### Classes checked and not present
- Literature: none left (class LIT); a scan of the 30 cases found no literature criterion or
  output.
- Lab flags against reference range: 0 mismatches.
- CK red herrings: all above the reference range.
- HPI pronouns: the only mismatches are relatives (wife, husband).

---

## 3. Per-case index (all 30)

Legend:
- (A) marks an approved case.
- "Class" lists the class edits that apply without a note.
- Note sub-points are labelled a, b, c in the order of the note text.
- Every case has **class K2, K3, K5, K6** where it applies, and **K4** in every case but RP02.

### NMDAR-ENC-M01 (28F, teratoma, Na 122, cephalosporin hives)
NB-87M:NMDAR-ENC-M01:policy_verdict
- (a) Pelvic MRI as an OR alternative: FIXED (K7A).
- (b) Resection criterion: DECLINED (K8).
- (c) Must 2 trade-off: FIXED (K3, PLEX).
- (d) Doses: FIXED (K3).
- (e) Combined start: FIXED (K3, combined with the HDU reason).
- (f) Must 7 timing: FIXED (K5).
- (g) Rituximab regimen: NO-ACTION (correct).
- (h) Cyclophosphamide dose: FIXED (K5).
- (i) Must 1 Graus wording: FIXED (K2).
- (j) Non-cephalosporin bacterial cover: FIXED (K2, meropenem plus vancomycin).
- (k) Bridging: FIXED (K4).

Class: K6 (must 9, must 8), K9 (glucose 95, ratio 0.67), K14 (fever 38.0).

### NMDAR-ENC-M02 (33F, negative ultrasound, penicillin rash)
NB-87M:NMDAR-ENC-M02:policy_verdict
- (a) Pelvic MRI now: FIXED (K7B new criterion and follow-up; K7C must 3).
- (b) Must 2 doses and IVIG: FIXED (K3, IVIG).
- (c) Must 7: FIXED (K5).
- (d) Must 1 Graus wording and non-penicillin cover: FIXED (K2, ceftriaxone plus vancomycin; the
  rash is non-severe).
- (e) Bridging: FIXED (K4).

Note on (d): the physician asked for a "non-penicillin regimen", and ceftriaxone is one (it is not
a penicillin).

Class: K7A, K6 (must 8).

### NMDAR-ENC-M03 (25F, equivocal ultrasound then MRI teratoma)
NB-87M:NMDAR-ENC-M03:policy_verdict
- (a) Lateralisation: FIXED (K11, discordance bullet: MRI and PET right, EEG left).
- (b) Must 2: FIXED (K3, IVIG).
- (c) Must 7: FIXED (K5).
- (d) Must 1 and antibacterial cover: FIXED (K2).

Class: K4, K6 (must 8). No K7A (the MRI is the characterisation step).

### NMDAR-ENC-M04 (27F, 3.8 cm teratoma, Na 129)
NB-87M:NMDAR-ENC-M04:policy_verdict
- (a) Lateralisation: FIXED (K11: MRI left, EEG and PET right).
- (b) Must 1 wording and bacterial cover: FIXED (K2).
- (c) Must 2 doses, combined start and trade-off: FIXED (K3, combined, IVIG with sodium
  monitoring).
- (d) Must 3: NO-ACTION (physician: correct).
- (e) Must 7: FIXED (K5).

Class: K4, K6 (must 9 Spasovski, must 8), K7A.

### NMDAR-ENC-M05 (30M, tumour-negative, Na 128, GCS 12)
NB-87M:NMDAR-ENC-M05:policy_verdict
- (a) Scenario recomputations: NO-ACTION (correct).
- (b) Step-10 Abboud misquote: ALREADY-FIXED (class LIT, commit 393c547e; it was a literature output).
- (c) MRI contrast: ALREADY-FIXED (K1).
- (d) Must 1: FIXED (K2; the Solomon option is moot, D2).
- (e) Must 2: FIXED (K3, combined, PLEX).
- (f) Must 3: FIXED (K7B CAP CT criterion `cap-ct-tumour-screen` with a normal report; K7C text).
- (g) Must 6: FIXED. "Admit to a high-dependency unit or the ICU according to airway status and
  seizure control (GCS 12 after recurrent seizures), with airway assessment and cardiac monitoring."
- (h) Must 7: FIXED (K5).
- (i) Must 8: FIXED (Lejuste 2016).
- (j) Must 9: FIXED (K6).
- (k) Bridging: FIXED (K4).

### NMDAR-ENC-P01 (22F, mild, teratoma, COC)
NB-87M:NMDAR-ENC-P01:policy_verdict
- (a) MRI contrast: ALREADY-FIXED (K1).
- (b) Post-intervention screen: FIXED (K12).
- (c) Must 1: FIXED (K2).
- (d) Must 2 and P2 timing: FIXED (K3 timing sentence; K15 P2 text).
- (e) Must 2 regimen: FIXED (K3, sequential, PLEX).
- (f) Must 3: NO-ACTION (correct).
- (g) Must 7: FIXED (K5).
- (h) Must 8: FIXED (Lejuste 2016).
- (i) Bridging: FIXED (K4).

Class: K7A, K9 (glucose 100, ratio 0.58; this reverses October's "sampling time" ruling, D21).

### NMDAR-ENC-P02 (19M, testicular teratoma, ICU)
NB-87M:NMDAR-ENC-P02:policy_verdict
- (a) Must 1 and bacterial cover (T 38.2, WBC 11.8): FIXED (K2).
- (b) Must 2 doses, combined start and trade-off: FIXED (K3, IVIG).
- (c) Must 3: NO-ACTION (correct).
- (d) Hyponatraemia must: FIXED. New must: "Monitor serum sodium daily and correct the mild
  hyponatraemia (131 <unit>) slowly, with fluid restriction if it follows an SIADH pattern; IVIG can
  worsen it (Abboud 2021)."
- (e) Bridging: FIXED (K4).

Class: K5 ("earlier end" clause), K6 (must 8).

### NMDAR-ENC-P03 (A) (28M, post-HSV)
NB-87M:NMDAR-ENC-P03:policy_verdict: NO-ACTION (approval).

Class (approved; template defects): K2 (post-HSV form plus cover), K3 (combined, IVIG), K4, K5,
K6 (must 8).

### NMDAR-ENC-P04 (22F, mild, teratoma, penicillin rash)
NB-87M:NMDAR-ENC-P04:policy_verdict
- (a) FDG-PET: FIXED (new `optional` criterion `brain-fdg-pet` `{modality: FDG_PET}`, answered by
  the stored `order_fdg_pet` follow-up; D16).
- (b) Must 1: FIXED (K2).
- (c) Must 2 and P2 timing: FIXED (option 1: start after the CSF anti-GluN1 result; K3 and K15).
- (d) Regimen: FIXED (K3, sequential, PLEX).
- (e) Step 6 "5-7": FIXED (K3, DDI output).

Class: K4, K5, K6 (must 7, the agitation must), K7A, K12.

### NMDAR-ENC-P05 (19F, catatonia, negative ultrasound)
NB-87M:NMDAR-ENC-P05:policy_verdict
- (a) Pelvic MRI now: FIXED (K7B, K7C).
- (b) Must 1: FIXED (K2).
- (c) Must 2: FIXED (K3, combined, IVIG).
- (d) Must 3: FIXED (K7C).

Class: K4, K5, K6, K7A.

### NMDAR-ENC-P06 (30F, teratoma, ICU)
NB-87M:NMDAR-ENC-P06:policy_verdict
- (a) MRI contrast: ALREADY-FIXED (K1).
- (b) EEG versus exam: FIXED (D26: the routine EEG states no clinical events during the recording;
  the cEEG and the ambulatory copy link 2 of the 5 seizures to staring with oromandibular
  automatisms).
- (c) Step 15 versus 16: FIXED (K13).
- (d) Must 1: FIXED (K2; the ibuprofen hold is kept).
- (e) Must 2: FIXED (K3, combined with the dysautonomia and seizures reason, IVIG with sodium
  monitoring).

Class: K4, K5, K6, K7A.

### NMDAR-ENC-P07 (A) (25F, bipolar II, teratoma)
NB-87M:NMDAR-ENC-P07:policy_verdict: NO-ACTION (approval).

Class: K2, K3 (combined, IVIG), K4, K5, K6 (must 8), K7A.

### NMDAR-ENC-P08 (A) (38F, teratoma, Na 130)
NB-87M:NMDAR-ENC-P08:policy_verdict: NO-ACTION (approval).

Class: K2, K3 (IVIG, Na 130), K4, K5, K6, K7A, K13 (performance status).

### NMDAR-ENC-RM01 (35F, negative ultrasound, cortical/meningeal MRI)
NB-87M:NMDAR-ENC-RM01:policy_verdict
- (a) Pelvic MRI and CAP CT: FIXED (K7B, K7C).
- (b) MOG-IgG and ANA: FIXED (D30). A new recommended criterion `mog-aqp4-antibodies`
  `{panels: [MOG_IgG_cell_based]}`, with a new negative "MOG and AQP4 antibodies (serum,
  cell-based assay)" panel. ANA `clinical_significance` filled; anti-dsDNA and ENA (negative) added
  to "Other autoantibodies"; NPSLE added to the differential as `low`; a MOG-antibody disease or
  overlap entry, `low`, with "serum MOG and AQP4 IgG negative".
- (c) Must 1 (3-week LP): FIXED (K2, with the ibuprofen hold).
- (d) Must 2 timing, doses, combined start and agent: FIXED (K3, combined with the reason, IVIG).

Class: K4, K5, K6, K7A.

### NMDAR-ENC-RM02 (A) (23F, teratoma, ICU)
NB-87M:NMDAR-ENC-RM02:policy_verdict: NO-ACTION (approval).

Class: K2 (with the ibuprofen hold), K3 (IVIG), K4, K5, K6, K7A.

### NMDAR-ENC-RM03 (62F, CAP CT negative, Na 128, penicillin rash)
NB-87M:NMDAR-ENC-RM03:policy_verdict
- (a) Whole-body PET: FIXED (K7B `whole-body-pet-tumour-screen`).
- (b) Mammography or breast MRI: CENTRAL 1 (no vocabulary term).
- (c) Must 1 (penicillin allergy; stop aciclovir once the PCR is negative): FIXED (K2, ceftriaxone,
  vancomycin and co-trimoxazole).
- (d) Must 2 timing (possible AE): FIXED (K3).
- (e) Combined start: FIXED (K3, changed to sequential).
- (f) Doses: FIXED (K3).
- (g) IVIG versus PLEX: FIXED (K3: IVIG for the orthostatic hypotension, with the divergence
  recorded and an osmolality check before a sodium fall is treated).

Class: K3 DDI output "5 to 7", K4, K5, K6 (must 8 Spasovski, must 9 Lejuste), K13.

### NMDAR-ENC-RP01 (61M, aphasia, CSF 1:4, serum negative)
NB-87M:NMDAR-ENC-RP01:policy_verdict
- (a) MRI contrast: ALREADY-FIXED (K1).
- (b) Osmolality: FIXED (K10, 286).
- (c) Diagnosis: the phenotype does not fit, so a confirmatory test: FIXED (D17).
  - The CSF `special_tests.NMDAR_antibodies` and the interpretation read: "Positive, titre 1:4
    (cell-based assay, IgG anti-GluN1); confirmed by tissue-based assay (rat brain
    immunohistochemistry, neuropil pattern) at the reference laboratory".
  - The second key-evidence bullet adds: "Because the phenotype is atypical for the antibody (older
    man, isolated aphasia, bland CSF, low titre), the positive cell-based assay was confirmed by a
    tissue-based assay, as Graus 2016 advises."
  - The phenotype rewrite option is DECLINED (it would undo October Q1).
- (d) Vascular imaging: FIXED (D18, `vascular-imaging` `{modality: MR_angiography}`, recommended,
  with a stored normal MRA; the stroke key features are updated and the ADC argument softened).
- (e) Confirmatory test: FIXED (as in c).
- (f) Whole-body PET: FIXED (K7B).
- (g) Must 1: FIXED (K2, with amoxicillin).
- (h) Must 2 indication, sequence after vascular imaging, sequential start, doses and PLEX: FIXED
  (K3). The sequence-constraint form is DECLINED (D18).
- (i) Gastric protection: FIXED (K16).

Class: K3 DDI output, K4, K5, K12. Glucose monitoring is kept.

### NMDAR-ENC-RP02 (76M, nivolumab, CKD)
NB-87M:NMDAR-ENC-RP02:policy_verdict
- (a) MRI contrast: ALREADY-FIXED (K1).
- (b) CrCl: FIXED (D19, creatinine 1.5 mg/dL; "about 46 mL/min (Cockcroft-Gault)" in musts 2 and
  5; the DDI bands are unchanged).
- (c) Babinski: FIXED (D19, right Babinski; left plantar equivocal).
- (d) Must 2 repeat PCR: FIXED (K2 early-LP form).
- (e) Renal dosing: FIXED (b).
- (f) Bacterial cover: FIXED (K2, RP02 form).
- (g) Must 3 steroids: NO-ACTION (correct).
- (h) PLEX 5-10: FIXED (K3; DDI output too).
- (i) Agent divergence: FIXED (K3, PLEX).
- (j) Taper: NO-ACTION (it is the bridging must).
- (k) PJP prophylaxis, glucose and sodium monitoring: FIXED (new must: "Give Pneumocystis
  prophylaxis (co-trimoxazole, renally adjusted, with potassium monitoring on lisinopril) while
  prednisone stays at 20 mg/day or more for 4 weeks or longer, and monitor glucose and sodium during
  high-dose steroids (ASCO 2021).").

Class: K5 (must 10, "earlier end" clause).

### NMDAR-ENC-RP03 (63M, post-HSV, coronary disease)
NB-87M:NMDAR-ENC-RP03:policy_verdict
- (a) MRI contrast: ALREADY-FIXED (K1).
- (b) Coronary angiography and CTA: FIXED (K17, two harm entries).
- (c) Must 1: FIXED (K2 post-HSV form; cover until CSF culture; ceftriaxone, vancomycin and
  co-trimoxazole).
- (d) Must 2 indication: NO-ACTION (supported).
- (e) Combined start: NO-ACTION (supported; the reason is stated, K3).
- (f) Doses: FIXED (K3).
- (g) IVIG versus PLEX: FIXED (K3, IVIG with the divergence recorded; sodium 131).

Class: K4, K5, K6 (must 8), K16 (gastric protection), D35 (PET sentence).

### NMDAR-ENC-RS01 (31F, teratoma, COC, ICU)
NB-87M:NMDAR-ENC-RS01:policy_verdict
- (a) MRI contrast: ALREADY-FIXED (K1).
- (b) Must 1 Graus wording: FIXED (K2).
- (c) Bacterial cover: FIXED (K2).
- (d) NSAIDs: NO-ACTION (correct, kept).
- (e) Must 2 timing and combined start: NO-ACTION (supported; the reason is stated).
- (f) Doses: FIXED (K3).
- (g) IVIG versus PLEX: FIXED (K3, IVIG with the divergence recorded).

Class: K3 DDI output, K4, K5, K6, K7A, K10 (osmolality 274).

### NMDAR-ENC-RS02 (50F, post-COVID, valproate, catheter)
NB-87M:NMDAR-ENC-RS02:policy_verdict
- (a) Pelvic ultrasound: FIXED (K7B `pelvic-ultrasound-screen`).
- (b) Mammography: CENTRAL 1.
- (c) Infection screen: FIXED (D28: `urine-culture` and `blood-cultures`, recommended; the
  differential gains intercurrent infection, `low`).
- (d) Must 1 (bacterial cover, avoid carbapenems): FIXED (K2, RS02 regimen).
- (e) Must 2 indication: NO-ACTION (supported).
- (f) Doses: FIXED (K3).
- (g) Divergence: FIXED (K3, PLEX).
- (h) PLEX valproate and enoxaparin timing: FIXED (K16).
- (i) If IVIG, sodium: FIXED (in the agent sentence).

Check that no avoided action matches a blood-culture or urine order.

Class: K4 ("after this second course"), K5, K6.

### NMDAR-ENC-RS03 (19M, GCS 9, aspiration)
NB-87M:NMDAR-ENC-RS03:policy_verdict
- (a) MRI contrast: ALREADY-FIXED (K1).
- (b) pH: FIXED (D22, 7.16; the summary and interpretation updated).
- (c) FiO2: FIXED (D22, "on 4 L/min nasal oxygen, FiO2 about 0.36", in the ABG panel or
  interpretation).
- (d) Chest imaging for aspiration and GCT: FIXED (K7B `chest-ct-aspiration-gct`; K7C must 3; the
  aspiration finding goes in `key_clinical_evidence`).
- (e) Must 1 explicit repeat PCR and cover (also for the aspiration pneumonia): FIXED (K2 early-LP
  form; "continue ceftriaxone as treatment of the right lower lobe aspiration pneumonia").
- (f) Must 2 indication and combined start: NO-ACTION (supported).
- (g) Doses: FIXED (K3).
- (h) IVIG: FIXED (K3).

Class: K3 DDI output, K4, K5, K6.

### NMDAR-ENC-RS04 (40F, optic neuritis, fever)
NB-87M:NMDAR-ENC-RS04:policy_verdict
- (a) MRI contrast: ALREADY-FIXED (K1).
- (b) Fever: FIXED (K14).
- (c) Pelvic MRI and CAP CT: FIXED (K7B, K7C).
- (d) Neurosarcoidosis: FIXED (D29). Criteria `ace-serum` `{panels: [ACE]}` (a stored normal ACE
  row) and `csf-flow-cytometry` `{special_tests: [flow_cytometry]}`. The initial CSF gains "Flow
  cytometry: polyclonal T-predominant lymphocytes, no clonal population". The CAP CT has no hilar
  adenopathy. A differential entry is added (`low`).
- (e) Must 1: FIXED (K2).
- (f) Must 2 timing and combined start: NO-ACTION (supported).
- (g) Doses: FIXED (K3).
- (h) Early PLEX with the divergence: FIXED (K3, PLEX for the threat to vision).
- (i) Levetiracetam after each exchange: FIXED (K16).

Class: K3 DDI output, K4, K5, K6, K7A.

### NMDAR-ENC-S01 (A) (24F, teratoma, COC)
NB-87M:NMDAR-ENC-S01:policy_verdict: NO-ACTION (approval).

Class: K2, K3 (combined, IVIG; DDI output), K4, K5, K6, K7A, K9 (glucose 106, ratio 0.58).

### NMDAR-ENC-S02 (A) (31F, teratoma, cephalosporin hives)
NB-87M:NMDAR-ENC-S02:policy_verdict: NO-ACTION (approval).

Class: K2 (meropenem with vancomycin), K3, K4, K5, K6, K7A, K9 (glucose 114, ratio 0.58).

### NMDAR-ENC-S03 (A) (19F, teratoma, COC)
- 7907651d-bd95-4a9d-a5b3-d1a415c47d15:
  - (a) MRI contrast: ALREADY-FIXED (K1).
  - (b) Glucose 102 versus 104: FIXED (K9, ratio 0.58).
- NB-87M:NMDAR-ENC-S03:policy_verdict: NO-ACTION (approval).

Class: K2, K3, K4, K5, K6, K7A.

### NMDAR-ENC-S04 (A) (27F, teratoma, penicillin rash)
- 0d6e3601-561b-440d-9a24-27d9e48f8dea:
  - (a) MRI contrast: ALREADY-FIXED (K1).
  - (b) Glucose 102 versus 96: FIXED (K9, ratio 0.67).
- NB-87M:NMDAR-ENC-S04:policy_verdict: NO-ACTION (approval).

Class: K2, K3, K4, K5, K6, K7A.

### NMDAR-ENC-S06 (A) (27F, teratoma, Na 126)
- 1d9f3e58-0a2f-4713-a0d9-520ceb6a918c: MRI contrast: ALREADY-FIXED (K1).
- NB-87M:NMDAR-ENC-S06:policy_verdict: NO-ACTION (approval).

Class: K2, K3 (IVIG with sodium), K4, K5, K6 (Spasovski, Lejuste), K7A.

### NMDAR-ENC-S09 (A) (23F, bilateral teratomas, Na 124)
- f0dd0c07-8328-4c28-9290-aa67d22befd9: MRI contrast: ALREADY-FIXED (K1).
- NB-87M:NMDAR-ENC-S09:policy_verdict: NO-ACTION (approval).

Class: K2, K3 (IVIG, divergence recorded), K4, K5, K6, K7A.

### NMDAR-ENC-S10 (A) (29F, teratoma, Na 127)
- 18186d99-284c-4af6-a373-2108c088a02c: MRI contrast: ALREADY-FIXED (K1).
- NB-87M:NMDAR-ENC-S10:policy_verdict: NO-ACTION (approval).

Class: K2, K3, K4, K5, K6, K7A.

---

## 4. CENTRAL requests

1. **Vocabulary: breast imaging.**
   - Add `order_body_imaging` study `breast_mammography` (CPT 77067) and possibly `breast_MRI`,
     with:
     - a priced row in `costs.yaml`;
     - a library normal in `fallback_library.yaml`;
     - the `review_api/services/tool_io.py` mirror and `TOOL_PARAMETER_VOCABULARY.md`.
   - Reason: Abboud box 1 item 6 (CT is insensitive for early breast cancer), requested for RM03
     and RS02.
   - Once it exists, add a recommended `mammography-tumour-screen` criterion with a stored normal
     report and a must clause in those two cases.
2. **Vocabulary (optional): a CSF tissue-based assay.**
   - Add an `analyze_csf` special test, for example `neuronal_surface_tissue_assay` (rat brain
     immunohistochemistry), so the Graus confirmatory test can be ordered and scored separately.
   - Interim: RP01 reports it inside the `NMDAR_antibodies` result (D17).
3. **Criteria pack `dataset-generation/criteria_packs/NMDAR-ENC.md`:** rewrite to this plan.
   - Section 2:
     - the pelvic MRI alternative;
     - the second-line tumour screen by demography (K7);
     - FDG-PET optional when other studies are uninformative;
     - blood and urine cultures when fever has a possible systemic source.
   - Section 3: drop the blanket "FDG-PET not a criterion" and "blood cultures removed" lines.
   - Section 9: canonical M1, M2, bridging, M7, the M9 correction source and M8 (Lejuste).
   - Add allow-list keys `[ESCMID_meningitis_2016]` (van de Beek D et al. Clin Microbiol Infect
     2016;22 Suppl 3:S37-S62) and, if the worker verifies it, the chest pain guideline for RP03.
   - Mirror the generator template musts in `conditions.yaml`.
4. **`condition_tool_guidance.yaml` claims and `test_guidance_claims`.**
   - The NMDAR claims will change: tumour screening counts (pelvic MRI recommended in 4 cases, CAP
     CT in M05, RM01, RS04 and RS03, whole-body PET in 2), FDG-PET now optional in 1 case, blood
     cultures in 1.
   - Regenerate after the round.
5. **Library or authoring (dataset-wide, informational).** The library-contradiction pass wrote
   one identical `order_cognitive_screen_post_intervention` output into all 30 NMDAR cases.
   - Consider whether a `post_intervention` screen should be authored at all in an acute encounter
     where no treatment has been recommended (ROUND_POLICY rule 4).
   - This round fixes only the three that contradict their baseline.
6. **Same defect in other conditions** (for their leads): the CSF paired serum glucose differs from
   the labs glucose in 7 MS-RR cases (M01, M02, M03, P01, P02, P03, RP05) and in ALZ-EARLY-P02.
   "5 to 7 exchanges" also appears in 1 MS-RR case.

## 5. Open questions

None needs information that only Andrea has. For awareness:
- D14 declines a physician's request (resection as a criterion) on the contract's rule 4. If Andrea
  wants surgical tissue diagnosis of a teratoma scored, that is a design change for all tumour
  conditions.
- Abboud numbers not reached in the search snippets (the 3-7 day steroid course, cyclophosphamide
  600-1000 mg/m², box items 9 and 13) are applied as R2's reading of the paper. A full-text check
  at the next round would close this.

<!-- PLAN COMPLETE -->
