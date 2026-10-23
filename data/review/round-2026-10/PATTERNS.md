# Error patterns the physician reviewers found (804 notes, 9 conditions, 23 October 2026)

Each pattern below appeared in many cases of the conditions that were reviewed, because the
August 2026 per-condition rewrite produced all 30 cases of a condition from shared text. Treat
every pattern as a question to ask of every case, including the eleven conditions nobody has
reviewed yet. The counts are notes / cases where the reviewers raised them.

## 1. Pathway and policy structure

- **Pathway order is not diagnostic order** (ALS 79/29, BACT-MEN 22/20, others). Follow-ups began
  with literature searches, drug-interaction checks, respiratory monitoring or genetics, while the
  studies that establish the diagnosis and exclude its mimics came later or sat only in the initial
  work-up. Reorder; see ROUND_POLICY "Pathway order".
- **Literature search used as a clinical step** (ALS, ALZ, BACT-MEN, GLIO-HG). See ruling 5.
- **Scoring key leaked into the material the agent receives**: a literature or drug-interaction
  output whose finding or summary is the `expected_evidence` text of a criterion, or an empty block
  whose summary repeats it (BACT-MEN M03, P01).
- **A must or a criterion that no action can satisfy**: a required assay absent from the action's
  assay list (GLIO-HG: 14 of 30 cases without an IDH assay, no CDKN2A/B, H3K27 in 2; SOX10 required
  but not orderable), a must naming a study no criterion orders (functional MRI, venous duplex,
  repeat EMG), a requirement already "done" in the history.
- **Treatment or consult disguised as a test**, or a step whose output is the response to
  treatment (ammonia as a treatment-response marker, HEP-ENC 12; a "48 h after rifaximin" panel;
  consults filed as `interpret_labs`, ALS 4). See ruling 4.
- **Diagnostic step offered before it is indicated**: genetic panel before the electrodiagnostic
  diagnosis (ALS 12), respiratory function treated as a diagnostic step rather than staging (ALS
  22), LP before imaging when imaging is indicated, cultures mandated in afebrile patients without
  infection risk (HEP-ENC 11), tests not indicated at all.
- **Contradictions between musts, prohibitions and avoided actions**: a must that forbids what
  another must requires (dexamethasone before vs after lymphoma biopsy), an avoided action that the
  pathway itself performs and then diagnoses from (LP in a patient with midline shift), a
  prohibition of a call the policy requires, thrombolysis door-to-needle in a must and
  contraindicated in the same case.
- **Required actions missing**: the central item of the case's management absent (meningococcal
  disease measures, DIC in septic shock, TEE when the source is cardiac, securing the aneurysm in
  SAH (10 of 30 never secured; DSA required in only 3), antiseizure therapy after a documented
  seizure (GLIO-HG 13), potassium and magnesium for a long QTc, blood pressure control before
  aneurysm securing (9), Listeria cover when a risk factor is present (11), performance status,
  safety and supportive actions (ALS 8)).
- **Wrong tool for the act** (consults as labs, BOLD fMRI under `perfusion_MRI`, cytology under the
  wrong specimen).

## 2. Clinical correctness

- **Outdated or wrong guideline**: IDSA 2004 imaging-before-LP criteria instead of WHO 2025 / NICE
  NG240 (BACT-MEN 22/19); acute stroke decisions not per AHA/ASA 2026 (24); ESCMID cited where it
  does not govern; antiseizure prophylaxis against AIOM; lactulose target 2-4 stools instead of 2-3
  (HEP-ENC 9); SAH securing window "24-72 h" in all 30 cases instead of as early as feasible,
  ideally within 24 h.
- **Wrong facts**: Ottawa SAH rule misapplied, nimodipine called teratogenic, sodium correction
  ceiling, labetalol use, zinc physiology inverted, fabricated guideline thresholds in literature
  outputs, wrong drug-interaction rationale (ALS 6).
- **Diagnosis overcalled or mis-staged**: definite ALS at a first EMG showing denervation in one
  region (ALS 23/5), MCI vs dementia staging (ALZ 6), cholinesterase inhibitor in MCI (8), atypical
  Alzheimer variants built from the amnestic template (9), CSF vs amyloid PET choice (5), a WHO
  name that does not exist ("giant cell glioblastoma" as an integrated diagnosis), a variant label
  the findings do not meet (GBS: AMSAN, bifacial weakness with paraesthesias but no sensory signs,
  pure areflexia with 5/5 strength), a grade 2 astrocytoma accepting "glioblastoma".
- **Differential not updated after the work-up** (ALS 24, HEP-ENC/GBS 21): mimics left moderate or
  high after the results exclude them; a mimic the case itself raises missing.
- **Comorbid contributors dismissed** (B12 deficiency with high MMA and homocysteine marked "no
  clinical significance", ALZ 6; thyrotoxicosis in a C9orf72 carrier).
- **Severity and scores wrong**: NIHSS, GCS, HINTS, Hunt-Hess, WFNS, Child-Pugh and MELD not
  derivable from the stored values (HEP-ENC 9), FVC 55-68% called "normal" and the 20 mL/kg rule
  applied without a weight (GBS 13), CK above 5x ULN called typical of ALS (5), HE grade inconsistent.
- **Unsupported antecedents** (GBS 9): a trigger infection asserted with nothing in the case to
  support it.

## 3. Internal consistency (cross-field)

- Narrative contradicts the reports (ALS 11), structured fields contradict the narrative (IADL
  marked false in dementia, `contrast_used`, ORGANISM "none" with a named isolate and MICs,
  "collected before antimicrobials" true after antibiotics (6), Factor V Leiden negative and
  positive), laterality flipped between exam, imaging and EEG (SE, SAH, ISCH), allergy listed and
  then the allergen mandated (10), timelines that cannot happen (20), duplicate analytes with
  different values in one panel (12), lab arithmetic and reference ranges wrong (17), impossible
  lab values (GLIO-HG 5), an exclusion-studies block contradicting the panel (SAH 3), a tumour
  marker reported as a serum analyte, a lesion placed in an anatomically impossible location,
  deficits no lesion explains, an impression omitting its own key finding (7).

## 4. Template carry-over

- Beta-hCG in men (SE 5), meningitis blood cultures in status epilepticus without infection (12),
  pneumococcal boilerplate in other pathogens' cases (13), imaging boilerplate identical across
  cases (4), generic prohibitions irrelevant to the case (haloperidol, 6), templated text across a
  condition (GLIO-HG 9), copied record errors (5), notes describing another case's content.

## 5. Language and engineering leakage

- Internal engineering notes inside clinical text ("DVT imaging tool is not in the 12-tool set,
  document in metadata.vocab_gap"), placeholders, mixed languages, duplicated sentences.
- Scoring-key leakage in any-query outputs (Andrea, 24 Oct 2026): a stored
  `search_medical_literature` or `check_drug_interactions` output (initial, followup or fallback)
  is served for any query or drug, so it must not repeat the `expected_evidence` of any action
  criterion, including the criterion of that same tool. Rewrite the output in report voice (what
  the source or the interaction check says), not the policy's wording. Check each case with
  `uv run pytest agent-platform/tests/test_case_guards.py -q -k CASE-ID`; the leak, followup and
  banned-string guards must pass.

## What the reviewers approved

Reviewer 2 approved 21 SAH, 26 SE, 7 GBS, 4 HEP-ENC and 5 ISCH-STR cases. Approval means the
reviewer found no blocking error, not that the case is free of the patterns above: check them, but
change an approved case only for a real error.
