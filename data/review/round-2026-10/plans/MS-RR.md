# MS-RR: condition plan for the October 2026 review round

Lead plan for the 30 MS-RR cases (M01-M04, P01-P05, RM01-RM04, RP01-RP05, RS01-RS06, S01-S06).
Written 24 Oct 2026 against the case files on branch `fix/review-round-2026-10`, ROUND_POLICY.md,
PATTERNS.md, the criteria pack `dataset-generation/criteria_packs/MS-RR.md`, TOOL_REPORT_STYLE_GUIDE.md,
POLICY_AUTHORING_GUIDE.md, TOOL_PARAMETER_VOCABULARY.md and `docs/benchmark/tool-contract.md`.

**Reviewer notes: none.** There is no reviewer notes file for MS-RR in this round. Every case log
writes under "Reviewer notes": `No reviewer notes for this case.` All changes below are own
findings (ROUND_POLICY rulings 2-8 and the leakage/realism rules), most of them classes copied by the
August per-condition rewrite into all 30 cases.

Baseline (checked 24 Oct): `perfect_agent.py` passes 30/30. Every case has `max_additional_actions: 0`
and puts the literature and drug-check criteria in `required_before_assessment`. Workers re-run
`perfect_agent.py CASE -v`, `case_io.py check CASE` and `pytest agent-platform/tests/test_case_guards.py -q -k CASE`
after every case, and edit only through `case_io` load/save.

Worker rule of thumb: when a case defect is not listed below, decide it with the canonical facts of
section 1 and the class texts of section 2; the same defect gets the same fix in every case.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which source governs what

| Topic | Source (all verified to exist) | Citation key |
|---|---|---|
| Diagnosis (DIS, DIT, CSF, optic nerve, age > 50) | Montalban X, Lebrun-Frénay C, Oh J, et al. Diagnosis of multiple sclerosis: 2024 revisions of the McDonald criteria. *Lancet Neurol* 2025;24(10):850-865 | `[McDonald_2024]` (CENTRAL: add to pack) |
| Previous criteria, only when a text explains what changed | Thompson AJ et al. Diagnosis of multiple sclerosis: 2017 revisions of the McDonald criteria. *Lancet Neurol* 2018;17:162-173 | `[McDonald_2017]` |
| MRI protocol (brain and spinal cord, gadolinium, follow-up) | Wattjes MP et al. 2021 MAGNIMS-CMSC-NAIMS consensus recommendations on the use of MRI in patients with multiple sclerosis. *Lancet Neurol* 2021;20:653-670 | `[Wattjes_2021]` (CENTRAL: add); `[MAGNIMS_2016]` only for lesion-region definitions |
| NMOSD | Wingerchuk DM et al. International consensus diagnostic criteria for NMOSD. *Neurology* 2015;85:177-189 | `[Wingerchuk_2015]` |
| MOGAD | Banwell B et al. Diagnosis of MOGAD: International MOGAD Panel proposed criteria. *Lancet Neurol* 2023;22:268-282 | `[Banwell_2023_MOGAD]` |
| OCT | Petzold A et al. Retinal layer segmentation in multiple sclerosis: a systematic review and meta-analysis. *Lancet Neurol* 2017;16:797-812 | `[Petzold_2017]` |
| Relapse treatment, DMT, monitoring | NICE NG220, Multiple sclerosis in adults: management (2022, updated June 2026 to reference the 2024 McDonald criteria) | `[NICE_NG220]` (CENTRAL: add) |
| Overview (only for general statements) | Reich DS, Lucchinetti CF, Calabresi PA. Multiple sclerosis. *N Engl J Med* 2018;378:169-180 | `[Reich_2018]` |

Do not cite "MAGNIMS-CMSC-NAIMS 2024/2025" (no such document could be verified; use `[Wattjes_2021]`).
Each criterion carries bracketed keys only (no duplicate free-text "Reich 2018 NEJM review" next to
`[Reich_2018]`; no "2024 revised McDonald criteria; NICE NG220 (2026)" prose string next to the key).

### 1.2 Canonical clinical facts (use these words; do not restate them differently)

F1. **Regions (2024).** Five DIS regions: periventricular, cortical/juxtacortical, infratentorial,
spinal cord, optic nerve. The optic nerve counts when shown by MRI (T2 signal or enhancement), OCT
(inter-eye difference of at least 6 µm in pRNFL or at least 4 µm in GCIPL) or VEP (prolonged P100).
Symptomatic and asymptomatic lesions both count. "Subcortical" or "deep white matter" is not a
region; the callososeptal interface belongs to the periventricular region (it is not a separate
region).

F2. **DIS needs at least 2 of 5 regions.** Never "three regions establish DIS" (20 cases say so).

F3. **When DIT is needed (2024).** With lesions in 4 or 5 regions, DIS alone (plus no better
explanation) establishes MS: no DIT and no CSF needed. With 2 or 3 regions, DIS is completed by any
one of: DIT (simultaneous gadolinium-enhancing and non-enhancing lesions on one scan, or a new
T2/enhancing lesion on a later scan), positive CSF (CSF-restricted OCB or an elevated kappa
free-light-chain index), or a central vein sign in at least six lesions ("select six").

F4. **Age over 50, vascular risk factors, migraine.** In these patients the 2024 criteria recommend
additional supporting evidence (a spinal cord lesion, positive CSF, or CVS) because non-specific white
matter lesions are common. Applies to RS01 (61), RP05 (54), and the migraine puzzles P01-P03.

F5. **T1 hypointense "black holes" do not count for DIT** (20 cases say they do). They indicate
chronic tissue damage only.

