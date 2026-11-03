# FTD round plan (October 2026)

Lead plan for the 30 FTD cases: M01-M10, P01-P08, S01-S12. There is no R-series. Written 24 Oct 2026 from a scripted survey of all 30 cases and a full read of M01, M05, P08, S11 and S12, plus the class sweeps for every other case.

**Reviewer notes.** `data/review/round-2026-10/notes/` holds no FTD file. No reviewer note ids apply. Every finding below is a lead finding, so each case log records it under "Own findings". The binding clinician input for FTD is Reviewer 1's July 2026 tool rulings in `condition_tool_guidance.yaml` under `ftd:` (all "applied"). This plan keeps them unless a section says otherwise and gives the reason.

How to use this plan:

1. Read sections 1 to 3 once, then work case by case from section 4.
2. Edit only through `case_io` load/save. After each case, run `perfect_agent` and `case_io.py check`. Before closing, run `test_case_guards`.
3. Write each log to `data/review/round-2026-10/logs/{CASE_ID}.md` in the ROUND_POLICY format:
   - Reviewer notes table: "none".
   - Own findings table: dim A-E, severity, field path, finding, FIXED or FLAGGED.
   - Changes paragraph.
   - CENTRAL.
   - Open questions.
4. Never change `case_id`, `condition`, `accepted[0]` or `icd_codes[0]`. Never hand-edit synonyms; list them under CENTRAL.
5. New text is in English, in the case's own spelling (most cases mix "Behavioral" in the label with "behavioural" in prose; keep each field's existing spelling) and has no em dashes.
6. Keep `criterion_id`s when re-ordering. Treatment is never a tool call.

Baseline on 24 Oct 2026:

- `perfect_agent` passes 30/30. This is false comfort: it replays each criterion's own arguments and never exercises a declared alternative or a library answer.
- `test_case_guards` fails 7 cases:
  - leak test: M01, M05, P03, P07, S01 and S11 (the literature output repeats `expected_evidence`);
  - index-order hijack: M03 (the literature criterion is answered by the repeat follow-up `wernicke_korsakoff_final_exclusion`).

All 7 must pass at close-out.

---

## 1. Governing guidelines and canonical facts

### 1.1 Citation keys

Use one bracketed key per source, for example `["[Rascovsky_2011]","[NICE_NG97]"]`. Never add a bare duplicate (`"Rascovsky_2011"`) or free text. Keys marked NEW are CENTRAL requests (section 5) and may be used in the round now, as other plans do.

| Key | Source | Use for |
|---|---|---|
| `[Rascovsky_2011]` | Rascovsky K et al. Brain 2011;134:2456-2477 (FTDC bvFTD criteria) | bvFTD diagnosis, levels of certainty |
| `[Gorno_Tempini_2011]` | Gorno-Tempini ML et al. Neurology 2011;76:1006-1014 | PPA and its variants (S11, S12) |
| `[Foster_2007]` | Foster NL et al. Brain 2007;130:2616-2635 | FDG-PET in FTD versus AD |
| `[Pottier_2016]` | Pottier C et al. J Neurochem 2016;138 Suppl 1:32-53 | FTD genetics (C9orf72, GRN, MAPT) |
| `[Bang_2015]` | Bang J, Spina S, Miller BL. Lancet 2015;386:1672-1682 | FTD overview and management |
| `[NICE_NG97]` | NICE NG97, Dementia, 2018 | Baseline blood tests; FDG-PET or perfusion SPECT when the subtype is uncertain; no cholinesterase inhibitor or memantine in FTD |
| `[SNLG_ISS_2024]` NEW | Istituto Superiore di Sanità, SNLG guideline on diagnosis and treatment of dementia and MCI (2024) | Reviewer 1's source for the lab panel |
| `[Ducharme_2020]` NEW | Ducharme S et al. Brain 2020;143:1632-1650 | bvFTD versus primary psychiatric disorder (M05, P02, P03, P07, M09) |
| `[Frisoni_2024]` NEW | Frisoni GB et al. Lancet Neurol 2024;23:302-312 | Biomarker choice: CSF AD markers, amyloid PET, FDG-PET |
| `[Amyloid_PET_AUC_2025]` | Rabinovici GD et al., amyloid PET appropriate use criteria 2025 (already used in ALZ-EARLY) | Amyloid PET when AD stays in the differential |
| `[Strong_2017]` NEW | Strong MJ et al. Amyotroph Lateral Scler Frontotemporal Degener 2017;18:153-174 | ALS-FTSD (P08) |
| `[Boxer_2013]` NEW | Boxer AL et al. Lancet Neurol 2013;12:149-156 | Memantine RCT in FTD: no benefit |
| `[ACMG_NSGC_2011]` | ACMG/NSGC practice guideline on genetic counselling and testing for AD and FTD (Goldman 2011) | Counselling before testing; predictive testing of relatives |
| `[EAN_ALS_2024]`, `[NICE_NG42]`, `[AAN_2009]`, `[Gold_Coast_2020]` | As in plans/ALS.md | P08 motor neuron disease work-up and respiratory care |
| `[Ulugut_2020]` NEW, optional | Ulugut Erkoyun H et al. Brain 2020;143:2831-2843 | Right temporal variant (M10) |

Retire these citations:

- `[AAN_dementia_2018]`. It is the Petersen 2018 MCI guideline and does not govern FTD labs or sequencing. Replace it with `[NICE_NG97]` (labs, imaging) or `[SNLG_ISS_2024]` (labs).
- The trazodone citation "Lebert et al., J Neurol Neurosurg Psychiatry 2004" (S02, S04 literature). The trial is Lebert F et al., Dement Geriatr Cogn Disord 2004;17:355-359. Literature outputs are being rewritten anyway (C1); do not carry the wrong journal into new text.

### 1.2 Canonical facts

1. **bvFTD (Rascovsky 2011).**
   - Possible bvFTD needs a progressive deterioration of behaviour or cognition and at least 3 of 6 features:
     - early disinhibition;
     - early apathy or inertia;
     - early loss of sympathy or empathy;
     - perseverative, stereotyped or compulsive behaviour;
     - hyperorality or dietary change;
     - an executive-predominant neuropsychological profile with relative sparing of memory and visuospatial function.
   - Probable bvFTD adds significant functional decline and imaging consistent with bvFTD: frontal and/or anterior temporal atrophy on MRI or CT, or frontal and/or anterior temporal hypoperfusion or hypometabolism on SPECT or PET.
   - Definite bvFTD needs histopathology or a known pathogenic mutation.
   - Exclusions: a better non-degenerative or medical explanation, a better psychiatric explanation, or biomarkers strongly indicating AD or another neurodegenerative process.
   - "Early" means within the first 3 years.
2. **PPA (Gorno-Tempini 2011).** Language is the most prominent deficit and the main cause of impaired daily living.
   - svPPA requires both of:
     - impaired confrontation naming;
     - impaired single-word comprehension.
   - svPPA also requires at least 3 of:
     - impaired object knowledge;
     - surface dyslexia or dysgraphia;
     - spared repetition;
     - spared speech production.
   - Imaging support for svPPA: anterior temporal atrophy or hypometabolism.
   - nfvPPA requires at least one of:
     - agrammatism;
     - effortful, halting speech with inconsistent speech sound errors (apraxia of speech).
   - nfvPPA also requires at least 2 of:
     - impaired comprehension of syntactically complex sentences;
     - spared single-word comprehension;
     - spared object knowledge.
   - Imaging support for nfvPPA: left posterior fronto-insular atrophy or hypometabolism.
   - PPA variants are not scored against the Rascovsky features.
