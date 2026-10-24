# NMDAR-ENC: condition plan for the October 2026 review round

Lead plan for the 30 anti-NMDA receptor encephalitis cases (M01-M05, P01-P08, RM01-RM03,
RP01-RP03, RS01-RS04, S01-S04, S06, S09, S10). Workers apply it to their cases so that every case
reaches the same decision. Read `ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not
repeat them.

**Reviewer notes.** There is no `notes/NMDAR-ENC.md`: no physician reviewed this condition in this
round. Every case log therefore has an empty "Reviewer notes" table (write "none: condition not
reviewed") and all work goes in "Own findings". The only physician input is the July 2026 tool
review in `condition_tool_guidance.yaml` (key `autoimmune_encephalitis_nmdar`, Reviewer 2). Its
rulings bind: brain MRI stays required, with exclusion of alternatives as its role; the CSF order
covers cells, protein, glucose, OCB or IgG index, HSV PCR and the CSF anti-GluN1 cell-based assay;
the serum anti-GluN1 cell-based assay is read with the CSF, never alone; routine EEG is required
with continuous EEG as a selected escalation; tumour screening is required in every case and
tailored by age and sex. No case is approved, so there is no approved-case restraint, but do not
churn correct prose.

**Baseline (24 Oct 2026, before any edit).**
- `perfect_agent.py` passes 30/30. This hides two unreachable criteria (class C1): the replayed
  ground-truth arguments include keys a real agent cannot send.
- `test_case_guards.py -k NMDAR-ENC`: 18 cases fail `test_any_query_outputs_do_not_leak_expected_evidence`
  (M01, M03, M05, P01-P08, S01-S04, S06, S09, S10). Class C3 fixes all of them.
- No case has a sequence constraint. Every stop rule has `max_additional_actions: 0`.

**Use.** Apply the classes of section 2 (canonical texts verbatim, `<...>` slots from the case),
then section 4, then rebuild criteria, follow-ups, sequence and stop rule per section 3; run
`perfect_agent.py -v`, `case_io.py check` and the case guards. Keep the case's spelling; no em or
en dashes; a new number must be plausible, distinct across cases and consistent; ids stay.

---

## 1. Governing guidelines and canonical facts

### 1.1 Sources and citation keys

| question | source | key |
| --- | --- | --- |
| Diagnostic criteria (possible AE, probable/definite anti-NMDAR, Hashimoto encephalopathy) | Graus F et al. Lancet Neurol 2016;15:391-404 | `[Graus_2016]` |
| Outcome, tumours, first/second-line (577 patients) | Titulaer MJ et al. Lancet Neurol 2013;12:157-165 | `[Titulaer_2013]` |
| Age 45 or more (fewer teratomas, more carcinomas) | Titulaer MJ et al. Late-onset anti-NMDAR encephalitis. Neurology 2013;81:1058-1063 | `[Titulaer_late_2013]` (new) |
| Clinical features, teratoma, tumour screening | Dalmau J et al. Lancet Neurol 2011;10:63-74 | `[Dalmau_2011]` |
| CSF versus serum testing | Gresa-Arribas N et al. Lancet Neurol 2014;13:167-177 | `[Gresa-Arribas_2014]` (new) |
| Extreme delta brush | Schmitt SE et al. Neurology 2012;79:1094-1100 | `[Schmitt_2012]` |
| Acute management (first-line, escalation, PLEX) | Abboud H et al. J Neurol Neurosurg Psychiatry 2021;92:757-768 | `[Abboud_2021]` (new) |
| Clinical update | Dalmau J et al. Lancet Neurol 2019;18:1045-1057; Dalmau J, Graus F. NEJM 2018;378:840-851 | `[Dalmau_2019]` (new), `[Dalmau_2018]` |
| Neuroleptic intolerance | Lejuste F et al. Neurol Neuroimmunol Neuroinflamm 2016;3:e280 | `[Lejuste_2016]` (new) |
| Post-HSV autoimmune encephalitis | Armangue T et al. Lancet Neurol 2018;17:760-772 | `[Armangue_2018]` (new) |
| Suspected encephalitis: aciclovir, HSV PCR, HIV | Venkatesan A et al. Clin Infect Dis 2013;57:1114-1128; Solomon T et al. J Infect 2012;64:347-373 | `[Venkatesan_2013]`, `[Solomon_2012]` (new) |
| Continuous EEG indications | Herman ST et al. J Clin Neurophysiol 2015;32:87-95 | `[Herman_2015]` (new) |
| Hyponatraemia grading and correction | Spasovski G et al. Eur J Endocrinol 2014;170:G1-G47 | `[Spasovski_2014]` (new) |
| Checkpoint-inhibitor irAE (RP02) | Schneider BJ et al. J Clin Oncol 2021;39:4073-4126 | `[ASCO_irAE_2021]` (new) |
| Paraneoplastic syndromes | Graus F et al. Neurol Neuroimmunol Neuroinflamm 2021;8:e1014 | `[Graus_2021]` (new) |
| `[Lancaster_2016]` | J Clin Neurol 2016;12:1-13 | keep where already cited |

New keys go to CENTRAL 1. Citation lists hold bracketed keys only: delete the free-text twins
("Graus 2016; Titulaer 2013", "Graus_2016", "Lancaster_2016") that sit beside a key in every
criterion of all 30 cases. Never cite a key for a claim it does not make.

**Which source governs.** Graus 2016 governs diagnosis. Acute treatment follows Titulaer 2013 and
Abboud 2021 (no randomised trial exists; say "observational evidence and expert consensus", never
"guideline-mandated"). Aciclovir follows Venkatesan 2013 / Solomon 2012. RP02 adds ASCO 2021.

### 1.2 Canonical clinical facts (use these, never other numbers)

- **Graus 2016, definite anti-NMDAR encephalitis:** one or more of the six major groups plus IgG
  anti-GluN1 antibodies, after reasonable exclusion of other disorders. Antibody testing should
  include CSF; a serum-only result needs confirmatory tests. Onset duration is not part of the
  definite criteria.
- **Six major groups:**
  1. abnormal behaviour (psychiatric) or cognitive dysfunction;
  2. speech dysfunction (pressured speech, verbal reduction, mutism);
  3. seizures;
  4. movement disorder, dyskinesias, rigidity or abnormal postures;
  5. decreased level of consciousness;
  6. autonomic dysfunction or central hypoventilation.
- **Graus 2016, probable:** rapid onset (under 3 months) of at least four groups, or three groups
  with a systemic teratoma, plus at least one of: an abnormal EEG (focal or diffuse slow or
  disorganised activity, epileptic activity, or extreme delta brush) or CSF pleocytosis or OCB.
  Reasonable exclusion of other disorders. MRI is NOT one of the probable criteria. The criteria
  pack's sentence ("Probable = clinical features + abnormal CSF or MRI suggestive") is wrong: never
  copy it (CENTRAL 6).
- **CSF vs serum:** all patients had CSF antibodies and about 14% were serum-negative in Gresa-Arribas
  2014. Serum can also be falsely positive at low titre. The CSF cell-based assay is decisive.
- **MRI:** abnormal in about a third of patients (Titulaer 2013), usually T2/FLAIR signal in the
  medial temporal lobes or cortical/subcortical regions, without restricted diffusion or
  haemorrhage. A normal MRI does not exclude the diagnosis.
- **EEG:** abnormal in most patients (diffuse or focal slowing, epileptiform activity, seizures).
  Extreme delta brush was found in 7 of 23 adults (30%) in Schmitt 2012. It is supportive, not
  pathognomonic, and its absence excludes nothing. Never write "highly specific", "30-50%" or
  "pathognomonic".
- **CSF:** lymphocytic pleocytosis, mildly raised protein and/or OCB in most patients. A normal CSF
  does not exclude the disease. Glucose is normal; a low CSF/serum glucose ratio (below about 0.5)
  is not a feature and points to another process.
- **Tumours:**
  - 38% of 577 patients had a tumour, nearly all ovarian teratomas (Titulaer 2013).
  - The frequency peaks in women of reproductive age.
  - Tumours are rare in men and in children under 12.
  - In patients 45 or older, tumours were found in about a quarter of patients and were mostly
    carcinomas (Titulaer_late_2013).
  - Post-HSV anti-NMDAR encephalitis is not tumour-associated (Armangue 2018).
- **Prodrome:** a viral-like prodrome (headache, fever, URI or GI symptoms) precedes the illness in
  about 70% of patients (Dalmau 2011).
- **Hyponatraemia:**
  - It occurs in anti-NMDAR encephalitis but is far more typical of anti-LGI1 encephalitis.
  - Grades (Spasovski 2014): mild 130-134, moderate 125-129, profound below 125 mmol/L.
  - Correction limit: at most 10 mmol/L in the first 24 h and 8 mmol/L in each later 24 h.
- **Post-HSV:** autoimmune encephalitis developed in 27% of HSV encephalitis patients within about
  3 months; 64% of them had NMDAR antibodies (Armangue 2018). Relapse of HSV encephalitis is
  excluded by a negative CSF HSV PCR.
- **Treatment (observational evidence and consensus):**
  - First-line therapy: IV methylprednisolone 1 g daily for 5 days, with IVIG 0.4 g/kg/day for 5
    days (2 g/kg total) or plasma exchange (5 to 7 exchanges). Steroid plus IVIG or plasma
    exchange is usual in moderate to severe disease. Tumour removal is part of first-line
    treatment.
  - In Titulaer 2013, 53% improved within 4 weeks of first-line therapy or tumour removal. Among
    first-line failures, second-line therapy was associated with better outcome. 81% had a good
    outcome (mRS 0-2) at 24 months.
  - Second-line therapy: rituximab (375 mg/m² weekly for 4 doses, or 1 g repeated after 2 weeks)
    and/or cyclophosphamide (750 mg/m² monthly). It is considered when there is no meaningful
    improvement about 10 to 14 days after first-line therapy (Abboud 2021).
  - Screen for hepatitis B (HBsAg, anti-HBc) before the first rituximab dose. This is a future
    pre-treatment step: it may appear in a must without a criterion.
  - Cyclophosphamide is gonadotoxic and teratogenic: discuss fertility in young women.
- **Neuroleptics:** severe neuroleptic intolerance (rigidity, hyperthermia, rhabdomyolysis,
  NMS-like reactions) was reported in a large share of exposed patients (Lejuste 2016).
  Benzodiazepines are first choice for agitation and catatonia. Haloperidol and other high-potency
  D2 antagonists are avoided.
- **Valproate:**
  - Avoid in women able to become pregnant unless other options fail (EMA 2018 restriction). It
    stays acceptable as an IV second-line agent for status epilepticus when needed.
  - Valproate roughly doubles lamotrigine exposure (halve the lamotrigine dose).
  - Carbapenems lower valproate levels sharply.
  - Valproate can cause hyperammonaemic encephalopathy.
- **Aciclovir:**
  - 10 mg/kg IV every 8 hours, extended to 12-hourly at CrCl 25-50 mL/min and 24-hourly at
    10-25 mL/min. Keep the patient well hydrated.
  - Stop once HSV PCR is negative and another diagnosis is established.
  - Repeat the PCR on a second sample when the first LP was within 72 hours of onset and HSV
    remains plausible (Venkatesan 2013, Solomon 2012).
- **Antibody titres:** report as end-point dilutions of one doubling series per case (1:2, 1:4,
  1:8 ... or 1:10, 1:20, 1:40 ...). A titre outside any series (S10 "1:56") is an error.

---

## 2. Error classes in this condition

No note ids exist (no reviewer notes). Each class lists the cases it covers and the fix.

### C1. Criteria a real agent cannot satisfy (all 30) [blocker]
- **Problem.** `action-2-analyze-csf` requires `basic: [...]`, which is not a parameter of
  `analyze_csf`. An agent following the schema never sends it, so the required CSF criterion
  always fails (verified: a schema-conformant call returns `criterion_matches False`).
  - `check_drug_interactions` criteria require `screen_for`, which is not a schema parameter.
  - Literature criteria require an exact `query` string (string equality).
  - `analyze_brain_mri` requires `protocol: standard`, rejecting the epilepsy protocol a clinician
    would choose for seizures.
  - The labs criterion requires 11 panels at once.
- **Fix.** Use the minimal required arguments of section 3.2, exactly. The `basic` and
  `screen_for` keys disappear from every criterion. CENTRAL 2 (63 cases dataset-wide carry `basic`).

### C2. Literature search used as a clinical step (all 30) [major]
- **Problem.** `search_medical_literature` is `recommended` in all 30 cases (ruling 5).
- **Fix.**
  - Set it to `optional` with `required_arguments: {}`.
  - Its follow-ups go last.
  - Its expected_evidence becomes "General published evidence on anti-NMDAR encephalitis diagnosis
    and immunotherapy", or a case-specific topic phrase written differently from the stored
    output.
  - Nothing required depends on it.

### C3. Scoring key and placeholders in any-query outputs (18 failing cases plus all lit/DDI outputs) [blocker]
- **Problem.**
  - Initial `literature_search` (M01, M03, P01-P07, S10) and the S01-S04, S06 follow-ups hold the
    placeholder finding "Confirms diagnostic criteria, treatment sequence, and emerging
    evidence ..." with `evidence_level` "see the case's cited guideline".
  - The DDI outputs (M01, M03, M05, P01-P03, P05, P06, P08, S10 initial; S01-S04, S09 follow-up)
    repeat the criterion's expected_evidence in `summary`/`warnings` with empty `interactions`.
  - The fallback DDI says `"proposed": "(agent not specified on this case's pathway)"`
    (engineering leak).
- **Fix.**
  - Replace every placeholder literature output with the canonical literature output below, keeping
    only the results relevant to the case.
  - The case-specific literature follow-ups (M04, M05, M02, P08, RM01-RM03, RP01-RP03, RS01-RS04,
    S09) keep their topic, but each finding must be checked against section 1.2. Delete fabricated
    claims (S09 "bilateral resection associated with better outcomes", RP03 "20-27%" becomes
    "27%"), delete patient-specific conclusions, and give a real `source`.
  - Write each DDI output in report voice from the patient's actual medication list (C10).
  - Set the fallback DDI `proposed` to `""`.
  - Run the guard until it passes.

Canonical literature output (store under `initial_tool_outputs.literature_search` key
`"anti-NMDA receptor encephalitis diagnosis and treatment"` or as the follow-up; trim to 3-5
results):
```
summary: "Published criteria and cohort data on anti-NMDA receptor encephalitis: definite diagnosis rests on CSF IgG anti-GluN1 antibodies; first-line immunotherapy and tumour removal are followed by second-line agents when there is no response."
results:
- source: "Graus F et al. Lancet Neurol 2016;15:391-404", evidence_level: "expert consensus criteria",
  finding: "Definite anti-NMDAR encephalitis requires one or more of six major symptom groups and IgG anti-GluN1 antibodies, with CSF testing included; probable disease requires four groups (or three with a teratoma) of rapid onset plus an abnormal EEG or CSF pleocytosis or oligoclonal bands."
