# MIG-AURA: condition plan for the October 2026 review round

Lead plan for the 30 MIG-AURA cases (M01..M08, P01..P09, RM11, RS11, S01..S11). Read
`ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them.

There are no reviewer notes for MIG-AURA (`notes/MIG-AURA.md` and `notes/MIG-AURA.json` do not
exist). The physician input is the July 2026 tool guidance for `migraine_with_aura` in
`agent-platform/config/review/condition_tool_guidance.yaml` (Reviewer 1 rulings, summarised in 1.3)
plus ROUND_POLICY. Every finding below comes from the lead's own survey; each log has an empty
"Reviewer notes" section that says "No reviewer notes for this case".

Baseline (24 October 2026, before any edit): `perfect_agent.py` passes 30/30. The leak guard
(`test_case_guards.py`) fails 13 cases: M05, M07, P01, P02, P04, P07, P08, P09, RM11, RS11, S02,
S05, S10 (stored literature or drug output whose text equals `expected_evidence` or the key
evidence). No case has sequence constraints. Every stop rule has `max_additional_actions: 0` and
lists the literature criterion as required.

Use: apply the classes of section 2 that name your case (canonical text verbatim, `<...>` slots
filled), then the decisions of section 4, rebuild criteria, follow-ups, constraints and stop rule per
section 3, run `perfect_agent.py CASE -v`, `case_io.py check CASE` and
`uv run pytest agent-platform/tests/test_case_guards.py -q -k CASE`, and write `logs/{CASE_ID}.md`.

New text: English, the field's existing spelling (British in this condition: oestrogen, haemorrhage),
no em or en dashes. New values must be plausible for age, sex, weight and medicines and differ from
the shared template values.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which source governs what

| question | source | key |
| --- | --- | --- |
| Diagnosis and subtypes | ICHD-3, Cephalalgia 2018;38:1-211 | `[ICHD_3]` (pack) |
| Who needs imaging | AHS evidence assessment of neuroimaging in migraine: Evans RW et al., Headache 2020;60:318-336; AAN 2000 practice parameter | `[AHS_neuroimaging_2020]` (CENTRAL), `[AAN_2000]` (pack) |
| Acute treatment, triptan use | AHS consensus statement 2021: Ailani J et al., Headache 2021;61:1021-1039; NICE CG150 | `[AHS_2021]`, `[NICE_CG150]` (CENTRAL) |
| Preventive treatment | AHS 2021 (thresholds below); Silberstein SD et al., Neurology 2012;78:1337-1345 (evidence grades of oral preventives) | `[AHS_2021]`, `[Silberstein_2012]` (CENTRAL) |
| Hormonal contraception, HRT | UKMEC 2016 (amended 2019); WHO MEC 5th ed. 2015; Sacco S et al., J Headache Pain 2017;18:108 (EHF/ESC consensus); NICE NG23 (menopause) | `[UKMEC_2016]`, `[WHO_MEC_2015]`, `[NICE_NG23]` (CENTRAL), `[Sacco_2017]` (check pack key `[Sacco_2022]`: use whichever exists, never both) |
| Topiramate and valproate in women who can become pregnant | MHRA Drug Safety Update June 2024 (topiramate pregnancy prevention programme); EMA PRAC 2023 | `[MHRA_topiramate_2024]` (CENTRAL) |
| Migraine with aura and vascular risk, PFO | Eigenbrodt AK et al., Nat Rev Neurol 2021;17:501-514 (EHF/EAN statement on migraine and cardiovascular disease); PREMIUM (Tobis JM, JACC 2017;70:2766-2774), PRIMA (Mattle HP, Eur Heart J 2016;37:2029-2036), MIST (Dowson A, Circulation 2008;117:1397-1404) | `[EHF_EAN_2021]`, trial keys (CENTRAL) |
| Pathophysiology only | Charles AC, Baca SM, Nat Rev Neurol 2013, or the pack `[Charles_2017]` | never cited for PFO, HRT or drugs |
| AF anticoagulation (P02, P07) | ESC 2024 AF guideline: Van Gelder IC et al., Eur Heart J 2024;45:3314-3414 (CHA2DS2-VA) | `[ESC_AF_2024]` (CENTRAL) |
| Secondary stroke prevention (P03, P07) | Kleindorfer DO et al., Stroke 2021;52:e364-e467 | `[AHA_ASA_2021_secondary]` (VASC-DEM pack; CENTRAL) |
| Unruptured aneurysm (P09) | Thompson BG et al., Stroke 2015;46:2368-2400 (AHA/ASA unruptured intracranial aneurysm) | `[AHA_UIA_2015]` (CENTRAL) |
| CADASIL (P04, P06) | Mancuso M et al., Eur J Neurol 2020;27:909-927 (EAN CADASIL guideline) | `[EAN_CADASIL_2020]` (CENTRAL) |
| MELAS (P08) | Parikh S et al., Genet Med 2017;19 (Mitochondrial Medicine Society patient care standards) | `[MMS_2017]` (CENTRAL) |
| Medication overuse (S11) | ICHD-3 8.2 | `[ICHD_3]` |
| Lactation (S06) | LactMed (NIH) entries for the drug | free-text source, no key needed |

Allowed pack citations: `[ICHD_3]`, `[AAN_2000]`, `[Charles_2017]`, `[Holland_2012]`, `[Sacco_2022]`.
`[Holland_2012]` is the AAN/AHS guideline on NSAIDs and complementary treatments: cite it only for
those (riboflavin, magnesium, NSAIDs), never for propranolol, topiramate, amitriptyline or
candesartan (those are `[Silberstein_2012]`). One citation per source in a `citations` list: delete
duplicates such as `"[ICHD_3]"` next to `"ICHD_3"`, and free-text strings such as
`"ICHD-3; NICE CG150 (2025)"` become separate keys. Until CENTRAL adds a key, cite it in the
rationale text by author, journal and year and leave it out of `citations`.

### 1.2 Canonical clinical facts (use these; do not restate them differently)

ICHD-3 codes. 1.2.1 migraine with typical aura; 1.2.1.1 typical aura with headache; 1.2.1.2 typical
aura without headache; 1.2.2 migraine with brainstem aura; 1.2.3 hemiplegic migraine (1.2.3.1
familial, 1.2.3.2 sporadic); 1.2.4 retinal migraine; 1.4.1 status migrainosus; 1.4.2 persistent aura
without infarction; 1.4.3 migrainous infarction; 1.4.4 migraine aura-triggered seizure (migralepsy);
1.5.2 probable migraine with aura. Several cases cite migrainous infarction as "1.4.1": that is
status migrainosus. Fix every occurrence.

ICHD-3 1.2 criteria. A: at least two attacks fulfilling B and C. B: one or more fully reversible aura
symptoms (visual, sensory, speech and/or language, motor, brainstem, retinal). C: at least three of
six: (1) at least one aura symptom spreads gradually over 5 min or more; (2) two or more aura
symptoms occur in succession; (3) each individual aura symptom lasts 5-60 min; (4) at least one aura
symptom is unilateral; (5) at least one aura symptom is positive; (6) the aura is accompanied or
followed within 60 min by headache. D: not better accounted for by another ICHD-3 diagnosis.
Motor aura may last up to 72 h (hemiplegic migraine). A single attack that otherwise fulfils the
criteria is 1.5.2 probable migraine with aura, not 1.2.1.

Brainstem aura: at least two of dysarthria, vertigo, tinnitus, hypacusis, diplopia, ataxia not
attributable to sensory deficit, decreased level of consciousness; no motor and no retinal symptoms.
Migrainous infarction: the attack is typical of previous attacks except that one or more aura
symptoms persist for more than 60 min, and neuroimaging shows ischaemic infarction in the relevant
area, not better accounted for by another diagnosis. A 20-minute aura with an infarct is not
migrainous infarction. Migralepsy: a seizure during, or within 1 h of, a migraine aura.

Imaging. A typical aura with a normal examination needs no imaging (AHS 2020; AAN Choosing Wisely).
Imaging is indicated for red flags: first aura over 50, change in aura pattern, aura over 60 min,
motor, brainstem or isolated aphasic aura, abnormal examination, thunderclap onset, aura always on
the same side, systemic features. MRI is preferred to CT. A brain MRI report never reports
angiography or venography: those are `order_advanced_imaging MR_angiography` or `MR_venography`.

DWI. A normal DWI excludes an acute infarct; it does not exclude a TIA (TIA is by definition without
infarction). Never write "normal DWI excludes TIA". The distinction from TIA is clinical: positive
symptoms, gradual spread over minutes, succession of symptoms, previous identical attacks.

Triptans. Contraindicated by label after stroke or TIA, in ischaemic heart disease, peripheral
vascular disease and uncontrolled hypertension. Avoided by label in hemiplegic migraine and migraine
with brainstem aura (no safety data; AHS 2021 notes emerging evidence of safety; treat as
"avoid, use NSAID plus antiemetic"). They are taken at headache onset, not during the aura: a dose
during the aura is ineffective, not harmful. Rizatriptan with propranolol: use rizatriptan 5 mg
(propranolol raises rizatriptan levels about 70%); sumatriptan has no such interaction. Triptan with
SSRI or SNRI: serotonin syndrome is rare (FDA 2006 warning, AHS 2018 review found the risk low);
co-prescription is allowed with counselling, not a contraindication. Ergots: never within 24 h of a
triptan; ergots are themselves avoided in migraine with aura with vascular risk.

Combined hormonal contraception (pill, patch, ring). UKMEC 4 and WHO MEC 4 in migraine with aura at
any age: stop and switch. Progestogen-only pill, implant, injectable and the LNG-IUS are UKMEC 2;
the copper IUD is UKMEC 1. Postpartum (S06): combined methods are UKMEC 4 under 6 weeks when
breastfeeding regardless of migraine, and the aura makes them 4 at any time. Write "UKMEC category
4", never "category 3-4".

HRT. Migraine with aura is not a contraindication to HRT, and WHO MEC does not classify HRT. NICE
NG23 and the EHF consensus: prefer transdermal oestradiol at the lowest effective dose, with
micronised progesterone or the LNG-IUS for endometrial protection; stop or review if the aura
worsens. Prohibitions such as "do not start HRT" in M05, P01 and P05 are wrong and go.

Preventive treatment (AHS 2021). Offer when at least 6 monthly headache days, at least 4 with some
disability, or at least 3 with severe disability; consider at 4-5 days without disability, 3 with
some disability, or 2 with severe disability. Also consider for prolonged or frequent aura,
hemiplegic or brainstem aura, and after migrainous infarction. About one attack a month without
disability (S01) and a single attack (M01, M07) do not need prevention. Options and cautions:
propranolol (asthma, depression, athletes), candesartan (pregnancy), topiramate (pregnancy
prevention programme: highly effective contraception, IUD or implant preferred; reduces the
efficacy of the progestogen-only pill at 200 mg/day), amitriptyline (sedation, lactation acceptable
at low dose), valproate (never in women who can become pregnant unless a pregnancy prevention
programme applies, MHRA 2024), CGRP monoclonal antibodies after failure of oral agents (NICE TA). For
hemiplegic migraine: verapamil, flunarizine (where licensed), acetazolamide, lamotrigine.

PFO. Not screened in migraine with aura (no routine bubble echo); closure is not indicated for
migraine (PREMIUM, PRIMA and MIST missed their primary end points). A PFO matters only after a
cryptogenic stroke under 60 (P03, P07 staging).

Medication overuse (S11). ICHD-3 8.2: headache on 15 or more days a month with regular overuse for
more than 3 months: simple analgesics on 15 or more days, opioids, triptans or combination
analgesics on 10 or more days. Codeine-containing combination analgesic on 10 or more days a month
qualifies.

### 1.3 July 2026 physician rulings (Reviewer 1, condition_tool_guidance.yaml)

- Required clinical tool in every case: `perform_clinical_assessment`
  `assessment_type: structured_headache_history_ichd3` (the 3-of-6 rule applied explicitly).
- MRI optional, for red flags only (the per-case tiers below make it recommended or required where
  the case has a red flag).
- CSF, ECG and EEG removed; RM11 keeps EEG (migralepsy).
- Labs optional.
- Echo removed from routine use; it stays in P03, P07 and P08 (stroke and cardiomyopathy work-up).
- Open composition question raised then and still open (section 6): P06 CADASIL, P07 cardioembolic
  stroke and P08 MELAS under this condition.

---

## 2. Error classes in this condition

Each class: what is wrong, which cases, the fix, canonical text where needed. "All" means all 30.

### A. Clinical-assessment output is a template (all)

What: `initial_tool_outputs.clinical_assessment` copies HPI sentences verbatim (often twice), has a
generic red-flag line ("SNNOOP10 red flags reviewed and recorded"), placeholder scores ("visual,
sensory, speech/language, motor and/or brainstem features as present in the history") and a
template impression. Specific contradictions: M01 and M07 describe a first attack while
`at_least_two_attacks` is true (M01) or the impression still concludes 1.2.1 (M07); M06 has a
"not better accounted for" criterion set false while concluding 1.2.1; P03 records an aura of 20 min
while concluding migrainous infarction.

Fix: rewrite the output as a structured clinical assessment of this patient.
- findings: one line per ICHD-3 element with the patient's own data (attack count, aura type and
  duration in minutes, spread, succession, laterality, positive symptoms, headache timing, previous
  identical attacks), the examination today, and a red-flag line that names which SNNOOP10 flags are
  present or absent for this patient (for example "age over 50 at first aura: present").
- scores or structured fields: the six C criteria each true or false with the count, A (attack
  count), and a final `criteria_met` that agrees with them.
- impression: what the assessment establishes (the ICHD-3 code it supports, or "probable" for one
  attack) and which mimic features are absent. No management, no imaging conclusion, no results of
  other modalities.
Do not copy HPI sentences: restate as clinician findings.

### B. Literature outputs echo the key, are empty or invent sources (all)

What: the initial or follow-up literature output is the ICHD-3 template whose summary equals
`expected_evidence` (guard failures above); follow-ups with `query: ""` and no content (P04 WMH, P08
two, P09 two, RS11, S02 diary, S05, S10 two); the `query` field set to the trigger slug;
patient-specific conclusions ("Patient was correct to stop", "CONCLUSION: sumatriptan appropriate");
invented references (P05 "Giles 2010" title, "Cammermans 2015", "Olesen 2018"; P02 "REDUCE-AF";
P06 invented titles; P07 invented Broderick paper; P03 "EHF 2022 guidelines"); wrong facts ("WHO
category 3-4" in S01 and S02; migrainous infarction "1.4.1" in P07; P03 literature calls triptans
"cautious use acceptable" after infarction while its drug output says contraindicated).

Fix (ROUND_POLICY 5): delete empty follow-ups. Keep at most one or two literature follow-ups per
case with a real question as trigger and `query` set to a natural query string; their output gives
general evidence with real citations from 1.1 and no patient conclusion. P02 alcohol and AF: the
real trial is Voskoboinik A et al., NEJM 2020;382:20-28 (abstinence reduced AF recurrence, 53% vs
73%). Remove the literature block from `initial_tool_outputs` when its text is the template; the
library or a follow-up answers. Literature follow-ups go last in `followup_outputs`.

### C. Drug-check outputs are empty, generic or wrong (all)

What: the criterion uses `{"context": ...}`, which no agent can send (`drug` is the required schema
parameter, and `_contains_required` compares exact folded strings), so a required drug check is
unattainable for a real agent; initial `drug_interactions` "general" blocks whose summary is the
expected text (M05, M07, P01, P02, P04, P07); summary-only blocks with empty `interactions`,
`contraindications` and `warnings`; fallback outputs that say "agent not specified". Wrong content:
M05 "avoid HRT containing oestrogen" (class H); M07 indometacin advice unrelated to the case; S04
claims a sumatriptan-propranolol interaction (none exists; the label adjustment is for rizatriptan);
M03 cites an LDL of 148 that is nowhere in the case.

Fix: criterion alternatives are `{"drug": "<name>"}` for each plausible name the agent could send
(generic name of the drug the case turns on, the patient's current drug as written in `patient`,
the brand if the case uses one; folded strings, e.g. "ethinylestradiol", "combined oral
contraceptive", "Microgynon"). The follow-up trigger tokens include those drug names so any of them
reaches the stored output. The stored output fills `interactions`, `contraindications` and
`warnings` with real content consistent with `patient` (medications, allergies, renal function) and
cites its source; summary one or two sentences, never the expected text. Tier by ROUND_POLICY 6,
case by case in section 4. Pathway position: after the diagnostic core, before literature.

### D. Engineering text in the ground truth (all)

What: `key_clinical_evidence` contains "July 2026 review applied end to end..." in all 30 cases and
"Tier per the July 2026 clinical review..." in many; some rationales say the same.

Fix: delete these sentences wherever they appear (key evidence, rationales, assessment). Log the
removal once per case.

### E. Red herrings point at nothing (most)

What: empty `location` or `field_path`; duplicates of the first entry with different wording; red
herrings citing data absent from the case: PFO or bubble echo (M02, S02, S09; P02 TOE), WMH or an
MRI finding in cases with no MRI output (S01 key evidence, S02, S03, S05, S06, S07, S08, S10, S11),
LDL or lipids (M03, M05), ECG, LVH or Holter (M07), thrombophilia (M02), CSF, antibodies, HSV PCR,
72-hour MRI and MRV (RM11), EEG (RS11, M01 differential), lactate (RS11).

Fix: each red herring names a real `field_path` whose text contains the misleading datum; delete
duplicates and entries whose data does not exist; do not invent data to keep a red herring alive.
If a case loses all red herrings, keep none rather than a fake one. A mimic left in the differential
needs its excluding feature in `key_features` (ROUND_POLICY 7).

### F. Differential not updated after the work-up (P01, P02, P03, P04, P05, P06, P08, RM11, S11)

What: P01 TIA high and GCA moderate after a normal MRI, normal ESR/CRP and a typical aura history;
P02 cardioembolic TIA high; P03 cardioembolic stroke high and PFO moderate after normal monitoring
and echo; P04 CADASIL moderate after NOTCH3 negative; P06 "migraine with aura" high when the label
is CADASIL; P08 sporadic hemiplegic migraine high when the label is MELAS; P05 TIA moderate;
RM11 familial hemiplegic migraine moderate with no family history; S11 medication-overuse headache
high when the label is migraine with aura at risk of overuse.

Fix: re-grade at assessment time: excluded mimics `low` (or removed) with the excluding result in
`key_features`; the labelled entity is not in its own differential.

### G. "Normal DWI excludes TIA" (M01, M02, M06, P01, P05, S09 and any other hit)

Fix: replace with the facts in 1.2 (DWI excludes infarction, the clinical features distinguish aura
from TIA). Canonical prohibition where the case has a TIA-versus-aura question:

> Do not start antiplatelet or anticoagulant therapy for presumed TIA: the episodes have the
> features of migraine aura (positive symptoms spreading over minutes, succession of symptoms,
> previous identical attacks) and imaging shows no infarct.

### H. HRT wrongly prohibited (M05, P01, P05)

Fix: delete the HRT prohibition. Where the patient has menopausal symptoms, the must is:

> If HRT is wanted for menopausal symptoms, migraine with aura is not a contraindication: prefer
> transdermal oestradiol at the lowest effective dose, with micronised progesterone or a
> levonorgestrel IUS for endometrial protection, and review if the aura changes (NICE NG23).

### I. Boilerplate prohibitions (about 25 cases)

What: "Do not co-administer triptans with ergotamines" when the patient takes no ergot; the combined
pill prohibition copied into cases where it does not apply.

Fix: delete the ergot line unless an ergot is in the medication list or the plan. Keep the combined
pill prohibition only in women of reproductive age (canonical: "Do not continue or start combined
hormonal contraception (pill, patch or ring): migraine with aura is UKMEC category 4; offer a
progestogen-only method or an IUD."). Case-specific triptan avoidance stays (P03, P07, P08, M03,
P09, RM11, RS11, M04).

### J. Musts that are diagnostic tests, or contradict the tiers (M01, M03, M04, M06, M07, M08, P01, P02, P05, P08, P09, RM11, RS11)

What: "Brain MRI/MRA required..." musts in cases where MRI is recommended or optional; P01
"prolonged monitoring and ESR" musts; P05 "obtain prolonged cardiac monitoring" with no criterion;
RM11 "genetic panel" must; P08 "ECG" must.

Fix: a diagnostic test is a criterion, not a must. Delete musts that duplicate or contradict a
criterion. Where the test is a follow-up plan the agent cannot order now (genetic testing in RM11
when no vocabulary term exists, section 5), keep it as a referral must ("Refer to clinical genetics
for hemiplegic migraine gene testing (CACNA1A, ATP1A2, SCN1A, PRRT2)").

### K. Vessel imaging inside brain MRI reports (M01..M08, P01, P02, P03, P05, P07, P09, RM11, RS11)

What: MRA or MRV findings embedded in brain MRI impressions (Kind 1 leakage, and it gives a vessel
study for free); M07 reports T1 post-gadolinium while the call has `contrast: false`; several brain
MRI structured findings are empty while the impression lists WMH.

Fix: strip angiography and venography text from every brain MRI report; make structured findings
agree with the narrative; fix contrast statements to the parameters the report answers (a
`contrast: false` report has no post-contrast sequences). Where vessel imaging is indicated, add a
separate `order_advanced_imaging` criterion and follow-up:
- `MR_angiography` required: P03, P07, P09.
- `MR_angiography` recommended: M03, M07, P01, P02, RS11 (delete their "routine MRA is waste"
  avoided action where present: M03, P01).
- `MR_venography` required: RM11 (cortical oedema and seizure on combined pill: CVT exclusion).
- Elsewhere no vessel study and the MRA text simply goes.

### L. Lab placeholders (P01, P03, P07, P08, RM11)

What: "Within reference range" with no values, units or ranges; panels named in the criterion not
answered by the output (P03 antiphospholipid, RM11 lactate).

Fix: real values with units and ranges, plausible for the patient, `is_abnormal` consistent. P03
and P07 antiphospholipid: lupus anticoagulant negative (dRVVT ratio), anticardiolipin and
anti-beta2-glycoprotein I IgG and IgM below 20 units. RM11 lactate normal (for example 1.3 mmol/L)
because the label is hemiplegic migraine, not MELAS.

### M. Fallback junk (most)

What: `fallback_tool_outputs.specialized_test` keyed "general_laboratory_panel",
"Neurodiagnostic assessment", "" or "general_neurodiagnostic_assessment";
`fallback_tool_outputs.advanced_imaging` keyed "MRA head and neck", "MRA" or "".

Fix: set these fallback entries to null so the library answers per parameter value. Keep a fallback
only when it is a correct normal report for this patient for a real vocabulary value.

### N. Citations (all)

Duplicates, free text and misuse, as in 1.1. `[Holland_2012]` for oral preventives becomes
`[Silberstein_2012]` (or the rationale text until CENTRAL adds it); `[Charles_2017]` for PFO is
deleted (PFO evidence is the trials in 1.1).

### O. Consults disguised as tests (P04, P06)

What: genetic counselling as `order_specialized_test`.

Fix: remove the criterion; add the must "Offer genetic counselling before NOTCH3 testing, covering
implications for relatives and the option not to test" (P04, before the test; P06, for relatives
after the result). P04: counselling precedes testing in the narrative too.

### P. Preventive therapy thresholds (S01, M01, M07, S10, M04, M06)

Fix: musts follow 1.2 (AHS 2021). S01, M01, M07: no preventive must; a must to keep a headache diary
and reassess. S10 (MIDAS IV) and M04, M06: preventive must with an agent chosen for the patient
(class Q).

### Q. Topiramate and valproate in women who can become pregnant (M06, RM11, S10 and any other woman of reproductive age with these drugs)

Canonical must when topiramate is proposed:

> If topiramate is chosen, start it only with highly effective contraception (copper or hormonal
> IUD, or implant) under the topiramate pregnancy prevention programme; it reduces the efficacy of
> oral and progestogen-only pills.

Valproate is not offered for prevention in these women.

---

## 3. Target pathway and tiers

### 3.1 Pathway order (followup_outputs and action_criteria)

1. Structured headache history and examination (`action-3-perform-clinical-assessment`, required
   in all).
2. Diagnostic imaging where indicated: brain MRI (`action-4-analyze-brain-mri`), then vessel imaging
   (MRA or MRV, class K).
3. Staging and confirmatory studies: labs, EEG (RM11), cardiac monitoring and echo (P02, P03, P07),
   MR spectroscopy (P08), genetic tests (P04, P06, P08), neuropsychology (P06).
4. Pre-treatment safety: drug check (`action-2-check-drug-interactions`).
5. Literature (`action-1-search-medical-literature`), optional, last.

Keep criterion ids unchanged when moving them. New ids: `action-mra`, `action-mrv`,
`action-mtdna-test`, `action-ecg` (P08), `action-labs-esr-crp` (P01 if relabelled), each
descriptive.

### 3.2 Criteria rules

- `action-3` structured history: required, `{"assessment_type": "structured_headache_history_ichd3"}`.
- Brain MRI: `required_arguments: {}` (any brain MRI answers the red-flag question; the current
  `{"contrast": false, "protocol": "standard"}` misses an agent that asks for contrast or the stroke
  protocol). Tier per section 4.
- Literature: tier `optional`, `required_arguments: {}`, moved last. Never in the stop rule.
- Drug check: `{"drug": ...}` alternatives (class C), tier per section 4: required only with the
  concrete issue named there.
- Avoided actions: keep the CT, CSF, routine echo, routine monitoring and EEG waste entries where
  section 4 does not make that study a criterion; delete an avoided action that matches a criterion
  of the same case (M03 and P01 MRA, class K). P05 TOE "harm" becomes waste (a TOE is not harmful at
  a corrected INR; it is not indicated).

### 3.3 Sequence constraints (all soft; no hard constraint in this condition)

- `action-3-perform-clinical-assessment` before `action-4-analyze-brain-mri` in every case with an
  MRI criterion (history defines the red flag that justifies imaging).
- Brain MRI before vessel imaging where both are criteria (P03, P07, P09, RM11; recommended pairs
  are not constrained).
- Brain MRI before echo and cardiac monitoring (P03, P07).
- Brain MRI before genetic testing (P04, P06, P08).
No constraint involves the literature or drug criteria.

### 3.4 Stop rule

- `required_before_assessment`: the required criteria only (never literature, never an optional or
  recommended criterion).
- `max_additional_actions`: 0 in S cases (typical aura, one or two actions suffice); 1 in M, P, RM
  and RS cases (one reasonable extra study).

### 3.5 Tier table (target)

| case | MRI | vessel | other diagnostic | drug check |
| --- | --- | --- | --- | --- |
| M01 | recommended (first aura, urgent TIA referral) | none | none | required (combined pill) |
| M02 | optional | none | none | required (combined pill) |
| M03 | recommended (motor aura) | MRA recommended | none | required (triptan avoidance) |
| M04 | recommended (brainstem aura) | none | none | required (combined pill; triptan avoidance) |
| M05 | recommended (new aura without headache at 48) | none | none | optional |
| M06 | recommended (prolonged aura) | none | none | required (combined pill; topiramate) |
| M07 | recommended (first attack, confusion) | MRA recommended | none | optional |
| M08 | optional | none | none | required (sertraline plus triptan) |
| P01 | required (first aura at 52, aphasia) | MRA recommended | ESR/CRP recommended | optional |
| P02 | recommended | MRA recommended | ILR required (keep) | required (apixaban plus NSAID; stop apixaban) |
| P03 | required (repeat MRI) | MRA required | labs recommended (aPL); 30-day monitor required; bubble echo required | required (triptans after infarct) |
| P04 | recommended (WMH re-review) | none | NOTCH3 required | optional |
| P05 | recommended | none | prolonged monitoring recommended (new) | required (warfarin) |
| P06 | recommended | none | NOTCH3 required; neuropsych recommended | recommended (triptan caution, EAN 2020) |
| P07 | required | MRA required | ILR required; echo required (fix type, 4); labs optional | required (aspirin to DOAC) |
| P08 | required | none | mtDNA test required (new); MRS recommended; TTE required; ECG recommended (new); lactate in labs recommended | required if the plan has an anticonvulsant or preventive, else recommended |
| P09 | required | MRA required | none | required (triptan avoidance; aneurysm) |
| RM11 | required | MRV required | video EEG required; labs recommended | required (combined pill plus topiramate) |
| RS11 | recommended | MRA recommended | none | required (triptan avoidance) |
| S01 | none | none | none | optional |
| S02 | none | none | none | optional (no hormonal contraception listed) |
| S03 | none | none | none | optional |
| S04 | none | none | none | optional (no real interaction; class C fix) |
| S05 | none | none | none | optional |
| S06 | none | none | none | required (lactation) |
| S07 | none | none | none | required (combined pill) |
| S08 | none | none | none | optional |
| S09 | none | none | none | optional |
| S10 | none | none | none | recommended (preventive choice) |
| S11 | none | none | none | required (rizatriptan with propranolol) |

---

## 4. Per-case index

Every case: classes A, B, C, D, M, N and 3.2-3.4 apply. Only the further classes and decisions are
listed.

### M cases

- **M01** (35 F, first sensory aura with headache, on combined pill, urgent GP TIA referral).
  Label "First-episode migraine with sensory aura (ICHD-3 1.2.1)" codes a single attack as 1.2.1;
  ICHD-3 requires two. Change `accepted[0]` to "Probable migraine with aura (ICHD-3 1.5.2), first
  sensory aura; combined pill to stop (UKMEC 4)" and keep `icd_codes[0]` G43.109; log it and list it
  under CENTRAL (synonym). Alternatively, if the HPI already records an earlier identical attack,
  keep the label and make `at_least_two_attacks` true consistently; choose by the HPI and log why.
  Classes E (EEG in differential), G, I, J (MRI must), K, P. MRI recommended. Drug check required:
  `{"drug": ...}` alternatives for her pill as written in `patient` plus "ethinylestradiol" and
  "combined oral contraceptive". Differential: TIA low with the excluding features; keep focal
  seizure, AVM and MS very low only if `key_features` say why.
- **M02** (29 F, visual plus sensory aura, combined pill). Label clause "small PFO, no closure
  indicated" has no supporting data (no echo in the case, and routine echo is not indicated). Remove
  the PFO clause from `accepted[0]` only if CENTRAL agrees (it is a management clause, not the
  entity); default: keep `accepted[0]` unchanged, delete PFO and thrombophilia red herrings and PFO
  text elsewhere, and list the label clause under CENTRAL. Do not add an echo. Classes E, G, I, K.
  MRI optional. Drug check required (combined pill).
- **M03** (42 M, first motor aura after previous visual auras; probable sporadic hemiplegic
  migraine). Remove the LDL 148 from the drug output and red herrings (PMH says no hyperlipidaemia).
  Review the empirical aspirin in the plan: no antiplatelet for hemiplegic migraine without infarct
  (class G prohibition text). Classes E, G, I (keep triptan avoidance specific to hemiplegic
  migraine), J, K. MRI recommended; MRA recommended (new; delete the MRA waste avoided action).
  Drug check required: triptans avoided in hemiplegic migraine (`{"drug": "sumatriptan"}`, and any
  triptan in `patient`). Must: genetic referral if a second episode or family history (plan, not a
  test).
- **M04** (33 F, brainstem aura, combined pill, preventive indicated). Label correct. The propranolol
  must is garbled: rewrite as one checkable must (dose, contraindications checked: asthma,
  depression). Triptan avoidance for brainstem aura per 1.2. Classes I, J, K, P, Q (if topiramate is
  in the plan). MRI recommended. Drug check required (combined pill, triptan).
- **M05** (48 F, new typical aura without headache, established migraine with aura, perimenopausal).
  Classes E (LDL), H (HRT prohibition goes; HRT must if symptoms), I, K. The drug output saying
  "avoid HRT containing oestrogen" is rewritten (class C). Differential: TIA low, with the features
  that distinguish acephalgic aura (positive symptoms, march over minutes, identical earlier auras).
  CENTRAL: synonyms "typical aura without headache", "acephalgic migraine" in the G43.109 group.
  MRI recommended. Drug check optional (no current interacting drug) unless HRT is in the plan, then
  recommended. Guard leak: fix the initial drug block.
- **M06** (31 F, aura over 60 min in some attacks, combined pill, preventive indicated). Fix the
  "not better accounted for" criterion contradiction (class A). Migrainous infarction "excluded by
  normal DWI" is right (DWI excludes infarction), but the differential cites migrainous infarction as
  1.4.1: it is 1.4.3; persistent aura is 1.4.2. Classes G, I, J, K, P, Q (preventive phrasing with
  contraception). MRI recommended. Drug check required (combined pill; topiramate if chosen).
- **M07** (27 M, single exercise-triggered attack with visual aura and confusion). Single attack:
  label to "Probable migraine with aura (ICHD-3 1.5.2), exercise-triggered visual aura; no structural
  cause" with `icd_codes[0]` unchanged; log and CENTRAL (same as M01). "Confusional aura" is not an
  ICHD-3 aura type: describe confusion as an accompanying feature and keep the brainstem-aura
  question explicit (decreased consciousness alone is one brainstem symptom; two are needed). Fix
  the T1 post-gadolinium contrast contradiction (class K). Delete the indometacin drug content and
  ECG, LVH and Holter red herrings (class E). Exercise-triggered first headache with confusion: MRA
  recommended (RCVS and dissection exclusion). Classes E, J, K, P. Guard leak: initial drug block.
  Drug check optional.
- **M08** (38 F, visual and sensory aura unmasked after sertraline; sertraline plus sumatriptan).
  Delete the MRI must (MRI optional). Drug check required: sertraline with sumatriptan, the output
  states the low serotonin syndrome risk and counselling (1.2), and the label clause about
  co-administration must agree with that (allowed with counselling). Classes I, J, K.

### P cases

- **P01** (52 F, first aphasic aura at 52, postmenopausal). Late-onset first aura: MRI required.
  Classes F (TIA and GCA low after normal MRI, ESR and CRP), G, H (HRT prohibition goes), I, J
  (delete prolonged-monitoring and ESR musts that have no criterion; ESR/CRP is the labs
  criterion), K, L. Labs: keep `action-5-interpret-labs` recommended with panels ESR, CRP,
  glucose, HbA1c, lipid panel answered with real values. MRA recommended (new); delete the MRA waste
  avoided action. She takes aspirin 75 mg and atorvastatin 20 mg: if the HPI says they were started
  for presumed TIA, the must is to stop aspirin (class G text) and review the statin by her own
  cardiovascular risk (not by the TIA label). Guard leak: initial drug block. Drug check optional (recommended if HRT is in the plan).
- **P02** (44 M, aphasic aura plus paroxysmal AF, alcohol-related, on apixaban, ILR shows nocturnal
  AF dissociated from the aphasic episodes). CHA2DS2-VA 0: anticoagulation is not indicated (ESC
  2024); the must is to stop apixaban after review, treat AF triggers (alcohol reduction) and
  rate or rhythm control per cardiology. 12-15 units a week is moderate, not heavy, drinking: fix
  every "heavy alcohol" claim. Delete the PFO and TOE claims and the GGT/ALT values that are not in
  the labs (classes B, E). Drug check required: apixaban with ibuprofen or naproxen (bleeding risk)
  while still on apixaban; `{"drug": "apixaban"}`, `{"drug": "ibuprofen"}`, `{"drug": "naproxen"}`.
  Replace "REDUCE-AF" with Voskoboinik 2020 (class B). Differential: cardioembolic TIA low, with the
  ILR timing in `key_features`. MRI recommended; MRA recommended (new); ILR required (keep, after
  MRI). Guard leak: initial drug and literature blocks.
- **P03** (38 F, migrainous infarction, right occipital). The data does not support the label:
  the aura lasted 20 min. Fix the HPI so the visual aura of this attack persisted beyond 60 min
  (for example 5 hours) while previous auras lasted 20-30 min; delete the HPI paragraph that quotes
  the outside clinic MRI read (timeline leak). MRI: a repeat study at about 4 weeks (DWI no longer
  restricted, a FLAIR lesion in the right occipital cortex, comparison with the outside scan), MRA as
  a separate required study (normal intracranial and cervical vessels; class K). Cardiac monitoring
  output becomes a 30-day event monitor report (no AF, matching the criterion `event_monitor_30d`).
  Bubble echo required (cryptogenic stroke under 60: PFO assessment). Labs: aPL with real values
  (class L), tier recommended. Differential: cardioembolic stroke low and PFO-related stroke low
  (state the echo and monitor results), RCVS and dissection low (MRA). Literature: delete "EHF 2022
  guidelines" and the "cautious triptan use" text; drug output and literature agree: triptans are
  contraindicated after infarction. She takes clopidogrel plus aspirin, Cerazette and sumatriptan
  100 mg. Drug check required: `{"drug": "sumatriptan"}`, `{"drug": "clopidogrel"}`,
  `{"drug": "aspirin"}`, `{"drug": "desogestrel"}`, `{"drug": "Cerazette"}`. Musts: stop sumatriptan
  (contraindicated after stroke; NSAID plus antiemetic instead); single antiplatelet long term per
  AHA/ASA 2021, DAPT only within the short window after a minor stroke, not long term; non-vasoactive
  preventive; contraception review (progestogen-only pill after stroke is UKMEC 3 to continue, copper
  IUD UKMEC 1: confirm the category against UKMEC before writing it). ICD: section 6 (G43.609). Synonyms: CENTRAL (the I63 group gives "cardioembolic stroke"
  and "lacunar stroke", which would credit the wrong mechanism). Sequence: MRI before MRA, echo and
  monitoring.
- **P04** (34 F, typical visual aura, WMH, family history; CADASIL excluded by NOTCH3). Make the
  family history a second-degree relative consistently (fix the must that says first-degree, or the
  HPI, so they agree). Remove the variant of uncertain significance (it contradicts "excluded");
  NOTCH3 output: no cysteine-altering variant in exons 2-24. Genetic counselling: remove the
  specialized-test criterion and add the class O must, placed before testing; the risk to children
  is not "none" until the result is known. MRI output is a formal re-review of the outside scan
  (WMH pattern: punctate frontal subcortical, no anterior temporal or external capsule involvement);
  drop the HPI radiology quote. Delete the empty WMH literature follow-up. Differential: CADASIL low
  after NOTCH3 negative. Guard leak. Drug check optional.
- **P05** (46 F, aphasic aura misdiagnosed as TIA, on warfarin with supratherapeutic INR and
  bleeding). 46 with regular cycles is not "postmenopausal": fix every occurrence (perimenopausal
  only if the HPI supports it). Delete the HRT prohibition (class H). TOE avoided action: harm to
  waste. Add `action-prolonged-monitoring` recommended (`order_cardiac_monitoring`, 14-day patch or
  30-day event monitor) only if the HPI keeps an unexplained palpitation or AF question; otherwise
  delete the "obtain prolonged monitoring" must (class J). Choose by the HPI and log. Delete the
  invented references (Giles 2010, Cammermans 2015, Olesen 2018). Drug check required: warfarin
  with paracetamol (INR rise at regular doses) and any NSAID; must: stop warfarin with INR reversal
  per bleeding severity (vitamin K), no antithrombotic for presumed TIA (class G). Differential:
  TIA low.
- **P06** (58 M, CADASIL with aphasic aura and early cognitive impairment, NOTCH3 R182C). Label
  kept (section 6). Genetic counselling becomes a must for relatives (class O). Neuropsychology:
  `test_type` must be `neuropsych_battery` in both criterion and output. Delete the HPI radiology
  leak (anterior temporal pole and external capsule WMH stated in the HPI while MRI is a criterion).
  Triptans: EAN 2020 CADASIL guideline advises avoiding triptans and vasoconstrictors; write it so
  (drug check recommended, `{"drug": "sumatriptan"}`). Delete invented literature titles. The
  differential's "migraine with aura" high goes (class F): the aura is a CADASIL manifestation.
- **P07** (41 F, cardioembolic right PCA-territory infarct during a migraine attack; paroxysmal AF
  on ILR; aspirin to DOAC). Chief complaint says "right eye" while the deficit is a left homonymous
  hemianopia: fix to "left visual field". Echo: the criterion asks `bubble_study` while the output is
  a TOE: make them agree (bubble TTE is the first study; a TOE is reasonable after a cryptogenic
  stroke; choose one and match criterion, output and trigger). MRA required (new, class K). Drug
  check required: `{"drug": "apixaban"}`, `{"drug": "rivaroxaban"}`, `{"drug": "edoxaban"}`,
  `{"drug": "dabigatran"}`, `{"drug": "aspirin"}`; output covers stopping aspirin when the DOAC
  starts and the combined pill if present. Migrainous infarction is 1.4.3 (not 1.4.1): fix. Delete
  the invented Broderick citation. Musts: DOAC per ESC 2024 (CHA2DS2-VA with stroke is at least 2);
  timing of DOAC start by infarct size. Synonyms: CENTRAL (restrict to cardioembolic and ischaemic
  stroke; plain "stroke" and "lacunar stroke" go). Guard leak.
- **P08** (29 F, MELAS, m.3243A>G; stroke-like episodes misdiagnosed as hemiplegic migraine). The
  data does not support MELAS (brief episodes, normal MRI, spectroscopy of an "affected territory").
  Fix the data, not the label: the latest episode is prolonged (days) with a residual left
  homonymous field defect; MRI shows a right parieto-occipital cortical stroke-like lesion that
  crosses vascular territories, with cortical DWI hyperintensity and no matching ADC drop pattern
  typical of arterial infarction; MR spectroscopy shows a lactate doublet in the lesion and in normal
  appearing cortex; serum lactate raised (for example 4.1 mmol/L, range 0.5-2.2). Add
  `action-mtdna-test` required with alternatives `interpret_labs {"panels": ["m3243A_G_mtDNA"]}`
  and `order_specialized_test {"test_type": "genetic_panel:mitochondrial"}` (urine or buccal
  heteroplasmy preferred to blood; the output states the sample and heteroplasmy level). The labs
  criterion keeps lactate and CK (recommended). TTE required (cardiomyopathy screening, MMS 2017);
  ECG recommended (new `action-ecg`, pre-excitation and conduction disease); delete the ECG must.
  MRS recommended. She takes only ibuprofen. Drug check required when the plan contains an
  anticonvulsant or preventive (valproate contraindicated in mitochondrial disease, POLG and MELAS;
  topiramate caution for acidosis; metformin avoided), otherwise recommended; alternatives
  `{"drug": "valproate"}`, `{"drug": "sodium valproate"}`, `{"drug": "topiramate"}`,
  `{"drug": "levetiracetam"}`. Musts: L-arginine in acute stroke-like episodes per MMS 2017 consensus
  (state it as consensus, low evidence), audiology and diabetes screening, genetic counselling for
  maternal relatives. Differential: sporadic hemiplegic migraine low (class F). Delete both empty
  literature follow-ups. Guard leak. Sequence: MRI before the mtDNA test.
- **P09** (36 M, probable sporadic hemiplegic migraine with an incidental 4 mm left MCA bifurcation
  aneurysm; "familial intracranial aneurysm", "MRA screening"). "Familial" and screening need two or
  more affected first-degree relatives (AHA 2015): add a second first-degree relative with an
  intracranial aneurysm to the family history, or remove "familial" and the screening claim from the
  data; prefer adding the relative (the label names it) and log. MRA as a separate required study
  (class K): the aneurysm finding moves from the brain MRI report to the MRA report. Musts: BP
  control, smoking cessation, neurovascular referral for a 4 mm aneurysm (PHASES-based surveillance),
  triptan avoidance (hemiplegic migraine). Delete the two empty literature follow-ups. Drug check
  required (triptan avoidance; `{"drug": "sumatriptan"}` and the patient's antihypertensive).
  Classes I, J, K. Guard leak.

### R cases

- **RM11** (26 F, sporadic hemiplegic migraine with migralepsy, reversible MRI changes, on combined
  pill Mercilon and topiramate 75 mg). MRV required (new `action-mrv`; cortical oedema with a seizure on the combined pill requires
  CVT exclusion; output normal venous sinuses). EEG: the video EEG output shows left hemispheric
  slowing without epileptiform discharges (right hemiparesis implies left hemisphere; check the
  laterality in `patient` and match). Labs: real values including lactate normal (class L),
  recommended. Delete the CSF claims, antibody, HSV PCR and 72-hour MRI red herrings that have no
  output (class E). Differential: familial hemiplegic migraine low (no family history), CVT low (MRV),
  MELAS low (lactate). Stop the combined pill (Mercilon) and use highly effective contraception
  if topiramate or another teratogenic preventive is chosen (class Q); lamotrigine or verapamil are
  alternatives. Genetic test: a referral must (class J; no vocabulary term, section 5). Literature
  criterion stays optional. Drug check required (combined pill; topiramate with the pill). Guard leak.
- **RS11** (39 M, sporadic hemiplegic migraine, two episodes). MRI optional to recommended (motor
  aura is a red flag). MRA recommended (new). The NSAID is named meloxicam in one field and
  loxoprofen in another: use the one in the medication list everywhere. Fix the laterality of the
  mouth symptom to match the hemibody side. Delete lactate, EEG and Holter claims (class E). Delete
  the empty literature follow-up. Drug check required (triptan avoidance). Guard leak.

### S cases

- **S01** (28 F, typical visual aura about once a month). No preventive must (class P); diary and
  acute plan (NSAID or triptan at headache onset). Delete the WMH key evidence (no MRI in the case).
  "WHO category 3-4" becomes "UKMEC category 4" (if she uses combined contraception the prohibition
  stays; otherwise delete it). Drug check optional. Stop rule max 0.
- **S02** (32 F, sensory aura, menstrually related). Delete PFO and WMH red herrings, the empty
  diary literature follow-up and "category 3-4" (she lists no hormonal contraception; a
  counselling must about combined methods is fine). Drug check optional. Guard leak.
- **S03** (24 F, typical visual aura). Delete the MRI or WMH red herring. Classes I. Drug check
  optional.
- **S04** (35 F, typical visual aura, stage 1 hypertension on lifestyle measures, takes sumatriptan;
  propranolol proposed as preventive). The literature output claims propranolol raises sumatriptan
  levels about 70% by CYP2D6: wrong (that is rizatriptan, via MAO-A, and sumatriptan has no such
  interaction). Delete it; the drug output states sumatriptan needs no dose change with propranolol
  and triptans are contraindicated only in uncontrolled hypertension. The preventive must cites
  `[Silberstein_2012]`, not `[Holland_2012]` (class N), and checks propranolol cautions (asthma,
  depression). Drug check optional.
- **S05** (22 F, new-onset typical visual aura). Delete the empty literature follow-up and the MRI
  red herring. No imaging (typical aura, normal examination). Guard leak. Drug check optional.
- **S06** (30 F, postpartum exacerbation, breastfeeding). The "doubly contraindicated" combined
  pill wording becomes 1.2 (UKMEC 4 from the aura at any time; under 6 weeks postpartum while
  breastfeeding also 4). Drug check required: lactation safety of the acute and preventive drugs
  (sumatriptan compatible; ibuprofen compatible; amitriptyline at low dose compatible; source
  LactMed). Delete the MRI red herring.
- **S07** (40 F, established aura on Yasmin and rizatriptan). Drug check required (combined pill:
  stop, switch to progestogen-only or IUD); alternatives `{"drug": "Yasmin"}`,
  `{"drug": "ethinylestradiol"}`, `{"drug": "drospirenone"}`, `{"drug": "combined oral contraceptive"}`. Delete the WMH red herring. Classes I.
- **S08** (26 F, untreated, triptan-naive). Delete the MRI red herring. Drug check optional (triptan
  start with no interacting drug). Acute plan: triptan at headache onset, not during the aura.
- **S09** (38 F, previous "TIA query" that was aura). Class G (TIA text), delete the PFO red herring.
  Drug check optional, unless an antiplatelet started for the presumed TIA is in `patient` (then
  stop-aspirin must and drug check recommended).
- **S10** (34 F, MIDAS IV, preventive indicated). Delete the two empty literature follow-ups;
  preventive must per 1.2 with class Q if topiramate; drug check recommended. Guard leak.
- **S11** (45 M, typical aura, co-codamol overuse risk, on amlodipine and rizatriptan 10 mg;
  topiramate or propranolol proposed). Drug check required: if propranolol is the preventive,
  rizatriptan drops to 5 mg (label); `{"drug": "rizatriptan"}`, `{"drug": "propranolol"}`,
  `{"drug": "topiramate"}`. Codeine withdrawal must stays. Preventive citation `[Silberstein_2012]`.
  Medication overuse thresholds per 1.2 (combination analgesic on 10 or more days a month);
  differential: medication-overuse headache graded by the days of use in the HPI (low or moderate,
  not high, if under 10 days a month). Delete the WMH red herring.

---

## 5. CENTRAL requests (outside the case files)

1. Synonyms (`diagnosis_synonyms.yaml`):
   - G43.109 group: drop "migraine aura" (its tokens are a subset of "migraine without aura", so a
     wrong diagnosis is credited). Add "probable migraine with aura" for M01 and M07 (or a
     G43.109-scoped entry if the label changes as in section 4), and "typical aura without
     headache", "acephalgic migraine" (M05).
   - New G43.609 group for migrainous infarction (P03): labels "migrainous infarction",
     "persistent migraine aura with cerebral infarction"; codes G43.609, G43.6, G43.619. P03 must
     not receive the I63 group's "cardioembolic stroke", "lacunar stroke" or "stroke".
   - P07: restrict to "cardioembolic stroke", "cardioembolic ischaemic stroke", "ischaemic stroke";
     drop "lacunar stroke" and plain "stroke" (already noted under "Synonym prune effects" in
     CENTRAL_PENDING.md: apply with this condition).
2. Vocabulary (`costs.yaml`, `tool_io.py` mirror, library): `genetic_panel:hemiplegic_migraine`
   (CACNA1A, ATP1A2, SCN1A, PRRT2) for M03, RM11, RS11, P09. Until it exists the test is a referral
   must.
3. Criteria pack `dataset-generation/criteria_packs/MIG-AURA.md`: literature and drug check no
   longer required (ROUND_POLICY 5, 6); allow-list additions: `[AHS_2021]`, `[Silberstein_2012]`,
   `[AHS_neuroimaging_2020]`, `[NICE_CG150]`, `[UKMEC_2016]`, `[WHO_MEC_2015]`, `[NICE_NG23]`,
   `[MHRA_topiramate_2024]`, `[EHF_EAN_2021]`, `[PREMIUM_2017]`, `[PRIMA_2016]`, `[MIST_2008]`,
   `[ESC_AF_2024]`, `[AHA_ASA_2021_secondary]`, `[AHA_UIA_2015]`, `[EAN_CADASIL_2020]`,
   `[MMS_2017]`, `[Voskoboinik_2020]`. Confirm whether the pack key is `[Sacco_2022]` or
   `[Sacco_2017]` and what it cites.
4. Labels changed or questioned (log here when applied): M01 and M07 to probable migraine with aura
   (1.5.2); M02 "small PFO" clause unsupported; P03 `icd_codes[0]` (section 6). Labels that carry
   management clauses ("combined OCP requires immediate discontinuation", "BP optimisation
   critical", "switch aspirin to DOAC") are long but not wrong: optional cleanup, no change this
   round.
5. Guidance claims (`condition_tool_guidance.yaml`): after the round, P03, P07, P08 keep echo; P08
   gains ECG; RM11 gains MRV; MRA becomes a separate study in P01, P02, P03, P07, P09, M03, M07,
   RS11. Refresh the guidance claims so the review app shows these.

---

## 6. Open questions for Andrea

1. Composition (open since July): P06 (CADASIL), P07 (cardioembolic stroke) and P08 (MELAS) are
   mimic cases labelled with another entity under MIG-AURA. Default: keep them as mimic cases with
   their own labels. Alternative: move them to the stroke or genetic conditions in a later round.
2. P03 `icd_codes[0]` is I63.9 for migrainous infarction; ICD-10-CM codes it G43.609 (persistent
   migraine aura with cerebral infarction) with I63 as an additional code. Default this round: keep
   I63.9 first (ROUND_POLICY 3) and add G43.609 to the codes; change the first code only if you
   rule it wrong.
3. M01 and M07: relabel single attacks as probable migraine with aura (1.5.2), or rewrite the HPI to
   add a previous identical attack and keep 1.2.1? Default: relabel when the HPI says first attack
   (keeps the case faithful to its story).
4. S cases have no MRI criterion and a stop rule of 0, so an MRI already costs the stopping score.
   Should a typical-aura S case also carry an MRI waste avoided action (AAN Choosing Wisely)?
   Default: no, to stay within the July ruling (MRI optional for red flags).
5. P02 (CHA2DS2-VA 0, alcohol-related AF): stopping apixaban follows ESC 2024; confirm the
   reviewers accept the must, since the patient was anticoagulated by another team.
6. Triptans with SSRI (M08): the case label treats co-administration as an issue. Default: allowed
   with counselling (low risk), and the label clause is read so.