3. **Reversible-cause blood tests (NICE NG97 1.2; SNLG/ISS).**
   - FBC, ESR or CRP, urea and electrolytes, calcium, HbA1c, liver function tests, thyroid function, B12 and folate.
   - Reviewer 1's required set in vocabulary terms is `CBC, CMP, TSH, B12, folate, ESR, CRP`. CMP carries the electrolytes, renal and liver function, calcium and glucose.
   - Syphilis and HIV serology, copper or ceruloplasmin, heavy metals, autoimmune antibodies and toxicology are targeted extras. They are served only when a criterion orders them or the history gives the indication.
4. **Structural imaging.**
   - MRI brain without contrast, dementia protocol, is the standard. Coronal T1 shows frontal and anterior temporal atrophy; FLAIR grades vascular load.
   - Gadolinium adds nothing to a degenerative work-up.
   - CT is the alternative only when MRI is not possible (S06) or as the first emergency study (M09).
   - A normal or near-normal MRI early in bvFTD is common, especially with C9orf72.
5. **Functional imaging (NICE NG97; Foster 2007; Frisoni 2024).**
   - FDG-PET, or perfusion SPECT where FDG-PET is unavailable, helps when the subtype is uncertain.
   - The FTD pattern is frontal and anterior temporal hypometabolism with relative sparing of posterior cingulate, precuneus and parietal cortex.
   - Functional imaging is optional when the clinical and structural picture already gives probable bvFTD. It is the only route to "probable" when the MRI is normal (Reviewer 1: optional; see C7 and Q2).
6. **AD biomarkers.**
   - CSF Abeta42/p-tau or amyloid PET is optional. Use it when AD stays in the differential: amnestic or posterior features, older onset, a mixed picture, an AD family history.
   - A negative result makes Alzheimer pathology unlikely. It does not exclude FTLD or any other neurodegeneration.
   - APOE genotype does not diagnose AD.
7. **Genetics (Pottier 2016; ACMG/NSGC 2011).**
   - C9orf72 expansion, GRN and MAPT account for most familial FTD.
   - Offer genetic counselling before testing. Testing is optional and is indicated by young onset, a family history of FTD, ALS or early dementia, or an FTD-MND phenotype.
   - Predictive testing of relatives follows counselling. It is deferred in minors.
   - Plasma progranulin is a screen for GRN haploinsufficiency. It is not needed in a known GRN carrier.
8. **Treatment.**
   - No disease-modifying therapy exists.
   - SSRIs (sertraline, citalopram) and trazodone have modest evidence for disinhibition, compulsions and agitation.
   - NICE NG97 advises against cholinesterase inhibitors and memantine in FTD. Memantine failed in an RCT (Boxer 2013). Cholinesterase inhibitors may worsen behaviour.
   - Antipsychotics are a last resort for dangerous agitation, given the cerebrovascular and mortality risk in dementia.
   - Benzodiazepines risk falls and paradoxical disinhibition.
9. **Safety and capacity.** These are management, not tool calls:
   - driving;
   - finances and fiduciary roles;
   - firearms;
   - work;
   - lasting power of attorney;
   - caregiver support and respite.
10. **FTD-MND (Strong 2017).**
    - ALS-FTD is ALS by Gold Coast criteria plus bvFTD or PPA.
    - EMG is required to establish lower motor neuron involvement.
    - Respiratory function is staging: recommended, never required, as in plans/ALS.md. AAN 2009 NIV markers are FVC below 50%, SNIP below 40 cmH2O, MIP weaker than -60 cmH2O, orthopnoea, or abnormal nocturnal oximetry.
    - Riluzole and MND multidisciplinary care are management.
11. **Psychiatric mimics (Ducharme 2020).**
    - New behavioural change after 40 to 45 with progressive functional decline is not explained by a prior, stable psychiatric illness.
    - Lithium toxicity (level above the 0.4-1.0 mmol/L range) and valproate toxicity (encephalopathy with or without hyperammonaemia, valproate-induced parkinsonism and cognitive decline) are reversible mimics. They are checked with `interpret_labs` (`lithium_level` with creatinine and TSH; `valproate_level` and `ammonia`), not with a drug-interaction check.

---

## 2. Error classes

Each class gives what is wrong, the cases it covers, the fix and the canonical text. Cases cited are those confirmed by the survey. Treat every class as covering all 30 cases: re-check each case even where it is not listed (memory note: blanket-sweep defects are classes, not instances).

### C1. Literature search is required, echoes the answer, or carries management essays

**Covers 30/30.**

- Required in: M02, M03, M04, M06, M07, M08, M09, M10, P01, P02, P04, P05, P06, P08, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12.
- Recommended in: M01, M05, P03, P07, S01.
- The initial output has the verbatim echo "Confirms Rascovsky 2011 criteria, FDG-PET evidence (Foster 2007), and management approach (Bang 2015)" in most cases. That is the leak that fails 6 guards.
- Some summaries are empty: P04, P06, P08, S07, S11, and the M06 follow-ups.
- Follow-ups are essays on management, capacity, litigation, firearms, driving or adolescent predictive testing. Their key findings state the case's own conclusion (M04, P02, P05, P06, S06, S08, S09, S10 and others).
- M03 has a repeat follow-up, `wernicke_korsakoff_final_exclusion`, that captures the criterion (index-order hijack).
- Literature ids sit inside `stop_rule.required_before_assessment` wherever the criterion is required.

**Fix.**

1. Set every literature criterion to `optional`, or delete it when the case gains nothing from it. Default: keep it, optional.
2. Move the literature criterion last in `action_criteria` and remove its id from `required_before_assessment`.
3. Rewrite `initial_tool_outputs.literature_search` to the canonical general text for the case's syndrome (below). It must contain no case finding and no phrase from `expected_evidence`, `key_clinical_evidence` or the musts.
4. Delete follow-ups whose content is a management or ethics essay (capacity, litigation, firearms, driving, adolescent testing, judicial disclosure, diabetes optimisation, "vascular contribution"). Keep at most one follow-up, and only when it answers a distinct clinical question with general literature. Example: M07, alcohol-related cognitive impairment versus bvFTD.
5. M03: delete `wernicke_korsakoff_final_exclusion`, or merge it into the single literature output, so the criterion is served by the initial output.
6. Use citations `["[Rascovsky_2011]","[Bang_2015]"]`, plus the syndrome key.
7. Re-run the leak guard on each case.

**Canonical literature output, bvFTD (all bvFTD cases):**

> summary: "Rascovsky and colleagues (2011) define possible behavioural variant FTD by three of six behavioural and cognitive features, probable bvFTD by added functional decline and frontal or anterior temporal involvement on structural or functional imaging, and definite bvFTD by histopathology or a pathogenic mutation. Psychiatric disorders are the main mimics and are excluded on course and examination rather than on a single test. Treatment is supportive: SSRIs or trazodone for behaviour, caregiver support and safety planning; cholinesterase inhibitors and memantine are not recommended."
> key_findings:
> - "Three of six core features within the first three years define possible bvFTD."
> - "Probable bvFTD requires functional decline and supportive imaging."
> - "Primary psychiatric disorders are the commonest misdiagnosis."
> - "No disease-modifying treatment is available."

Syndrome variants. Replace the middle sentence and one key finding, nothing else:

- **Familial / genetic** (M02, M04, P01, P02, P03, P04, P05, P07, S03, S05, S07, S10): "C9orf72 expansions and GRN and MAPT variants cause most familial FTD; counselling precedes any genetic test and any predictive testing of relatives." Add `[Pottier_2016]`.
- **AD versus FTD** (M04, P06): "FDG-PET with frontal and anterior temporal hypometabolism and posterior cingulate sparing favours FTD; amyloid PET or CSF AD markers help when Alzheimer disease remains possible." Add `[Foster_2007]`, `[Frisoni_2024]`.
- **Psychiatric mimic** (M05, P02, P03, P07, M09): "New behavioural change in mid-life with progressive functional decline should prompt a neurodegenerative work-up even in a person with a psychiatric history." Add `[Ducharme_2020]`.
- **FTD-MND** (P08): "Up to about 15% of people with bvFTD develop motor neuron disease, most often with a C9orf72 expansion; electromyography establishes lower motor neuron involvement." Add `[Strong_2017]`.
- **svPPA** (S11): summary "Gorno-Tempini and colleagues (2011) define semantic variant PPA by impaired confrontation naming and single-word comprehension with at least three of impaired object knowledge, surface dyslexia or dysgraphia, spared repetition and spared speech production; imaging support is anterior temporal atrophy or hypometabolism." Citation `[Gorno_Tempini_2011]`.
- **nfvPPA** (S12): summary "... define non-fluent/agrammatic PPA by agrammatism or apraxia of speech with at least two of impaired syntactic comprehension, spared single-word comprehension and spared object knowledge; imaging support is left posterior fronto-insular atrophy or hypometabolism. Progressive supranuclear palsy and corticobasal degeneration are common underlying pathologies." Citation `[Gorno_Tempini_2011]`.

For PPA variants, key findings are 3-4 general statements built from the summary. Do not mention "surface dyslexia on irregular words" with an example word used in the case.

### C2. `check_drug_interactions` outputs are wrong, and the tool is misused

**Covers 30/30 via the fallback, and 13 cases via criteria or follow-ups.** Every case has `check_drug_interactions` reachable (a case fallback in 13; follow-ups in S02, S04, S06, S08, S09, M01, M03, M07, P06 and others). Criteria exist in M01, M05, M08, P01, P03, P04, S01, S02 and S09. The outputs:

- put a doctor's plan in `proposed`, with doses ("Sertraline 50 mg", "levodopa continuation", "lipid-lowering therapy");
- list cholinesterase inhibitors as "CONTRAINDICATED" when nobody proposed one;
- give surveillance advice ("Monitor for ALS features annually (EMG)");
- in M08, state a cobicistat interaction for Biktarvy. Biktarvy is bictegravir, emtricitabine and tenofovir alafenamide, with no cobicistat; its relevant interactions are polyvalent cations, metformin and strong inducers.

Three criteria use the tool as a toxicity test, which it cannot do:

- P01 valproate, required;
- M05 lithium, required;
- P04 levodopa, required.

**Fix.**

1. A drug-check criterion stays only if there is a concrete interaction between the medication list and a drug the case would plausibly start. It is `optional` unless the interaction changes management, then `recommended`. It is never required in FTD.
2. Toxicity questions move to `interpret_labs`:
   - M05: `lithium_level`. Creatinine and TSH are already in CMP/TSH.
   - P01: `valproate_level`, `ammonia`.
3. Order: drug-check criteria sit after the diagnostic criteria and before literature.
4. Rewrite outputs to the tool's format:
   - `proposed` names the agent requested, without a dose;
   - `interactions` are pairs with the actual medication list;
   - `contraindications` are true drug-disease or allergy contraindications for that agent;
   - `warnings` hold class warnings for that agent only.
   - No surveillance, genetics or ChEI text unless the proposed agent is a ChEI.
5. Delete every `fallback_tool_outputs.drug_interactions` that reads "proposed: (agent not specified on this case's pathway)" (13 cases). Delete drug-check follow-ups with no criterion, unless they answer a plausible agent with correct content.