- source: "Gresa-Arribas N et al. Lancet Neurol 2014;13:167-177", evidence_level: "retrospective cohort",
  finding: "All patients had antibodies in CSF, whereas about 14% were negative in serum; CSF titres related more closely to outcome than serum titres."
- source: "Titulaer MJ et al. Lancet Neurol 2013;12:157-165", evidence_level: "observational cohort (n=577)",
  finding: "38% had a tumour, mostly ovarian teratoma; 53% improved within 4 weeks of first-line immunotherapy or tumour removal; second-line rituximab or cyclophosphamide after first-line failure was associated with better outcome; 81% had mRS 0-2 at 24 months."
```
Optional extra results: Schmitt 2012 (extreme delta brush in 7 of 23 adults, with a more prolonged
illness) and Lejuste 2016 (frequent severe antipsychotic intolerance: rigidity, hyperthermia,
rhabdomyolysis).
Post-HSV cases add Armangue 2018 ("27% of patients with HSV encephalitis developed autoimmune
encephalitis, 64% of them with NMDAR antibodies, typically within about 2 months"). Older
patients add Titulaer_late_2013 ("patients aged 45 or more had fewer teratomas; tumours, mostly
carcinomas, were found in about a quarter").

### C4. CSF result in the serum report; pending CSF antibodies contradicted (all 30) [blocker]
- **Problem.**
  - Every labs report carries CSF anti-NMDAR results ("CSF anti-NMDA receptor IgG", "Anti-NMDA
    receptor Ab (CSF)"), sometimes inside the panel named "Serum anti-GluN1 cell-based assay"
    (P02, P03, RM01, RP03). In RP01 it is a whole CSF panel.
  - In 14 cases the CSF report itself says the antibody is "Pending" while the labs report gives
    its titre (M01-M05, P01, P04-P08, RM02, RM03).
  - In P02 and P03 the CSF report says both "pending" and "Positive".
  - RP02's CSF report says "Positive" without a titre.
- **Fix.**
  - The CSF report carries the final CSF result: one key `NMDAR_antibodies` with value
    `"Positive, titre 1:<x> (cell-based assay, IgG anti-GluN1; reference laboratory, resulted day <n>)"`,
    taking the titre from the labs CSF entry.
  - Delete the duplicate display keys (`Anti-NMDA receptor antibodies`, `Anti_NMDA_receptor_antibodies`,
    `NMDAR_antibody_CSF`, `anti_NMDAR_CSF`, `anti_NMDAR_antibody`, `Anti-NMDA receptor antibodies (CSF)`).
  - Mention the result once in `interpretation`.
  - Delete every CSF entry from the labs report.
  - The labs report keeps one serum entry, in a panel named `Serum anti-GluN1 IgG (cell-based assay)`.
  - S10: CSF titre 1:56 becomes 1:64.

### C5. Labs report: duplicates, leaky "Exclusion studies", narrative, missing tests (all 30) [major]
Rebuild `initial_tool_outputs.labs` to these panels, keeping the case's values:
- CBC; BMP or CMP plus Hepatic panel; Coagulation; `Inflammatory markers` (CRP, ESR once).
- `Thyroid function` (TSH, free T4); `Thyroid autoantibodies` (anti-TPO, anti-thyroglobulin once).
- `Serum anti-GluN1 IgG (cell-based assay)`.
- `Autoimmune encephalitis antibodies (serum)`: LGI1, CASPR2, GABA-B, AMPA, plus DPPX, GABA-A and
  IgLON5 where the case has them, each Negative unless the case says otherwise.
- `Onconeural antibodies (serum)`: Hu, Yo, Ri, CV2/CRMP5, Ma2, amphiphysin, SOX1, each Negative.
  This replaces the line `paraneoplastic_panel: No abnormality identified`.
- `Infection serology`: HIV-1/2 Ag/Ab, plus RPR if present.
- `Toxicology` (urine drug screen, ethanol); CK in `Other`.
- `beta-hCG` (serum, Negative) in every woman aged 12-50. Add it where missing: all women except
  S03, S10 and RM03.
- In cases with sodium below 130 mmol/L: serum osmolality (low), urine osmolality (above 100
  mOsm/kg) and urine sodium (above 30 mmol/L), values consistent with SIADH. RS01 already has
  serum osmolality.

Delete:
- the `Exclusion studies` panel and its text "Ordered to exclude an alternative cause; the result
  does not support one, which is what this case's diagnosis rests on" (30 cases);
- `Reviewed inflammatory markers` (30);
- anti-TPO inside the autoimmune panel;
- any second copy of an analyte.

Set `clinical_significance: null` everywhere. Make `interpretation` and `abnormal_values_summary`
a plain recital ("Sodium 126 mmol/L (L)"): delete parentheticals such as "(severe SIADH)",
"(post-ictal)", the "stress hyperglycemia" tail, "(elevated from seizure/movements)", "(SIADH pattern)".
Fix `is_abnormal` against the reference range.

### C6. Pathway and criterion order (all 30) [major]
Follow-ups begin with literature or DDI in 18 cases, and the cEEG sits after them. Reorder per
section 3.1 and keep the ids.

### C7. Continuous EEG: musts name a study the pathway cannot answer (all 30) [major]
- **Problem.**
  - Every case has the must "obtain continuous EEG monitoring".
  - 17 cases have no cEEG follow-up (M02, P02, P04, P08, RM01-RM03, RP01, RS01-RS04, S01-S04,
    S06), so an agent ordering it receives the library's normal cEEG. That contradicts routine
    EEGs that captured seizures (S01, S02, P02, RS01...).
- **Fix.**
  - Every case gets a cEEG follow-up (`analyze_eeg`, `eeg_type: continuous_icu`, trigger
    `request_continuous_eeg`) consistent with its routine EEG: same lateralisation, same
    patterns, plausible evolution, nothing contradicting it.
  - The criterion `action-<n>-analyze-eeg` with `{eeg_type: continuous_icu}` is `recommended` in
    29 cases. In RP01 there is no cEEG criterion, but the follow-up is still authored (no seizures).
  - New criteria use id `cEEG-escalation`. Expected evidence: "Seizure burden and evolution of the
    background over 24 hours or more".
  - The cEEG must appears only in cases with the criterion (canonical must M5).

Report template:
```
impression: "This is an ABNORMAL continuous EEG (<24/48> hours) due to: 1. <background>. 2. <n> electrographic seizures of <side> <region> onset, <clinical correlate or 'without clinical correlate'>. 3. <extreme delta brush present/absent>. Clinical correlation recommended."
```
Do not write "confirming that seizures are from a new process" (P03) or "very active disease"
(S09): they are kind 1 leakage.

### C8. Templated differential, never updated (all 30) [major]
- **Problem.** The same four entries appear in every case: HSV `high`, other AE `moderate`, primary
  psychiatric `moderate`/`low`, drug/NMS `low`, with identical key_features. In every case the HSV
  PCR is negative and the panels are negative.
- **Fix (assessment-time view).**
  - HSV-1 encephalitis (or HSV relapse in P03, RP03): `low`. Key features: "<n> CSF HSV PCR
    negative; <MRI without haemorrhage or restricted diffusion>; CSF anti-GluN1 positive".
  - Other antibody-mediated encephalitis: `low`. Key features: "serum <and CSF> neuronal-surface
    panel negative (LGI1, CASPR2, GABA-B, AMPA)". Remove the demographic-skew essay.
  - Primary psychiatric disorder: `low`. Key features name this case's seizures, dyskinesias,
    dysautonomia, EEG or CSF findings.
  - Drug-induced psychosis / NMS: `low`. In M02, M04, P07 and RM02 (antipsychotic exposure) state
    the CK, temperature and rigidity values that argue against NMS.
  - Add the mimics the case itself raises (section 4): SREAT/Hashimoto encephalopathy (P08, RM01,
    RM02), MOG-antibody or AQP4 overlap / ADEM (RM02, RS02, RS04), CJD (RP01, RP02, RM03),
    leptomeningeal carcinomatosis and checkpoint-inhibitor encephalitis (RP02), bipolar relapse
    (P07), thiazide- or SSRI-induced hyponatraemia (RM03), valproate encephalopathy (RS02).

### C9. Templated musts and prohibitions (all 30) [major]
Replace the seven template musts with the canonical set below. Keep only the musts that apply and
add case-specific ones. Delete the must "Send paired CSF and serum..." (a diagnostic step already
scored by criteria, and duplicated by prohibition P5).

Canonical musts:
- **M1 Antiviral.** "Start IV aciclovir 10 mg/kg every 8 hours at presentation<, adjusted to
  creatinine clearance (<value> mL/min): every 12 hours>, and stop it once CSF HSV PCR is negative
  and the antibody diagnosis is established; repeat the PCR on a second CSF sample if the first LP
  was within 72 hours of onset and HSV encephalitis remains plausible." Post-HSV cases instead:
  "Restart IV aciclovir 10 mg/kg every 8 hours until CSF HSV PCR excludes HSV relapse, then stop."
- **M2 First-line.** "Start first-line immunotherapy without waiting for the antibody result once
  infection is reasonably excluded: IV methylprednisolone 1 g daily for 5 days with IVIG 0.4
  g/kg/day for 5 days (2 g/kg total) or plasma exchange (5 to 7 exchanges)." Add case cautions:
  diabetes (glucose monitoring), CKD (IVIG infusion rate and hydration), IgA deficiency if known.
- **M3 Tumour.** One of:
  - Teratoma found: "Arrange prompt surgical removal of the <side> ovarian teratoma
    (laparoscopic, ovary-sparing where feasible) as part of first-line treatment, with
    gynaecology."
  - Screen negative, woman under 45: "Pelvic ultrasound shows no tumour: repeat pelvic imaging
    (MRI or transvaginal ultrasound) if the response to immunotherapy is poor or the disease
    relapses, and continue tumour surveillance during follow-up."
  - Screen negative, man under 45: "Scrotal ultrasound shows no tumour; no further tumour
    imaging is needed unless the course is atypical or refractory."
  - Testicular mass (P02): see section 4.
  - Older patients and RP02: see section 4.
- **M4 Seizures.** "Treat seizures with an antiseizure medication such as levetiracetam<,
  renally adjusted> or lacosamide<; avoid valproate in a woman able to become pregnant><; with
  lamotrigine on board, avoid valproate or halve the lamotrigine dose>; seizures respond mainly
  to immunotherapy."
- **M5 cEEG** (cases with the criterion). "Monitor with continuous EEG for non-convulsive seizures
  while consciousness fluctuates or seizures persist."
- **M6 Level of care.** One of:
  - Case features (any of: GCS 12 or less, central hypoventilation or SpO2 drop, HR above 130 or
    labile BP with diaphoresis, status epilepticus, catatonia with refusal of food/fluids): "Admit
    to the ICU / neurocritical care for <features>, with airway assessment<, cardiac monitoring>."
  - Otherwise: "Admit to a neurology ward with seizure precautions and continuous cardiac
    monitoring."
- **M7 Escalation.** "If there is no meaningful clinical improvement 10 to 14 days after
  first-line therapy, escalate to rituximab (375 mg/m² weekly for 4 doses or 1 g twice 2 weeks
  apart, after hepatitis B screening) and/or cyclophosphamide<; discuss fertility preservation>."
  P cases with severe disease (ICU) may say "consider early escalation".
- **M8 Agitation/catatonia** (where present). "Treat agitation, insomnia and catatonia with
  benzodiazepines (lorazepam) first<; stop <current antipsychotic> and monitor CK and
  temperature>."
- **M9 Hyponatraemia** (Na below 130). "Treat the <moderate|profound> hyponatraemia (<value>
  mmol/L) as SIADH after review of <thiazide/SSRI>: fluid restriction<, hypertonic saline for
  seizures>, correcting by no more than 10 mmol/L in 24 hours."
- **M10 Team.** "Neurology-led care with psychiatry for behavioural management<; gynaecology for
  the teratoma><; urology for the testicular mass><; oncology for <tumour>>." No conditional
  consults for tumours the case has excluded.

Canonical prohibitions (keep P1-P5 in every case, edited as below; add case-specific ones):
- **P1.** "Do not give haloperidol or other high-potency D2 antagonists for agitation: patients
  with anti-NMDAR encephalitis are prone to severe extrapyramidal and neuroleptic-malignant-like
  reactions."
- **P2.** Keep "Do not delay immunotherapy while waiting for the anti-NMDAR antibody result..." as is.
- **P3.** "Do not attribute the presentation to a primary psychiatric disorder while seizures,
  dyskinesias, autonomic instability, an abnormal EEG or CSF inflammation remain unexplained."
  This removes "in a young patient", which is wrong in RM03 and RP01-RP03.
- **P4.** Keep the LP-without-imaging prohibition.
- **P5.** Keep the serum-negative prohibition.

### C10. Drug-interaction tier and content (all 30) [major]
- **Tier (ruling 6).**
  - `required` only where a concrete interaction changes management: P07 (lamotrigine; quetiapine
    and risperidone exposure) and RP02 (lamotrigine, CKD 3, nivolumab).
  - `recommended`: M02 (olanzapine), M04 (quetiapine), RM02 (risperidone), RM03 (citalopram,
    thiazide, hyponatraemia), RS02 (prior valproate).
  - `optional` in all others.
- **Arguments.** `required_arguments: {}` (the stored output answers any drug).
- **Output.** `interactions` lists real pairs between the patient's medicines and aciclovir,
  methylprednisolone, IVIG, levetiracetam and the case's other drugs (examples in section 1.2:
  valproate-lamotrigine, oestrogen COC lowering lamotrigine, SSRIs/thiazides and hyponatraemia,
  QTc with citalopram/quetiapine, aciclovir nephrotoxicity with CKD or NSAIDs, steroid
  hyperglycaemia with diabetes). `contraindications` include haloperidol / D2 antagonists only
  as a class warning. `warnings` include HBV screening before rituximab.
- The output agrees with the patient's allergies and medications and restates no
  expected_evidence, which is case-specific (e.g. "Valproate would raise the lamotrigine level").

### C11. Wrong tool or wrong study for tumour imaging (P02, P03, RM03, RS02, RP02) [major]
- **Problem.**
  - P02 and P03 order a chest-abdomen-pelvis CT through `order_ct_scan` (head and neck only),
    with `contrast_used: false` and an impression that names histology.
  - RM03 (62F) and RS02 (50F) have pelvic ultrasound while their musts call for CT; women 45 or
    older need a carcinoma search.
  - RP02 must says "testicular ultrasound" in a 76-year-old with known lung cancer; RP03 must says
    testicular ultrasound in a 63-year-old.
- **Fix.**
  - Tumour criterion by demography:
    - women 12-44: `pelvis_abdomen_ultrasound`;
    - men under 45: `testicular_ultrasound`;
    - anyone 45 or older: `chest_abdomen_pelvis_CT` with `contrast: true`.
  - The stored report must be that study.
  - Per-case details are in section 4.

### C12. Body-imaging impressions written as lab text (24 cases) [major]
- **Problem.** "Abnormal values: Left ovary ... (H)." and "All values within normal limits." are
  lab templates.
- **Fix.** Rewrite in radiology voice, consistent with `findings`:
  - Abnormal: "1. <Side> ovarian <size> cm complex cystic lesion with <echogenic nodule, posterior
    acoustic shadowing, fat-fluid level>, consistent with a mature cystic teratoma (dermoid).
    2. <Other ovary> and uterus normal. No free fluid beyond physiological."
  - Normal: "Normal pelvic and abdominal ultrasound. Both ovaries normal in size and echotexture;
    no adnexal mass." Male: "Normal scrotal ultrasound. No testicular mass."
- **Characteristic features.** Where the case intends a teratoma (musts plan removal) but the
  finding is vague or non-specific (P01, P04, P06, P07, P08, RM02), give the lesion the
  characteristic features (echogenic Rokitansky nodule, shadowing calcification or fat-fluid
  level). M03 stays equivocal and gets a pelvic MRI (section 4).
- **Modality.** Ultrasound has no "density": S10 "fat density" becomes "echogenic fat-containing
  component".

### C13. Cross-modality and management text in reports (many) [minor]
Strip per the style guide: MRI "correlate with CSF" (P06; one hedged HSV sentence may stay);
EEG "requiring urgent continuous EEG monitoring" becomes "Continuous EEG monitoring
recommended." (P08 also loses "requiring urgent diagnosis"); ECG "likely from agitation and
autonomic instability" (P02, P03, RS01, RP03, RM01, RM02) and "account for a syncopal episode"
(RM03); CSF values "supports intrathecal antibody production" (RS01); CT text listed under RP02.
EEG impressions open "This is an ABNORMAL EEG due to:" with a numbered list; "epileptogenic"
becomes "epileptiform". Do not rewrite structured `findings`.

### C14. Fallback outputs that contradict the case (all 30) [major]
- `fallback_tool_outputs.advanced_imaging` (FDG-PET "No abnormality identified") and
  `.specialized_test` ("neuropsychological_testing", in S10 "Nerve conduction study / EMG") are
  served for EVERY modality or test type of that tool. Delete both (set to null) so the library
  answers per value.
- Fallback `ecg` (M01, M03-M05, P01, P04-P08, S06, S09, S10; rate 58-88) contradicts HR 91-138.
  Replace it with an `initial_tool_outputs.ecg`: sinus tachycardia at the vitals HR, normal
  intervals, no non-cardiac text. No ECG criterion.
- Fallback `cardiac_monitoring` (all 30: Holter, average 68-82) contradicts HR 96-138 and
  documented lability. Rewrite: "Sinus rhythm with episodes of sinus tachycardia to <exam max>
  bpm; no pauses, AV block or sustained arrhythmia", with `heart_rate_range` matching the exam.
  In RM03 (HR 60, orthostatic) match the case.
- Keep fallback echo, CT head and the generic literature fallback.

### C15. Red herrings and key clinical evidence templated or wrong (all 30) [major]
- **Hyponatraemia red herring (26 cases).** Its data_point says "Mild hyponatremia" whatever the
  value: M01 122, S09 124, S06 126, S10 127, RM03 128, M04 and M05 129 are not mild. Use the
  grade of section 1.2. correct_interpretation: "Hyponatraemia occurs in anti-NMDAR encephalitis
  but is more typical of anti-LGI1 encephalitis; it needs its own work-up and correction and does
  not point away from the diagnosis." Remove the red herring where sodium is normal.
- **Prodrome red herring (15 cases).** Keep it only where the HPI has a prodrome; remove it in
  RP02 (no fever, no cough). Its correct_interpretation must not say "should redirect the workup
  to anti-NMDAR antibody testing" after a negative HSV PCR alone. Use: "A viral-like prodrome
  precedes about 70% of anti-NMDAR encephalitis; it does not establish viral encephalitis, which
  CSF PCR addresses."
- **CK red herring.** Write "markedly raised CK" for NMS (not "CK typically >1000") and name
  seizures and dyskinesias as the cause.
- **"Acute psychiatric presentation ... in a previously well young adult".** Rewrite where the
  patient is not young (RM03, RP01-RP03) or has a psychiatric history (P07 bipolar, M01-M03 and
  P01 anxiety).
- **key_clinical_evidence.** The text is identical in all 30 and contains wrong claims ("100%
  sensitive", "highly specific (30-50% sensitivity)", "CT chest/abdomen/pelvis ... mandatory in
  women of reproductive age", "~50% of young women"). Replace with 4-6 case-specific bullets
  built from:
  1. "<onset> of <groups present>, <n> of the six Graus 2016 groups."
  2. "CSF IgG anti-GluN1 positive (titre 1:<x>) on cell-based assay: definite anti-NMDAR
     encephalitis (Graus 2016); serum <positive 1:<y>|negative> is read with the CSF."
  3. "MRI <finding>; MRI is normal or non-specific in about two thirds and excludes HSV
     encephalitis and structural causes."
  4. "EEG <finding>; extreme delta brush, when present, supports but does not establish the
     diagnosis."
  5. "<tumour result and what it means for treatment>."
  6. "Earlier immunotherapy and tumour removal are associated with better outcome (Titulaer 2013)."

### C16. Rationale = label, generic expected evidence (all 30) [minor]
Every criterion's `rationale` repeats its `label`. Write one sentence of clinical reason with the
case anchor. Examples:
- MRI: "Excludes HSV encephalitis, structural lesions and overlapping demyelination before LP; it
  is normal in most patients and does not confirm the diagnosis."
- Tumour: "<Group> carry a <teratoma|carcinoma> risk; tumour removal is part of first-line
  treatment."

Make the tumour criterion's expected_evidence case-specific ("Left ovarian 2.3 cm mature cystic
teratoma" / "No testicular mass").

### C17. Template carry-over in numbers and text [minor]
- Identical values copied across cases:
  - M01-M03 CSF: 12 cells, IgG index 0.72, "2 faint bands".
  - M04 and M05 labs and CSF: Hb 13.1, Hct 40.5, Na 129, CK 148, CRP 0.8, ESR 22; CSF 14 cells,
    IgG index 0.74.
  - S02-S04: left ovarian mass 2.3 cm; ECG 118 bpm.
  - M01 and M02: serum 1:80 / CSF 1:128.
- **Fix.** Keep the lowest-numbered case and change the others to distinct plausible values:
  M05 to male ranges, Hb about 15; S03 and S04 to different lesion sizes. Make each ECG rate the
  vitals HR within ±5.
- Diagnosis leaks in medication indications: M04 quetiapine and M05 zopiclone say "to be
  discontinued given likely autoimmune encephalitis". Write the prescriber's indication only.
- Medication lists that disagree with the HPI: P07 (quetiapine 100 vs 200 mg, risperidone
  missing), RM02 (risperidone started outside, missing), RS02 (valproate status), M05 (ED
  levetiracetam listed as a home medication: move it to the HPI).

### C18. Stop rule and sequence (all 30) [minor]
- `max_additional_actions` becomes 2: room for one repeat or a reasonable extra study, such as an
  ECG.
- Sequence constraints are in section 3.4.

---

## 3. Target pathway and tiers

### 3.1 Order of `action_criteria` and `followup_outputs`
Criteria, in this order (the ids stay):
1. serum labs (`action-4-interpret-labs` or the case's id);
2. brain MRI;
3. CSF;
4. routine EEG;
5. tumour imaging;
6. cEEG;
7. case-specific diagnostic extras (pelvic MRI M03, staging CT and tumour markers P02, SIADH
   osmolalities, MOG/AQP4 where separate);
8. drug interactions;
9. literature (optional).

Follow-ups, in the same order: cEEG, then diagnostic extras (pelvic MRI, staging CT), then DDI,
then literature last. Delete dead or duplicate follow-ups named in section 4.

### 3.2 Tiers and minimal `required_arguments` (verbatim)

| criterion | tier | alternatives (`required_arguments`) |
| --- | --- | --- |
| serum labs | required | A: `panels: [CBC, CMP, TSH, anti_TPO, HIV, NMDAR_IgG_cell_based]`; B: same with `thyroid` instead of `TSH`. Women 12-50 add `beta-hCG` to both. Patients 45 or older (RM03, RS02, RP01-RP03) add `paraneoplastic_panel` and `autoimmune_encephalitis_panel`. RM02, RS02, RS04 add `MOG_IgG_cell_based` and `AQP4_IgG_cell_based` |
| brain MRI | required | `{contrast: true}` |
| CSF | required | A: `special_tests: [HSV_PCR, NMDAR_antibodies, oligoclonal_bands]`; B: `[HSV_PCR, NMDAR_antibodies, IgG_index]`. RP01 adds `RT_QuIC` to both |
| routine EEG | required | `{eeg_type: routine}`, `{eeg_type: video}`, `{eeg_type: continuous_icu}` (a first cEEG satisfies the baseline) |
| tumour imaging | required | women 12-44 `{study: pelvis_abdomen_ultrasound}`; men under 45 `{study: testicular_ultrasound}`; age 45 or more `{study: chest_abdomen_pelvis_CT, contrast: true}` |
| cEEG | recommended (29), none in RP01 | `{eeg_type: continuous_icu}` |
| SIADH work-up (Na below 130: M01, M04, M05, S06, S09, S10, RM03, P08) | recommended | `{panels: [serum_osmolality, urine_osmolality]}`, answered by the initial labs report, which must name both |
| drug interactions | per C10 | `{}` |
| literature | optional | `{}` |

Drop `protocol`, `basic`, `screen_for`, `query` and the exact eleven-panel list. Expected evidence
for the labs criterion: "Serum anti-GluN1 <result>; <sodium>; thyroid and other antibodies
<results>". Do not write "can be false positive or false negative in isolation" as evidence.

### 3.3 Avoided actions
- Keep waste entries for echocardiogram, EMG/NCS, amyloid PET and DaTscan, with these exceptions:
  - RS02: remove EMG/NCS waste if the exam shows flaccid weakness or areflexia (section 4).
  - RM03: amyloid PET stays waste (subacute course with seizures and dyskinesias).
- Do not add harm entries for LP: the prohibition and the sequence constraint cover it.

### 3.4 Sequence constraints (every case)
- `{before: <MRI id>, after: <CSF id>, strength: soft}`. Rationale: "Imaging before LP in a
  patient with seizures or altered consciousness; CT head is an acceptable alternative, so the
  constraint is soft."
- No hard constraint anywhere. Even RP02 (epidermoid with mild compression) already had a CT head
  in the ED.

### 3.5 Stop rule
- `required_before_assessment`: the five required ids.
- `max_additional_actions: 2`.

---

## 4. Per-case index

No case has reviewer notes. Every case gets C1-C10, C13-C16 and C18. The bullets list what is
specific or extra.

### NMDAR-ENC-M01 (28F, moderate)
- Na 122 (profound): red herring "Mild" becomes "Profound hyponatraemia (122 mmol/L)"; add M9 with
  hypertonic saline because of seizures; add the SIADH criterion and osmolalities.
- Sertraline was increased to 100 mg in the HPI but the med list says 50 mg: reconcile to 100 mg.
  Note SSRI-associated SIADH in the differential key features.
- CSF NMDAR pending, 1:128 in labs: C4.
- Initial lit/DDI placeholders: C3. Fallback ECG: C14.
- US: left 1.2 cm lesion with shadowing calcification is a teratoma: M3 removal. Cephalosporin
  allergy: no conflict.

### NMDAR-ENC-M02 (33F)
- Olanzapine 5 mg started 5 days ago, CK 200: stop olanzapine (M8); NMS `low` with values; DDI
  recommended.
- Sertraline: the HPI says it was increased to 100 mg but the list says 50 mg; reconcile.
- US normal: M3 negative-screen text.
- No cEEG follow-up: author one (routine EEG had one brief seizure); criterion recommended.
- C17 against M01: change CSF counts and the titre pair.

### NMDAR-ENC-M03 (25F)
- US "1.2 cm complex echogenic focus ... small dermoid or hemorrhagic cyst" is equivocal. Add a
  recommended criterion `pelvic-MRI-characterisation`, `{study: pelvis_abdomen_MRI}`, with a
  follow-up: a 1.2 cm left ovarian lesion with macroscopic fat on fat-suppressed sequences,
  consistent with a mature cystic teratoma. M3 then says removal. Order it after the ultrasound.
- Initial lit/DDI: C3. Fallback ECG: C14. C17 CSF numbers.

### NMDAR-ENC-M04 (27F, label includes left ovarian teratoma)
- Quetiapine "to be discontinued given likely autoimmune encephalitis" is a diagnosis leak (C17).
  Stop quetiapine (M8). Its red herring "initial symptomatic improvement" is fine.
- Na 129 (moderate): M9 and the SIADH criterion.
- The DDI follow-up `check_quetiapine_nmdar_encephalitis` cites "Expert consensus, Dalmau 2011":
  verify and rewrite in report voice. DDI recommended.
- Red herring "Mild CRP elevation (7 mg/L)" must match the lab value (CRP 0.8 mg/dL = 8 mg/L).
- MRI impression "may represent early limbic encephalitis": allowed as one hedged sentence.
- US impression: C12 (keep the dermoid wording). Fallback ECG: C14.

### NMDAR-ENC-M05 (30M, tumour-negative)
- Zopiclone indication leak and levetiracetam in the med list: C17.
- Testicular US normal. Must "Screen ... testicular ultrasound and contrast-enhanced CT CAP"
  becomes the M3 male-negative text; drop the urology/oncology consult.
- Na 129: M9 and the SIADH criterion. C17: change M05's copied labs and CSF to male ranges.
- Lit follow-ups (second-line, aciclovir) stay optional, last, facts checked (section 1.2).
- Initial DDI leak: C3. Fallback ECG: C14.

### NMDAR-ENC-P01 (22F, puzzle)
- CSF 3 cells, OCB equivocal, MRI near-normal, EEG FIRDA: probable criteria are not met before the
  antibody (fewer than 4 groups). The diagnosis rests on CSF anti-GluN1 1:32 (C4, put in the CSF
  report). Key evidence must say so.
- US lesion vague: make it a characteristic teratoma (C12); M3 removal.
- Initial lit/DDI: C3. Fallback ECG: C14.
- Aspirin allergy: no conflict.

### NMDAR-ENC-P02 (19M, testicular teratoma)
- The CAP CT follow-up is `order_ct_scan`: convert it to `order_body_imaging`,
  `study: chest_abdomen_pelvis_CT`, `contrast: true`, trigger `request_ct_chest_abdomen_pelvis`.
  Impression: "No retroperitoneal or thoracic lymphadenopathy; no pulmonary nodules; known 1.4 cm
  right testicular lesion". Delete "Clinical stage I testicular teratoma" (histology from CT).
- Add recommended `germ-cell-staging-CT` with that study, and recommended `germ-cell-tumour-markers`
  with `{panels: [AFP, beta-hCG, LDH]}`; put the values (normal) in the initial labs.
- M3: "Refer urgently to urology for radical inguinal orchiectomy of the right testicular mass,
  with tumour markers and staging CT, as part of first-line treatment."
- CSF has both pending and Positive: C4 (titre 1:128). The "Serum anti-GluN1" panel holds the CSF
  value; replace it with serum 1:64.
- GCS 12, catatonic posturing (waxy flexibility), seizures on EEG, fever 38.2: M6 ICU, M8
  lorazepam for catatonia, cEEG criterion and follow-up.
- ECG "likely from agitation": C13.

### NMDAR-ENC-P03 (28M, post-HSV)
- Delete FU1 (`order_ct_scan` CAP plus scrotal ultrasound): a CAP CT is not indicated after a
  normal testicular US in a 28-year-old with post-HSV disease, and it is the wrong tool. Delete
  FU2 (comparison MRI): the initial MRI already compares.
- M1 post-HSV text. Valacyclovir is on the med list: the M1 restart replaces it.
- The differential carries "HSV encephalitis relapse": `low` with HSV PCR negative.
- The must "testicular US + CAP CT" becomes M3 male-negative. Drop the urology consult.
- CSF pending and Positive: C4 (1:256). The serum panel holds the CSF value: fix it (serum 1:64).
- cEEG FU3 impression "confirming that the seizures are from a new process": C7.
- Key evidence cites Armangue 2018.

### NMDAR-ENC-P04 (22F)
- CSF NMDAR pending in two keys, and labs "Anti-NMDAR antibody (CSF) 1:10": C4, titre 1:10.
- US "Left ovarian mass identified" has no description: write findings and impression as a
  teratoma (C12); M3 removal.
- Staring episodes with FIRDA: add cEEG criterion and follow-up (show subclinical events or none,
  consistent with routine).
- Penicillin allergy: no conflict. Initial lit: C3. Fallback ECG: C14.

### NMDAR-ENC-P05 (19F, catatonia)
- Waxy flexibility and refusal to eat: M8 catatonia with lorazepam; M6 ICU if the case shows
  dehydration or autonomic instability, otherwise ward.
- US normal: M3 negative.
- Initial lit/DDI: C3. Fallback ECG: C14. CSF pending: C4 (1:16).

### NMDAR-ENC-P06 (30F)
- MRI "should be correlated with CSF analysis": C13.
- HPI "postpartum-equivalent stress" is odd: write "anxiety and stress".
- US left 2.8 cm complex cystic: characteristic features (C12); M3 removal.
- Initial lit/DDI: C3. Fallback ECG: C14. CSF pending: C4 (1:20).

### NMDAR-ENC-P07 (25F, bipolar II)
- On lamotrigine and quetiapine, with risperidone added: DDI `required` (C10). M4 lamotrigine
  clause; M8 stop risperidone and taper quetiapine.
- Med list: quetiapine dose and missing risperidone (C17).
- THC positive "(residual)": check the social history mentions cannabis; if not, add it, or make
  the screen negative.
- Differential adds "bipolar disorder relapse" (`low`, with its key features).
- MRI caudate signal only, no temporal change: fine.
- The DDI follow-up keeps its content in report voice.
- Red herring wording "previously well young adult" is wrong: C15.
- Initial lit: C3. Fallback ECG: C14. CSF pending: C4 (1:32).

### NMDAR-ENC-P08 (38F, Hashimoto)
- Differential adds "Hashimoto encephalopathy / SREAT" (`low`: anti-TPO 128 is non-specific,
  euthyroid, a well-characterised neuronal antibody is present, which Graus 2016 excludes).
- EEG "Continuous EEG monitoring urgently indicated. Findings support severe encephalopathy
  requiring urgent diagnosis": C13. Add cEEG criterion and follow-up (rhythmic right temporal
  theta: show subclinical right temporal seizures).
- Na 130: mild, no M9.
- US right 5.2 cm complex mass: characteristic features (C12); M3 removal.
- HR 119 with diaphoresis and BP lability: M6 by the rule.
- Initial DDI: C3. Fallback ECG: C14. CSF pending: C4 (1:64).

### NMDAR-ENC-RM01 (35F)
- CSF `cell_count` is missing (WBC None). Add a lymphocytic count consistent with OCB 4 bands and
  IgG index 0.82 (e.g. 18 cells/uL, 90% lymphocytes) and update `interpretation`.
- TSH 6.8, anti-TPO 312, anti-Tg 185 on levothyroxine: differential adds SREAT (`low`, as P08).
  The labs report shows TSH high (no hidden interpretation).
- The labs "Serum anti-GluN1" panel holds the CSF value: C4 (serum 1:10).
- Add cEEG criterion and follow-up (one subclinical left temporal seizure on routine).
- Autonomic lability to 130: M6 rule.
- DDI follow-up (levetiracetam): optional; the "valproate contraindicated if pregnant" line
  becomes "avoid in women able to become pregnant".

### NMDAR-ENC-RM02 (23F)
- MRI multifocal white matter and basal ganglia T2 signal with oedema: add MOG-IgG and AQP4-IgG
  (serum, cell-based, Negative) to labs and the labs criterion; differential adds "ADEM / MOG
  antibody-associated disease" (`low` with negative MOG-IgG).
- Risperidone started outside (HPI) but missing from meds (C17): stop it (M8); DDI recommended.
- GCS 12 and intermittent central hypoventilation: M6 ICU.
- Add cEEG criterion and follow-up (two subclinical left temporal seizures).
- US left 2.3 cm cystic-solid with possible calcification: characteristic (C12); M3 removal.
- CSF pending: C4 (1:64).

### NMDAR-ENC-RM03 (62F)
- Age 62: the tumour criterion becomes `chest_abdomen_pelvis_CT` with contrast. Replace the pelvic
  US initial with a CAP CT report (no mass; keep incidental findings plausible for age), or keep
  the US as a follow-up only if you also keep a pelvic criterion (do not).
- The must "FDG-PET if cross-sectional imaging is unrevealing" names an unorderable body PET:
  write "repeat tumour screening during follow-up if the course is refractory".
- Na 128 on co-amilozide (hydrochlorothiazide) and citalopram: M9 with "stop the thiazide";
  differential key features name thiazide and SSRI; SIADH criterion and osmolalities.
- Orthostatic hypotension and syncope: M6 ward with telemetry unless the rule applies.
- ECG "that would account for a syncopal episode": C13.
- Labs criterion adds the onconeural and autoimmune panels (age 45 or more). The CJD
  differential stays `low`. Red herrings: "young adult" wording (C15).
- Penicillin allergy: no conflict.
- Add cEEG criterion and follow-up (one suspicious left temporal event).
- CSF pending: C4 (1:64).

### NMDAR-ENC-RP01 (61M, label "Post-COVID-19 seronegative autoimmune encephalitis") [label decision]
- The label names a different entity than the condition, and the accepted list (filled by the
  condition synonyms) grants "anti-NMDAR encephalitis" for a case whose CSF and serum are
  negative: the scoring key is self-contradictory.
- Decision (lead): recast as anti-NMDAR encephalitis after COVID-19 with a CSF-positive,
  serum-negative result, which is a recognised scenario (Gresa-Arribas 2014) and the criteria
  pack's own red herring.
  - `accepted[0]` becomes "Anti-NMDA receptor encephalitis following COVID-19 (CSF-positive,
    serum-negative)". Do not touch the appended synonyms.
  - CSF `NMDAR_antibodies` becomes "Positive, titre 1:4 (cell-based assay, IgG anti-GluN1)".
    Serum stays Negative.
  - Delete the CSF panel from labs (C4). Delete both `metadata.case_body_concerns` entries: they
    describe the defect now fixed. Log both changes.
  - Keep the normal cell count, absent OCB and near-normal EEG (CSF and EEG can be normal); the
    key evidence must say the diagnosis rests on the CSF assay.
- MRI cortical ribboning with DWI change raises CJD: CSF criterion adds `RT_QuIC`; the CSF report
  gives RT-QuIC negative (and 14-3-3 if present); differential CJD `low` with that evidence.
- CSF glucose ratio 0.40 (serum 168): raise CSF glucose to about 100 mg/dL (ratio 0.6); a low
  ratio is not a feature of the disease.
- Tumour criterion CAP CT (age 61, 20 pack-years). Drop the testicular-US and urology musts.
- No cEEG criterion; author a follow-up without seizures. M6 ward.
- CENTRAL 3 records the label change.

### NMDAR-ENC-RP02 (76M, nivolumab-associated)
- Musts are template-wrong (testicular ultrasound; "levetiracetam or valproate" with lamotrigine
  on board). Add:
  - "Withhold nivolumab and discuss permanent discontinuation with oncology (grade 3-4
    neurological irAE, ASCO 2021)";
  - M2 with ASCO high-dose steroid wording (methylprednisolone 1 g daily for 3 to 5 days, then
    IVIG or plasma exchange if no improvement);
  - aspiration pneumonia treatment compatible with the penicillin rash allergy (a cephalosporin
    is acceptable after a non-severe rash);
  - M1 renally adjusted (creatinine 1.3, age 76: CrCl about 45 mL/min, aciclovir every 12 h);
  - airway protection for GCS 7 (M6 ICU).
- DDI required: lamotrigine-valproate, aciclovir and CKD, levetiracetam renal dosing,
  steroid-nivolumab.
- CSF: glucose 38 mg/dL (ratio 0.35) and lactate 4.1 point to bacterial, mycobacterial or
  carcinomatous meningitis and conflict with the label. Correct the data to glucose about 64
  mg/dL (ratio about 0.6) and delete the CSF lactate. Keep cytology negative and add "Cytology
  (second sample): no malignant cells". Differential adds leptomeningeal carcinomatosis (`low`,
  2 cytologies negative, no leptomeningeal enhancement).
- CSF NMDAR "Positive" without titre: C4 (1:32 from labs).
- The CAP CT impression mentions "ovarian or testicular mass (not applicable)": delete it.
  "In the setting of decreased level of consciousness": C13.
- Red herring "Viral prodrome (URI, fever, cough)": the HPI denies them; delete it (C15).
- Differential: "Checkpoint-inhibitor encephalitis without neuronal antibody" is not separable
  here; CJD `low` (24-h onset).
- Sequence: soft only (CT done in ED).

### NMDAR-ENC-RP03 (63M, post-HSV)
- Tumour CAP CT stays (age 63). The must "testicular ultrasound" and the urology consult go.
  M3: "CT shows no tumour; post-HSV anti-NMDAR encephalitis is not tumour-associated (Armangue
  2018)".
- M1 post-HSV text. Levetiracetam already on board: M4 dose review.
- The labs "Serum anti-GluN1" panel holds the CSF value: C4 (serum 1:10).
- HPI calendar dates "April 2017 / June 2017" become relative ("2 months ago").
- Diabetes (diet): steroid glucose monitoring in M2. CAD on aspirin: no conflict.
- ECG text: C13.

### NMDAR-ENC-RS01 (31F)
- Central hypoventilation needing oxygen, waxy flexibility, 3 seizures: M6 ICU, M8 catatonia.
  Add cEEG criterion and follow-up.
- CSF special-test interpretive values: C13.
- US left 2.8 cm teratoma with fat/calcification: C12 wording; M3 removal.
- The DDI follow-up's valproate line: valproate is "avoided in women able to become pregnant", not
  "contraindicated".
- The lit follow-up "EDB in 30%": correct.

### NMDAR-ENC-RS02 (50F, post-COVID)
- Age 50: tumour criterion CAP CT with contrast; replace the pelvic US report with a CAP CT (no
  mass).
- Labs criterion adds the onconeural and autoimmune panels plus MOG and AQP4 (already in labs,
  Negative), for the dentate, peduncle and corticospinal lesions with restricted diffusion.
- Outside valproate: state in the HPI whether it continues; if so, list it, add normal ammonia and
  valproate level, differential "valproate-associated encephalopathy" (`low`). DDI recommended.
- Quadriparesis, urinary retention: brisk reflexes and extensor plantars need no extra study;
  flaccid, areflexic or a sensory level gets a recommended `spine_MRI` criterion with follow-up
  and loses the EMG/NCS waste entry. Log which.
- Methylprednisolone pulses already given: M2 reads "IVIG or plasma exchange now; repeat
  steroids".
- Add cEEG criterion and follow-up (three behavioural arrests, seizures on EEG). M6 ICU.

### NMDAR-ENC-RS03 (19M)
- GCS 9, recurrent seizures, pH 7.25 and lactate 8.1 after seizures: M6 ICU with airway
  assessment. Add cEEG criterion and follow-up.
- HHV-7 PCR positive in CSF: keep it as a red herring if it is listed in the CSF `special_tests`;
  if it appears only in `interpretation`, add the key. The lit follow-up on HHV-7: keep it
  optional and hedged; delete "molecular mimicry" as established fact.
- The must "testicular US + CAP CT" becomes M3 male-negative.
- Remote COVID 18 months ago: fine.

### NMDAR-ENC-RS04 (40F, optic neuritis)
- Bilateral optic nerve enhancement: labs criterion adds MOG and AQP4 (cell-based); keep them
  Negative. Differential adds "MOG antibody-associated disease / NMOSD overlap" (`low`, negative
  antibodies).
- Musts add "Ophthalmology review with visual acuity and fields"; plasma exchange is preferred
  with steroids for severe optic neuritis (Abboud 2021 discusses PLEX in severe disease; word it
  as "consider early plasma exchange").
- EEG "requiring urgent continuous EEG monitoring": C13. Add cEEG criterion and follow-up.
- US normal: M3 negative.
- MRI "atypical for pure HSV encephalitis given bilateral symmetric involvement": one hedged
  sentence only.

### NMDAR-ENC-S01 (24F)
- Hb 14.2 with Hct 35.4 (L) is inconsistent: set Hct about 42.4 (normal) and update the abnormal
  summary.
- US: right 1.8 cm teratoma, C12 wording ("Abnormal values:" template); M3 removal.
- Two electrographic seizures: add cEEG criterion and follow-up. The EEG limitations line
  "continuous EEG monitoring recommended" is fine.
- Fever 38.4: M1.
- Lit/DDI follow-up placeholders: C3.

### NMDAR-ENC-S02 (31F)
- No hyponatraemia: there is no hyponatraemia red herring; keep the CK red herring.
- Cephalosporin allergy: no conflict.
- Add cEEG criterion and follow-up (three seizures).
- US teratoma: C12; M3 removal.
- C3 placeholders.

### NMDAR-ENC-S03 (19F)
- C17: lesion size distinct from S02's 2.3 cm; ECG rate to the vitals HR (115). Outside sodium
  133 is a prior encounter: fine.
- Add cEEG criterion and follow-up. C3.

### NMDAR-ENC-S04 (27F)
- PMH ovarian cyst 2 years ago is consistent; the US may compare with it.
- C17 lesion size and ECG rate. Add cEEG criterion and follow-up. C3.

### NMDAR-ENC-S06 (27F)
- Na 126 (moderate) with K 3.2: M9, SIADH criterion, potassium replacement in musts.
- MRI "subtle bilateral frontal subcortical changes" and EEG impression are terse: expand within
  modality.
- US 4.5 cm complex cystic mass: characteristic features; M3 removal.
- HR 128, BP 162/98, fever 38.2: M6 rule (ICU).
- Add cEEG criterion and follow-up.
- Fallback ECG: C14. Codeine intolerance: no conflict. C3.

### NMDAR-ENC-S09 (23F)
- Bilateral ovarian teratomas: M3 "laparoscopic removal of both teratomas, ovary-sparing
  cystectomy where feasible". Add prohibition "Do not perform bilateral oophorectomy when
  ovary-sparing resection is feasible."
- The lit follow-up claims "bilateral resection associated with better outcomes" and "~10%
  bilateral": delete unsupported numbers.
- Na 124 (profound): M9 with hypertonic saline for seizures; K 3.0 replacement.
- HR 138, BP 172/108: M6 ICU.
- Prior febrile illness with neck stiffness and no LP 4 weeks ago: fine as history.
- Amoxicillin allergy: no conflict. Fallback ECG: C14. C3 DDI.

### NMDAR-ENC-S10 (29F, 14 months post-partum)
- Timeline: "the newborn disrupting sleep" conflicts with 14 months post-partum and a 1-year-old
  child. Write "the baby".
- State breastfeeding status. Decision: weaned at 12 months. The DDI follow-up on breastfeeding
  then becomes irrelevant: rewrite it as a general interaction check and set the DDI tier to
  optional. Its lactation advice ("pump and discard 24 h") is unsupported: delete it.
- CSF 1:56 becomes 1:64 (C4).
- US "fat density" (C12). Growing right 5.8 cm dermoid: M3 removal.
- Na 127 (moderate): M9 and the SIADH criterion.
- LMP 6 weeks ago: beta-hCG negative is present; keep it.
- Fallback `specialized_test` "Nerve conduction study / EMG": delete (C14). Fallback ECG: C14.
  Initial lit/DDI: C3.

---

## 5. CENTRAL requests

1. **Citation registry.** Add keys `[Titulaer_late_2013]`, `[Gresa-Arribas_2014]`, `[Abboud_2021]`,
   `[Dalmau_2019]`, `[Lejuste_2016]`, `[Armangue_2018]`, `[Venkatesan_2013]`, `[Solomon_2012]`,
   `[Herman_2015]`, `[Spasovski_2014]`, `[ASCO_irAE_2021]`, `[Graus_2021]` to the NMDAR-ENC
   allow-list (criteria pack section 8).
2. **Non-schema keys in criteria (dataset-wide).** `analyze_csf.basic` (63 case files) and
   `check_drug_interactions.screen_for` are not schema parameters, and `pattern_matches` fails
   when a key is absent, so schema-conformant agents fail these criteria while `perfect_agent.py`
   passes by replaying ground truth. Request: strip annotation keys before matching, or a test
   that rejects non-schema criterion keys. The tool contract's `ANNOTATION_KEYS` allow-list in
   `validate_cases.py` no longer exists.
3. **Label change RP01.** `accepted[0]` becomes "Anti-NMDA receptor encephalitis following COVID-19
   (CSF-positive, serum-negative)". The existing G04.81 and G04.81+nmdar synonyms then fit.
   Rerun `apply_diagnosis_synonyms.py`.
4. **Fallback library and case fallbacks.**
   - A case fallback for `order_advanced_imaging` or `order_specialized_test` is served for every
     modality or test type, whatever modality it names. Request a validator rule: a case fallback
     for a catchall tool must not carry a specific `modality`/`test_type`, or must be resolved by
     it.
   - The library's normal reports for alternative studies (pelvic MRI or CT when the pathway holds
     an ultrasound) can contradict the pathway; worth a note in the tool contract.
5. **Literature criterion matching.** `query` is matched by string equality, so any
   query-specific literature criterion is unreachable. Request a test that flags `query` in
   `required_arguments`.
6. **Criteria pack NMDAR-ENC.md.** Update it:
   - "Probable = clinical features + abnormal CSF or MRI suggestive" is wrong (section 1.2);
   - "EDB 30-50%" becomes 30%;
   - `check_drug_interactions` and `search_medical_literature` are listed as "Required";
   - the tumour line says CT CAP "OR transvaginal ultrasound ... all women".
   Align it with this plan and the July tool review.
7. **Difficulty field (FYI).** All S and RS cases are `moderate` with `expected_agent_confidence`
   0.80-0.85 (the generator's "straightforward" value). Not edited; a dataset-wide decision.

## 6. Open questions for Andrea

- **RP01 (decided, flagged for veto).** I recast RP01 as a CSF-positive, serum-negative
  anti-NMDAR case instead of leaving a seronegative autoimmune encephalitis inside the NMDAR
  condition, where the accepted synonyms reward the wrong answer.
  - Revert path: keep the case seronegative, ask CENTRAL for `except_cases: [NMDAR-ENC-RP01]` on
    the `G04.81+nmdar` synonyms, and accept that the condition then holds 29 anti-NMDAR cases.
  - Only you can say whether a seronegative mimic was intended for this condition. Nothing else
    needs your input.
