# Criteria pack: Hepatic encephalopathy

**ICD-10:** K72.x (hepatic failure with encephalopathy), K76.82 (HE without acute hepatic failure)
**Condition enum:** `NeurologicalCondition.HEPATIC_ENCEPHALOPATHY`
**Case ID prefix:** `HEP-ENC`

Updated 24 Oct 2026 to the rulings of the October 2026 physician-review round
(`data/review/round-2026-10/plans/HEP-ENC.md`, `HEP-ENC-summary.md`).

---

## 1. Diagnostic criteria

ACG 2026 [ACG_HE_2026] and EASL 2022 [EASL_HE_2022] govern wherever they differ from the 2014
AASLD/EASL guideline [AASLD_2014]: they are current, and the reviewers cite them. HE is a syndrome
of neuropsychiatric disturbance in patients with liver dysfunction (acute liver failure, cirrhosis,
or portosystemic shunts), after excluding other causes of altered mental status. Diagnosis is
**clinical**: West Haven grade, evidence of liver disease and exclusion of other causes of altered
mental status (ACG 2026; EASL 2022).

**West Haven grades** [AASLD_2014] [Ferenci_2002]: minimal (detected only on psychometric testing);
1 = mild confusion, slowed cognition, inverted sleep-wake; 2 = lethargy, disorientation to time,
asterixis; 3 = somnolent but rousable, grossly disoriented; 4 = coma.

- **Covert HE is minimal HE or West Haven grade 1; overt HE is grade 2 or higher** (ACG 2026 key
  concept 1).
- Where a label gives a range, the exam must support the upper bound; otherwise use the lower. Labels
  carry one grade, not a range.
- **Ferenci type:** A = acute liver failure; B = portosystemic bypass without intrinsic liver
  disease; C = cirrhosis, with or without a shunt.

**Ammonia** [ACG_HE_2026] [EASL_HE_2022]: ammonia **neither grades nor confirms HE**, and repeat
levels never measure or titrate response (ACG 2026 recommendation 5, key concept 14). A normal
ammonia in a confused cirrhotic should prompt a search for another cause (EASL 2022). Reference range
for the condition: **11-51 µmol/L**. One admission ammonia per case; no serial values, no "falling
ammonia confirms response".

**Severity scores:** Child-Pugh (bilirubin <2 / 2-3 / >3 mg/dL; albumin >3.5 / 2.8-3.5 / <2.8 g/dL;
INR <1.7 / 1.7-2.3 / >2.3; ascites none / mild / moderate-severe; HE none (minimal HE counts as none)
/ grade 1-2 / grade 3-4; class A 5-6, B 7-9, C 10-15). MELD (UNOS) = round(10 x (0.957 ln Cr + 0.378
ln bili + 1.120 ln INR + 0.643)), values below 1 count as 1, creatinine capped at 4; if MELD > 11,
MELD-Na = MELD + 1.32 x (137 - Na) - 0.033 x MELD x (137 - Na), Na bounded to 125-137
[Kim_MELDNa_2008]. Every stated score must be derivable from the printed labs and exam; a prior
score is dated as prior.

## 2. Standard workup hierarchy

Canonical criterion order (the review app reads it as the work-up sequence): core labs, blood
cultures, diagnostic paracentesis, urine culture, CT, MRI, EEG, case-specific steps, drug-interaction
check last.

**Required:**
- `interpret_labs` core: alternative 1 `{"panels": ["CBC", "CMP", "coagulation", "ammonia"]}`, alternative 2 `{"panels": ["CBC", "BMP", "LFTs", "coagulation", "ammonia"]}`, both plus the case extras (only advertised `interpret_labs` terms, e.g. `tox_screen`, not `toxicology`): blood count, electrolytes, renal and liver function, glucose, INR, ammonia and CRP, with toxicology where alcohol or drugs are in question. Confirms liver dysfunction and identifies metabolic and infective precipitants [ACG_HE_2026]
- `order_microbiology` (`{"specimen": "ascitic_fluid"}`): **required whenever ascites is present**: diagnostic paracentesis in every hospitalised cirrhotic with ascites who has encephalopathy, GI bleeding, infection, or worsening liver or renal function (cell count with differential, total protein and albumin, Gram stain and culture in blood-culture bottles). SBP is an ascitic PMN count of 250 cells/mm3 or more. No criterion and no output without ascites; never filed under `interpret_labs` [EASL_decomp_2018] [AASLD_ascites_2021]

