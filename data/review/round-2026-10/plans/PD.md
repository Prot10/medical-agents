# PD: condition plan for the October 2026 review round

This is the lead plan for the 30 PD cases (M01..M05, P01..P04, RM01..RM05, RP01..RP05, RS01..RS05, S01..S06). Workers follow it case by case, so that every case reaches the same decision for the same defect. Read `ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them.

No reviewer has annotated this condition. There is no notes file and no note id to cite. Every class below comes from the lead survey of all 30 cases:

- scripts over every field (criteria, outputs, fallbacks, discriminators, shared sentences, MoCA and RBD mentions, medication lists);
- a full read of M01, M02, M03, M04, M05, P01, P02, P03, P04, RM01 to RM05, RP01 to RP05, RS01, RS03 and RS04, and the criteria, outputs, differential and evidence of the other cases;
- the MockServer routing code and the library defaults that an unstored call reaches.

Ruling 2 applies: fix each class in every case where it occurs, not only in the cases named. A worker who finds a defect this plan does not name logs it and fixes it by the closest class.

The July 2026 tool review (Reviewer 1, `condition_tool_guidance.yaml` key `parkinsons`, sources MDS criteria, NICE NG71, DGN Parkinson guideline) is the only physician input. Reviewer 1 ruled:

- MRI required (CT as the alternative: S06);
- ECG and EEG removed;
- labs optional and targeted (metabolic, toxic, infectious, Wilson, pre-treatment questions);
- EMG/NCS, RNS, biopsies, evoked potentials, autonomic and tilt testing removed;
- neuropsychology optional when cognition is clinically relevant;
- genetics optional, only for young onset, a significant family history or patient request.

Not from Reviewer 1 but decided here (generator panel and NICE NG71): neuropsychology required before DBS (RP04); polysomnography optional when dream enactment is reported and not yet PSG-confirmed; DaTscan only for a live degenerative-versus-nondegenerative differential (C8). Two departures from Reviewer 1 are argued in the case: the ECG and Holter in RP01 (syncope with known WPW: ESC 2018 requires an ECG in every syncope), and the required DaTscan where the label itself rests on it (M01, M02, M03, RM02).

## Baseline measured on 24 October 2026, before any edit

- `perfect_agent.py`: 30/30 pass. This is a false pass. The literature criteria require exact `query` strings, and the drug criteria require exact `drug` strings ("increased carbidopa-levodopa", "DBS pre-operative evaluation", "review current regimen", "carbidopa-levodopa trial reassessment"). The MRI criteria require `{"contrast": false, "protocol": "standard"}`, so an MRI ordered with no arguments scores nothing. A real agent misses all three.
- `test_case_guards` leak test fails in P02 and P03. The initial `drug_interactions` and `literature_search` outputs repeat the expected evidence (C1, C2).
- Discriminator check (`discriminator_defects` from `test_case_guards.py`, run by hand because PD is not yet in `DISCRIMINATOR_CONDITIONS`): 30/30 fail, all on `fallback_tool_outputs.echo` without `echo_type`. P03's advanced-imaging fallback says `FDG-PET`, not `FDG_PET` (not flagged, fix anyway).
- Lead re-verification (24 Oct, second pass) corrected this plan where the first pass misread the histories: M01 and M04 do report sleep-related dream enactment or limb movements (their PSG stays optional), P04 reports dream enactment (PSG added), RS01 has no stored DaTscan (one is added), and M02's hyposmia began after metoclopramide.
- Shared text measured: 76 strings of 40 characters or more are repeated verbatim in 4 or more cases (the two "July 2026" evidence lines and `metadata.revision_reason` in all 30, the MRI rationale in 29, `difficulty_rationale` in 26, the three generic musts and three generic prohibitions in 20, the generic DaTscan/PSG/neuropsych/labs `expected_evidence` and rationale in 9 to 12). Each is handled by a class below.

## How to use this plan

1. Apply every class of section 2 to your case, in order. Use the canonical text verbatim where one is given, filling the `<...>` slots from the case.
2. Apply the per-case decisions of section 4.
3. Rebuild `action_criteria`, `followup_outputs`, `avoided_actions`, `sequence_constraints` and `stop_rule` as section 3 says.
4. Run the checks of 3.6 and write `logs/<CASE_ID>.md` in the ROUND_POLICY format.

## Conventions for all new text

- English in the spelling of the field you edit; no em or en dashes; the case's units (mmHg, MoCA n/30, mg/day of levodopa).
- Never change `case_id`, `condition`, `diagnosis.accepted[0]` or `icd_codes[0]`; never hand-edit synonyms; edit only through `case_io.load/save`.
- An added result fits the case (age, sex, medicines, side of onset, other reports) and differs in its figures from other cases.
- Laterality: a DaTscan deficit is contralateral to the clinically worse side.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which guideline governs what

| Question | Source | Key |
| --- | --- | --- |
| PD: entry criterion, supportive criteria, absolute exclusions, red flags, clinically established vs probable | Postuma RB et al., Mov Disord 2015;30:1591-1601 | `[Postuma_2015]` |
| Prodromal markers (RBD on PSG, hyposmia, constipation) | Berg D et al., Mov Disord 2015;30:1600-1611 | `[Berg_2015]` |
| DaTscan in clinically uncertain parkinsonism; normal in DIP, ET and vascular parkinsonism | Marshall VL et al., Mov Disord 2009;24:500-508 | `[Marshall_2009]` |
| SWI nigrosome-1 (swallow-tail) sign | Schwarz ST et al., PLoS One 2014;9:e93814 | `[Schwarz_2014]` |
| Diagnostic pitfalls, mimics | Tolosa E et al., Lancet Neurol 2021;20:385-397 | `[Tolosa_2021]` |
| When to use DaT SPECT; first-line treatment; ICD and EDS warnings with agonists | NICE NG71 (2017) | `[NICE_NG71]` (not in the pack: CENTRAL R1) |
| MSA: clinically established and clinically probable MSA, MRI markers | Wenning GK et al., Mov Disord 2022;37:1131-1148 | `[Wenning_2022]` (CENTRAL R1) |
| DLB: core features, indicative and supportive biomarkers | McKeith IG et al., Neurology 2017;89:88-100 | `[DLB_2017]` (exists in the ALZ-EARLY pack; CENTRAL R1 adds it to PD) |
| PSP: MDS criteria, PSP-RS | Höglinger GU et al., Mov Disord 2017;32:853-864 | `[Hoglinger_2017]` (CENTRAL R1) |
| PD-MCI level I and II | Litvan I et al., Mov Disord 2012;27:349-356 | `[Litvan_2012]` (CENTRAL R1) |
| Syncope work-up, 12-lead ECG in every syncope (RP01) | Brignole M et al., Eur Heart J 2018;39:1883-1948 | `[ESC_2018]` (SYNC-CARD pack; CENTRAL R1) |
| Wilson disease screening (P04) | EASL Clinical Practice Guidelines: Wilson's disease, J Hepatol 2012;56:671-685 | `[EASL_Wilson_2012]` (CENTRAL R1) |

Use bracketed keys only. Drop every unbracketed duplicate (`"Schwarz_2014"` next to `"[Schwarz_2014]"`). Do not cite `[Gilman_2008]` or `[McKeith_2017_DLB]`. Until CENTRAL R1 lands, use the pack key that is closest and log the missing one, as NPH did.

### 1.2 Canonical facts (use these, do not restate them differently)

**F1. MDS 2015 PD categories.** The entry criterion is parkinsonism: bradykinesia with rest tremor or rigidity, or both.

- **Clinically established PD:** no absolute exclusion, at least two supportive criteria, no red flag.
- **Clinically probable PD:** no absolute exclusion; red flags allowed only if counterbalanced by supportive criteria (one red flag needs one supportive criterion, two red flags need two); never more than two red flags.
- **Supportive criteria (only these four):**
  - a clear and dramatic beneficial response to dopaminergic therapy;
  - levodopa-induced dyskinesia;
  - rest tremor of a limb on examination;
  - olfactory loss on a validated test for age and sex (UPSIT, Sniffin' Sticks), or cardiac sympathetic denervation on MIBG.
- **Not supportive:** RBD (it is a prodromal marker, [Berg_2015]), constipation, self-reported or bedside smell loss, a family history, an SWI nigrosome sign, an abnormal DaTscan.
- **Red flags used in this condition:** rapid gait progression needing a wheelchair within 5 years; recurrent falls (more than one a year) because of impaired balance within 3 years of onset; severe autonomic failure within 5 years (an orthostatic fall within 3 minutes of at least 30 mmHg systolic or 15 mmHg diastolic, or severe urinary incontinence or retention); inspiratory stridor; bilateral symmetric parkinsonism; disproportionate anterocollis; early bulbar dysfunction; no progression over 5 years; unexplained pyramidal signs.
- **Absolute exclusions used here:** cerebellar abnormalities; downward vertical supranuclear gaze palsy; probable bvFTD or PPA within 5 years; parkinsonism restricted to the legs for more than 3 years; dopamine-blocker exposure in a dose and time course consistent with drug-induced parkinsonism; no response to high-dose levodopa (at least 600 mg/day) despite at least moderate severity; normal presynaptic dopaminergic imaging; a documented alternative condition.
- **Consequence:** a first-visit patient who has never taken levodopa has at most one supportive criterion (rest tremor), unless a validated smell test or an MIBG is in the case. Such a patient is **clinically probable PD**, never "established". Probable PD needs no supportive criterion when there is no red flag. The response to levodopa can add a supportive criterion later.
- **Current D2-blocker exposure (M01, M02, M03):** while metoclopramide is taken, the exposure is an absolute exclusion, so the MDS criteria cannot yet be met. The label rests on the abnormal DaTscan (pure drug-induced parkinsonism has normal presynaptic imaging) and on non-motor features a D2 blocker does not cause (RBD, hyposmia); the diagnosis is confirmed when the parkinsonism persists after withdrawal.

**F2. Drug-induced parkinsonism and DaTscan.** Metoclopramide and prochlorperazine are central D2 antagonists. Valproate and lithium cause parkinsonism by other mechanisms. In pure drug-induced parkinsonism the DaTscan is normal and the signs resolve over weeks to months after withdrawal. An abnormal DaTscan shows a presynaptic deficit, so an underlying degenerative parkinsonism has been unmasked [Marshall_2009]. DaTscan does not separate PD from MSA, PSP or DLB, and DaT ligands are not displaced by D2 antagonists. NICE NG71 recommends DaT SPECT for people with tremor when essential tremor cannot be clinically differentiated from parkinsonism; it gives no indication for a clinically clear case (write it so, never "NICE says do not use it").

**F3. MSA, MDS 2022 [Wenning_2022].**

- Autonomic dysfunction is one of: an orthostatic fall of at least 20/10 mmHg within 3 minutes; urinary urge incontinence; a post-void residual of at least 100 mL.
- **Clinically established MSA** requires all of:
  - autonomic dysfunction;
  - poorly levodopa-responsive parkinsonism or a cerebellar syndrome (or both);
  - at least two supportive motor or non-motor features;
  - at least one MRI marker.
- **Clinically probable MSA** requires at least two of autonomic dysfunction, parkinsonism and a cerebellar syndrome, plus one supportive feature.
- **Supportive features:** motor: rapid progression within 3 years of motor onset; moderate to severe postural instability within 3 years; levodopa-induced craniocervical dystonia without limb dyskinesia; severe speech or swallowing impairment within 3 years; unexplained Babinski sign; jerky myoclonic postural or kinetic tremor; postural deformities (antecollis, Pisa, camptocormia). Non-motor: stridor; inspiratory sighs; cold discoloured hands and feet; erectile dysfunction (below age 60 for probable MSA); pathological laughter or crying.
- **Poor levodopa response:** by history, or less than 30% improvement on MDS-UPDRS III, on up to 1000 mg/day levodopa as needed and tolerated for at least 1 month. No trial means poor response cannot be stated.
- **MRI markers:** putaminal atrophy with signal decrease on iron-sensitive sequences; middle cerebellar peduncle or pontine atrophy; the hot cross bun sign.
- Cardiac MIBG is usually preserved in MSA. Olfaction is usually preserved in MSA.

**F4. DLB, McKeith 2017 [DLB_2017].**

- Dementia with functional decline is essential.
- **Core features:** fluctuating cognition; recurrent visual hallucinations; RBD; parkinsonism.
- **Indicative biomarkers:** reduced DaT uptake; abnormal (low) MIBG; PSG-confirmed REM sleep without atonia.
- **Supportive biomarkers:** preserved medial temporal lobes; occipital hypometabolism with the cingulate island sign on FDG-PET; posterior slow-wave EEG.
- Severe neuroleptic sensitivity is a supportive clinical feature.
- **Probable DLB:** two or more core features, or one core feature with one or more indicative biomarkers.

**F5. PSP, MDS 2017 [Hoglinger_2017].** Probable PSP-RS is O1 (vertical supranuclear gaze palsy) or O2 (slow vertical saccades), with P1 (repeated unprovoked falls within 3 years) or P2 (a tendency to fall on the pull test within 3 years). A poor levodopa response is supportive. The MRI midbrain atrophy (hummingbird sign) is supportive, not required.

**F6. Imaging facts.**

- Brain MRI is normal in PD. It is done to exclude vascular lesions, NPH, mass, and the midbrain, pontine and putaminal signs of PSP and MSA. A standard parkinsonism MRI is non-contrast.
- Evans index above 0.30 is abnormal; 0.31 is never "upper limit of normal".
- MIBG is reduced in PD and DLB (postganglionic denervation) and usually normal in MSA and PSP.
- MIBG and DaTscan reports are binary statements of the finding, with no disease name.

**F7. Levodopa facts.**

- Immediate-release carbidopa-levodopa tablets are 10/100, 25/100 and 25/250. A "25/200" immediate-release tablet does not exist. Daily levodopa is the per-dose milligrams times the doses: 25/250 three times daily is 750 mg/day.
- Iron salts chelate levodopa: give them at least 2 hours apart.
- MAO-B inhibitors (rasagiline label): meperidine, tramadol, methadone, dextromethorphan, St John's wort, cyclobenzaprine and other MAO inhibitors are contraindicated; sympathomimetic amines are avoided.
- With an SSRI, the serotonin-syndrome risk is rare. The labels advise caution, and fluoxetine and fluvoxamine are best avoided with rasagiline.
- "Sertraline plus levodopa causes serotonin syndrome" is false. Do not write it.
- Dopamine agonists: warn about impulse control disorders and excessive daytime sleepiness, and ask about them at each visit [NICE_NG71].

**F8. ICD-10-CM.**

- G20.A1: PD without dyskinesia, without fluctuations.
- G20.A2: with fluctuations.
- G20.B1: with dyskinesia, without fluctuations.
- G20.B2: with dyskinesia, with fluctuations.

RM05 (G20.A2) and RP04 (G20.B2) are correct. MSA stays G90.3 as `icd_codes[0]` (CENTRAL R6: WHO ICD-10 and ICD-10-GM now code MSA-P G23.2 and MSA-C G23.3), DLB G31.83, PSP G23.1.

**F9. Orthostatic measurement.** `perform_clinical_assessment {"assessment_type": "orthostatic_blood_pressure"}` exists (supine 5 minutes, then 1 and 3 minutes standing). Where the history reports orthostatic light-headedness and the exam gives no lying and standing figures (M01, RM04, RP04), it is an `optional` criterion with a stored `ClinicalAssessmentReport` follow-up (C23). Where the figures are already in the exam, it is not a criterion.

---

## 2. Error classes in this condition

### C1. Literature search as a clinical step, with fabricated citations and leaks (ruling 5)

**Found:**

- Every case has a literature criterion with an exact `query` string that no agent can match: `required` in 28 cases (and in their stop rules), `recommended` in P02 and P03.
- The outputs carry misattributed or invented papers: a Wenning "Clinical differentiation" paper in Lancet Neurol 2022, Koga and Dickson in Ann Neurol 2022, "Marshall 2019" on secondary parkinsonism, Bronstein 2011 as JAMA Neurol, Curran and Lang as Arch Neurol, Postuma's RBD cohort as Lancet Neurol 2019, authors "Various".
- Gilman 2008 is given as current. RM04, RM05, RP03 and RP04 have empty summaries. RM04 embeds `[Postuma_2015]` in a `key_finding`. RS03 and RS04 carry "self-mutilation" searches from their seed. P02 and P03 fail the leak test.

**Fix (as NPH C1):**

- Delete the literature criterion; remove its id from `stop_rule` and from every sequence constraint.
- Set `initial_tool_outputs.literature_search` and `fallback_tool_outputs.literature_search` to null.
- Delete every `search_medical_literature` follow-up. The library returns its generic guideline text.
- A real clinical point carried by a deleted output goes into a must (C16), never into another tool call. Example: in RP01, the positional syncope and blunted heart-rate response favour orthostatic syncope.

### C2. Drug-interaction checks: wrong tier, unmatchable arguments, wrong content (ruling 6)

**Found:**

- Every case has a drug criterion: `required` in 27 cases, `recommended` in P01, P02 and P03.
- The `required_arguments` carry exact `drug` strings and `current_medications` lists, often with drugs the patient does not take (RS01 lists acetaminophen, omits lithium, and is copied from S01).
- Outputs list the current medicines as "proposed" (P01), read "(agent not specified...)" in fallbacks, omit the interaction that matters (RP01 omits tamsulosin in a patient with syncope), and assert false pharmacology: sertraline plus levodopa "serotonin syndrome" (RM03, RP02), propranolol "decreasing dopaminergic metabolism" (RM03), domperidone beside flecainide (RP02), metoclopramide as an "alternative" (RM05).

**Fix:**

1. **Tier:**
   - `required` only where a dopamine-blocking drug is on the list or the referral asks for the review: M01, M02, M03 (metoclopramide), RM05 (prochlorperazine), RP04 (pre-DBS review: iron with levodopa, rasagiline before surgery).
   - `recommended` where a real pair changes management: P01, RP01, RP02 and RP03 (drugs that worsen neurogenic orthostatic hypotension); P02 (rivastigmine with midodrine and syncope); RS01 (lithium with lisinopril); RM02 (valproate).
   - `optional` in the other 18 cases.
2. **Arguments:** `check_drug_interactions {}`. Any call counts. The case output reviews the whole list, whatever drug is proposed.
3. **Output:** one stored output, `initial_tool_outputs.drug_interactions = {"general": {...}}`. Delete every drug follow-up and set the drug fallback to null. The MockServer serves the first stored value for any `drug`, and the library would otherwise say "no interaction".
4. **Content:**
   - `proposed` is "Carbidopa-levodopa (proposed)", or for RP04 "Current regimen before STN-DBS".
   - `interactions` and `warnings` name only the patient's own medicines.
   - Nothing from `expected_evidence`, the musts or `key_clinical_evidence` is copied. The leak test must pass.
5. **Order:** the drug criterion sits after the diagnostic criteria.
6. **Canonical sentences** (use those that apply):
   - **Metoclopramide (M01-M03):** "Metoclopramide is a central dopamine D2 receptor antagonist: it causes and worsens parkinsonism and opposes levodopa. For gastroparesis use a prokinetic without central D2 blockade, such as domperidone where available after an ECG for the QTc, or short-term erythromycin."
   - **Prochlorperazine (RM05):** "Prochlorperazine is a phenothiazine D2 receptor antagonist: even intermittent doses worsen parkinsonism and oppose levodopa. Ondansetron or domperidone (with a QTc check) are alternatives for migraine-associated nausea."
   - **Orthostatic drugs (P01, RP01, RP02, RP03, and optional mentions elsewhere):** "<Tamsulosin (alpha-1 blocker)/amlodipine/lisinopril/hydrochlorothiazide/metoprolol/propranolol> lowers standing blood pressure and adds to the orthostatic fall; levodopa can lower it further. Review the need for each and measure lying and standing blood pressure at each levodopa dose step." P01 adds "sildenafil adds to hypotension". Write midodrine as a consideration with supine-pressure monitoring, never as "contraindicated" at a supine 140-150 systolic.
   - **Iron (RP04):** "Ferrous sulfate chelates levodopa and reduces its absorption: give it at least 2 hours apart from levodopa doses."
   - **Rasagiline (RP04):** "Rasagiline: meperidine, tramadol, methadone, dextromethorphan, St John's wort and cyclobenzaprine are contraindicated, and sympathomimetic amines are avoided; tell the anaesthetic team before surgery."
   - **SSRI with a future MAO-B inhibitor (RM01, RM03, RS02, RS03, RS04, RP02):** "<Sertraline/fluoxetine> with an MAO-B inhibitor: serotonin syndrome is rare; use the lowest dose and monitor. Fluoxetine and fluvoxamine are best avoided with rasagiline."
   - **Lithium (RS01):** "Lithium causes postural tremor and, less often, parkinsonism. Lisinopril raises lithium levels: keep the level monitored. Levodopa has no pharmacokinetic interaction with lithium."
   - **Valproate (RM02):** "Valproate can cause reversible parkinsonism, and hyperammonaemia at therapeutic levels. Any change of mood stabiliser is planned with psychiatry. Lamotrigine has a lower tremor and parkinsonism burden."
   - **Benzodiazepines (RM01, RM02, RP01, RP02, RP04):** "<Clonazepam/lorazepam> adds sedation and fall risk with dopaminergic drugs in older patients."
   - **Anticholinergic (S02):** "Oxybutynin is a centrally active anticholinergic: it adds to confusion and hallucination risk with dopaminergic treatment in older patients. Trospium or mirabegron are alternatives."
   - **Rivastigmine (P02):** "Rivastigmine is vagotonic: bradycardia and syncope are possible, and midodrine can cause reflex bradycardia; check the ECG and heart rate before starting and at each dose step."

### C3. Criterion text: label equals rationale, duplicated and missing citations

**Found:**

- In all 30 cases every criterion's `rationale` is a copy of its `label`.
- Every `citations` list has the bracketed and the bare key.
- `[NICE_NG71]` is used, but it is not in the pack.

**Fix:**

- Write a distinct rationale, one sentence saying why the step is indicated in this patient.
- Replace the generic `expected_evidence` strings shared by 9 to 12 cases ("Abnormal striatal uptake supports nigrostriatal degeneration but does not distinguish PD from MSA or PSP", "Document REM sleep without atonia if the clinical RBD question remains unresolved", "Characterize the cognitive profile and functional implications", "Address the specific metabolic, toxic, young-onset or pretreatment question in this case") with a restatement of what this case's stored report shows (figures, side, domains).
- Drop the bare keys.
- **MRI label:** "Brain MRI to exclude a structural, vascular or atypical-parkinsonism cause". **MRI rationale:** "PD is a clinical diagnosis; MRI is normal in PD and excludes vascular lesions, NPH, mass and the midbrain, pontine and putaminal signs of PSP and MSA [Postuma_2015]". Add `[Schwarz_2014]` only where the report gives an SWI nigrosome finding.
- **S06 CT:** keep the CT label; rationale "MRI is not possible because of severe claustrophobia; CT excludes mass, haemorrhage, hydrocephalus and strategic infarcts, with lower sensitivity for atypical-parkinsonism signs".

### C4. Engineering sentences in `key_clinical_evidence`

**Found:** every case has "Tier per the July 2026 clinical review: ..." and "July 2026 review applied: ...".

**Fix:** delete both. They describe the dataset, not the patient.

### C5. MRI criterion arguments too narrow

**Found:** every MRI criterion requires `{"contrast": false, "protocol": "standard"}`. The tool has no defaults, so an MRI ordered without those exact values does not score.

**Fix:** `analyze_brain_mri {}`; S06: `order_ct_scan {}`.

### C6. "Clinically established PD" overcalled; wrong supportive criteria (F1)

**Found:**

- "Clinically established" at first visits before any levodopa: S01, S02, S03, S04, RS01, RS02, RS03, RS04, RS05, RM04, M05, RP05 and S05, in musts or `key_clinical_evidence`.
- M05 counts RBD as supportive.
- RM04 and S05 claim a levodopa response that the case never documents; S06's evidence claims hyposmia as supportive.
- Self-reported smell loss is counted as supportive.

**Fix:**

- **Canonical must:** "Diagnose clinically probable PD (MDS 2015): <bradykinesia with rest tremor/rigidity>, no absolute exclusion, <no red flag / red flag X counterbalanced by supportive criterion Y>; the response to levodopa may add a supportive criterion [Postuma_2015]".
- **M01, M02, M03 diagnostic must (canonical):** "Diagnose Parkinson's disease unmasked by metoclopramide: current D2-blocker exposure is an MDS absolute exclusion while it continues, but the abnormal DaTscan shows a presynaptic dopaminergic deficit that pure drug-induced parkinsonism does not cause<, and RBD/hyposmia are not drug effects>; confirm that the parkinsonism persists after withdrawal [Postuma_2015][Marshall_2009]". Fill the RBD/hyposmia slot only with what the case's history reports (M01 RBD; M02 RBD and hyposmia; M03 neither).
- "Clinically established" stays only where two supportive criteria are in the data:
  - M04: rest tremor, and UPSIT 28/40, which is moderate microsmia for a 64-year-old man, not "mild";
  - RM05: documented response of more than 50%, and rest tremor;
  - RP04: dramatic response, dyskinesia and rest tremor.
- Delete every claim of a levodopa response that the patient block does not contain.

### C7. Non-PD labels scored against PD criteria (F3, F4, F5)

**Found:** P01 (MSA-P), P02 (DLB), P03 (PSP-RS) and RP03 (MSA-P/C) carry the generic must "Apply MDS 2015 PD criteria", and their evidence lines mix PD and MSA criteria. P02 calls MIBG and PSG "supportive" (they are indicative). P01's differential and metadata claim a "poor levodopa response", but P01 has had no trial.

**Fix:**

- **Musts:**
  - P01: "Diagnose clinically probable MSA-P (MDS 2022): neurogenic orthostatic hypotension (34/26 mmHg at 1 minute without heart-rate compensation), urinary urgency with incomplete emptying, parkinsonism, with supportive features <early postural instability with falls, erectile dysfunction before 60, rapid progression> and MRI markers <list from the report>; poor levodopa responsiveness cannot be stated until a trial of up to 1000 mg/day for at least a month [Wenning_2022]". Add a must: "Start a levodopa trial titrated up to 1000 mg/day as tolerated, with lying and standing blood pressure at each step".
  - RP03: "Diagnose clinically established MSA (MDS 2022)" with the same structure. It meets it: poor response by history to 600 mg/day for 6 weeks (at most 10 to 15% subjective benefit, within "up to 1000 mg/day as tolerated"), urge incontinence, nOH 44/28 mmHg at 3 minutes, supportive stridor, anterocollis and early postural instability, and the MRI markers.
  - P02: "Diagnose probable DLB (McKeith 2017): dementia with <n> core features <list>; MIBG and PSG are indicative biomarkers [DLB_2017]".
  - P03: "Diagnose probable PSP-RS (MDS 2017): O1 <finding> with P1 <falls> [Hoglinger_2017]".
- Delete "poor levodopa response" from P01 wherever it is stated as a fact.

### C8. DaTscan: tier, dependence and the normal library default (F2)

**Found:**

- DaTscan is `optional` everywhere, yet musts, prohibitions and evidence depend on its result:
  - M01, M02 and M03 "Use DaTscan to differentiate";
  - M04 "Order DaTscan... establishes PD";
  - P04's prohibition cites an "abnormal DaTscan";
  - RP05 calls the scan "load-bearing";
  - RM02 and RM03 "DaTscan is the key differentiator".
- 18 cases store no DaTscan at all: M05, P01, P03, RM01, RM04, RP01, RP02, RP03, RP04, RS01 to RS05, S01 to S04. The library default is "Normal DaTscan. No evidence of presynaptic nigrostriatal dopaminergic deficit". That is an MDS absolute exclusion of PD, and it is false in MSA and PSP. Any agent that orders the scan is told the label is wrong.
- Several stored reports interpret: RM05's "supporting a degenerative nigrostriatal syndrome rather than pure intermittent prochlorperazine-induced parkinsonism"; the "comma-to-period" and "presynaptic dopaminergic deficit confirmed" wording.

**Fix:**

1. **Tiers:**
   - `required`: M01, M02, M03, RM02. The label (PD unmasked by a drug, or PD despite valproate) rests on it.
   - `recommended`: RP05 (vascular versus PD: the referral question, with Fazekas 2 on MRI).
   - `optional`: M04 and RM03 (prior ET, but the rest tremor and decrement make PD clinically clear, so NICE NG71 does not ask for the scan), P02, P04, RM05, RS01, S05, S06.
   - `waste` (in `avoided_actions`) in the 17 others. Rationale: "DaT SPECT is indicated when tremor cannot be clinically separated from parkinsonism; here the clinical diagnosis is clear and the scan would not change management [NICE_NG71]". For P01, P03, RP01, RP02 and RP03 the rationale is instead "A DaTscan does not separate PD from MSA or PSP [Marshall_2009]".
2. **Storage:** every case stores a DaTscan follow-up, including the waste cases. Trigger `request_datscan`, `modality: "DaTscan"`, `tracer_or_protocol: "123I-ioflupane SPECT"`.
3. **Report, PD and DLB cases:** "Abnormal DaTscan: reduced striatal dopamine transporter binding, asymmetric, more marked in the <right/left> posterior putamen (contralateral to the clinically worse side), with relative caudate sparing. Presynaptic dopaminergic deficit."
4. **Report, MSA and PSP cases:** "Abnormal DaTscan: bilateral, relatively symmetric reduction of striatal dopamine transporter binding involving putamen and caudate. Presynaptic dopaminergic deficit."
5. **Report rules:** findings give binding ratios with the normal value. No disease name. No "rather than". No "confirms".
6. **Musts and prohibitions** may cite only the results of required or recommended criteria. Delete or rewrite those that cite optional ones: P04's prohibition, S05's and S06's evidence on the laterality of the scan.

### C9. Other library defaults that contradict the case

**Found:**

- The library neuropsychological battery returns MoCA 28/30 and "average range", against exam MoCA scores of 24 to 27. This affects M01, M02, M04, M05, P01, RM01, RM03, RP05, RS02, S03 and S04.
- The library PSG is normal, against witnessed dream enactment or a known RBD diagnosis in cases with no stored PSG: P02 (RBD a core feature), P04 (two witnessed arm-waving episodes), RM01 (clonazepam whose listed indication is RBD; the HPI says "restless sleep episodes": align the HPI with the list), RP01 (RBD confirmed by a prior sleep study), RP02, RP04. The other cases without a stored PSG deny dream enactment (RS02 only sleep-talks), and the normal library PSG fits them.
- M01 (talking, moving his arms and striking his wife in sleep) and M04 (talking and limb movements in sleep for 8 months) do report dream enactment: their optional PSG criteria stay.
- The library ECG is normal, against known WPW in RP01.
- The library MIBG is normal, which does not fit RP01 once its data are made PD (C21).

**Fix:**

- Read the history; the regex count above is a guide only.
- Where the exam MoCA is below 28, store a neuropsychological battery consistent with it: trigger `request_neuropsych_testing`, `test_type: "neuropsych_battery"`, impression in the C10 form. It becomes a criterion only where section 4 says so.
- Where dream enactment is reported or RBD was diagnosed, store a PSG with REM sleep without atonia (C10 form). It is an `optional` criterion only where the history reports dream enactment and no PSG has confirmed it (this adds one to P04). M05 is `recommended`.
- Where the history has no dream enactment, no case carries a PSG criterion (none does today), and no evidence line claims RBD.
- RP01: an initial ECG. RP01 and RP02: an MIBG follow-up (section 4).

### C10. Auto-generated impressions with wrong flags, and empty reports

**Found:**

- PSG and neuropsychological impressions read "Abnormal values: ..." with inverted flags: sleep efficiency 68% "(H)", clock 4/10 "(H)", FAB 8/18 "(H)", Stroop z -2.0 "(H)", CVLT z -1.5 "(H)".
- Thin PSG reports are a single conditional sentence: RP05 "REM sleep without atonia would confirm RBD...", M04 and RM04 "a strong prodromal synucleinopathy marker".

**Fix:**

- **PSG impression (canonical):** "REM sleep without atonia (<n>% of REM epochs) with dream-enactment behaviour on video, meeting the polysomnographic criterion for REM sleep behaviour disorder; <AHI n/h: no/mild/moderate obstructive sleep apnoea>; <PLMI n/h>. Clinical correlation recommended."
- **PSG content:** a full report with total sleep time, efficiency, REM latency, RSWA percentage, video behaviours, AHI, SpO2 nadir and PLMI, matching the case's figures.
- **Neuropsychological impression (canonical):** "Impaired <processing speed/executive function/phonemic fluency/delayed recall/visuospatial function>, with preserved <domains>; profile of <mild cognitive impairment of frontal-subcortical type/multi-domain impairment in the dementia range with ...>. <Mood scale result>."
- **Flags:** `abnormal` follows the reference range in the right direction.
- No diagnosis name in either report.

### C11. Reports that state the diagnosis or the answer (Kind 1)

**Found:**

- Labs: M04 "hyperthyroidism excluded... no metabolic or toxic mimic"; RM05's TSH `clinical_significance` "does not explain asymmetric levodopa-responsive parkinsonism".
- MIBG: RP02 "as is typically seen in Lewy-body parkinsonism"; RP03 "characteristic of Lewy-body parkinsonism... suggesting autonomic dysfunction of preganglionic origin".
- FDG: P02 "classic DLB metabolic pattern"; P03's FDG fallback "distinct from the temporoparietal pattern seen in an Alzheimer-type process".
- Holter: RP01 "This significantly reduces the likelihood that the patient's recent syncopal episodes are WPW-related".
- Amyloid PET fallbacks (M04, M05, RM04, RP04, RP05, S06): "does not resolve the current diagnostic question".

**Fix:**

- **Labs:** values and flags only; `interpretation` "Abnormal: <list>. Other results within reference ranges."
- **MIBG:** "Reduced cardiac MIBG uptake (early H/M <x>, delayed H/M <y>, washout <z>%): cardiac sympathetic denervation." or "Normal cardiac MIBG uptake (...)."
- **FDG:** the regional pattern only (occipital hypometabolism with relative sparing of the posterior cingulate).
- **Holter:** "Two patient-triggered events for light-headedness coincided with sinus rhythm at <n>/min."
- **Amyloid fallbacks:** null. The library returns a negative amyloid PET.

### C12. MRI reports

**Found:**

- "Post-gadolinium" or "no enhancement following gadolinium" on a non-contrast study: M02, M04, P01, P02, P03, RP02, RP03, S04.
- MRA lines on a standard protocol: M05, P04, S02, S03.
- Evans 0.31 called "upper limit of normal": M01, M02.
- `expected_evidence` that the report does not support:
  - S01 and RS01 claim a swallow-tail loss;
  - RP02 says "no hot cross bun, no putaminal slit" over a report with putaminal atrophy and rim;
  - RP01 says "no putaminal slit" over a putaminal rim.
- P01's MSA template is copied into RP02.
- RM03 has a right hand-knob "thinning" on the wrong side for right-hand signs, and cervical spondylosis in a brain report.
- RM04's nigrosome finding is filed under "Age-appropriate cortical atrophy" and "Normal midbrain morphology".

**Fix:**

- Delete the gadolinium and MRA lines. RP05 keeps its MRA (prior TIA).
- Evans index 0.28.
- `expected_evidence` restates the report.
- RP01 and RP02 MRIs become normal for age (C21).
- RM03: delete the hand-knob finding and the cervical line.
- RM04: one finding per structure.

### C13. Differential not updated to the assessment-time view (ruling 7)

**Found** (high or moderate entries that the work-up excludes):

- M01, M02, M03: drug-induced parkinsonism high, vascular moderate.
- S01, RS01, S05: ET moderate. S06: ET high. M04: ET high, dystonic tremor moderate. RM03: ET high.
- M05: MSA and DLB moderate.
- P01: "PD with autonomic involvement" high, PSP moderate.
- P02: PDD high, AD moderate. P03: PD moderate.
- P04: Wilson high; DRD, functional and genetic moderate.
- RP01, RP02: MSA high. RP03: PD with cerebellar comorbidity moderate.
- RM02: valproate parkinsonism high. RM05: prochlorperazine high, MSA moderate, hypothyroidism moderate.
- RP05: vascular high. RS03: vascular moderate. RM01: PSP moderate.

**Fix:**

- After the required and recommended results these become `low`, with the excluding finding in `key_features`.
- A real contributor that coexists with the label is written so in `key_features` ("coexists; contributes to <x>; not the cause of the parkinsonism"), at `low`. Examples: ET in M04, RM03 and RP04; prochlorperazine in RM05; the TSH in RM05; valproate in RM02.

### C14. Red herrings that are absent, copied or mis-addressed

**Found:**

- "Brief metoclopramide mention" in P01, RP02 and RS04, whose histories deny any exposure.
- P01: "asymmetric motor onset" over a symmetric exam.
- RS01: "Sister with ET and 10 pack-year smoking" is copied from S01. RS01 has a brother with ET and never smoked.
- M05: `field_path` and `location` point to the wrong list indices.
- RP04: the ET red herring says "DaTscan confirms" with no DaTscan.
- RM03: the metadata red herring "subclinical hypothyroidism" has no labs behind it.

**Fix:**

- Delete a red herring whose data point is not in the patient block.
- Repoint paths to real indices.
- Replace a deleted one only with a real case datum (section 4).

### C15. Evidence and musts that assert absent data; impossible timelines

**Found:**

- M05: "normal autonomic battery", "normal cognition on neuropsych battery". Neither test exists in the case.
- M01, M02 and M03: "premotor features (RBD, constipation, hyposmia) preceding metoclopramide" (musts, red herrings, evidence). M03 denies RBD and has no hyposmia. M02's RBD (18 months) and hyposmia (12 months) both began after metoclopramide (24 months); only her constipation predates it. M01 has no hyposmia, an undated RBD, and constipation for 2 years against metoclopramide for 18 months.
- M03: metoclopramide for 3 years, symptoms for 1 year, and "gait changes preceded the medication".
- Constipation is no evidence in M01 to M03: their gastroparesis confounds it.
- S02: "baseline neuropsych testing" with no such criterion.

**Fix:**

- Evidence lines restate patient data or results of required and recommended criteria only.
- M01 to M03: replace the "preceding metoclopramide" argument everywhere by the C6 canonical must's reasoning (abnormal DaTscan; RBD and hyposmia are not drug effects). The M03 timeline is fixed in section 4.

### C16. Musts and prohibitions: generic templates instead of case management

**Found:** in about 20 cases the same three musts appear: "Apply MDS 2015...", "Document temporal sequence...", "Review the full medication list...". Treatment is vague or absent.

**Fix:** three to five case-specific musts, built from:

- the C6 or C7 diagnostic must;
- **levodopa start (canonical):** "Start carbidopa-levodopa 25/100 mg, half a tablet three times daily with food, increasing over 2 to 4 weeks to one tablet three times daily (300 mg/day levodopa), and review the response after 2 to 3 months [NICE_NG71]";
- **agonist caution (canonical, where an agonist is plausible, under 70):** "If a dopamine agonist is used, warn about impulse control disorders and excessive daytime sleepiness and ask about them at every visit [NICE_NG71]";
- the C2 drug consequence;
- non-motor management that the case raises: RBD bedroom safety, orthostatic measures, constipation, depression, falls and physiotherapy, and speech-language assessment for dysphagia in P03 and RP03.

Prohibitions are case-specific:

- **Canonical (all):** "Do not prescribe metoclopramide, prochlorperazine, haloperidol or other centrally acting D2-blocking antiemetics or antipsychotics; if an antipsychotic is needed, use quetiapine or clozapine".
- **P02 adds:** "Do not give haloperidol or another typical antipsychotic: severe neuroleptic sensitivity [DLB_2017]".

### C17. Fallback outputs

**Found:**

- `fallback_tool_outputs.echo` has no `echo_type` (30/30).
- P03's advanced fallback says `FDG-PET`.
- The amyloid fallbacks (C11).
- Vague text: ECG "Largely normal ECG with a benign incidental finding" (S02, S03, S04); echo "Structurally near-normal heart with a benign incidental finding" (RM03, RP03, RS02, S02).
- M04's ECG fallback reads "sinus bradycardia, beta-blocker" at a resting HR of 62.
- RM03's "Normal ECG" at HR 58 on propranolol.

**Fix:**

- `echo_type: "TTE"`; P03 `modality: "FDG_PET"`.
- Concrete normal text: "Sinus rhythm <HR>/min, normal axis and intervals, no ST change." For RM03: "Sinus bradycardia 58/min".
- Echo: "Normal left ventricular size and function, EF <55-65>%, no significant valve disease."

### C18. Dose arithmetic and missing medicines

**Found:**

- P03: "25/250 TID (600 mg/day)" (it is 750), while the medication list still says 25/100 TID.
- RP03: "25/200 mg three times daily". There is no such tablet, and levodopa is absent from the list.

**Fix:**

- P03: "two tablets of 25/100 three times daily (600 mg/day levodopa)", in both the HPI and the medication list.
- RP03: the same form for its 600 mg/day, and add "Carbidopa-levodopa 25/100 mg, two tablets three times daily (trial, no benefit)" to the list.

### C19. Metadata

**Found:**

- Difficulty descriptions mention data that are not in the case: RM01 "upper-normal TSH"; RM03 "subclinical hypothyroidism"; RS03 "Levodopa challenge is positive"; RP02 "poor acute levodopa response"; RP03 "monoclonal IgA gammopathy, elevated inflammatory markers"; P01 "poor levodopa response".
- RM05's "young-onset" panel at onset age 53.

- `metadata.revision_reason` (30 cases) and `metadata.difficulty_rationale` ("3 required tool actions after the independent reviewer audit", 26 cases) are shared engineering text that the edits make false.

**Fix:** metadata describes the case as edited. RM05's genetic criterion is justified by the first-degree relative. `difficulty_rationale` says in one sentence what makes this case hard (the confounder) and how many required criteria it has after the edit; `revision_reason` reads "October 2026 review round: plans/PD.md" plus the main changes, and `last_revised` is "2026-10-24".

### C20. Stop rule and sequence constraints

**Found:**

- `max_additional_actions` is 0 in all 30 cases.
- `required_before_assessment` lists the literature and drug ids.
- Sequence constraints "labs before drug check" (M04, RM02, RM05, RP04, RS01, RS03, RS04, RS05) have reasons that do not fit.

**Fix:**

- `required_before_assessment`: the required criteria only.
- `max_additional_actions: 2` (one optional test and the medication review).
- Sequence: keep only "MRI before DaTscan" (`soft`, reason "Exclude structural and vascular causes on MRI before interpreting a DaTscan [Postuma_2015]"), and only where the DaTscan is required, recommended or optional. Delete every other constraint.

### C21. Data that contradict the PD label (ruling 3: fix the data)

**Found:** RP01, RP02, RS03 and RS04 are labelled PD, but their data meet more than two MDS red flags: symmetric parkinsonism without rest tremor, an MSA-type putaminal MRI (RP01, RP02), an orthostatic fall of 30/15 or more, and recurrent falls within 18 months (RP02 falls on every pull-test trial). RS03 and RS04, called "straightforward", have a 4-month subacute course with falls and a wide-based gait.

**Fix:** keep the labels and make the data clinically probable PD (F1): asymmetric onset with a rest tremor on examination, a normal-for-age MRI, at most one red flag counterbalanced by a supportive criterion (validated olfactory loss in RP01, reduced MIBG in RP02), and for RS03 and RS04 a 20-month history without falls. Details in section 4.

### C22. Templated and duplicated patients

**Found:**

- RS03 and RS04 are the same patient: both are "Mrs. Delgado", with the same PMH (including a Roux-en-Y bypass and a cholecystectomy) and the same five medicines.
- RS01 is a copy of S01 in its medication list and red herrings.

**Fix:**

- RS04 gets a different surname, and loses the bypass and the cholecystectomy.
- RS01's drug, red-herring and differential text are rebuilt from RS01's own data (lithium, brother with ET).

### C23. Orthostatic light-headedness without measured figures (F9)

**Found:** M01 (on tamsulosin), RM04 (on tamsulosin and amlodipine) and RP04 (pre-DBS) report light-headedness on standing, but the exam gives no lying and standing pressures, and the library has no answer that fits each case.

**Fix:** add `optional` criterion `orthostatic-bp` (`perform_clinical_assessment {"assessment_type": "orthostatic_blood_pressure"}`), placed after the MRI, and a follow-up (trigger `request_orthostatic_bp`, `tool_parameters {"assessment_type": "orthostatic_blood_pressure"}`) whose output is a `ClinicalAssessmentReport`: `assessment_type`, `scores` (supine, 1 minute and 3 minutes BP and HR), `impression` "Fall of <x>/<y> mmHg at 3 minutes with a heart-rate rise of <n>/min: no orthostatic hypotension by consensus criteria." Use different figures per case, none meeting 20/10 (for example M01 supine 128/76 HR 74, 3 min 116/70 HR 82; RM04 134/80 HR 72, 3 min 120/74 HR 80; RP04 136/80 HR 74, 3 min 124/76 HR 84). The case's drug output then names the alpha-blocker as the likely contributor. Run the routing check for this tool too.

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers

| # | criterion | tool and `required_arguments` | tier |
| --- | --- | --- | --- |
| 1 | brain MRI (S06: CT) | `analyze_brain_mri {}` / `order_ct_scan {}` | required |
| 2 | targeted labs | `interpret_labs` with the case's panels as one-item alternatives | required P04 (`ceruloplasmin`, `serum_copper`, `24h_urinary_copper`); recommended RS01 (`lithium_level`), RM02 (`valproate_level`, `ammonia`), RM05 (`TSH`, `free_T4`); optional M04, RP04, RS03, RS04, RS05; absent elsewhere |
| 3 | ECG, Holter (RP01 only) | `analyze_ecg {}`; `order_cardiac_monitoring {"monitor_type": "holter_24h"}` | recommended |
| 3b | orthostatic BP (C23) | `perform_clinical_assessment {"assessment_type": "orthostatic_blood_pressure"}` | optional M01, RM04, RP04 |
| 4 | DaTscan | `order_advanced_imaging {"modality": "DaTscan"}` | C8 |
| 5 | cardiac MIBG | `order_advanced_imaging {"modality": "MIBG_scan"}` | recommended RP02; optional P01, P02, RP01, RP03 |
| 6 | FDG-PET (P02) | `order_advanced_imaging {"modality": "FDG_PET"}` | optional |
| 7 | video-PSG | `order_specialized_test {"test_type": "polysomnography"}` | recommended M05; optional where dream enactment is reported and not PSG-confirmed (section 4) |
| 8 | neuropsychological battery | `order_specialized_test {"test_type": "neuropsych_battery"}` | required RP04; optional P02, P03, RM02, RM04, RM05, RP01, RP02, RP03, RS03 |
| 9 | genetic panel | `order_specialized_test {"test_type": "genetic_panel:PD"}` | optional P04, RM05 |
| 10 | medication review | `check_drug_interactions {}` | C2 |

There is no literature criterion. There is no EEG, CSF, echo, autonomic or tilt criterion. The echo in RP01 is optional only: WPW can sit with structural disease, but the ECG and Holter carry the question.

### 3.2 Follow-ups and initial outputs

- Order the follow-ups as in 3.1. Every required and recommended criterion is served by a case output, never by the library.
- New follow-ups carry `tool_parameters` with the discriminator term and use the panel's trigger names (`conditions.yaml` `parkinsons.common_followups`): `request_datscan` (DaTscan), `request_mibg` (MIBG_scan), `request_sleep_study` (polysomnography), `request_neuropsych_testing` (neuropsych_battery), `request_holter`, `request_orthostatic_bp`.
- Keep existing triggers when they already route correctly. Rename only those that name a deleted step.
- Initial outputs: `mri` (S06 `ct`); `labs` where labs are a criterion or the case already stores them; `drug_interactions` (C2); `ecg` in RP01.
- EEG and CSF stay null with their fallbacks.

### 3.3 `avoided_actions`

- **Keep** EEG, CSF, echo and cardiac monitoring as `waste` with a case-specific rationale, where present. Do not add EEG to P02 or P03 (posterior slowing is a supportive DLB biomarker) or echo and monitoring to RP01 (it lists only EEG and CSF). RP02 keeps echo.
- **Keep** ECG as `waste` where present; RP01 and RP02 do not list it, and must not.
- **Add** DaTscan `waste` per C8.
- **Add** `order_specialized_test {"test_type": "autonomic_testing"}` and `{"test_type": "tilt_table"}` as `waste` in every case: "Formal autonomic testing is not part of the PD work-up; bedside orthostatic measurement suffices". In P01, RP01, RP02 and RP03 the rationale reads "bedside orthostatic blood pressure already documents the neurogenic orthostatic hypotension".
- **Keep** amyloid and FDG-PET `waste` where present (M04, M05, RM04, RP04, RP05, S06), except FDG in P02.

### 3.4 Sequence constraints

Only "MRI before DaTscan", `soft` (C20).

### 3.5 Stop rule

- `required_before_assessment`: the ids of the required criteria.
- `max_additional_actions: 2`.

### 3.6 Check after editing

- `uv run python data/review/round-2026-10/bin/perfect_agent.py <ID> -v` passes. In `-v`, every required and recommended action is served by a case output.
- `uv run python data/review/round-2026-10/bin/case_io.py check <ID>` passes.
- `uv run pytest agent-platform/tests/test_case_guards.py -q -k <ID>` passes, including the leak test.
- Routing check with `MockServer(case).get_output`, script in its own folder:
  - `DaTscan`, `MIBG_scan` and `amyloid_PET` each return their own output or the library, never another modality's;
  - `polysomnography` and `neuropsych_battery` return the case's report;
  - `check_drug_interactions` with `drug: "levodopa"` and with `drug: "rasagiline"` returns the case output;
  - in M01, RM04 and RP04, `perform_clinical_assessment {"assessment_type": "orthostatic_blood_pressure"}` returns the case's report.
- Grep the case for "established", "gadolinium", "Abnormal values:", "Lewy", "serotonin syndrome", "Tier per", "July 2026 review applied": each hit is allowed by a class.

---

## 4. Per-case index

Every case receives C1, C2, C3, C4, C5, C10, C11, C12, C13, C16, C17, C19 and C20. The bullets give only what is specific to the case. No reviewer notes exist for PD, so no note id appears below.

### PD-M01 (man, 70, PD unmasked by metoclopramide 18 months for gastroparesis; symmetric-left, no rest tremor; DaTscan R>L putamen)
- DaTscan `required`; drug check `required` (metoclopramide sentence; tamsulosin with his standing light-headedness).
- Diagnostic must: C6 M01-M03 canonical, with "RBD is not a drug effect" (wife reports him talking, moving his arms and striking her in sleep). No hyposmia: delete every hyposmia claim. Constipation is not evidence (C15).
- PSG stays `optional` with its stored report (RSWA 42%, two arm-flailing episodes): rewrite the impression in C10 form (sleep efficiency 72% is low, not "(H)"); AHI 5.8 is mild OSA, PLMI 18.
- C23: optional orthostatic BP criterion and report.
- Evans 0.28 (the report also says "upper limit of normal" in its prose; delete that); callosal angle stays. "Mild ventricular enlargement" finding: write "ventricles proportionate to sulci".
- Store a neuropsychological battery (MoCA 25) without a criterion.
- Musts: withdraw metoclopramide (C2 sentence); "Reassess after withdrawal: drug-induced signs can take weeks to months to resolve; the abnormal DaTscan shows an underlying presynaptic deficit that withdrawal will not reverse [Marshall_2009]"; the levodopa start once the drug is stopped and signs persist. Keep the prohibition "Do not start levodopa while metoclopramide remains in the regimen"; delete the duplicate must that says the same.
- Differential: DIP `low` "coexisting contributor"; vascular `low` (scattered punctate periventricular foci only).

### PD-M02 (woman, 64, PD unmasked by metoclopramide 2 years; constipation precedes it, RBD and hyposmia follow it)
- As M01, except: no orthostatic criterion (no orthostatic symptoms); diagnostic must with "RBD and hyposmia are not drug effects" (both began after metoclopramide; never call them "preceding").
- Evans 0.28; delete "gadolinium".
- Store a neuropsychological battery (MoCA 25). PSG stays optional (dream enactment for 18 months), C10 impression.

### PD-M03 (man, 75, PD unmasked by metoclopramide; DaTscan is the only biomarker)
- As M01, except: no PSG and no orthostatic criterion; the diagnostic must names only the DaTscan.
- C15 timeline: keep metoclopramide at 3 years and the 12 to 14 month motor history; delete from the HPI the clause "and his wife believes the gait changes preceded the medication initiation, though she is not entirely certain of the timeline", and every evidence line built on it.
- Delete the RBD and PSG mentions in red herrings, musts and evidence: the history denies dream enactment and has no hyposmia.

### PD-M04 (man, 64, longstanding ET on propranolol, new right-hand rest tremor; UPSIT 28/40; SWI nigrosome finding)
- Clinically established PD is allowed (rest tremor and UPSIT microsmia); write UPSIT as "moderate microsmia for age and sex".
- DaTscan `optional` (C8); drug check `optional` (propranolol blunts tachycardia with orthostasis).
- Labs optional (TSH); delete ceruloplasmin and RPR padding at 64 and the lab interpretation (C11).
- PSG stays `optional` (talking and limb movements in sleep for 8 months); replace the thin report by a full C10 report with RSWA. The laterality of the rest of the case (right signs, left DaTscan deficit) is checked against every report.
- ECG fallback: "Sinus rhythm 62/min".
- Differential: ET `low` "coexists"; dystonic tremor `low`.
- Store a neuropsychological battery (MoCA 27).

### PD-M05 (man, 69, akinetic-rigid PD with violent dream enactment and OSA; self-reported anosmia)
- C6: delete "RBD supportive" and "established"; write probable PD.
- C15: delete the "normal autonomic battery" and "normal cognition on neuropsych" evidence.
- PSG `recommended` (violent episodes, OSA as an RBD mimic); the stored PSG shows both RSWA and the OSA figures.
- DaTscan `waste` (store abnormal R or L per worse side).
- Differential MSA and DLB `low`. Red-herring `field_path` repointed (C14). Delete MRA.
- Store a neuropsychological battery (MoCA 27).

### PD-P01 (man, 60, MSA-P: symmetric, falls within 6 months, nOH 34/26 at 1 min, urinary retention, ED at 57, putaminal MRI markers)
- C7: clinically probable MSA-P. Delete "poor levodopa response" (no trial) from the differential, metadata and evidence.
- MIBG optional (normal, C11 form). Drug check `recommended`: tamsulosin, lisinopril, sildenafil; midodrine as a consideration, with supine 142/88 to 150/93 monitored.
- Rewrite the initial drug output (C2).
- C14: delete the metoclopramide and "asymmetric onset" red herrings. Replace them with the tamsulosin-for-BPH attribution of the urinary symptoms, if the HPI supports it.
- Differential: PD with autonomic involvement `low`, PSP `low`.
- DaTscan `waste` (store the symmetric MSA report).
- Store a battery (MoCA 25). No PSG: the history denies dream enactment.

### PD-P02 (man, 68, DLB with four core features and haloperidol sensitivity; MoCA 19)
- C7: probable DLB; MIBG and PSG are indicative biomarkers.
- Check that the HPI documents functional decline (instrumental ADLs). If it does not, add one sentence (finances or medications now managed by the spouse).
- Drug check `recommended` (rivastigmine sentence; midodrine already on the list).
- DaTscan, MIBG and FDG optional. The FDG report gives the pattern without "classic DLB".
- Store a PSG with RSWA (RBD diagnosed by history 3 years ago); optional criterion (indicative biomarker).
- Neuropsych optional; impression in C10 form.
- Differential: PDD `low` ("parkinsonism did not precede dementia by a year"), AD `low`.
- Leak test: fixed by C1 and C2.
- Prohibition: neuroleptic sensitivity (C16).

### PD-P03 (woman, 72, PSP-RS: vertical gaze palsy, early falls, frontal behaviour, no tremor, no levodopa benefit)
- C7: probable PSP-RS. C18: the levodopa arithmetic in the HPI and the medication list.
- Neuropsych optional (C10 impression). FDG fallback `FDG_PET`. DaTscan `waste` (symmetric report).
- The red herring: falls are a PSP core feature (P1), not an "absolute exclusion"; rewrite `correct_interpretation`.
- Differential: PD `low`.
- Must: speech-language assessment of dysphagia; fall prevention.
- Leak test: fixed by C1 and C2.

### PD-P04 (man, 42, young-onset PD; Wilson screen normal, no KF rings)
- Labs `required` with the copper alternatives (3.1). Rationale: "Wilson disease is treatable and is screened for in unexplained movement disorders of young adults (EASL 2012: consider it from age 3 to 55) [EASL_Wilson_2012]". Do not write "before any other diagnosis is accepted" or "definitively exclude"; write "make Wilson disease unlikely" (normal ceruloplasmin, serum and urinary copper, no Kayser-Fleischer rings). The stored labs keep ceruloplasmin, serum and 24 h urinary copper normal; interpretation per C11.
- Genetics optional (age 42). DaTscan optional; delete the "abnormal DaTscan" prohibition and evidence (C8).
- Differential: Wilson `low`; DRD, functional and genetic `low` with their excluding data.
- Evidence: replace "dopamine agonists typically preferred in young patients" with "In young-onset PD levodopa, a dopamine agonist or an MAO-B inhibitor are all options; agonists carry the ICD warning [NICE_NG71]".
- Delete the labs-before-DaTscan constraint.
- Drug check optional (calcium antacid: no clinically relevant interaction).
- PSG: add an `optional` criterion and a stored PSG (C9: two witnessed arm-waving dream-enactment episodes in 3 months), with RSWA and no sleep apnoea, figures distinct from other cases.
- Rest tremor on examination is the only supportive criterion: clinically probable PD (C6). The current must lists "micrographia, asymmetric onset, probable abnormal DaTscan" as supportive criteria: none is (F1). Delete "with abnormal DaTscan establish" from the "do not dismiss as functional" must and the DaTscan clause from the matching prohibition; the organic signs (true rest tremor with re-emergence, decrement, cogwheel rigidity) carry the point. Delete the DaTscan evidence line.
- Genetics evidence: "Offer counselled testing of a PD gene panel at onset before 50 (PRKN is the commonest recessive cause)", not "regardless of family history, as de novo mutations occur".

### PD-RM01 (woman, 68, 8-year PD on 300 mg/day levodopa; episodic saccadic freezing and diplopia)
- Keep the label. Differential PSP `low` (full vertical range, preserved OKN); wearing-off `low` (no dose-related pattern described).
- Drug check optional (clonazepam: sedation, falls, saccade latency; sertraline with a future MAO-B inhibitor).
- C19: delete "upper-normal TSH" from the metadata.
- Musts: increase levodopa (for example to 25/100 one tablet four or five times daily, or 1.5 tablets three times daily) and reassess the eye movements and limb signs; orthoptic review of the convergence insufficiency (base-in prisms for near).
- DaTscan `waste`. Store a PSG (RBD on clonazepam) and a battery (MoCA 27).

### PD-RM02 (man, 68, PD with valproate, past olanzapine, post-encephalitic illness; DaTscan asymmetric L>R)
- DaTscan `required`. Labs `recommended` (valproate level 72, ammonia 58): the C11 interpretation.
- Drug check `recommended` (valproate sentence; clonazepam; tamsulosin).
- Differential: valproate parkinsonism `low` "coexisting contributor"; past olanzapine DIP `low` (stopped 8 weeks before a 20-month course); add post-encephalitic parkinsonism `low` (the RBD and constipation predate the illness).
- Rename the follow-up trigger `search_postencephalitic_parkinsonism_vs_pd` away (it is deleted by C1).
- Musts: plan any change of mood stabiliser with psychiatry; "If antipsychotic treatment is ever needed, use quetiapine or clozapine".

### PD-RM03 (man, 62, prior ET on propranolol, new right-sided PD; uncle with PD; HR 58)
- DaTscan `optional` (C8). Drug check optional: rewrite the output (propranolol blunts the orthostatic tachycardia; sertraline sentence; delete the false propranolol and serotonin claims).
- C12: delete the hand-knob finding and the cervical line.
- Delete the right FDI wasting and the grip 4+/5: C5-C6 spondylosis cannot explain them, and they create an unexplained lower motor neuron sign.
- C19: delete "subclinical hypothyroidism".
- ECG fallback "Sinus bradycardia 58/min". Echo fallback concrete (C17).
- Differential ET `low` "coexists".

### PD-RM04 (man, 73, left-sided PD misread as adhesive capsulitis; C5-C6 spondylosis; MoCA 24)
- C6: delete the "levodopa response" and "established" claims; probable PD.
- C12: restructure the MRI findings.
- Drug check optional (tamsulosin and amlodipine with the reported orthostatic light-headedness). C23: optional orthostatic BP criterion and report.
- Neuropsych optional (impression already in C10 form; keep). PSG optional; rewrite the thin report.
- DaTscan `waste`. Amyloid fallback null.

### PD-RM05 (woman, 58, 4-year PD with predictable wearing-off and freezing; prochlorperazine; TSH 5.8 on levothyroxine; mother with PD)
- G20.A2 stays. Established PD is allowed.
- Drug check `required` (prochlorperazine sentence). Delete metoclopramide from `alternatives` and the levothyroxine-calcium sentence.
- Labs `recommended` (TSH, free T4); delete the `clinical_significance` interpretation.
- Genetics optional: rationale "first-degree relative with PD"; panel name "Parkinson disease gene panel", not "young-onset".
- DaTscan optional; binary report (C8).
- Differential: prochlorperazine `low` "aggravating factor"; MSA `low`; hypothyroidism `low` "coexists".
- Musts: wearing-off management (more frequent levodopa doses, or adding entacapone, an MAO-B inhibitor or an agonist); freezing and falls physiotherapy with cueing; stop prochlorperazine.
- Delete the drug-before-labs constraint.

### PD-RP01 (man, 62, PD with orthostatic syncope wrongly blamed on known WPW; RBD on PSG; Sniffin' Sticks 6/12; MoCA 24)
- **C21 data fix:**
  - left-predominant bradykinesia with decrement, and a 4-5 Hz left-hand rest tremor on examination;
  - delete "no decrement pattern typically seen in classic PD", "irregular postural tremor" and "wide-based";
  - pull test 2 steps;
  - near-falls stay as near-falls;
  - MRI normal for age (delete the putaminal volume loss and rim);
  - keep the orthostatic figures (26/16 at 1 min, 32/20 at 3 min: one red flag, counterbalanced by the rest tremor and the Sniffin' Sticks result).
- Supportive criteria: rest tremor and validated hyposmia, so clinically probable PD. PD-MCI level I from the MoCA [Litvan_2012].
- **ECG `recommended`:** initial output "Sinus rhythm 72/min, short PR 0.10 s, delta waves, QRS 0.12 s: ventricular pre-excitation pattern". Rationale: ESC 2018 ECG in every syncope.
- **Holter `recommended`:** keep it; rewrite the impression (C11).
- Echo optional (TTE normal). MIBG optional (store reduced).
- Drug check `recommended` (tamsulosin, amlodipine, clonazepam; the current output omits tamsulosin).
- Differential: MSA `low` (rest tremor, normal MRI, hyposmia); cardiac syncope `low` (no arrhythmia in symptomatic events); DLB `low`.
- Musts: orthostatic measures and review of tamsulosin and amlodipine; cardiology review of the WPW pathway (risk stratification is the cardiologist's) without attributing the syncope to it.
- DaTscan `waste`.
- Avoided: EEG and CSF stay; do not add ECG, echo or monitoring; autonomic and tilt `waste`.

### PD-RP02 (man, 63, "PD with early prominent autonomic failure"; seed PMC7458143, MIBG resolves the puzzle)
- **C21 data fix:**
  - right-predominant bradykinesia and rigidity, and a right-hand rest tremor on examination;
  - delete the symmetric statements and the nuchal and axial rigidity;
  - pull test 2 to 3 steps with recovery;
  - one fall at 18 months stays, and "five near-falls" becomes "two near-falls";
  - freezing deleted;
  - MRI normal for age, replacing P01's template (C12); give an SWI nigrosome loss if wanted.
- Keep the orthostatic figures, the cardiac history (WPW ablated, paroxysmal AF on flecainide, metoprolol, apixaban) and the post-viral anosmia red herring.
- Note in the HPI that metoprolol limits the heart-rate response, and delete "blunted heart rate response" as a sign.
- **MIBG `recommended`:** "Reduced cardiac MIBG uptake (early H/M 1.42, delayed H/M 1.21, washout 38%): cardiac sympathetic denervation"; no "Lewy-body". This gives a second supportive criterion beside the rest tremor, counterbalancing the severe-autonomic-failure red flag, so clinically probable PD.
- Drug check `recommended`: metoprolol and orthostasis; "Domperidone is not advised with flecainide (QT)"; sertraline sentence; delete the serotonin-syndrome claim.
- ECG not waste: store "Sinus rhythm 64/min, no pre-excitation, QRS 0.10 s".
- C14: delete the metoclopramide red herring; use the father's and brother's ET (the PCP's initial ET label) and the URI attribution of the anosmia.
- C19: delete "poor acute levodopa response".
- Differential MSA `low`. DaTscan `waste`. Neuropsych optional (MoCA 23).

### PD-RP03 (man, 74, clinically established MSA, mixed P and C features; levodopa 600 mg/day without benefit; nOH 44/28; urge incontinence; stridor on PSG)
- C7: MDS 2022 established MSA. C18: levodopa in the HPI and the medication list.
- Delete the seed remnants "jaw and joint pain" and "low-grade temperatures up to 37.8": at 74 they would demand an ESR, a CRP and a GCA work-up, which the case does not intend. Delete the matching metadata (C19).
- MIBG optional (normal, C11 form). PSG optional (stridor, RSWA, AHI 12.4: C10 impression).
- Neuropsych optional.
- Drug check `recommended`: tamsulosin, amlodipine 10 mg and propranolol worsen the nOH; "the post-void residual" sentence is deleted unless a bladder scan is added to the exam.
- Delete "post-gadolinium" (C12).
- Differential: PD with cerebellar comorbidity `low`.
- Must: urgent ENT laryngoscopy for the stridor (risk of sudden death) [Wenning_2022].
- DaTscan `waste` (symmetric report). Echo fallback concrete.

### PD-RP04 (woman, 58, 9-year PD with fluctuations and dyskinesia, STN-DBS candidacy; coexisting ET; ferrous sulfate; MoCA 25, DRS-2 128)
- G20.B2 stays; established PD allowed.
- Neuropsych `required`; drug check `required` (iron and rasagiline sentences, lorazepam, pramipexole 4.5 mg/day with the ICD warning, amantadine).
- Labs optional (iron studies, already stored).
- C14: delete "DaTscan confirms" from the ET red herring.
- Delete the drug-before-labs constraint.
- Musts:
  - "Separate ferrous sulfate from levodopa by at least 2 hours and reassess the wearing-off before surgery";
  - "A formal levodopa challenge (MDS-UPDRS III OFF and ON, at least 30% improvement) is needed for candidacy" (vocabulary gap, CENTRAL R4);
  - the cognitive profile is PD-MCI, which does not exclude DBS.
- DaTscan `waste`. Amyloid fallback null. Store a PSG (dream enactment).
- C23: optional orthostatic BP criterion and report (light-headedness on standing, pramipexole and lisinopril).

### PD-RP05 (woman, 77, left-sided PD with vascular risk, prior TIA, Fazekas 2)
- DaTscan `recommended`; the stored report is binary (C8).
- Rewrite the thin PSG (C10). PSG optional.
- Drug check optional (amlodipine and hydrochlorothiazide with orthostasis; amantadine dose in CKD).
- Differential vascular `low` "coexisting small-vessel disease".
- Evidence: delete "dramatic levodopa response, if demonstrated"; replace it with probable PD (rest tremor supportive; smell loss informal).
- Amyloid fallback null. Store a battery (MoCA 26).

### PD-RS01 (man, 69, straightforward PD on lithium 600 mg twice daily, level 0.72; brother with ET; father PD at 72)
- C22: rebuild the drug list and output from RS01's own medicines (lithium, lisinopril, metformin, atorvastatin, tamsulosin). Drug check `recommended` (lithium sentence).
- Labs `recommended` (lithium level). Delete the RPR padding.
- C14: replace the copied sister-and-smoking red herring with "lithium therapy": correct interpretation "lithium causes postural tremor and occasionally parkinsonism, but not an asymmetric rest tremor with RBD and hyposmia".
- Differential: add lithium-associated parkinsonism `low`; ET `low`.
- DaTscan `optional` (lithium can cause tremor and parkinsonism: a live drug-related differential). RS01 stores no DaTscan today: add one (C8 PD report, left posterior putamen for the right-sided signs) with a criterion and the MRI-before-DaTscan constraint. PSG optional (dream enactment for 2 years). C6, C12 (swallow-tail).
- Delete acetaminophen from every drug list (RS01 does not take it); metformin and tamsulosin stay.

### PD-RS02 (man, 62, right-sided PD; VP shunt for aqueductal stenosis 10 years ago; father PD at 68)
- C6. Drug check optional (sertraline sentence).
- Must: "If the shunt valve is programmable, check its setting after the MRI".
- Echo fallback concrete. DaTscan `waste`. Store a battery (MoCA 27). Sleep talking alone does not need a PSG.

### PD-RS03 (woman, 69, PD; seed with self-injurious behaviour; post-bariatric)
- **C21 data fix:**
  - an 20-month history, right-hand rest tremor first, the left hand involved after a year;
  - no falls; near-fall once;
  - narrow-based gait; Pisa posture may stay;
  - orthostatic fall 12/6;
  - urinary urgency without incontinence;
  - delete the near-syncope;
  - MoCA 26.
- Delete the vascular `moderate` (`low`). Labs optional (B12, copper after bypass).
- Drug check optional (fluoxetine sentence).
- C1 deletes both self-mutilation searches. C19: delete "levodopa challenge positive".
- Neuropsych optional (rewrite the battery to match MoCA 26, C10). DaTscan `waste`.

### PD-RS04 (woman, 68, PD; the RS03 template)
- C22: a new surname; delete the bypass and the cholecystectomy from the PMH.
- **C21 data fix:**
  - a 20-month history;
  - "vertigo" becomes "unsteadiness on turning";
  - falls deleted;
  - narrow-based gait;
  - right-predominant rest tremor (the left hand milder).
- C14: delete the metoclopramide red herring and the duplicate DIP entry. Use the mother's ET as the red herring.
- Labs optional. Drug check optional. Neuropsych optional only if the MoCA stays at 24 with the memory complaint; otherwise store without a criterion. DaTscan `waste`.

### PD-RS05 (woman, 56, right-sided PD; topiramate; TSH 5.8; father PD at 74; self-reported smell loss)
- C6: probable PD.
- Labs optional (TSH stored). Repoint the red-herring path to the stored thyroid panel.
- Drug check optional. Genetics is not indicated (onset at 55, father's onset at 74); no criterion.
- DaTscan `waste`.

### PD-S01 (man, 65, right-sided PD; father PD at 73; tamsulosin)
- C6. C12: `expected_evidence` without the swallow-tail claim.
- Drug check optional (tamsulosin sentence).
- ET `low`. DaTscan `waste`.

### PD-S02 (woman, 62, right-sided PD; oxybutynin)
- C6. C15: delete "baseline neuropsych testing".
- Drug check optional (oxybutynin sentence, a must).
- ECG and echo fallbacks concrete. Delete MRA. DaTscan `waste`.

### PD-S03 (man, 71, right-sided PD; tamsulosin; naproxen with aspirin)
- C6. PSG optional (stored; C10 impression). Drug check optional (tamsulosin sentence).
- ECG fallback concrete. Delete MRA. DaTscan `waste`. Store a battery (MoCA 27).

### PD-S04 (man, 67, right-sided PD; tamsulosin; self-reported smell loss)
- C6. Delete "after gadolinium administration". Drug check optional.
- ECG fallback concrete. DaTscan `waste`. Store a battery (MoCA 27).

### PD-S05 (man, 67, right-sided PD with a mild postural tremor component; mother with ET)
- C6, C15: delete "dramatic levodopa response" and "hyposmia supportive" (the smell loss is self-reported).
- DaTscan optional (stored); delete the laterality evidence line (C8).
- ET `low`.
- Drug check optional (amlodipine and orthostasis).

### PD-S06 (woman, 71, left-sided PD; CT only because of claustrophobia; mother with tremor)
- The CT criterion stays `required` with its exemption; reorder it first (the drug check is listed first now).
- In the CT report, delete "MRI was not completed because..." (it is history, not a finding).
- DaTscan optional; delete the "DaTscan laterality is mandatory" evidence (C8).
- Evidence: delete "hyposmia" as supportive (self-reported).
- ET `low`. Drug check optional (lisinopril; alendronate is not relevant).
- Amyloid fallback null.

---

## 5. CENTRAL requests

- **R1 (pack and keys):** `criteria_packs/PD.md`.
  - Literature and drug checks are no longer `REQUIRED` (rulings 5, 6).
  - Add `[NICE_NG71]`, `[Wenning_2022]`, `[DLB_2017]` (alias of `[McKeith_2017_DLB]`), `[Hoglinger_2017]`, `[Litvan_2012]`, `[ESC_2018]` and `[EASL_Wilson_2012]`.
  - Mark Gilman 2008 superseded by Wenning 2022.
  - State F1's established-versus-probable rule and the four supportive criteria.
- **R2 (generator):**
  - Stop emitting literature criteria and required drug checks for PD.
  - Stop the "Abnormal values: ..." impression builder for PSG and neuropsychological reports: its H/L flags are inverted for lower-is-worse measures.
  - Stop the two "July 2026 review" evidence sentences.
  - Stop the amyloid PET fallback template and the MRI `{"contrast": false, "protocol": "standard"}` arguments.
  - Update the `parkinsons` follow-ups in `conditions.yaml` to section 3.
- **R3 (guard):** add PD to `DISCRIMINATOR_CONDITIONS` when the 30 cases pass.
- **R4 (vocabulary):**
  - `perform_clinical_assessment` type `levodopa_challenge` (MDS-UPDRS III OFF and ON, for RP04 and any DBS case);
  - `order_specialized_test` type `olfactory_test` (UPSIT or Sniffin' Sticks), so a validated smell test can be ordered rather than only stated in the exam;
  - `laryngoscopy` for MSA stridor (RP03) if other conditions need it.
- **R5 (library):**
  - The DaTscan default is normal, which in any parkinsonism condition (PD, DLB, MSA, PSP) is an absolute exclusion of the label.
  - Either make the library DaTscan, MIBG, PSG and neuropsychological defaults condition-aware, or add a guard that fails a case when a library default would contradict the patient block. Contradictions to catch: exam MoCA below 28 with no stored battery; dream enactment with no stored PSG; a parkinsonism label with no stored DaTscan.
- **R6 (ICD):** WHO ICD-10 (2019 edition) and ICD-10-GM code MSA-P as G23.2 and MSA-C as G23.3, where MSA previously went to G90.3. Verify the US ICD-10-CM tabular, then add G23.2 (P01, RP03) and G23.3 (RP03) to the accepted codes through the synonyms file; `icd_codes[0]` stays G90.3 until Andrea rules.
- **R9 (guidance answers):** `condition_tool_guidance.yaml` `parkinsons` `our_response` texts become false after this round and must be regenerated from the edited cases: "no Parkinson case orders an ECG" (RP01 now recommends ECG and Holter), "Nine of 30 cases retain targeted optional studies" (labs are now required in P04 and recommended in RM02, RM05, RS01), "Polysomnography is optional in 11 cases", the neuropsychology counts, and the genetics counts. The ECG departure must be shown to Reviewer 1 with its reason (ESC 2018: 12-lead ECG in every syncope).
- **R10 (vocabulary in use):** `perform_clinical_assessment` `orthostatic_blood_pressure` is used here for the first time in a case (C23); confirm the slot name the MockServer uses for a stored assessment follow-up when wiring the batch.
- **R7 (perfect agent and scorer):**
  - `perfect_agent.py` should call each tool with the minimal arguments a real agent would use. Free-text `required_arguments` (`query`, `drug`) then fail it, and the false pass seen here is caught.
  - A guard could forbid free-text values in `required_arguments` for knowledge tools.
- **R8 (condition scoping):** P01, P02, P03 and RP03 are MSA, DLB and PSP under condition `parkinsons` with a PD prefix (their metadata `case_body_concerns` say so). This plan keeps them as PD-mimic cases (question Q1). Whatever Andrea decides, the paper's per-condition counts should describe them.

## 6. Open questions for Andrea

Andrea's ruling of 24 October stands: the plan decides judgment calls itself. These are confirmations, with the default that the workers apply.

- **Q1.** P01 (MSA-P), P02 (DLB), P03 (PSP-RS) and RP03 (MSA) stay in the PD condition as PD-mimic cases, with their own criteria (C7). The alternative is to move them under their own conditions in a later round. Default: keep.
- **Q2.** RP01 and RP02 have data that meet MSA-P better than PD. The plan fixes the data to clinically probable PD (C21), as ruling 3 asks and as RP02's seed resolved. The alternative is to relabel them MSA-P. Default: fix the data.
- **Q3.** RS03 and RS04 are rewritten from a 4-month subacute course with falls into a typical 20-month PD history. The alternative is to drop them as straightforward cases. Default: rewrite.
- **Q4.** DaTscan is `waste` in the 17 cases with a clear clinical diagnosis (NICE NG71 indication: tremor not clinically separable from parkinsonism; Reviewer 1 did not comment on DaTscan). The stored result is still abnormal, so the data stay consistent. Default: waste.
- **Q6.** RP01 recommends an ECG although Reviewer 1 asked to remove the ECG from PD: the case is a syncope with known WPW, where ESC 2018 requires one. Default: keep, and show it to Reviewer 1 (R9).
- **Q5.** Literature is deleted in all 30 cases, as in NPH, rather than kept optional with canonical text, as in FTD: almost every PD literature output carries invented or misattributed citations. Default: delete.