**Canonical sertraline output** (adapt `interactions` to the case's list):

> {"proposed": "Sertraline", "interactions": ["Sertraline + aspirin: additive bleeding risk; consider gastroprotection"], "contraindications": ["Concurrent MAO inhibitor"], "warnings": ["Hyponatraemia risk in older adults; check sodium after starting", "QT prolongation is minimal at standard doses"]}

Interaction lines to use when the drug is on the list:

- NSAID or aspirin: bleeding.
- Thiazide: hyponatraemia.
- Lithium: serotonin toxicity (rare) and hyponatraemia.
- Tramadol or triptan: serotonin toxicity.
- Metformin: "no clinically significant interaction". Do not claim glycaemic effects as an interaction.
- Levothyroxine: "no clinically significant interaction".
- Methotrexate (P03, escitalopram): "no clinically significant pharmacokinetic interaction; methotrexate itself needs no change".

### C3. The clinical-assessment output is auto-generated and contradicts the history

**Covers 30/30.** `initial_tool_outputs.clinical_assessment` has these defects:

- Domain findings are sentence fragments cut at 70 characters and attached to the wrong feature. Examples: S11 "There is no personality change, no disinhibition..." filed as evidence FOR disinhibition, apathy and perseveration; P04 "She describes behaviors that preceded their marriage..." for a man.
- "Bedside cognitive testing" is duplicated.
- `criteria_met` contradicts the history:
  - M01: apathy and hyperorality false though present.
  - P01, P03, P07, S02, S04, S06, S10, S12: informant false although an informant gives the history (S04: the daughter is the historian).
  - Empathy false in most S-cases despite documented loss.
  - S11 and S12 mark 5 of 6 Rascovsky features in PPA patients with none.
  - M06 marks one feature while the label says probable.
- The template impression in all 30 reads "The diagnosis is behavioural and is made on this assessment; imaging supports it ... Memory and visuospatial function are relatively spared ...". It references imaging the agent has not ordered. It is false in S04 (MMSE 20, impaired recall and clock) and S01 (clock severely abnormal), and wrong for PPA.

**Fix.** Rebuild the output from the case's own history and examination:

1. One finding per Rascovsky feature, in the order of 1.2 item 1. Each finding is a short paraphrase from the HPI or exam, with `present` or `absent`. If the feature is absent, write the absence, for example "No change in diet or eating reported by the wife."
2. One informant line.
3. One bedside screen line with the real score and its lost domains.
4. One functional-decline line.
5. `criteria_met` keys must agree with the findings. `three_or_more_features_for_possible_bvFTD` follows the count.
6. Impression: canonical text, no imaging, no essay.
7. Use `assessment_type: cognitive_screen` (unchanged).

**Canonical bvFTD impression:**

> "{N} of the 6 Rascovsky features are present on informant history and examination ({list}), with {documented / no documented} decline in daily function. This meets possible bvFTD; imaging and neuropsychological testing decide whether it is probable. {Memory and visuospatial function are relatively preserved on the bedside screen. | Memory and visuospatial items are also impaired on the bedside screen, which keeps Alzheimer disease in the differential.}"

**PPA cases (S11, S12).**

- Replace the Rascovsky keys with Gorno-Tempini keys.
- S11 keys:
  - `impaired_confrontation_naming`
  - `impaired_single_word_comprehension`
  - `impaired_object_knowledge`
  - `surface_dyslexia_or_dysgraphia`
  - `spared_repetition`
  - `spared_speech_production`
  - `language_most_prominent_deficit`
  - `informant_history_obtained`
- S12 keys:
  - `agrammatism`
  - `apraxia_of_speech`
  - `impaired_complex_syntax_comprehension`
  - `spared_single_word_comprehension`
  - `spared_object_knowledge`
  - `language_most_prominent_deficit`
  - `informant_history_obtained`
- Behavioural features are stated once, as absent.
- **Canonical PPA impression:** "Language is the dominant and earliest deficit, with {core features}. This meets the clinical criteria for {semantic / non-fluent agrammatic} variant primary progressive aphasia (Gorno-Tempini 2011); behaviour and episodic memory are preserved."

Check whether the schema validates `criteria_met` key names (`case_io.py check`). If the keys are fixed by the schema, keep the Rascovsky keys for S11/S12, set all six features false, and put the Gorno-Tempini features in the findings. Log which way was taken.

### C4. Criterion text is templated

**Covers 30/30.**

- `rationale` equals `label` everywhere.
- S11 and S12 carry the Rascovsky label on the clinical-assessment criterion.
- The labs label says "... RPR/HIV per risk" while `required_arguments` do not include them.
- Citations are duplicated, as `"[Rascovsky_2011]","Rascovsky_2011"`, plus free text.
- `[AAN_dementia_2018]` is cited for labs, MRI and sequencing.

**Fix.**

1. Write a rationale that says why the step matters in this case (one sentence, at most about 30 words).
2. Change the labels to the canonical texts below.
3. Use bracketed keys only; replace `[AAN_dementia_2018]` per 1.1.

Canonical labels and rationales. Rationales may be tailored, but must not presume a result:

| Criterion | Label | Rationale (default) | Citations |
|---|---|---|---|
| clinical assessment (bvFTD) | "Structured informant history and bedside cognitive screen scored against the Rascovsky features" | "The diagnosis of bvFTD rests on the behavioural features obtained from an informant; the screen documents the cognitive profile." | `[Rascovsky_2011]` |
| clinical assessment (PPA) | "Structured language history and bedside screen scored against the Gorno-Tempini PPA features" | "The PPA variant is defined by which language features are impaired and which are spared." | `[Gorno_Tempini_2011]` |
| neuropsych battery | "Neuropsychological battery including executive and social-cognition measures" | "Quantifies the executive and social-cognition profile and the relative sparing of memory and visuospatial function." | `[Rascovsky_2011]` |
| labs | "Reversible-cause blood tests: CBC, CMP, TSH, B12, folate, ESR, CRP" | "Excludes metabolic, endocrine, nutritional and inflammatory contributors before attributing decline to neurodegeneration." | `[NICE_NG97]`, `[SNLG_ISS_2024]` |
| MRI | "MRI brain without contrast, dementia protocol" | "Shows the frontal and anterior temporal atrophy pattern and excludes structural and vascular causes." | `[Rascovsky_2011]`, `[NICE_NG97]` |
| FDG-PET | "FDG-PET when the structural picture is unresolved" | "Frontal and anterior temporal hypometabolism with posterior sparing supports FTD over AD." | `[Foster_2007]`, `[NICE_NG97]` |
| genetics | "Genetic counselling and FTD gene panel (C9orf72, GRN, MAPT)" | case-specific indication (family history / young onset / MND) | `[Pottier_2016]`, `[ACMG_NSGC_2011]` |
| amyloid PET / CSF AD markers | "AD biomarker (amyloid PET or CSF Abeta42/p-tau) when AD remains in the differential" | case-specific | `[Frisoni_2024]`, `[Amyloid_PET_AUC_2025]` |

### C5. Lab outputs are incomplete, padded and carry an engineering leak

**Covers 30/30.**

- Folate is missing in 21 cases, calcium in nearly all; LFTs, albumin and platelets are often missing.
- Copper, ceruloplasmin and heavy metals appear unrequested in most cases. P02 also has autoimmune antibodies and M04 anti-TPO.
- The panel name `Reviewed_FTD_panel_additions` appears in 28 cases.
- Panels are misgrouped (RPR/HIV under "Vitamins").
- M06 reports CSF NfL as a blood test.

**Fix.** Rebuild `initial_tool_outputs.labs` with these panels:

- Haematology: Hb, WBC, platelets, MCV.
- Inflammatory: ESR, CRP.
- Chemistry: sodium, potassium, urea, creatinine/eGFR, glucose, calcium (adjusted), ALT, AST, ALP, bilirubin, albumin.
- Thyroid: TSH, plus free T4 only if TSH is abnormal.
- Vitamins: B12, folate.

Rules for the rebuilt labs:

1. Keep every existing case-specific value and abnormality that the case depends on, such as the M05 lithium-related creatinine and eGFR, or the S01 glucose 112 red herring.
2. Add the missing analytes with values consistent with the case: diabetic patients' glucose, CKD creatinine, and so on.
3. Extras appear in a separately named panel only when a criterion or follow-up orders them:
   - `ammonia`, `valproate_level` in P01;
   - `lithium_level` in M05;
   - HIV and CD4 in M08;
   - tox screen, BAL and ammonia in M09;
   - CK in P08;
   - `plasma_progranulin` as its own follow-up in P02.
4. Move unrequested extras to keyed follow-ups if they are clinically plausible orders (syphilis serology, copper). Otherwise delete them.
5. Delete the `Reviewed_FTD_panel_additions` panel name.
6. M06: remove CSF NfL from the labs.

Also apply the "first-order rule": `initial_tool_outputs.labs` answers the first labs order of any kind. That includes a targeted first order (P02 `plasma_progranulin`, M05 `lithium_level`). So every targeted panel must also exist as a keyed follow-up matched on its panel tokens. Verify this by calling the MockServer with the targeted order first.

### C6. Fallbacks contradict the case

| Fallback | Cases | Fix |
|---|---|---|
| `fallback_tool_outputs.advanced_imaging`, modality "advanced imaging (off-pathway)", "No abnormality" | 30/30 | Delete it. It answers FDG-PET, amyloid PET and DaTscan alike, without the discriminator guard. Let keyed follow-ups and the library answer by modality. |
| `fallback_tool_outputs.drug_interactions` "agent not specified" | 13 | Delete (C2). |
| `fallback_tool_outputs.ct` normal | 27 | Replace with a CT that shows the case's atrophy pattern at CT resolution (canonical below). S04: remove the calcified granuloma that the MRI does not show. |
| Library `perfusion_SPECT` (normal) answering an FTD patient | 30 | Every case with an FDG-PET criterion gets `perfusion_SPECT` as a declared alternative in that criterion, with a keyed follow-up whose pattern matches the FDG result. S12 (SPECT criterion) gets `FDG_PET` as an alternative and an FDG follow-up. |
| Library `amyloid_PET` / CSF AD markers normal | where not authored | Acceptable: a negative amyloid study is the expected result in FTD. Check that no case text contradicts it. |
| `fallback_tool_outputs.eeg`, `ecg`, `echo`, `cardiac_monitoring` | most | Keep them normal and short. They are waste-tier and must not carry interpretive essays. |

Canonical CT fallback: "Non-contrast CT head: {bifrontal / left anterior temporal / ...} volume loss with widened sulci and enlarged frontal horns, out of proportion to age. No haemorrhage, mass, hydrocephalus or established infarct. CT is insensitive to early or subtle atrophy; MRI characterises the pattern better."

### C7. Functional-imaging tier

- FDG-PET is `optional` in 29 cases. S12 has perfusion SPECT optional.
- In P01 and P05 the MRI is normal or near normal. In P02 and P07 it is borderline.
- Without functional imaging these cases meet only possible bvFTD, while the label says probable.
- Several FDG follow-ups carry `recommended_actions` such as "Amyloid PET" or "Genetic testing".
- The S12 SPECT report says "FDG uptake".

**Fix.**

1. Raise FDG-PET to `recommended` in P01, P05, P02 and P07. Alternative: `perfusion_SPECT`. Rationale: "With a normal or equivocal MRI, functional imaging is the imaging support that probable bvFTD requires." Flag this as Q2 (it departs from Reviewer 1's "optional").
2. M09: keep FDG-PET optional. The MRI follow-up shows atrophy.
3. Keep optional elsewhere.
4. Strip `recommended_actions` from FDG outputs unless the result itself calls for the action.
5. In S12, change "FDG uptake" to "perfusion" in the SPECT report.

### C8. Red herring "mild bilateral upper-extremity rigidity" copied across cases

**Covers S01-S10 and M-cases where present.**

- The same exam line, the same red-herring entry ("common in advanced bvFTD ... does not warrant DaTscan") and a KCE line are pasted into S02-S10.
- In several of these the exam elsewhere says "No rigidity", or the gait is described as normal.
- The line is noise: DaTscan is already waste in 29 cases.

**Fix.**

1. Keep it where it is coherent with the stage and phenotype: S01 (advanced, shuffling), S04, S07 (GRN, where asymmetric motor signs may emerge) and S09 (advanced).
2. Remove the exam phrase, the red-herring entry and the KCE line from S02, S03, S05, S06, S08 and S10, and make the gait consistent.
3. Where kept, use the canonical interpretation: "Mild symmetric rigidity without rest tremor or bradykinesia is compatible with bvFTD and does not by itself call for dopamine transporter imaging."

### C9. Template musts duplicated, or presuming optional results

**Covers 25 cases with the template block.** The block is: Rascovsky; capacity; caregiver; genetic counselling. In 25 cases it is pasted next to case-specific versions of the same musts. Musts that presume an optional test result:

- P08: "given confirmed C9orf72 expansion";
- M06: "confirm reduced plasma progranulin";
- P06: "definitively exclude AD with amyloid PET";
- P02: "mandates FDG-PET and genetic panel";
- S07 KCE: "mandates genetic panel";
- M02: "Pursue genetic testing".

**Fix.**

1. Use 4 to 6 musts per case, each case-specific, no duplicates.
2. No must may depend on a non-required result.
3. Use the canonical forms below, merging each with its case-specific counterpart.

Canonical musts:

- "Apply the Rascovsky 2011 criteria: state which features are present, the functional decline, and the level of certainty (possible or probable)." For PPA: "Apply the Gorno-Tempini 2011 criteria and name the variant."
- "Explain why {the case's mimic} does not account for the progressive syndrome." The mimic is psychiatric illness, alcohol, HIV, lithium, vascular disease or AD, depending on the case.
- "Address safety and capacity: driving, finances {and the case's specific risk: firearms, legal practice, judicial office, employment}."
- "Arrange caregiver education and support, and a plan for behavioural symptoms that avoids cholinesterase inhibitors and memantine."
- Familial or young-onset cases: "Offer genetic counselling before any genetic test, and discuss what a result would mean for relatives."

### C10. Prohibition wording overstated

**Covers 30/30.** The prohibitions read: "Do not start acetylcholinesterase inhibitors ... may worsen behavioral symptoms" and "Do not start memantine ... may worsen behavioral symptoms". The memantine RCT showed no benefit and a worse cognitive score, not a behavioural harm.

**Fix.** Replace with:

- "Do not start a cholinesterase inhibitor (donepezil, rivastigmine, galantamine): no benefit in FTD, NICE NG97 advises against it, and it may worsen behaviour."
- "Do not start memantine: a randomised trial showed no benefit in FTD and NICE NG97 advises against it."

Keep the antipsychotic and benzodiazepine prohibitions. In S11, the "aciclovir for presumed HSV sequelae" prohibition stays (it is tied to the red herring).

### C11. Differential not updated to the assessment-time view

Examples:

- M01: AD rated high.
- M09: bipolar mania and substance intoxication rated high after the tox screen, BAL and course refute them.
- S12: stroke rated high despite the DWI-negative MRI and the progressive course.
- P08: "ALS without FTD" and AD rated moderate.
- Most S-cases: AD moderate with a frontal pattern.

**Fix.**

1. Rate each entry as it stands when the agent submits, after the required work-up. Usually 2-4 entries.
2. Use low likelihood for refuted mimics, with a one-line "against" reason.
3. Never list a mimic as high when the required results exclude it.

### C12. Key clinical evidence and metadata notes cite results that do not exist

**Covers 30/30.**

- KCE lines read "Negative amyloid biomarkers exclude (AD / neurodegenerative pathology)" in S01, S02, S04, M10, P06 and P07, where amyloid is optional or absent. The claim is also false: a negative amyloid study does not exclude FTLD.
- The engineering line "Tier per the July 2026 clinical review: FDG-PET supports ..." appears in 7 cases (P05, P06, P07 and others).
- `metadata.notes` mention C9orf72 where the case has no genetic result (P01), or amyloid where there is none (M01, M10). P06 notes say "negative amyloid PET definitively excludes AD".

**Fix.**

1. KCE lists only evidence that the required pathway produces, or that is in the patient presentation.
2. Replace amyloid lines with: "The frontal and anterior temporal pattern with relative posterior sparing makes Alzheimer disease less likely; an amyloid or CSF AD biomarker study is optional if doubt remains."
3. Where an amyloid result is authored and optional, a KCE line may state: "If obtained, a negative amyloid study makes Alzheimer pathology unlikely; it does not exclude FTLD."
4. Delete every "Tier per the July 2026 clinical review" line.
5. Correct `metadata.notes` to match the case and drop "definitively" and "pathognomonic".

### C13. Neuropsychological impressions truncated or templated

- About 10 S-cases end with "Selective anterior-network deficit pattern with posterior cortical sparing", cut mid-sentence.
- P04 and P06 share a template impression.
- M06's impression describes only apraxia.
- S08 embeds a capacity assessment.

**Fix.**

1. Finish each impression in one or two sentences on the profile itself.
2. A report may commit to a confidence-qualified syndrome. It must not state the final diagnosis or management.
3. Move capacity content out of the neuropsych report (S08) into the clinical assessment or the musts.

Canonical ending: "The profile is executive and social-cognitive predominant with relative sparing of {memory recognition / visuospatial function}, consistent with a frontal-network syndrome."

### C14. Exam contradiction on primitive reflexes

**Covers M01, M09 and 5 other cases.** The exam says "No primitive reflexes on cranial nerve exam" while another field records a snout or grasp reflex.

**Fix.** Keep the case's intended finding (the primitive reflex is present where the HPI or exam uses it). Delete the contradicting phrase. Primitive reflexes are not a cranial nerve finding; place them under "Other" or the reflex line.

### C15. Sequence constraints

Today only M08 (MRI before CSF, soft) and M09 (CT before MRI, soft) have constraints, both citing `[AAN_dementia_2018]`. No order in this condition is unsafe in reverse, so every constraint is soft.

**Add or keep:**

| Constraint (before → after) | Cases | Citation | Reason |
|---|---|---|---|
| MRI → CSF | M08, and any case with a CSF criterion | `[NICE_NG97]` | "Imaging first excludes a mass lesion before lumbar puncture and shows whether white-matter disease makes JCV testing relevant." |
| CT → MRI | M09 | `[NICE_NG97]` | "In the emergency department CT is the first rapid study; MRI characterises the degenerative pattern afterwards." |
| EMG → genetic panel | P08 | `[EAN_ALS_2024]` | "The motor neuron diagnosis is established clinically and electrophysiologically before genetic testing is discussed." |
| clinical assessment → genetic panel | all cases with a genetics criterion | `[ACMG_NSGC_2011]` | "Genetic testing follows the clinical diagnosis and counselling." |

Do not add assessment → neuropsych or assessment → MRI. Those orders are natural, and a soft penalty for parallel ordering is not justified.

---

## 3. Target pathway and tiers

### 3.1 bvFTD (28 cases)

| Tier | Action | Arguments | Notes |
|---|---|---|---|
| required | `perform_clinical_assessment` | `assessment_type: cognitive_screen` | Informant history plus screen (C3). |
| required | `order_specialized_test` | `test_type: neuropsych_battery` | Reviewer 1. |
| required | `interpret_labs` | `panels: [CBC, CMP, TSH, B12, folate, ESR, CRP]` | NICE NG97 / SNLG. P08 keeps `CK`, `LFTs`. |
| required | `analyze_brain_mri` | `contrast: false, protocol: dementia` | S06: `order_ct_scan` required instead. M09: CT and MRI both required, CT first. |
| recommended | `order_advanced_imaging` FDG_PET (alt perfusion_SPECT) | | P01, P02, P05, P07 only (C7, Q2). |
| case-specific required | `analyze_csf` | `special_tests: [HIV_RNA]` plus JCV and cryptococcal antigen only if the case's MRI shows white-matter lesions or the CD4 is low | M08 only; verify the current set against the MRI (see M08). |
| case-specific required | EMG/NCS (`order_specialized_test emg_ncs`) | | P08. |
| case-specific recommended | `order_specialized_test respiratory_function` | | P08 (staging). |
| case-specific required | `interpret_labs` targeted | `lithium_level` (M05); `valproate_level`, `ammonia` (P01); `tox_screen`, `BAL`, `ammonia` (M09: keep if already so) | Replaces drug-check misuse. |
| optional | FDG_PET / perfusion_SPECT | | Everywhere else. |
| optional | genetic panel `genetic_panel:FTD` (P08 `genetic_panel:ALS`) | | Familial, young-onset, MND. |
| optional | amyloid_PET or CSF `Abeta42`, `phospho_tau`, `total_tau` | | M04, P03, P06, and wherever AD is in the differential; declare amyloid PET and CSF AD markers as alternatives of one criterion. |
| optional | `interpret_labs plasma_progranulin` | | P02 only. |
| optional | DaTscan | | P04 (known PD) only. |
| optional | `check_drug_interactions` | | Only with a concrete interaction (C2); M08 recommended. |
| optional, last | `search_medical_literature` | | C1. |
| avoid (waste) | EEG, ECG, echo, cardiac monitoring, carotid duplex, MRS, perfusion MRI, DaTscan (except P04), CT (except S06, M09) | | Unchanged. |
| avoid | MRI in S06 | | Change severity from harm to waste: the patient declines MRI without sedation. Ordering it is futile, not harmful. |

Keep `stop_rule.max_additional_actions: 0`. `required_before_assessment` lists exactly the required criteria, with no literature or drug check.

### 3.2 PPA (S11, S12)

As for bvFTD, plus:

- **recommended:** `order_specialized_test` with `test_type: speech_language_evaluation`. Criterion id `action-speech-language-evaluation`, as in ALZ-EARLY-P02. Authored output: a formal speech-language assessment of the variant features, without a diagnosis.
- **MRI:** `contrast: false, protocol: dementia` in both. S11 is currently `contrast: true`; change it and remove the post-contrast sequence from the report.
- **Functional imaging:** optional. S11: FDG_PET with alternative perfusion_SPECT. S12: perfusion_SPECT with alternative FDG_PET, plus an authored FDG follow-up showing left posterior fronto-insular hypometabolism.
- **Neuropsych battery:** stays required (Reviewer 1: validated neuropsychological testing in all 30).

---

## 4. Per-case index

All 30 cases are affected by classes C1, C3, C4, C5, C6, C9, C10, C11 and C12. The bullets below list the case-specific work on top of those classes.

### M-series

- **FTD-M01** (64 M, probable sporadic bvFTD)
  - C3: apathy and hyperorality present in the history, so set them true.
  - C2: the sertraline criterion and its "discontinuation" follow-up become a real sertraline output (C2 canonical); the criterion stays optional.
  - C14: snout reflex versus "no primitive reflexes".
  - C11: AD from high to low/moderate.
  - C12: drop amyloid from `metadata.notes`.
  - Literature: from recommended to optional, last, fixing the leak guard.
- **FTD-M02** (57 F, familial, ALS in a first-degree relative)
  - Genetic output reads "Abnormal values: ..." (template). Rewrite it as a report: result, repeat count, interpretation in one sentence, counselling note.
  - The MRI impression says "metabolic correlation is essential" (cross-modality steering): delete.
  - Must "Pursue genetic testing" becomes the canonical counselling must.
  - Delete the KCE rigidity line (no rigidity on exam).
  - C15: assessment before genetics.
- **FTD-M03** (61 M, bvFTD with small-vessel disease, Fazekas 2)
  - C1 hijack: delete or merge `wernicke_korsakoff_final_exclusion`.
  - The vascular contribution stays in the differential (low/moderate) and in one KCE line. The lobar pattern does not fit vascular dementia.
- **FTD-M04** (53 F, young-onset)
  - Labs: move anti-TPO out (no criterion) or into a keyed follow-up.
  - Amyloid PET stays optional: declare CSF AD markers as an alternative and write the C4 rationale (young-onset AD in the differential).
  - Reword the HR/employment must as part of the safety must.
  - C15: assessment before genetics.
- **FTD-M05** (66 M, bvFTD with bipolar I on lithium)
  - Replace the lithium drug-check criterion (required) with `interpret_labs lithium_level`, required, keeping its criterion id. The lithium level of 1.28 mmol/L is above range with CKD (eGFR 64); the case uses lithium toxicity as a mimic.
  - The labs output must carry the level in a keyed follow-up.
  - Delete the follow-up `lithium_adjusted_recheck_behavioral_persistence` (6 weeks after dose reduction). It breaks ruling 4: it serves a future result.
  - Drug check optional only if an agent with a concrete interaction is plausible. Sertraline with lithium is concrete (serotonin toxicity, hyponatraemia).
  - Note: empagliflozin lowers lithium levels; aspirin at low dose and metoprolol have no significant effect. Do not invent an interaction causing toxicity.
  - Must: explain why the persisting syndrome is not lithium toxicity or bipolar relapse, without presuming a follow-up level.
  - Literature becomes optional with the psychiatric-mimic variant.
- **FTD-M06** (59 F, known GRN carrier with early CBS features)
  - C3: only 1 feature marked true; re-read the history and set the features that are present.
  - Neuropsych impression covers apraxia only; add the executive and social profile (C13).
  - Delete the must "confirm reduced plasma progranulin" (the carrier status is known).
  - Remove CSF NfL from the labs (C5).
  - Literature follow-ups are empty: delete them.
  - Label "probable" against Rascovsky "definite" with a known pathogenic variant: Q1. Do not change `accepted[0]`.
- **FTD-M07** (62 M, bvFTD with alcohol use disorder and cerebellar degeneration)
  - Delete the disulfiram claim from the drug-check follow-up (no criterion): disulfiram in an impulsive patient with FTD is a safety issue. Delete the follow-up entirely.
  - Maternal early dementia: genetics optional, assessment before genetics.
  - Literature (optional) may keep one general follow-up on alcohol-related brain damage versus bvFTD.
  - Musts: abstinence support and thiamine are management; fine as musts.
- **FTD-M08** (55 F, bvFTD in well-controlled HIV)
  - CSF stays required (the HAND / CSF escape mimic). The required set is `[HIV_RNA]` plus JCV and cryptococcal antigen only if the MRI shows white-matter lesions or the CD4 is low. Check the MRI and labs; if neither, move JCV and cryptococcal antigen to an optional alternative criterion. Log the decision.
  - MRI → CSF soft constraint: change its citation from `[AAN_dementia_2018]` to `[NICE_NG97]` and use the canonical reason.
  - Drug check (recommended) against Biktarvy: remove the cobicistat statement. Sertraline with bictegravir has no significant interaction; the interactions that matter are polyvalent cations and metformin, if listed.
  - Labs: HIV viral load and CD4 in their own panel.
- **FTD-M09** (61 M, ED presentation)
  - The CT initial output is interpretive (diagnosis in the report): reduce it to findings and a one-line impression.
  - CT → MRI soft constraint: change its citation and reason per C15.
  - Labs: tox screen, BAL and ammonia stay targeted and keyed.
  - C11: bipolar and substance from high to low with reasons.
  - C14: primitive reflexes.
  - FDG stays optional.
- **FTD-M10** (64 F, right temporal variant)
  - Delete the sertraline must, or reword it as a behavioural plan without a drug name.
  - Delete amyloid from KCE and notes (there is no amyloid criterion).
  - Literature becomes optional; `[Ulugut_2020]` may be added.
  - C3: prosopagnosia and person-knowledge loss go in the findings, but do not count as Rascovsky features. Count only the six.

### P-series

- **FTD-P01** (54 M, near-normal MRI, suggestive family history, on valproate)
  - Replace the required valproate drug check with `interpret_labs [valproate_level, ammonia]`, required, keeping the criterion id. Add a keyed follow-up with the authored levels; confirm what the case intends (in range or toxic). Delete the valproate drug-check output.
  - FDG-PET becomes recommended (C7), with SPECT as alternative.
  - Notes mention C9orf72 although no genetic result is authored: either author a genetic follow-up consistent with the family history, or remove C9orf72 from the notes. Prefer the removal; genetics stays optional.
  - C3: informant set to true.
- **FTD-P02** (48 F, young-onset, prior psychiatric misdiagnosis, on quetiapine)
  - Keep `plasma_progranulin` optional as its own keyed follow-up.
  - Remove the unrequested autoimmune antibodies from the labs (or move them to a keyed follow-up).
  - Delete the must "mandates FDG-PET and genetic panel".
  - FDG becomes recommended (C7).
  - Literature becomes optional with the psychiatric-mimic variant.
  - Drug check (none today): leave it so.
- **FTD-P03** (58 F, MAPT, comorbid depression, on methotrexate, NSAID allergy)
  - The escitalopram drug check stays optional; rewrite its output (C2: no significant interaction with methotrexate, hydroxychloroquine or folic acid; hyponatraemia warning).
  - Amyloid stays optional with the CSF alternative.
  - KCE amyloid line per C12.
  - C3: informant set to true.
  - Leak guard.
- **FTD-P04** (52 M, C9orf72 with co-existing PD on levodopa)
  - The levodopa drug check goes from required to optional, or is deleted. Rewrite its output: levodopa with sertraline has no significant interaction. Remove the ChEI, EMG and genetic-counselling text.
  - DaTscan stays optional, with an authored abnormal result if present (it confirms PD).
  - C3: the domain fragment uses "She ... their marriage" for a male patient; rebuild.
  - Neuropsych impression is a template (C13).
  - Rewrite the genetic output from the template.
  - The empty literature follow-up `pdd_vs_bvftd_diagnostic_discussion`: delete it.
- **FTD-P05** (56 M, high cognitive reserve, normal MRI, C9orf72)
  - FDG becomes recommended (C7).
  - Delete the litigation-capacity and cognitive-reserve literature follow-ups (C1).
  - Delete the "Tier per the July 2026..." KCE line.
  - Notes: drop "pathognomonic" and "completely masks".
  - Father's "sudden cardiac death": no cardiac work-up (waste unchanged).
- **FTD-P06** (63 F, APOE e4, maternal AD, Fazekas 2, on metformin, lisinopril, levothyroxine)
  - Amyloid PET stays optional with the CSF alternative. Delete the must "definitively exclude AD with amyloid PET" and replace it with the mimic must (AD and vascular).
  - KCE "securely excludes" becomes C12 wording.
  - Delete the KCE tier line.
  - Delete the diabetes-optimisation drug-check follow-up (no criterion; no concrete interaction).
  - Delete the judicial-ethics and vascular-quantification literature follow-ups.
  - Notes: remove "definitively".
- **FTD-P07** (54 M, familial, borderline MRI, treated depression, on sertraline)
  - FDG becomes recommended (C7).
  - KCE: replace the amyloid line; delete the tier line.
  - C3: informant set to true (the history comes from the family); empathy per history.
  - Leak guard.
  - C15: assessment before genetics.
- **FTD-P08** (56 F, FTD-MND)
  - EMG stays required.
  - Respiratory function goes from required to recommended, consistent with plans/ALS.md. Remove it from `required_before_assessment`.
  - The respiratory impression states a management threshold ("FVC above 50% ...", NIV timing): strip it to the findings plus one interpretive sentence.
  - Add musts:
    - "Refer to the motor neuron disease multidisciplinary team" `[NICE_NG42]`;
    - "Discuss riluzole" `[EAN_ALS_2024]`;
    - "Discuss non-invasive ventilation: the reduced inspiratory pressure meets an AAN marker for NIV" `[AAN_2009]`. Verify the MIP value in cmH2O in the respiratory output before writing it; if only % predicted is given, write "Arrange respiratory follow-up and discuss NIV when markers are met".
  - Delete "given confirmed C9orf72 expansion" from the must (genetics optional).
  - Rewrite the genetic output from the template.
  - C15: EMG before the genetic panel.
  - C11: "ALS without FTD" and AD to low.
  - KCE: delete "making respiratory function testing a load-bearing required step".
  - CENTRAL: FTD-MND synonyms.

### S-series

- **FTD-S01** (58 M)
  - Keep the rigidity red herring (C8, coherent with the shuffling gait).
  - Keep the alcohol and glucose red herrings.
  - Sertraline drug check stays optional; rewrite the output against amlodipine and metformin (no significant interactions; hyponatraemia warning).
  - KCE: "effectively exclude underlying neurodegenerative pathology" becomes C12 wording.
  - The bedside clock is severely abnormal, so use the second impression variant (C3).
  - Leak guard.
- **FTD-S02** (62 F, on levothyroxine, naproxen)
  - Remove the rigidity from the exam, the red-herring entry and the KCE line (C8).
  - Sertraline drug check stays optional. Interaction: naproxen with sertraline increases bleeding risk. The levothyroxine "monitor thyroid" claim is weak; drop it. Delete the "contraindicated" ChEI line.
  - Literature: delete the management follow-up, including its wrong trazodone citation.
  - C3: informant (the son) set to true; empathy per history.
- **FTD-S03** (55 M, familial, C9orf72)
  - Remove the rigidity (C8).
  - Delete the C9orf72 literature follow-up (it states prognosis and surveillance numbers).
  - Genetics optional; assessment before genetics.
- **FTD-S04** (60 F, no medications)
  - Keep the rigidity, with the canonical interpretation.
  - Delete the calcified granuloma from the CT fallback.
  - Delete the KCE "exclude neurodegenerative pathology" line.
  - C3: daughter as informant set to true. MMSE 20 with recall and orientation loss, so use the second impression variant.
  - Delete the drug-check follow-up (no medications, no criterion).
  - Delete the literature management follow-up.
- **FTD-S05** (57 M, affected brother)
  - Remove the rigidity (C8).
  - The KCE counselling line is good; keep it.
  - Delete the C9orf72 management literature follow-up.
- **FTD-S06** (64 M, claustrophobia, declines sedation; on aspirin, metoprolol, atorvastatin, ramipril)
  - CT stays required.
  - The MRI avoided action goes from harm to waste.
  - Reword the CT impression to findings (C6 canonical style).
  - Remove the rigidity (C8).
  - Delete the firearms literature follow-up. Keep the firearms safety point as a must.
  - Drug-check follow-up (no criterion): delete, or keep with correct aspirin and sertraline bleeding content.
  - KCE: keep the head-trauma line.
- **FTD-S07** (59 F, GRN, on alendronate)
  - Keep the rigidity (GRN, emerging motor signs).
  - KCE "mandates genetic panel" becomes "supports offering genetic counselling and testing".
  - The empty GRN literature follow-up: delete it (it also states trial status).
  - Assessment before genetics.
- **FTD-S08** (56 M, lawyer)
  - Remove the rigidity (C8).
  - Move the capacity content out of the neuropsych report (C13).
  - Delete the capacity literature follow-up.
  - Drug-check follow-up (no medications): delete.
  - Keep the must on legal practice.
- **FTD-S09** (61 F, advanced; on hydrochlorothiazide, levothyroxine)
  - Keep the rigidity (advanced).
  - Sertraline drug check stays optional. Interaction: thiazide with SSRI raises the hyponatraemia risk (real). Remove the trazodone dose and the ChEI "contraindicated" text.
  - KCE: "AChE inhibitors are contraindicated" becomes "are not recommended (NICE NG97)".
  - Delete the driving literature follow-up; keep driving in the safety must.
- **FTD-S10** (53 M, paternal early dementia, C9orf72)
  - Remove the rigidity (C8).
  - Delete the adolescent-predictive-testing literature follow-up. Its content belongs in the counselling must ("predictive testing of minors is deferred").
  - Genetics optional; assessment before genetics.
  - C3: informant set to true.
- **FTD-S11** (65 M, svPPA)
  - Rebuild C3 with Gorno-Tempini features. Every behavioural feature is currently marked present, which is wrong.
  - MRI criterion: `contrast` from true to false; delete the post-contrast sequence from the report.
  - Add `speech_language_evaluation` (recommended), with an authored output: naming, single-word comprehension, object knowledge, reading of irregular words, repetition and fluency, without naming the variant.
  - The clinical-assessment label becomes the PPA label (C4).
  - The red-herring `data_point` claims MRI text appears in the HPI. Reword it to what the patient presentation contains (the wife recalls a prior "asymmetry" on an old scan).
  - Keep the HSV aciclovir prohibition.
  - Literature becomes optional with the svPPA text; leak guard.
  - CENTRAL: accepted synonyms include bvFTD.
- **FTD-S12** (69 F, nfvPPA, remote TIA; on lisinopril, rosuvastatin, aspirin)
  - Rebuild C3 with Gorno-Tempini nfvPPA features.
  - SPECT report: "FDG uptake" becomes "perfusion". Add FDG_PET as an alternative with an authored follow-up.
  - Add `speech_language_evaluation` (recommended), with an authored output: agrammatism, apraxia of speech features, sentence repetition, single-word comprehension.
  - C11: stroke from high to low (DWI-negative, progressive course). PSP speech-predominant stays moderate/low.
  - Add a must: "Plan longitudinal review for emerging PSP or corticobasal features (falls, gaze palsy, limb apraxia)".
  - The clinical-assessment label becomes the PPA label.
  - CENTRAL: check that synonyms do not accept bvFTD.

---

## 5. CENTRAL requests

1. **Criteria pack** `criteria_packs/FTD.md` lists literature search as required. Change it to "optional, last". Replace `AAN_dementia_2018` in its allowed citations with `NICE_NG97`, `SNLG_ISS_2024` and `Frisoni_2024`. Add a PPA section (Gorno-Tempini features, `speech_language_evaluation`).
2. **Citation keys** to register: `[SNLG_ISS_2024]`, `[Ducharme_2020]`, `[Frisoni_2024]`, `[Strong_2017]`, `[Boxer_2013]`, `[Ulugut_2020]` (optional). Confirm that `[NICE_NG97]`, `[ACMG_NSGC_2011]`, `[Amyloid_PET_AUC_2025]`, `[EAN_ALS_2024]`, `[NICE_NG42]` and `[AAN_2009]` are registered.
3. **Synonyms** (`diagnosis_synonyms.yaml`, G31.09):
   - S11 (svPPA) accepts bvFTD labels and S12 must be checked the same way. The PPA cases need variant-specific accepted labels ("semantic dementia", "svPPA", "semantic variant PPA"; "nfvPPA", "progressive non-fluent aphasia", "agrammatic PPA"). A bvFTD answer must not score as correct for a PPA case. This may need per-case rather than per-code synonyms.
   - P08: add "ALS-FTD", "FTD-ALS", "FTD with motor neuron disease", "ALS with frontotemporal dementia", "ALS-FTSD". Decide whether G12.21 should be an accepted secondary code.
4. **perfect_agent** should exercise every declared alternative (perfusion_SPECT for FDG_PET, CSF AD markers for amyloid PET) and report any answer that came from the fallback library. Today 30/30 passes while the alternatives are never served.
5. **Fallback library**: `perfusion_SPECT`, `FDG_PET` and `DaTscan` defaults are normal reports. With the case `advanced_imaging` fallback deleted (C6), any un-authored functional-imaging order in a degenerative case gets a normal scan. Consider a per-condition library tier, or keep the C6 rule that every FDG criterion declares and authors its SPECT alternative.
6. **condition_tool_guidance.yaml `ftd:`**:
   - Record the C7 departure (FDG recommended in P01, P02, P05, P07) once ruled (Q2).
   - Record the S06 MRI severity change (harm to waste).
   - Record P08 respiratory as recommended.
   - Record `speech_language_evaluation` (recommended) in S11 and S12.
   - The guidance claims test (`test_guidance_claims.py`) will need the update.
7. **Leak guard**: the six failing FTD cases share one literature string. Consider making the guard also catch the paraphrase "Confirms Rascovsky 2011 criteria ..." in other conditions' templates.

---

## 6. Open questions for Andrea

1. **M06 label.** The patient is a known GRN pathogenic-variant carrier with a bvFTD syndrome. By Rascovsky 2011 that is definite bvFTD, while the label says "probable". Changing `accepted[0]` needs a reviewer ruling (rule 3). Until then the plan keeps the label. Should the round ask the reviewers to rule "definite", or should the case text stay silent on the level of certainty?
2. **FDG-PET tier with a normal or equivocal MRI** (P01, P02, P05, P07). Reviewer 1 ruled FDG-PET optional in all 30. Without it, these cases meet only possible bvFTD, while their labels say probable. The plan raises FDG-PET to recommended in these four. Keep that, or keep optional and change nothing?
3. **S06 MRI avoided action.** The patient declines MRI without sedation. The plan changes severity from harm to waste. Agree?
4. **M08 CSF set.** The required set may shrink to `HIV_RNA`, with JCV and cryptococcal antigen optional, if the MRI shows no white-matter lesions and the CD4 is not low. Agree that the indications decide?
5. **PPA scoring.** Should S11 and S12 keep the bvFTD-oriented Rascovsky keys in `criteria_met` (if the schema fixes them), or should the schema allow per-syndrome keys?
6. **CT as waste in 27 cases.** Reviewer 1 ruled CT "optional, only as the MRI alternative". The plan keeps CT as waste where MRI is available and done, and required only in S06 and M09. Confirm this reading.

Re-read check: no FTD notes file exists, so no note ids apply, and every case log records "Reviewer notes: none".