**Cultures (tier rule):** `order_microbiology` `{"specimen": "blood_culture"}` and `{"specimen": "urine"}` (arguments are the specimen only; no `before_antimicrobials`, no `tests` list):
- **Required** when the temperature is 38.0 °C or more, the WBC is above 11 x10^9/L, or an infective precipitant is in the label or HPI. Infection is the commonest precipitant of overt HE and can be occult [EASL_HE_2022]. One exception: a WBC just above 11 drawn within hours of a generalised seizure in an afebrile patient (post-ictal demargination) leaves the screen recommended, and the rationale says so (P06)
- **Recommended** otherwise, as an infection screen for an occult precipitant
- One specimen and one time point per output: either a final organism with its susceptibility, or "no growth at 48 hours" with the organism null; no culture result in the admission panel

**Brain imaging** (`order_ct_scan` `{}`, `analyze_brain_mri` `{}`): **not routine** in cirrhosis with confusion (ACG 2026 recommendation 6). Required only with an ACG trigger: **a new focal deficit, seizure, head trauma, an atypical first episode, or no response to treatment**; optional otherwise. MRI where the case raises a specific alternative (Wilson, Wernicke, leptomeningeal or shunt work-up). Rationale names the trigger present; excludes haemorrhage or mass [ACG_HE_2026]

**Recommended:**
- `analyze_eeg` (`{}`): diffuse slowing, with or without triphasic waves, supports a metabolic encephalopathy and excludes non-convulsive seizures; **required** where NCSE is the question. NCSE is excluded by the EEG, never by a benzodiazepine (or naloxone) challenge [EASL_HE_2022]
- Case-specific steps where the case raises them: `order_body_imaging` (TIPS Doppler, renal ultrasound for loin pain with AKI and UTI, abdominal shunt imaging), `order_specialized_test` `neuropsych_battery` (covert HE), `genetic_panel:wilson`

