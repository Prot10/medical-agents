# Criteria pack: Functional Neurological Disorder (FND)

**ICD-10:** F44.4 (motor), F44.5 (non-epileptic seizures), F44.6 (sensory), F44.7 (mixed)
**Condition enum:** `NeurologicalCondition.FUNCTIONAL_NEUROLOGICAL_DISORDER`
**Case ID prefix:** `FND`

---

## 1. Diagnostic criteria

DSM-5: Functional Neurological Symptom Disorder — (a) ≥1 symptom of altered
voluntary motor or sensory function, (b) clinical findings provide evidence
of incompatibility with neurological/medical conditions, (c) symptom not
better explained by another disorder, (d) clinically significant distress
or impairment. **RULE-IN** signs are essential — diagnosis is positive, not
purely exclusionary. Examples: Hoover's sign (functional leg weakness),
tremor entrainment (functional tremor), Tinel's-like give-way weakness,
fixed dystonic posturing, midline splitting of sensory loss, tubular visual
fields, ictal eye closure (functional seizures), pelvic thrusting with
preserved awareness, prolonged duration with normal post-ictal state.

## 2. Standard workup hierarchy

> **Clinical tool review, July 2026 — the reviewers' option 2, and the tiers that make it real.**
> They asked whether FND should be replaced by dementia with Lewy bodies, since it is a purely
> clinical diagnosis, or kept with **every diagnostic tool optional** if the project also wants to
> measure *diagnostic overuse*. It is kept: overuse is an objective, cost is tracked against
> reference tariffs, and FND is the only condition in which the correct behaviour is to withhold
> testing. (DLB is added regardless, so nothing they proposed is lost.)
>
> The tiers below were rewritten on 2026-08-06 because the decision had been recorded but not
> implemented: all 30 cases still required a brain MRI *with gadolinium* and a laboratory battery,
> none performed a structured functional-signs examination, and nothing was tiered optional.
> Beyond the metric, that encoded the discredited diagnosis-of-exclusion model. **The required
> act is now the examination.** In the 8 non-paroxysmal cases the whole required workup costs
> 138 EUR — the cheapest *fully specified* pathway in the benchmark. It is not the numerically
> lowest: 15 migraine-with-aura cases require nothing that costs anything, because their only
> required acts are the two zero-cost tools and the ICHD-3 structured history the reviewers named
> as that condition's one true required test is still absent from the cases. That is a hole to fix
> in migraine, not a virtue to claim here.

**Required:**
- `perform_clinical_assessment` (`assessment_type: functional_neuro_signs`) — the diagnostic act.
  Document *which sign was positive*, not which disease was excluded: Hoover sign and hip abductor
  sign for functional leg weakness, entrainment and distractibility for functional tremor,
  collapsing (give-way) weakness, midline-splitting or non-dermatomal sensory loss, dragging
  monoplegic gait, convergence spasm for functional diplopia, agonist-antagonist co-contraction.
  DSM-5 criterion B is *clinical incompatibility* — a positive finding, not an absence
  [Espay_2018] [Stone_2018] [DSM5_FND]
- `analyze_eeg` (`eeg_type: video`) — **required only where the phenotype is paroxysmal**
  (22 of 30 cases). Capturing a habitual event with no ictal EEG correlate is the positive
  diagnostic act for psychogenic non-epileptic seizures at the ILAE *documented* level of
  certainty; it is not an exclusion test and no bedside sign substitutes for it. Where there are
  no events, there is nothing to record and this item does not apply [ILAE_PNES_2013]

**Recommended:**
- `analyze_brain_mri` (`contrast: false`) — **once, and only for a specific alternative question**:
  an acute focal presentation being triaged as a stroke mimic, a new deficit on top of multiple
  sclerosis or Parkinson's disease, acute paraplegia, or functional diplopia before convergence
  spasm is accepted. 7 of 30 cases. Never with gadolinium absent an indication [Espay_2018]
- `interpret_labs` — **named assays on a named suspicion**, never a battery: glucose where symptoms
  followed an insulin dose, electrolytes with magnesium and thiamine in protracted vomiting with
  weight loss. 3 of 30 cases [Stone_2018]
- `check_drug_interactions` — review of agents that worsen the picture: antiseizure drugs started
  for misdiagnosed events, benzodiazepines, dopamine-blocking agents

**Optional:**
- `order_specialized_test` (`test_type: neuropsych_battery`) — quantifies the comorbidity that
  treatment will target (mood, anxiety, somatic symptom burden, dissociation, psychosocial
  context) with performance-validity measures, and documents that the deficit is not
  effort-dependent. Optional, in all 30 cases, and for a reason worth stating: at 1 104 EUR it is
  the most expensive item on this pathway and it does not make the diagnosis. It informs the
  treatment plan [Stone_2018]
