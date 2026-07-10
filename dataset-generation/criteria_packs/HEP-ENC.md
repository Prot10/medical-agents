# Criteria pack: Hepatic encephalopathy

**ICD-10:** K72.x (hepatic failure with encephalopathy), K76.82 (HE without acute hepatic failure)
**Condition enum:** `NeurologicalCondition.HEPATIC_ENCEPHALOPATHY`
**Case ID prefix:** `HEP-ENC`

---

## 1. Diagnostic criteria

AASLD/EASL 2014: HE is a syndrome of neuropsychiatric disturbance in patients
with liver dysfunction (acute liver failure, cirrhosis, or portosystemic
shunts), after excluding other causes of altered mental status.
**West Haven criteria** (grades): 0 = minimal/covert (subclinical, detected
only on psychometric testing); I = mild confusion, slowed cognition,
inverted sleep-wake; II = lethargy, gross disorientation, asterixis;
III = somnolent but rousable, marked confusion, abnormal behavior; IV = coma.
Diagnosis is **clinical** + evidence of liver disease + exclusion of other
causes. Ammonia level supports diagnosis but isn't required (poor sensitivity
+ specificity, doesn't correlate with severity), per AASLD.

## 2. Standard workup hierarchy

**Required:**
- `interpret_labs` (CMP including AST/ALT/bilirubin/INR/albumin, ammonia, CBC, glucose, electrolytes including K/Mg, BUN/Cr, lactate, blood cultures, urine cultures) — confirm liver dysfunction + identify precipitant [AASLD_2014]
- `analyze_brain_mri` OR `order_ct_scan` — exclude alternate causes of AMS (stroke, hemorrhage, mass); not specific for HE [AASLD_2014]
- `search_medical_literature` — confirm West Haven grading, precipitant management
- `check_drug_interactions` — lactulose, rifaximin, sedative use review

**Recommended:**
- `analyze_csf` — only if meningitis/encephalitis suspected; otherwise not indicated
- `analyze_eeg` — triphasic waves classic but non-specific (metabolic encephalopathy generally); useful if non-convulsive status epilepticus on differential
- Specialist referral *(clinical action — `tool_name: null`, no tool call)* — hepatology + critical care for grades III-IV

**Optional:**
- `analyze_ecg` — baseline if elderly or comorbid cardiac disease
- `order_cardiac_monitoring` — if arrhythmia suspected from electrolyte abnormalities

## 3. Tools that are typically USELESS

- `order_echocardiogram` — only if hepatopulmonary syndrome / portopulmonary hypertension on workup
- `order_advanced_imaging` (any modality) — generally not needed
- `order_specialized_test` (most) — not needed for diagnosis

## 4. Tools that are HARMFUL / contraindicated

- `check_drug_interactions` flagging benzodiazepines / opioids — actively reviewing these is essential, but PRESCRIBING them in HE precipitates worsening. Not a tool harm; a treatment decision the agent should flag.

## 5. Sequence constraints

- `order_ct_scan` OR `analyze_brain_mri` → `analyze_csf` (`hard`): when AMS, exclude mass effect before LP [AASLD_2014]

## 6. Subtype variations

- **M (mild):** Grade I HE; minimal workup, address precipitant (constipation, GI bleed, infection, electrolytes)
- **S (standard):** Grade II HE with clear precipitant (typically infection or GI bleed in cirrhosis); standard workup
- **P (progressive / severe):** Grades III-IV; ICU level care, intubation if airway compromise, comprehensive workup for precipitants, exclude alternate diagnoses with imaging
- **R (reverse / mimic):** alternate cause of AMS in patient with cirrhosis — hypoglycemia, electrolyte derangements (hyponatremia, hypocalcemia), uremia, drug toxicity, intoxication, infection without HE, intracranial bleed (cirrhotic coagulopathy increases risk), non-convulsive status epilepticus, Wernicke encephalopathy

## 7. Common red-herring categories

- **Normal ammonia level** — does NOT exclude HE; ammonia poorly correlates with grade
- **Elevated ammonia** — does not confirm HE; many other causes (urea cycle disorders, valproate, hemolysis specimen handling)
- **Asterixis** — supports metabolic encephalopathy but not specific to HE (also uremia, hypercapnia, drug toxicity)
- **Cirrhotic patient with new AMS = HE** — not necessarily; must exclude infection (SBP especially), GI bleed, intracranial bleed, electrolytes
- **Improvement with lactulose** — supports HE but other entities also improve with general supportive care

## 8. Allowed citations

- `[AASLD_2014]` — Vilstrup H et al. Hepatic encephalopathy in chronic liver disease: 2014 Practice Guideline by AASLD and EASL. Hepatology 2014;60:715-735
- `[EASL_2010]` — EASL Clinical Practice Guidelines on the management of ascites, spontaneous bacterial peritonitis, and HE in cirrhosis. J Hepatol 2010
- `[Bajaj_2011]` — Bajaj JS. Review article: the modern management of hepatic encephalopathy. Aliment Pharmacol Ther 2010;31:537-547
- `[Wijdicks_2016]` — Wijdicks EF. Hepatic encephalopathy. NEJM 2016;375:1660-1670
- `[Ferenci_2002]` — Ferenci P et al. Hepatic encephalopathy — definition, nomenclature, diagnosis, and quantification (West Haven and ISHEN). Hepatology 2002;35:716-721