**Drug-interaction check** (`check_drug_interactions`): **required only for a concrete interaction, allergy or dosing issue that changes management** (the patient's medicines against the drugs in the musts, the allergies, renal or hepatic dosing); otherwise optional, with a short real output ("no clinically relevant interaction between lactulose, rifaximin and the current medicines; avoid sedatives"). One follow-up whose trigger names the drugs, last in the pathway; `initial_tool_outputs.drug_interactions` null. A non-severe penicillin rash does not contraindicate ceftriaxone (low cross-reactivity: give with monitoring); penicillin anaphylaxis needs an alternative or specialist advice before any beta-lactam.

**Optional:**
- `analyze_ecg`: baseline if elderly or comorbid cardiac disease
- `order_cardiac_monitoring`: if arrhythmia suspected from electrolyte abnormalities

**Not a clinical step:** `search_medical_literature` is not part of the pathway (October 2026
ruling 5): no literature criterion, no literature follow-up, `initial_tool_outputs.literature_search`
null.

**Management is a must, never a tool call** (ruling 4). No follow-up may deliver treatment, a
consult or a treatment response (lactulose/rifaximin response panels, empirical thiamine, transplant
evaluation, endoscopy, withdrawal monitoring, post-treatment EEG). Canonical facts for the musts:
- **Lactulose** titrated to **2-3 soft bowel movements per day** (ACG 2026 recommendation 10; EASL 2022): "Lactulose 25 mL every 1-2 hours until at least two soft bowel movements, then titrated to 2-3 soft bowel movements per day; avoid over-titration, which causes dehydration, hypokalaemia and kidney injury." Never "2-4" or "3-4"
- **Rifaximin** 550 mg twice daily is added after a recurrent overt episode, not in a first episode
- Response is reviewed for adherence and symptoms at 4-8 weeks (ACG 2026 key concept 8); it is not a 72-hour test. Failure to improve with adherence should prompt reconsideration of the diagnosis
- SBP: IV ceftriaxone 2 g daily (or cefotaxime), adjusted to culture, plus albumin 1.5 g/kg on day 1 and 1 g/kg on day 3 when Cr > 1 mg/dL or bilirubin > 4 mg/dL; repeat paracentesis at 48 hours if no clinical improvement [EASL_decomp_2018]
- Variceal bleeding: vasoactive drug, ceftriaxone 1 g daily for up to 7 days, restrictive transfusion to haemoglobin 7-8 g/dL, upper endoscopy within 12 hours after resuscitation [Baveno_VII]
- Parenteral thiamine before any glucose; Wernicke: thiamine 200 mg IV three times daily [EFNS_Wernicke_2010]
- Transplant referral for decompensated cirrhosis with overt HE, with the computed MELD-Na [EASL_decomp_2018]
- Alcohol-related hepatitis on prednisolone: Lille score on day 7, stop if 0.45 or more [Lille_2007] [EASL_ALD_2018]

## 3. Tools that are typically USELESS

- `order_echocardiogram`: only if hepatopulmonary syndrome / portopulmonary hypertension on workup
- `order_advanced_imaging` (any modality): generally not needed; MRI is ordered with `analyze_brain_mri`, never under advanced imaging
- `order_specialized_test` (most): not needed for diagnosis
- `analyze_csf`: no routine role; only for a specific meningitis or encephalitis question the case raises

## 4. Tools that are HARMFUL / contraindicated

- No tool call is harmful by itself. Prescribing sedatives is a treatment decision handled by prohibitions: no benzodiazepines or other sedatives for agitation or sleep (they precipitate and prolong HE; manage agitation with reorientation, a safe environment and treatment of the precipitant) [EASL_HE_2022]; with active alcohol withdrawal, no scheduled or long-acting benzodiazepines, symptom-triggered lowest-dose lorazepam or oxazepam [EASL_ALD_2018]; never withhold a benzodiazepine for seizure termination because of HE [AES_2016]. Acetaminophen up to 2 g per day.

## 5. Sequence constraints

None. The former hard CT/MRI-before-CSF constraint is deleted: no LP remains in the condition's
pathway, and no reverse order is unsafe. Stop rule: `required_before_assessment` lists exactly the
required ids; `max_additional_actions` 0.

## 6. Subtype variations

- **M (mild):** covert or grade 2 HE with a clear precipitant (constipation, electrolytes, medicines, GI bleed, infection); core labs, paracentesis with ascites, cultures per the tier rule
- **S (standard):** overt grade 2-3 HE with a clear precipitant (typically infection or GI bleed in cirrhosis); standard workup
- **P (progressive / severe):** grade 3-4, or an atypical presentation; ICU level care, airway protection, comprehensive search for precipitants, imaging and EEG when an ACG trigger or NCSE question is present
- **R (reverse / mimic):** alternate cause of altered mental status in a patient with cirrhosis: hypoglycaemia, electrolyte derangements (hyponatraemia, hypocalcaemia), uraemia, drug toxicity, intoxication, infection without HE, intracranial bleed (cirrhotic coagulopathy increases risk), non-convulsive status epilepticus, Wernicke encephalopathy, Wilson disease

## 7. Common red-herring categories and pitfalls

- **Normal ammonia level:** does NOT exclude HE; it prompts a search for another cause
- **Elevated ammonia:** does not confirm or grade HE; many other causes (urea cycle disorders, valproate, haemolysis, specimen handling)
- **Asterixis:** supports metabolic encephalopathy but not specific to HE (also uraemia, hypercapnia, drug toxicity)
- **Cirrhotic patient with new altered mental status = HE:** not necessarily; exclude infection (SBP especially), GI bleed, intracranial bleed, electrolytes
- **Improvement with lactulose:** supports HE but other entities also improve with general supportive care; reviewed at 4-8 weeks
- **Zinc:** zinc deficiency, not excess, is associated with HE; excess zinc causes copper deficiency (anaemia, neutropenia, myeloneuropathy), not HE
- **Post-ictal CK:** rises after some hours and peaks at 24-72 hours [Brigo_2015]
- **CT reports:** CT cannot show restricted diffusion; cirrhotic pallidal change is a T1 MRI hyperintensity, not a CT hypodensity (putaminal CT hypodensity in Wilson disease is acceptable)
- **Differential:** SBP is `low` once the ascitic PMN is below 250; an alternative the work-up excludes is `low` with the excluding result

## 8. Allowed citations

- `[ACG_HE_2026]`: Bajaj JS, Jakab SS, Jesudian AB, et al. ACG Clinical Guideline: Hepatic Encephalopathy. Am J Gastroenterol 2026;121:588-618, doi:10.14309/ajg.0000000000003899
- `[EASL_HE_2022]`: Montagnese S et al. EASL Clinical Practice Guidelines on the management of hepatic encephalopathy. J Hepatol 2022;77:807-824
- `[AASLD_2014]`: Vilstrup H et al. Hepatic encephalopathy in chronic liver disease: 2014 Practice Guideline by AASLD and EASL. Hepatology 2014;60:715-735 (West Haven grades; ACG 2026 and EASL 2022 govern where they differ)
- `[Ferenci_2002]`: Ferenci P et al. Hepatic encephalopathy: definition, nomenclature, diagnosis, and quantification. Hepatology 2002;35:716-721
- `[EASL_decomp_2018]`: EASL Clinical Practice Guidelines for the management of patients with decompensated cirrhosis. J Hepatol 2018;69:406-460
- `[AASLD_ascites_2021]`: Biggins SW et al. Diagnosis, evaluation, and management of ascites, SBP and hepatorenal syndrome: 2021 AASLD practice guidance. Hepatology 2021;74:1014-1048
- `[Baveno_VII]`: de Franchis R et al. Baveno VII: renewing consensus in portal hypertension. J Hepatol 2022;76:959-974
- `[EASL_ALD_2018]`: EASL Clinical Practice Guidelines: management of alcohol-related liver disease. J Hepatol 2018;69:154-181
- `[Lille_2007]`: Louvet A et al. The Lille model. Hepatology 2007;45:1348-1354
- `[EFNS_Wernicke_2010]`: Galvin R et al. EFNS guidelines for diagnosis, therapy and prevention of Wernicke encephalopathy. Eur J Neurol 2010;17:1408-1418
- `[AES_2016]`: Glauser T et al. Evidence-based guideline: treatment of convulsive status epilepticus (AES). Epilepsy Curr 2016;16:48-61
- `[Brigo_2015]`: Brigo F, et al. Postictal serum creatine kinase for the differential diagnosis of epileptic seizures and psychogenic non-epileptic seizures: a systematic review. J Neurol 2015;262:251-257, doi:10.1007/s00415-014-7369-9 (post-ictal CK)
- `[AASLD_Wilson_2022]`: Schilsky ML et al. A multidisciplinary approach to the diagnosis and management of Wilson disease: 2022 AASLD practice guidance. Hepatology 2023;77:1428-1455 (executive summary verified for P04)
- `[Kim_MELDNa_2008]`: Kim WR et al. Hyponatremia and mortality among patients on the liver-transplant waiting list. NEJM 2008;359:1018-1026
- `[Wijdicks_2016]`: Wijdicks EF. Hepatic encephalopathy. NEJM 2016;375:1660-1670 (background)
- `[EXTRIP_lithium_2015]`: Decker BS, Goldfarb DS, Dargan PI, et al. Extracorporeal treatment for lithium poisoning: systematic review and recommendations from the EXTRIP Workgroup. Clin J Am Soc Nephrol 2015;10:875-887 (P02; verified 24 Oct 2026)
- `[EASL_PBC_2017]`: European Association for the Study of the Liver. EASL Clinical Practice Guidelines: the diagnosis and management of patients with primary biliary cholangitis. J Hepatol 2017;67:145-172 (M05, cholestatic pruritus; verified 24 Oct 2026)
- `[AASLD_IDSA_HCV_2023]`: Bhattacharya D, et al.; AASLD-IDSA HCV Guidance Panel. Hepatitis C Guidance 2023 Update: AASLD-IDSA recommendations for testing, managing, and treating hepatitis C virus infection. Clin Infect Dis 2023 (online 25 May 2023), doi:10.1093/cid/ciad319; living version at hcvguidelines.org (S07, decompensated cirrhosis regimens; verified 24 Oct 2026)
- `[EASL_HBV_2025]`: European Association for the Study of the Liver. EASL Clinical Practice Guidelines on the management of hepatitis B virus infection. J Hepatol 2025, doi:10.1016/j.jhep.2025.03.018 (S05; supersedes the 2017 EASL HBV guideline; verified 24 Oct 2026)

**Superseded (do not cite; kept for traceability):**
- `[EASL_2010]`: EASL Clinical Practice Guidelines on the management of ascites, spontaneous bacterial peritonitis, and hepatorenal syndrome in cirrhosis. J Hepatol 2010. Superseded by `[EASL_decomp_2018]`
- `[Bajaj_2011]`: Bajaj JS. Review article: the modern management of hepatic encephalopathy. Aliment Pharmacol Ther 2010;31:537-547. Superseded by `[ACG_HE_2026]`