F6. **CSF.** Positive CSF = at least two CSF-restricted oligoclonal bands (IEF with paired serum) or a
kFLC index above the laboratory-validated cutoff (cutoffs about 5-6.6 are in use; reports state the
laboratory's own, e.g. "reference < 6.1"). The IgG index is supportive only and never substitutes for
OCB or kFLC. Myelin basic protein is obsolete for MS diagnosis: delete it from every CSF report.
Typical MS CSF: WBC 0-15/µL lymphocytic (> 50/µL argues against MS), protein normal or mildly raised
(< 70 mg/dL). OCB are absent in about 5-10% of MS: OCB negativity never excludes MS.

F7. **Acute optic neuritis timeline.** In the first weeks the disc is normal (retrobulbar) or mildly
swollen; pallor appears after about 4-6 weeks. Acute OCT: pRNFL normal or increased (swelling),
GCIPL normal or minimally reduced; pRNFL/GCIPL thinning develops over 1-3 months. Thinning or pallor in
the first 3 weeks is acceptable only in an eye with a documented earlier episode, and the report then
attributes it to that episode. VEP: prolonged P100 (often with reduced amplitude) in the affected eye.

F8. **NMOSD/MOGAD discriminators.** NMOSD: LETM (3 or more contiguous vertebral segments, central),
area postrema syndrome, severe or bilateral optic neuritis, OCB usually absent, AQP4-IgG by cell-based
assay. MOGAD: optic neuritis with perineural enhancement and long optic-nerve lesions, conus
involvement, ADEM-like lesions, MOG-IgG by cell-based assay (live CBA preferred). MS cord lesions:
short (< 2 segments), peripheral/dorsolateral, less than half the cross-section.

F9. **Relapse treatment (NICE NG220).** For a relapse that affects function: methylprednisolone oral
500 mg daily for 5 days, or IV 1 g daily for 3-5 days (IV when oral is unsuitable, has failed, or the
relapse is severe/inpatient); exclude infection first (urine dipstick in bladder symptoms); plasma
exchange for severe relapse not responding to steroids. Steroids speed recovery; they do not change
long-term outcome. Never chronic oral steroids for MS.

F10. **Tumefactive lesions.** Open-ring (incomplete) enhancement with the open side toward the cortex,
less mass effect than size predicts, peripheral restricted diffusion, intralesional veins, other typical
MS lesions and CSF OCB favour demyelination. When PCNSL or glioma is not excluded, withhold
corticosteroids until tissue is obtained (steroids can make lymphoma non-diagnostic); dexamethasone only
for impending herniation, after neurosurgical discussion. LP is contraindicated with midline shift,
effaced basal cisterns, a posterior fossa mass compressing the fourth ventricle, or papilloedema with a
mass lesion.

F11. **Drug facts.** Amlodipine (dihydropyridine) does not cause bradycardia; the fingolimod/S1P
cautions are beta-blockers, verapamil/diltiazem, digoxin, class Ia/III antiarrhythmics, second- or
third-degree AV block, recent MI/stroke, QTc prolongation and severe untreated sleep apnoea.
Corticosteroids do not reduce combined oral contraceptive efficacy (oestrogens raise steroid exposure).
High-dose steroids raise glucose (metformin/sulfonylurea users need glucose monitoring and insulin
cover) and add GI-bleeding risk with NSAIDs/aspirin (consider a PPI). Teriflunomide is teratogenic
(effective contraception; accelerated elimination before conception, also advised for men wishing to
father a child) and raises ethinylestradiol/levonorgestrel exposure. Topiramate does not cause
lymphopenia. Natalizumab: PML risk rises with anti-JCV index (index > 1.5 = high risk), duration > 2
years and prior immunosuppression. Before anti-CD20 or S1P therapy: HBsAg, anti-HBc, HCV, HIV, VZV IgG;
live vaccines at least 4-6 weeks before starting and not during treatment.

F12. **What MRI is ordered.** Brain MRI with gadolinium on an MS protocol (3D FLAIR, T2, DWI, pre/post T1,
SWI optional for CVS) and cervical plus thoracic spinal cord MRI with gadolinium, ideally in the same
session ([Wattjes_2021]). A brain MRI report describes brain and at most the upper cervical cord in its
field of view; it never reports thoracic cord.

### 1.3 July 2026 physician guidance (Reviewer 1, condition_tool_guidance.yaml)

Brain MRI and spine MRI with MS protocol and gadolinium: required. CSF: optional/conditional (OCB or
kFLC). Labs required as a mimic-exclusion panel. ECG and EEG removed. Specialized tests optional (OCT,
VEP only). AQP4/MOG targeted to atypical or optic-neuritis cases. This plan keeps that guidance and makes
the "targeted" rule exact (section 3.2, AQP4/MOG tiers).

---

## 2. Error classes in this condition

Each class: what is wrong, where, the decided fix, and the canonical text where one is needed.

### A. Template criteria (all 30)

Shared ids: `action-1-analyze-brain-mri`, `action-2-order-body-imaging`, `action-3-search-medical-literature`,
`action-4-check-drug-interactions`, `action-5-analyze-csf`, `action-6-interpret-labs`,
`action-7-order-specialized-test` (VEP), `action-8-order-specialized-test` (OCT). Keep the ids.

A1. Label and rationale are the same sentence in every criterion. Write a rationale that says why this
patient needs it (one sentence, case-specific: the syndrome, the region it tests, the mimic it excludes).

A2. `action-1` brain MRI `{contrast: true, protocol: ms}` required: keep. Label (canonical):
"Brain MRI with gadolinium on an MS protocol". expected_evidence: the case's own lesion regions and
enhancement status, in the report's words. Citations `[McDonald_2024]`, `[Wattjes_2021]`.

A3. `action-2` spine MRI `{contrast: true, study: spine_MRI}` required: keep. Label: "Cervical and
thoracic spinal cord MRI with gadolinium". Citations `[McDonald_2024]`, `[Wattjes_2021]`.

A4. `action-3` literature: required in 29, recommended in S03, with a long `query` string. Fix
(ruling 5): importance `optional`, `required_arguments {}`, expected_evidence empty, last in the list,
removed from `required_before_assessment`.

A5. `action-4` drug check uses non-schema keys `proposed_class` and `screen_for`; no agent can match
them (the tool takes only `drug`, `current_medications`, `patient_conditions`). Fix: `required_arguments {}`
(or `{"drug": "<agent>"}` only when the case is about one named drug). Tier per ruling 6 and section 3.2:
`recommended` only in RP03 and RP05 (oral hypoglycaemics and high-dose steroids); `optional` elsewhere.
Removed from `required_before_assessment` everywhere. Placed after the diagnostic core.

A6. `action-5` CSF requires `special_tests [oligoclonal_bands, IgG_index, kappa_free_light_chain_index]`
(an agent that orders OCB alone misses it). Fix: two alternatives,
`{special_tests: [oligoclonal_bands]}` and `{special_tests: [kappa_free_light_chain_index]}`.
Label: "CSF with paired serum for oligoclonal bands or kFLC index". Tier per section 3.2. Add a
`kappa_free_light_chain_index` result to every stored CSF report (class J).

A7. `action-6` labs requires 9 analytes (11 with AQP4/MOG). `CMP` does not satisfy `calcium` or
`glucose` in the scorer, so a sensible panel fails. Fix: `{panels: ["CBC", "vitamin_B12", "TSH", "HIV"]}`,
required. Label: "Mimic-exclusion blood panel (CBC, B12, thyroid, HIV)". The stored initial labs keep
the full panel (CBC, ESR, CRP, CMP, calcium, glucose, TSH, B12, HIV, plus what the case adds).
Remove AQP4/MOG from this criterion (A8).

A8. AQP4/MOG embedded in `action-6` in 13 cases. Fix: new criterion `action-aqp4-mog-cba`, placed
right after labs, tier per section 3.2, alternatives:
`{panels: ["AQP4_IgG_cell_based", "MOG_IgG_cell_based"]}`, `{panels: ["AQP4_IgG", "MOG_IgG"]}`,
`{panels: ["NMO_MOG"]}`. Label: "Serum AQP4-IgG and MOG-IgG by cell-based assay". Citations
`[Wingerchuk_2015]`, `[Banwell_2023_MOGAD]`. Results live in `initial_tool_outputs.labs` (as in the
13 cases now): two rows, test names "AQP4-IgG (cell-based assay)" and "MOG-IgG (live cell-based assay)",
value "Negative", reference "Negative", `is_abnormal: false`, `clinical_significance: null`. Cases with
no AQP4/MOG criterion (P01, P02, P03, RM03, RS04, RS05) store no result.

A9. `action-7` VEP and `action-8` OCT: optional; keep where they exist, add where section 4 says so
(the case's KCE relies on a study that is never served). Ids for new ones:
`action-vep` / `action-oct` if the template id is absent. Citations: VEP `[McDonald_2024]`; OCT
`[Petzold_2017]`, `[McDonald_2024]`.

### B. AQP4/MOG targeting and the must that contradicts it (21 cases plus variants)

Template must T1 "Exclude NMOSD and MOGAD with AQP4-IgG and MOG-IgG cell-based assays before committing
to an MS diagnosis and DMT" (21 cases) and variants (M04, P04 "Send AQP4...", S01-S05) are diagnostic
tests disguised as musts, and in 8 cases ask for a test that the case does not score or serve. P05's
must even says the results are "negative here" while P05 stores no result. Fix: delete T1 and every
"send/obtain/order <test>" must everywhere; the AQP4/MOG criterion (A8) carries it. S01-S04 and RS03
label the stored row "NMO-IgG (Aquaporin-4 antibodies)" with no method: relabel as in A8.

### C. Differential not updated (ruling 7; nearly all)

NMOSD "high" and MOGAD "high" in about 20 cases whatever the results; neurosarcoidosis "moderate" with
normal ACE and no leptomeningeal enhancement; in tumefactive cases lymphoma and glioblastoma "high"
after biopsy or MRS. Fix: each likelihood from the whole work-up, `key_features` naming the case's own
discriminating results (e.g. "AQP4-IgG and MOG-IgG negative by CBA; short dorsolateral C3-C4 lesion;
CSF-restricted OCB: low"). Where the work-up does not test a mimic, the entry says what argues against
it. Required entries: NMOSD, MOGAD (all); neurosarcoidosis when ACE/hypercalcaemia/cranial neuropathy is
in the case; B12 deficiency in myelopathy cases; small-vessel disease when age > 45 or vascular risk;
migraine-related white matter lesions in P01-P03; ADEM and PCNSL/high-grade glioma in tumefactive
cases; CNS lupus when an ANA row exists.

### D. Shared key_clinical_evidence (all 30)

Delete (engineering text, not evidence): "July 2026 review applied end to end..." (30), "Tier per the
July 2026 clinical review..." (29). Rewrite or delete: "The 2024 revised McDonald framework recognizes..."
(30). Wrong facts to delete: "a lesion in three of these regions establishes DIS" (20; F2), "T1 black
holes ... contribute evidence of dissemination in time" (20; F5). Template carry-over to delete: the
tumefactive "Open-ring enhancement with..." line in the 20 non-tumefactive cases, "AQP4-IgG and MOG-IgG
must be ordered as cell-based assays" (20), the DMT-choice line (20, management), the vitamin D line
(12) unless the case has a low vitamin D row, "If the initial brain MRI does not include the spinal
cord..." (generic). Also delete wording about the benchmark itself ("red herring to avoid", "trap",
"carefully planted distractor", "essential for case validity").

Canonical KCE content, 4-7 bullets, all observable in this case: (1) the presenting syndrome and the
lesion that explains it; (2) one DIS line in the form "DIS: <n> of 5 regions: <region (site from the
report)>, ..."; (3) where F3 needs it, one line "DIT: <how>" or "Positive CSF: <OCB count / kFLC
value>"; (4) prior attack(s) from the history when present; (5) the result that excludes the main mimic;
(6) any distractor result and why it does not explain the picture. A KCE line may cite only a result the
case serves (stored output or exam).

### E. Lab rows with leaked significance (19 cases, 22 rows)

"Mimic exclusion" rows carry `clinical_significance: "Reported negative in this case's own workup;
excludes this reversible mimic"`. Set `null` (normal rows carry no interpretation). Vitamin D 18 ng/mL
copied into 7 cases: vary per case (12-28 ng/mL) or remove where the case does not use it. No identical
CBC/CMP values across cases of the same batch.

### F. Future-data and treatment-response follow-ups (ruling 4; 17 cases)

`request_repeat_mri_3months` (`analyze_brain_mri`) reports new lesions three months later in M01, M02,
M03, P01, P02, P03, RM02, RM03, RS01, RS02, RS03, RS04, S01, S02, S03, S04 (and S01's twin wording).
The agent is assessing now; a scan from the future cannot be part of the work-up. Delete every one (a
repeat brain MRI order then returns the initial study). RP03 `request_repeat_mri_post_steroids` and the
literature follow-up `request_steroid_trial`: treatment response, delete. Where the label depended on the
future scan (P01, P02, P03), fix the initial data (section 4).

### G. Wrong tool for the study

G1. SSEP filed as `interpret_labs` `request_somatosensory_evoked_potentials` ("All values within normal
limits"): P02, P03. Delete (SSEP adds nothing here; not in the July guidance list).
G2. Biopsy filed as `interpret_labs` `request_biopsy_pathology`: RM01, RP02. Move to
`obtain_tissue_diagnosis` follow-up (`procedure: stereotactic_biopsy`, site = the lesion) with a
TissueDiagnosisReport: specimen_adequate true; histological_diagnosis "Active demyelinating lesion with
relative axonal preservation"; findings: macrophages with myelin debris (CD68), perivascular T-cell
cuffs, reactive (Creutzfeldt) astrocytes, neurofilament/SMI-31 showing preserved axons; molecular_findings
CD20_IHC "scattered reactive B cells, no atypical B-cell infiltrate", IDH1_IHC "negative" (and EBER_ISH
"negative" if listed); impression = the histology only. Strip "Low Ki-67 and no IDH mutation exclude
glioma" style synthesis; no "consistent with tumefactive MS" (the integrated diagnosis is the
clinician's).
G3. RP01 `interpret_labs` `request_ct_body` ("All values within normal limits"): replace with
`order_body_imaging` `{study: chest_abdomen_pelvis_CT, contrast: true}` follow-up, a real normal report
(no primary tumour, no lymphadenopathy, no hilar adenopathy), optional criterion `action-ct-cap`.
G4. RM03 `interpret_labs` `request_myasthenia_gravis_workup` (stub): delete (the pontine lesion and the
fixed abduction deficit explain the diplopia; MG is low in the differential with the reason).
G5. MR spectroscopy as `analyze_brain_mri` `request_mri_spectroscopy` (RM02, impression "See findings
above"): move to `order_advanced_imaging` `{modality: MR_spectroscopy}` with real content (NAA mildly
reduced, choline mildly raised, Cho/NAA < 2, glutamate/glutamine peak, no lipid peak or a small one),
optional criterion `action-mrs`.
G6. Perfusion as `analyze_brain_mri` `request_perfusion_mri` (RP02): move to `order_advanced_imaging`
`{modality: perfusion_MRI}`; keep its rCBV 1.4 content; optional criterion `action-perfusion`. RP02's
MRS sentence inside the brain MRI report moves to an `MR_spectroscopy` follow-up (the brain MRI does
not report spectroscopy it was not asked for).
G7. Stubs "None :: None" (literature in RM03, RP02, RS01, S04): write the general evidence (class O) or
delete.

### H. Spinal cord findings inside the brain MRI report

M02, M03, RS02 (thoracic T9-T10, impossible on a brain study), RS03, RS04, RS06, S01, S03, S04, plus
S01's "No longitudinally extensive transverse myelitis". This pre-empts the spine criterion and shows the
answer of a study the agent must order. Fix (F12): remove every cord finding from the brain MRI
findings, impression and additional_observations; the impression lists brain regions only; add one
observation "Spinal cord not assessed on this study." The cord lesions live only in the spine
follow-up, which must report them (levels, length in segments, position, cross-section, enhancement).

### I. Acute optic neuritis timing and OCT reports (F7)

Disc pallor at 3-10 days: S01 (3 d), RS03 (4 d), S03 (5 d), S04 (10 d): change to "normal optic disc
(retrobulbar)" or "mild disc swelling". OCT thinning in acute ON: S01, S02, S03, S04, RS03, S05 (and P04,
where the eye had an earlier episode: keep, attribute). OCT reports reading "Abnormal values: ... (L)"
with no eye labels, and S01's quantitative data for one eye only. Canonical acute OCT report
(numbers vary per case): "Right eye: average pRNFL 104 µm (normal 80-110), GCIPL 81 µm (normal 70-90).
Left eye: average pRNFL 118 µm, mildly increased in the superior and inferior quadrants consistent with
optic disc swelling; GCIPL 78 µm. Inter-eye GCIPL difference 3 µm." Impression: "Mild peripapillary
RNFL swelling in the left eye; no RNFL or GCIPL thinning." Both eyes always reported. For cases with an
earlier episode in the same eye (P04, M02, P05, RM04, RP04, RP05, RS02, S06), thinning is correct and the
impression says it is in the eye with prior optic neuropathy.

### J. CSF reports

Interpretation is a recital with the junk string "(N/A PMN/N/A lymph)" in many: rewrite as a pattern
statement (canonical: "Mild lymphocytic pleocytosis with normal glucose, CSF-restricted oligoclonal
bands and raised kFLC index: intrathecal immunoglobulin synthesis."). Delete myelin basic protein (F6).
Add `kappa_free_light_chain_index`: OCB-positive cases above the cutoff (vary 12-90), OCB-negative cases
below (vary 1.5-4.5). Fix contradictory flags (M01 IgG index 0.65 labelled "borderline elevated" against
"< 0.70": normal). RP02 CSF says "intact blood-brain barrier" (not a CSF finding) and lists serum
AQP4/MOG: delete both phrases (and see L).

### K. Musts and prohibitions template

Musts T0 (DIS), T2 (DIT) are interpretation; T1 is a test (B); T3-T6 generic. Prohibitions T7-T13 in
20 cases verbatim. Fix, per case:
- One formulation must (canonical): "State relapsing-remitting MS by the 2024 McDonald criteria, naming
  the regions that give DIS and, where needed, what gives DIT or positive CSF." Delete T0/T2.
- Relapse must from F9, specific to the case (oral or IV by severity; infection excluded first when
  bladder symptoms; PLEX if refractory). In tumefactive cases with lymphoma not yet excluded: "Withhold
  corticosteroids until tissue diagnosis; ..." (F10).
- DMT must: "Offer disease-modifying therapy after diagnosis, choosing efficacy by disease activity
  (<case's activity markers>), after discussing pregnancy plans and contraception" (the pregnancy clause
  only in women of child-bearing potential).
- Pre-DMT screening must (F11), one line, matched to the drug class the case favours.
- One or two case-specific musts (bladder: PVR and antimuscarinic or intermittent catheterisation;
  painful tonic spasms: carbamazepine; vitamin D replacement only with a low value; smoking cessation
  only in a smoker; Uhthoff counselling only if reported).
- Prohibitions: keep T7 (non-specific lesions) and T11 (chronic steroids) everywhere; T10 only in women
  of child-bearing potential (present in men and to delete: M03, P03, RM01, RM03, RS01, RS04, S04);
  T9 only with a case cardiac reason (OSA in RP05; none in others: delete); T8 only where an anti-JCV
  result is in the case (P05); T12 keep (generic but correct); T13 only where myelopathic signs exist.
  Add a case-specific prohibition where the case has one (e.g. "Do not attribute the white matter lesions
  to small-vessel disease without explaining the cord lesion and CSF" in RP05/RS01).
- Wrong facts: RP02 drug check "corticosteroids may reduce efficacy of hormonal contraception" (F11:
  false; delete). RP05 "amlodipine additive bradycardic" (F11: false; delete). P01 "topiramate ... may
  cause lymphopenia" (false).

### L. LP with a mass lesion (F10)

RP02 (4.1 cm mass, 6 mm midline shift, bilateral papilloedema) recommends CSF and serves a CSF
follow-up, with a hard MRI-before-CSF constraint. RP03 (3.8 cm posterior fossa mass compressing the
fourth ventricle, GCS 8) serves an initial CSF. Fix both: delete `action-5-analyze-csf`; add avoided action
`avoid-contra-lp-mass-effect`, `analyze_csf {}`, severity `contraindicated`, rationale from F10; delete the
sequence constraint that names action-5; move the CSF content to `fallback_tool_outputs.csf` (RP02 from
its follow-up, RP03 from `initial_tool_outputs.csf`), so an agent that does the LP still gets a coherent
report. RM01 and RM02: brain MRI reports mild mass effect without midline shift and no papilloedema, so
LP is allowed (keep CSF, recommended) and the soft MRI-before-CSF constraint stays.

### M. Fallbacks

`fallback_tool_outputs.advanced_imaging` with modality written "FDG-PET" in prose: set `FDG_PET`. ECG/EEG
fallbacks may stay as plain normal reports (except RM01 and RP03, where the EEG fallback must fit the case:
RM01 right hemispheric slowing, no epileptiform discharges; RP03 diffuse slowing, no status). CT
fallbacks in RM01, RP02, RP03 must show the lesion (hypodensity with oedema, mass effect as in the MRI).

### N. Avoided actions

All 30 carry five `waste` avoided actions (EEG, head CT, echo, cardiac monitoring, FDG-PET). Keep them
except: RM01 (first generalized seizure with headache in the ED: head CT and EEG are appropriate; delete
both avoided entries), RP02 (1-day headache, vomiting, hemiparesis, papilloedema: head CT appropriate;
delete the CT entry), RP03 (post-operative coma GCS 8: head CT and EEG appropriate; delete both). Rewrite
each remaining rationale in one case-tied sentence; citations `[Wattjes_2021]` for CT/PET, none needed for
echo/monitoring.

### O. Literature and drug outputs

Literature outputs present the 2017 criteria as current (DIS "2 of 4 regions", OCB "substitute for DIT"),
patient-specific conclusions, or stubs. Canonical general text (vary the focus by the case's question):
"The 2024 revision of the McDonald criteria (Montalban et al., Lancet Neurol 2025) adds the optic nerve
as a fifth region, accepts the kFLC index as an alternative to oligoclonal bands, and allows the central
vein sign and paramagnetic rim lesions as supporting markers. Lesions in four or five regions establish
dissemination in space without a separate test of dissemination in time; with two or three regions,
dissemination in time, positive CSF or the central vein sign is needed. In people over 50 or with
vascular risk factors, additional supporting evidence is recommended." Drug outputs (`proposed`,
`interactions`, `summary`): list each current medication and allergy against the drug in `proposed` with
the real effect (F11) or "no clinically significant interaction"; never an empty `interactions` list
with a summary that states the expected text; never a DMT choice argued in the summary.

### P. Pathway order (all)

`followup_outputs` and `action_criteria` in this order: brain MRI, spine MRI, labs, AQP4/MOG, CSF,
VEP, OCT, advanced imaging (MRS/perfusion), body CT, biopsy, drug check, literature. Stop rule
(section 3.4).

### Q. Diagnosis block

accepted[0] is "Multiple sclerosis, relapsing-remitting type" (25) or "... (tumefactive variant)" (RM01,
RM02, RP01, RP02, RP03). Keep. `icd_codes` include G35.B and G35.C (progressive forms) and the label
"demyelinating disease" (matches any demyelinating answer, NMOSD included): CENTRAL (synonyms file);
do not hand-edit the appended synonyms.

### R. Patient-block realism

- "Contrast dye (mild reaction)" allergy (M02, S02) while the case requires gadolinium: specify
  "Iodinated CT contrast (mild urticaria)", which does not bar gadolinium.
- Chief complaints that contradict the exam (M01-M03 "bilateral leg weakness" with a left- or
  right-predominant exam): reword to the exam's side ("progressive leg weakness, worse on the left").
- Lhermitte sign with no cervical lesion on the spine report (P04, RP01, S04): add a short dorsal
  cervical lesion to the spine follow-up (C2-C4, < 1 segment, non-enhancing) or delete Lhermitte; add
  the lesion (it also adds a region).

---

## 3. Target pathway and tiers

### 3.1 Standard pathway

1. Brain MRI, gadolinium, MS protocol (required).
2. Cervical and thoracic cord MRI, gadolinium (required).
3. Mimic-exclusion labs (required).
4. AQP4-IgG/MOG-IgG CBA (tier by 3.2).
5. CSF OCB or kFLC with paired serum (tier by 3.2; contraindicated in RP02, RP03).
6. VEP, OCT (optional; where present).
7. Tumefactive only: MRS/perfusion (optional), body CT (RP01, optional), biopsy (tier by case).
8. Drug check (optional; recommended RP03, RP05).
9. Literature (optional, last).

### 3.2 Tier rules (decide every case by these)

**AQP4/MOG (`action-aqp4-mog-cba`):**
- `required` when any red flag: severe optic neuritis (acuity 20/200 or worse, or hand motions),
  bilateral ON, LETM, area postrema or brainstem-encephalitic syndrome, tumefactive lesion, encephalopathy,
  onset at age 50 or later. Cases: M04, RM01, RM02, RP01, RP02, RP03, RP05, RS01.
- `recommended` when optic neuritis or myelitis is part of the current attack or the history, without a
  red flag. Cases: M01, M02, M03, P04, P05, RM04, RP04, RS02, RS03, RS06, S01, S02, S03, S04, S05, S06.
- none (no criterion, no stored result) otherwise: P01, P02, P03, RM03, RS04, RS05.

**CSF (`action-5-analyze-csf`):**
- `recommended` when F3/F4 make CSF useful to the decision or a mimic must be excluded: P01, P02, P03
  (migraine-lesion puzzle; OCB negative must not stop the diagnosis), RM01, RM02, RP01 (tumefactive:
  cytology/flow and OCB), RS01, RP05 (age > 50 with vascular risk).
- `optional` in all other cases (4-5 regions, or DIS plus MRI DIT already met).
- contraindicated (L): RP02, RP03.
No case has CSF required: in every case the corrected MRI data meet F3 without CSF, and F4 cases have a
cord lesion.

**VEP/OCT:** optional wherever present or added.
**Drug check:** recommended RP03, RP05; optional elsewhere.
**Literature:** optional everywhere.
**Biopsy (`action-biopsy`, `obtain_tissue_diagnosis` `{procedure: stereotactic_biopsy}`):** recommended
in RP02 (LP contraindicated, MRS/perfusion indeterminate, lymphoma and glioma not excluded) and RP03 (right
temporal lesion, see section 4); optional in RM01 (follow-up kept; imaging plus CSF already favour
demyelination); none in RM02, RP01.
**Advanced imaging (MRS/perfusion):** optional where a follow-up exists (RM01, RM02, RP01, RP02, RP03).

### 3.3 Sequence constraints

- Soft `action-1-analyze-brain-mri` -> `action-5-analyze-csf` where CSF is a criterion; reason: "Brain
  imaging before lumbar puncture to exclude a mass lesion with herniation risk"; no citation needed.
- Soft `action-1-analyze-brain-mri` -> `action-biopsy` in RM01, RP02, RP03 (target and trajectory come
  from the MRI).
- No hard constraint remains (RP02's goes with its CSF criterion).

### 3.4 Stop rule

`required_before_assessment` = the required criteria only (brain MRI, spine MRI, labs, plus AQP4/MOG
where required). `max_additional_actions`: 2 in S/RS and M/RM-moderate cases; 3 in P, RP and the
tumefactive RM01/RM02.

### 3.5 Tier table (after the fix)

| Case | AQP4/MOG | CSF | VEP | OCT | Other | Drug | Max add. |
|---|---|---|---|---|---|---|---|
| M01 | rec | opt | opt | - | - | opt | 2 |
| M02 | rec | opt | opt (add, FU exists) | - | - | opt | 2 |
| M03 | rec | opt | opt (add, FU exists) | - | - | opt | 2 |
| M04 | req | opt | opt | opt | - | opt | 2 |
| P01 | - | rec | opt | - | - | opt | 3 |
| P02 | - | rec | opt | - | - | opt | 3 |
| P03 | - | rec | opt | - | - | opt | 3 |
| P04 | rec | opt | opt | opt | - | opt | 3 |
| P05 | rec | opt | - | - | - | opt | 3 |
| RM01 | req | rec | - | - | MRS opt, biopsy opt | opt | 3 |
| RM02 | req | rec | - | - | MRS opt | opt | 3 |
| RM03 | - | opt | - | - | - | opt | 2 |
| RM04 | rec | opt | - | opt (add) | - | opt | 2 |
| RP01 | req | rec | - | - | MRS opt, CT CAP opt | opt | 3 |
| RP02 | req | contra | - | - | MRS opt, perfusion opt, biopsy rec | opt | 3 |
| RP03 | req | contra | - | - | MRS opt, biopsy rec | rec | 3 |
| RP04 | rec | opt | opt (add) | opt (add) | - | opt | 3 |
| RP05 | req | rec | opt (add) | opt (add) | - | rec | 3 |
| RS01 | req | rec | - | - | - | opt | 2 |
| RS02 | rec | opt | - | - | - | opt | 2 |
| RS03 | rec | opt | opt | opt | - | opt | 2 |
| RS04 | - | opt | - | - | - | opt | 2 |
| RS05 | - | opt | - | - | - | opt | 2 |
| RS06 | rec | opt | - | - | - | opt | 2 |
| S01-S05 | rec | opt | opt | opt | - | opt | 2 |
| S06 | rec | opt | opt (add) | opt (add) | - | opt | 2 |

("add" = new criterion; for M02/M03 the VEP follow-up exists but check whether action-7 exists and add
it if not.)

---

## 4. Per-case index

Every case: apply A (A1-A9 as the tier table says), B, C, D, E, J, K, O, P, Q-none, and the stop rule;
then the case bullets. "H" = remove cord findings from the brain MRI; "F" = delete the 3-month repeat
MRI; "I" = fix acute ON timing/OCT.

### M cases

**M01** (33 F, 6-week myelopathy, left RAPD 20/40)
- F. R: chief complaint to the exam side. J: IgG index 0.65 is normal against < 0.70; OCB "2 bands"
  stays (positive); add kFLC.
- DIS: periventricular, juxtacortical, infratentorial + spine C3-C4 + optic nerve (VEP left) = 5; CSF
  optional (was recommended).
- AQP4/MOG recommended (myelitis + optic neuropathy): add result rows.
- Left eye findings: if the HPI has no prior visual episode, add one (prior left painful visual blur,
  e.g. 2 years ago) so the RAPD/VEP make sense; otherwise keep.

**M02** (28 F, myelitis, prior left ON 18 months, RAPD and pallor)
- F, H (C3-C4 in the brain MRI impression). R: allergy to "Iodinated CT contrast"; chief complaint side.
- Pallor and VEP correct (prior ON). AQP4/MOG recommended (ON + myelitis).
- DIS: PV, JC, cord (C3-C4, T6-T7), optic nerve = 4; CSF optional.
- Drug output: DMF with ibuprofen/albuterol/ferrous sulfate: write real lines (no interaction; NSAID
  GI risk only if steroids are the proposed drug).

**M03** (38 M, myelitis, right colour desaturation, prior right-hand episode)
- F, H (C3-C4 in brain MRI). K: delete T10 (male). R: chief complaint side.
- DIS: PV, JC, cord, optic nerve (VEP right) = 4 (no infratentorial lesion although nystagmus: add a
  small middle cerebellar peduncle lesion or keep 4; keep 4). CSF optional.
- Literature output presents 2017 criteria as current: rewrite (O).

**M04** (26 F, severe left ON, hand motions, prior hemibody sensory episode)
- AQP4/MOG required (hand-motion acuity). OCT normal: correct, keep (F7).
- MRI impression "at least three of four characteristic MS regions": rewrite to 2024 (F1).
- KCE "MRI alone does NOT establish DIT, making the CSF OCB load-bearing": wrong under F3 (PV, JC, IT,
  optic nerve + C5-C6 cord = 5 regions). Replace with "DIS: 5 of 5 regions...; no DIT needed; CSF OCB
  supportive". Keep the CIS-versus-MS point without benchmark wording.
- Must M+1 ("≥3 regions ... OCB-for-DIT substitution"): rewrite as the canonical formulation must;
  prohibitions on ELISA assays: keep one ("Do not rely on an ELISA AQP4 or MOG assay"), delete the NMOSD
  diagnosis prohibition (it restates the differential).
- Vitamin D 18 ng/mL KCE: keep only as a comorbidity line (E: vary value if copied).

### P cases

**P01** (25 F, vertigo episodes, right-hand clumsiness, migraine, topiramate)
- F: delete the repeat MRI, which is now the only support for the label. Fix the data: the initial MS-protocol
  brain MRI shows, in addition to the subcortical foci, at least one ovoid periventricular lesion
  perpendicular to the ventricle, a lesion in the left middle cerebellar peduncle or pons (explains the
  vertigo episodes), and one lesion with incomplete-ring enhancement (DIT); radiologist impression
  neutral ("pattern includes lesions typical of inflammatory demyelination; some subcortical foci are
  non-specific"). The HPI's outside MRI ("nonspecific white matter changes") stays as history.
- DIS then PV, IT, cord (C3-C4), optic nerve (VEP interocular 10 ms: write the absolute right/left
  latencies so one eye is prolonged, or drop the optic region) = 3-4; DIT by enhancement; OCB negative
  (keep: the puzzle), kFLC below cutoff. CSF recommended.
- Drug output: delete "topiramate ... lymphopenia" (F11).

**P02** (31 F, 8 months vertigo, fatigue, paresthesias, BPPV label)
- F; G1 (SSEP stub delete). Fix the data as P01: the initial brain MRI keeps two periventricular foci,
  adds a periventricular ovoid lesion with incomplete-ring enhancement (DIT) and an infratentorial lesion
  (pontine or MCP, fits the end-gaze nystagmus). DIS: PV, IT, cord (C3-C4), optic nerve (VEP right
  118 ms) = 4. OCB negative stays; kFLC below cutoff. CSF recommended.
- KCE "If the initial brain MRI does not include the spinal cord..." delete (D).

**P03** (22 M, positional vertigo, fatigue, left-hand tingling)
- F; G1. Fix the data: initial MRI with a periventricular ovoid lesion perpendicular to the ventricle,
  a juxtacortical lesion, a pontine lesion, one enhancing lesion; spine follow-up gets a short dorsal
  C5-C6 left lesion for the left-hand tingling (currently "normal"). DIS: PV, JC, IT, cord = 4.
- VEP follow-up "All values within normal limits" (stub): write a real normal VEP report with both eyes'
  P100 and amplitudes.
- K: delete T10 (male). ANA 1:40-1:80 KCE: keep only if the labs carry that ANA row.

**P04** (31 F, right ON 16 days, left myelopathy T10 level, prior right blur at 28)
- OCT thinning at 16 days: keep, attribute to the prior right episode (I); pallor absent: keep.
- MRI impression counts the callososeptal interface as a fourth region: rewrite (F1): PV, JC, IT + optic
  nerve (MRI/VEP) + cord = 5.
- R: Lhermitte with "cervical cord unremarkable": add a short dorsal C3-C4 lesion to the spine report.
- B: delete the "Send AQP4" must. AQP4/MOG recommended. KCE "four regions" lines: rewrite to the F1/F3
  count. Literature output mentions an area postrema triad the patient does not have: make it general.

**P05** (24 F, highly active disease, prior right ON and left-leg episode, JCV index 2.84)
- AQP4/MOG recommended (ON + myelitis): add the CBA rows (the must says "negative here" with no result;
  delete that must: B).
- KCE: delete NEDA-3 and DMT-choice lines (management, generic); keep "highly active" only as observable
  facts (14 T2 lesions, 4 enhancing, two attacks in 18 months). JCV index 2.84 -> must "prefer an
  anti-CD20 agent (ocrelizumab/ofatumumab) over natalizumab given anti-JCV index 2.84" and keep T8.
- MRI impression "tumefactive or vasculitic process cannot be fully excluded" is a differential essay:
  trim to findings.

### RM cases

**RM01** (29 M, seizure, left hemiparesis; tumefactive variant). Data cannot support the label as written:
the HPI and MRI read as ADEM, neuro-Behçet or lymphoma (thunderclap "worst headache of his life", months of
lethargy and personality change, 30-45 lb weight loss, URI 3 weeks earlier, confluent brainstem and
thalamic signal, no prior attack). Fix the data (ruling 3):
- HPI: headache progressive over 2-3 weeks (not thunderclap); delete the weight loss and the months of
  lethargy/personality change; delete the URI; add one prior attack (e.g. 2 years ago, 3 weeks of
  right-hand numbness attributed to carpal tunnel, no imaging). Keep the family Behçet history as a
  distractor with "no oral or genital ulcers, no uveitis".
- MRI: the brainstem/cerebellar finding becomes discrete ovoid lesions (dorsal pons, right MCP) rather
  than confluent swelling; splenial lesion becomes a discrete callosal (periventricular) lesion; delete
  the right thalamic/basal ganglia extension; add 2-3 small ovoid periventricular lesions; keep the
  4.2 cm open-ring lesion with mild mass effect and no shift. Impression: findings only.
- G2: biopsy follow-up to `obtain_tissue_diagnosis`, optional. KCE "brain biopsy should be a last resort"
  delete (KCE lists findings).
- N: delete avoided CT and EEG; M: CT and EEG fallbacks consistent. AQP4/MOG required; CSF recommended
  (no shift, no papilloedema). Steroid must: IVMP after CSF cytology/flow (lymphoma excluded by the
  biopsy if done, or by CSF plus imaging); levetiracetam continued; K: delete T10.
- If after these edits the case still cannot be made coherent, log BLOCKED with the reasons.

**RM02** (29 F, left homonymous hemianopia, 4.2 cm right parieto-occipital open-ring lesion)
- Monocular findings incompatible with a retrochiasmal lesion: set acuity 20/20 both eyes and remove the
  left-eye colour loss (or add a left optic neuritis with RAPD; prefer the first). Floaters line: delete.
- F (repeat MRI shows shrinkage: delete). G5: MRS to `order_advanced_imaging`.
- AQP4/MOG required; CSF recommended. Spine follow-up "lateral cord" with no level: give a level.
- Drug check: methylprednisolone with ibuprofen GI risk: keep that content, tier optional.
- Musts: steroids after CSF cytology/flow negative and MRS favouring demyelination; T14/T15 rewrite with
  F10.

**RM03** (29 M, left abduction deficit, diplopia 2 weeks, keratoconus right eye)
- F; G4 (MG stub delete); G7 (literature stub). K: delete T10 (male).
- DIS: PV, JC, IT (left dorsal pons with partial ring enhancement), cord C5-C6 = 4. CSF optional.
- No AQP4/MOG criterion: NMOSD/MOGAD low with key features (short cord lesion, OCB positive, typical
  brain lesions).
- J: OCB "2 bands" with IgG index 0.64: keep; add kFLC above cutoff.

**RM04** (46 F, partial myelitis, painful tonic spasms, prior right visual episodes, hypercalcaemia)
- KCE cites OCT RNFL/GCL thinning; no OCT is served: add an OCT follow-up (right eye chronic thinning,
  inter-eye difference above F1 thresholds) and optional criterion. Right pallor in the exam: correct.
- AQP4/MOG recommended (myelitis + prior ON; Afro-Brazilian woman).
- KCE: "pathognomonic" tonic spasms -> "characteristic"; delete "respond to carbamazepine" (management ->
  must). Hypercalcaemia/sarcoid KCE: keep, needs the serum ACE row in labs (add if absent).
- Drug: natalizumab-amlodipine: fine; optional.

### RP cases

**RP01** (37 F, 7 months headache, Lhermitte, 2.1 cm open-ring right periventricular lesion)
- R: Lhermitte with a normal spine MRI: add a short dorsal C2-C3 lesion to the spine report (DIS then
  PV, JC, IT, cord = 4).
- G3: body CT to `order_body_imaging` chest_abdomen_pelvis_CT, optional.
- MRS follow-up: keep, `order_advanced_imaging` MR_spectroscopy, optional.
- MBP "normal: < 1.5" reference contradiction: delete MBP (J).
- AQP4/MOG required; CSF recommended. Brain MRI impression differential essay (glioma, metastasis,
  abscess): trim to findings.

**RP02** (28 F, 1-day right hemiparesis, headache, vomiting, papilloedema, 4.1 cm left parietal mass, 6 mm shift)
- L: delete the CSF criterion, add contraindicated LP avoided action, CSF content to fallback, delete the
  hard constraint. N: delete avoided CT; fallback CT shows the mass.
- G6: perfusion and MRS to `order_advanced_imaging`; brain MRI no longer reports MRS. G2: biopsy to
  `obtain_tissue_diagnosis`, recommended. G7: literature stub.
- Label support after L: DIS PV (right periventricular), JC/PV (left parietal), cord C3-C4 = 2-3; DIT by
  enhancing plus non-enhancing lesions; biopsy confirms demyelination. Keep.
- K: delete "corticosteroids may reduce efficacy of hormonal contraception" (F11). Musts: neurosurgical
  stereotactic biopsy before corticosteroids; ICP measures (head elevation, osmotherapy; dexamethasone
  only for impending herniation after neurosurgical discussion); IVMP after histology; PLEX if refractory.
- AQP4/MOG required: rows in labs (they were in the CSF report).

**RP03** (34 F, post-laparotomy coma GCS 8, quadriparesis; 3.8 cm left MCP/medulla lesion compressing the fourth ventricle)
- Plausibility: a 3.8 cm medullary-peduncular lesion in a patient "neurologically intact preoperatively"
  is implausible. Add a 2-3 week prodrome to the HPI (unsteadiness, dysphagia, hiccups, attributed to the
  abdominal illness and opioids) with acute post-operative decompensation.
- Exam: "Appears globally aphasic" cannot be assessed at GCS 8 (V2): delete; chief complaint "aphasia" ->
  "unresponsiveness".
- L: CSF contraindicated (move initial CSF to fallback). N: delete avoided CT and EEG; fallbacks
  consistent.
- F: delete `request_repeat_mri_post_steroids` and literature `request_steroid_trial`. Then label support
  needs tissue: add `obtain_tissue_diagnosis` follow-up of the right temporal lesion (non-dominant,
  accessible) with demyelination per G2, recommended criterion `action-biopsy`.
- MRS: optional. Drug check recommended: IVMP with metformin/glibenclamide (hyperglycaemia; insulin
  sliding scale, glucose monitoring; hypoglycaemia risk when steroids stop).
- AQP4/MOG required (brainstem/area postrema region, coma).

**RP04** (47 M, 6 weeks right leg weakness, right INO, right pallor; OCB negative)
- KCE cites OCT RNFL 74 µm and VEP P100 124 ms, never served: add both follow-ups (right eye chronic)
  with optional criteria. KCE "correlating with the left leg numbness 8 years ago": wrong (optic finding vs
  leg episode); rewrite as "prior subclinical right optic neuropathy".
- DIS: PV, JC, IT, cord (C5-C6, T4-T5), optic nerve = 5: no DIT needed; MRI DIT present anyway. KCE on OCB
  negativity: keep, rephrased to F3/F6.
- MRI impression items 3-4 ("fulfill MRI criteria for DIT/DIS"): delete (Kind 1, criteria are the
  clinician's). AQP4/MOG recommended.

**RP05** (54 M, vascular risk, progressive right leg weakness, Lhermitte, left RAPD/pallor)
- KCE cites OCT and VEP, never served: add both (left eye chronic, prior episode 8 months ago).
- F4: age 54 with vascular risk: cord lesions (C4-C5 enhancing) and OCB positive provide the extra
  evidence; KCE states it this way. CSF recommended. AQP4/MOG required (age ≥ 50; African American man
  with ON + myelitis).
- K: delete "amlodipine additive bradycardic" (F11); T9 may stay tied to treated OSA and the S1P class;
  no T10 present. Drug check recommended: steroids with metformin (hyperglycaemia).
- Homocysteine/B12 KCE: keep only if those rows exist in labs.

### RS cases

**RS01** (61 M, one week of diplopia and left facial weakness, PPRF lesion, left amblyopia)
- F; G7 (literature stub). K: delete T10.
- F4: age 61, hypertension, dyslipidaemia: cord lesion C5-C6 and OCB positive are the additional
  evidence; rationale and KCE say so; CSF recommended; AQP4/MOG required (age). Add a differential entry
  for brainstem stroke (DWI shows no restriction: low) and small-vessel disease.
- Amblyopia left (0.08): any VEP/OCT stays absent; the exam already notes no RAPD.
- Difficulty stays "straightforward" (ID convention); the rationale notes the age rule.

**RS02** (27 F, left leg myelopathy, prior right ON 8 months)
- F; H (T9-T10 and C2-C3 in the brain MRI: delete). Two literature follow-ups: keep at most one, general.
- DIS: PV, JC, IT, cord, optic nerve (prior ON, pallor) = 5. AQP4/MOG recommended.
- COC on the list: drug output notes teriflunomide raises ethinylestradiol exposure only if teriflunomide
  is the proposed drug.

**RS03** (37 F, right ON day 4, prior leg numbness 8 months)
- I: pallor -> normal disc or mild swelling; OCT to the acute canonical form with both eyes (current "(L)"
  flags read as left eye in a right ON case). H ("spinal cord distributions" in the brain MRI). F
  (the repeat MRI also mentions an optic-nerve lesion never reported on the initial study: deleted anyway).
- B: relabel the AQP4 row (CBA). AQP4/MOG recommended. VEP reference "< 102 ms" vs "< 115 ms" elsewhere:
  use the lab's one reference consistently within the report.

**RS04** (29 M, left CN VI palsy, left pontine enhancing lesion, obesity)
- F; H (C5-C6 in the brain MRI). K: delete T10.
- DIS: PV, IT, cord = 3 ("subcortical left temporal" is not a region, F1); DIT by the enhancing pontine
  lesion. No AQP4/MOG criterion. Add IIH to the differential only if the case raises it (fundi normal:
  low).

**RS05** (43 M, right hemiataxia, dysarthria, right MCP open-ring lesion, amlodipine)
- KCE: delete JCV monitoring line (management) and the "sensitivity ~80%" number; keep cerebellar
  localisation, ANA, ACE lines if those rows exist.
- DIS: PV, JC, IT, cord C3-C4 = 4. No AQP4/MOG criterion.

**RS06** (32 F, left arm numbness, gait ataxia, Lhermitte, B12 228)
- H (cervical cord in the brain MRI). KCE "2017 McDonald ... OCB fulfil DIT": rewrite to F3 (4 regions:
  no DIT needed). KCE OCT line: no OCT served and the fundi are normal: delete. B12 228 line: delete
  "carefully planted distractor"; keep "low-normal B12 does not explain enhancing brain lesions and OCB";
  add MMA only if labs have it.
- AQP4/MOG recommended (cervical myelitis).

### S cases

**S01** (28 F, left ON day 3, prior right arm/torso episode)
- I (pallor at day 3 -> normal disc; OCT both eyes, acute). H (left optic nerve stays in brain MRI;
  cervical cord and "No LETM" move to the spine report). F.
- B: relabel AQP4 row. AQP4/MOG recommended. Literature output (2017 as current): O.

**S02** (31 F, right ON 2 weeks, leg weakness, prior leg episode)
- I (OCT thinning at 14 days -> acute form). F. R: contrast allergy wording.
- KCE spinal-cord generic line: delete. Black-hole statements: F5. AQP4/MOG recommended.

**S03** (24 F, left ON day 5, prior right-hand episode, COC)
- I (pallor day 5; OCT). H. F. Literature criterion was recommended: optional (A4).
- AQP4/MOG recommended; relabel row.

**S04** (36 M, right ON 10 days, spastic paraparesis, Lhermitte)
- I (pallor at 10 days -> mild swelling or normal; OCT acute). H. F. G7 (literature stub). K: delete T10.
- Spine report "thoracic cord" with no level: give a level (T4-T6, < 1 segment, faint enhancement) and
  add a dorsal cervical lesion for Lhermitte (R).
- AQP4/MOG recommended; relabel row.

**S05** (29 F, left ON day 5 with disc swelling, prior right-leg attack with residual signs)
- I (OCT thinning at day 5 -> acute form; disc swelling correct). Delete the must "Obtain brain MRI"
  (test). KCE "internal consistency of the laterality is essential for case validity": delete. KCE "two
  attacks with objective evidence" stays (exam has residual right Babinski).
- AQP4/MOG recommended.

**S06** (34 M, right leg weakness, left INO, left pallor without ON history)
- KCE cites OCT, VEP and AQP4/MOG CBA, none served: add OCT and VEP follow-ups (left chronic thinning and
  P100 delay; prior subclinical optic neuropathy) and AQP4/MOG rows; criteria per the tier table.
- DIS: PV, JC, IT (left MLF), cord C5-C6, optic nerve = 5.

---

## 5. CENTRAL requests

1. **Criteria pack `dataset-generation/criteria_packs/MS-RR.md`**: add the keys `[McDonald_2024]`
   (Montalban et al., Lancet Neurol 2025;24:850-865), `[Wattjes_2021]` (Lancet Neurol 2021;20:653-670)
   and `[NICE_NG220]`; update its diagnostic text from McDonald 2017 to the 2024 revision (optic nerve
   region, 4-5 regions without DIT, kFLC, CVS/PRL, age > 50 rule); remove literature search and drug
   check from its required pathway.
2. **Diagnosis synonyms `agent-platform/config/policies/diagnosis_synonyms.yaml` (G35 entry)**: remove the
   progressive-course codes G35.B and G35.C from the accepted codes of a relapsing-remitting label
   (check the FY2026 ICD-10-CM G35 subcodes before editing); remove the label "demyelinating disease"
   (token match accepts "NMOSD, an inflammatory demyelinating disease"). Consider whether the bare label
   "MS" is acceptable given token matching ("MOGAD rather than MS" matches); flag for the scorer owner.
   Re-run `apply_diagnosis_synonyms.py` after the edit (not by hand).
3. **`condition_tool_guidance.yaml` and `test_guidance_claims.py`**: the MS-RR claims (AQP4/MOG in 13
   cases; ECG/EEG removed) change: AQP4/MOG criterion in 24 cases (8 required, 16 recommended); EEG and CT
   no longer avoided in RM01/RP03 (CT also RP02). Update the claims after the batch lands.
4. **Fallback library / vocabulary check**: confirm `kappa_free_light_chain_index`, `AQP4_IgG_cell_based`,
   `MOG_IgG_cell_based`, `NMO_MOG`, `MR_spectroscopy`, `perfusion_MRI`, `chest_abdomen_pelvis_CT`,
   `stereotactic_biopsy` resolve in `costs.yaml` and `tool_io.py` (they appear in TOOL_PARAMETER_VOCABULARY;
   a missing one is a CENTRAL vocabulary addition, not a case change).
5. **Optional guard** (test_case_guards): an `analyze_brain_mri` output must not contain "thoracic cord",
   "T[1-9]-T" or "conus" text (class H recurs across conditions with spine criteria).

## 6. Open questions for Andrea

None that need information only Andrea has. All judgment calls are decided above (ROUND_POLICY 24 Oct
2026). For awareness only: RM01 needs the largest data rewrite of the condition (section 4); the plan
fixes the data and allows BLOCKED only if the worker cannot make it coherent.