- `analyze_brain_mri` (`contrast: false`) — in the remaining 23 cases a single scan is defensible
  but earns no diagnostic credit: the signs have already made the diagnosis, and a normal scan
  costs 294 EUR and strengthens the search for an organic cause
- `interpret_labs` (CBC, CMP, TSH, B12) — same reasoning; defensible once, required never
- Specialist referral *(clinical action — `tool_name: null`, no tool call)* — psychiatry or health
  psychology for treatment

## 3. Tools that are typically USELESS

- `analyze_csf` — no role unless other diagnosis genuinely suspected
- `analyze_ecg` — unrelated
- `order_echocardiogram` — unrelated
- `order_cardiac_monitoring` — unrelated unless syncope on differential
- `order_ct_scan` — MRI is preferred when imaging needed
- `order_advanced_imaging` (most) — none indicated for typical FND
- `order_specialized_test` (`emg_ncs`) — **scored as a useless call in all 30 cases**, not merely
  discouraged in prose: the deficit is not neuromuscular, the study is uncomfortable, and a normal
  result is itself a harm because it reinforces the search for an organic cause. Prose is not
  measured; a `useless_tools` entry is
- `order_specialized_test` (`ssep`) — evoked potentials answer a question about a lesion in the
  somatosensory pathway, and midline-splitting sensory loss is not that question. Also scored
- `order_specialized_test` (`muscle_biopsy / nerve_biopsy`) — invasive testing reinforces the
  somatic illness model; not indicated
- **Repetition of any normal study.** Encode the first unnecessary call in `avoided_actions`
  when it is case-specific; repeated identical calls are also caught by the harness's
  redundant-call penalty. In FND the iatrogenic harm is usually the second and third
  investigation, not the first [Stone_2018]

## 4. Tools that are HARMFUL / contraindicated

- Over-investigation in general (not a single tool, but a pattern). The principal harm in FND is iatrogenic — every additional negative test reinforces patient illness conviction and delays definitive diagnosis. Per Stone 2018, repeated negative workups WORSEN prognosis.

## 5. Sequence constraints

(none — workup parallel, but the principle is "as little as needed to confirm rule-in signs + exclude alarm features")

## 6. Subtype variations

- **M (mild):** circumscribed symptom, clear rule-in sign on examination; the examination is the
  whole required workup
- **S (standard):** mixed motor/sensory or functional seizures; the examination plus video-EEG
  where there are events to record, and nothing else required
- **P (progressive / severe):** disabling symptoms, multiple body regions, prolonged duration,
  refractory. The diagnostic requirement does not grow with severity — that is the trap the tier
  structure now refuses to reward. What grows is the treatment plan
- **R (reverse / mimic):** the "FND" diagnosis was wrong — actually MS, stroke, dystonia, autoimmune encephalitis, neuromyelitis optica, or rare metabolic disease; workup adds the targeted rule-out (e.g., LP+OCBs for MS, MOG/AQP4 antibodies, paraneoplastic panel, B12, ceruloplasmin)

## 7. Common red-herring categories

- **Psychiatric history** — does not exclude organic disease; FND can coexist with organic
- **Symptoms during stress** — many organic diseases (MS, migraine) also flare with stress
- **"Patient is dramatic"** — bedside impression is unreliable; rule-in signs are reliable
- **Normal initial workup** — does not equal FND; positive rule-in evidence is required
- **Fluctuating symptoms** — common in FND but also in MG, MS

## 8. Allowed citations

- `[Espay_2018]` — Espay AJ et al. Current concepts in diagnosis and treatment of functional neurological disorders. JAMA Neurology 2018;75:1132-1141
- `[Stone_2018]` — Stone J et al. Functional disorders in the neurology clinic: a complete diagnostic neurological approach. Pract Neurol 2018;18:267-278
- `[ILAE_PNES_2013]` — LaFrance WC Jr et al. ILAE Nonepileptic Seizures Task Force: minimum diagnostic standards. Epilepsia 2013;54:2005-2018
- `[Carson_2012]` — Carson AJ, Lehn A. Epidemiology of functional disorders. Handb Clin Neurol 2016;139:47-60
- `[Nielsen_2015]` — Nielsen G et al. Physiotherapy for functional motor disorders: consensus recommendations. J Neurol Neurosurg Psychiatry 2015;86:1113-1119
- `[DSM5_FND]` — American Psychiatric Association. Diagnostic and Statistical Manual of Mental Disorders, 5th ed. Functional neurological symptom disorder (conversion disorder), criterion B: clinical findings provide evidence of incompatibility. 2013
