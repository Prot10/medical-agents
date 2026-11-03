# How different are the conditions? Case diversity analysis (3 Nov 2026)

Code: `scripts/paper/case_diversity.py` (numpy, scipy, scikit-learn; embeddings from the CERN AI gateway).

```bash
nice -n 10 uv run --no-project --python 3.12 --with numpy --with scipy --with scikit-learn \
  python -u scripts/paper/case_diversity.py --permutations 9999      # --no-embeddings to skip the gateway
```

Raw outputs: `outputs/paper/diversity/` (gitignored): `summary.json`, `views.csv`, `pairwise_<view>.csv`
(190 condition pairs), `condition_distance_<view>.csv` (20×20 energy distances), `per_condition.csv`,
`copy_baseline.csv`, `tool_by_condition.csv`. Dataset state: commit `7aa9ae29`, 600 cases, 20 conditions
× 30. Seed 20261103, 9999 permutations. All policies are still `draft`: every number below describes
the dataset as authored, not a physician-approved reference.

PERMANOVA and silhouette were checked against scikit-bio 0.7 and scikit-learn on two views: the F
statistics agree to four decimals (88.8628, 92.6711) and so do the silhouettes (0.394, 0.533).

## Question and answer in one paragraph

Each condition was written by its own authoring agent, so "the cases differ" can mean two things: the
clinical work-up really differs, or each author has a recognisable way of writing. The analysis
separates the two. **The work-up is where conditions differ most**: the condition explains 55–85% of
the variation in required tools, arguments, avoided actions and order, against 3% for shuffled labels,
and copying the work-up of the most similar case from another condition recovers 10% of the required
items (tool level 42%), against 78% from a case of the same condition. **The text is less separated
than it looks**: semantically (embeddings) the narratives of different conditions overlap a lot
(AUC 0.68), and a large part of what makes a narrative recognisable is authorial style (function
words and sentence shape alone identify the condition 58% of the time, chance 5%). Three pairs are
close in work-up (Alzheimer's/FTD, ischaemic stroke/SAH, FND/migraine), the cognitive family is the
least separated, and the proposed test conditions are among the hardest 5% of all 4845 possible test
sets to solve by copying training work-ups.

## Verdicts

| Question | Verdict |
|---|---|
| 1. Do conditions differ in the work-up (tools, arguments, order, what to avoid)? | **YES, strongly**: R² 0.55–0.85, p = 1e-4 in every view; 189–190 of 190 condition pairs differ after Holm (167–171 in the order views) |
| 2. Do they differ in the narrative? | **YES, weakly in meaning, strongly in vocabulary and style**: embedding R² 0.27, AUC 0.68; style alone gives 1-NN 0.59 (chance 0.05) |
| 3. Is it a location shift or just different spread? | **Location**: PERMDISP p 0.77–0.89 in every view |
| 4. Is it explained by difficulty or encounter type? | **NO**: difficulty R² ≤ 0.011; encounter adds ≤ 0.005 once the condition is known |
| 5. Do the a-priori families hold? | **WEAKLY, and only for tools and order**: with our families, gap p 0.0004–0.03 and ARI 0.14–0.24; with the groups of Fig. 2b only required tools survive (p 0.034). Arguments, avoided actions and narrative meaning follow neither |
| 6. Which conditions are near-duplicates? | **Alzheimer's/FTD** (required tools R² 0.016, the one pair not significant after Holm), **stroke/SAH** (0.067), **FND/migraine** (0.099) |
| 7. Can a model solve a new condition by copying a known one? | **NO**: leave-condition-out copy recovers token F1 0.10, diagnosis 6%; no better than copying the most common work-up |
| 8. Is the proposed split a fair held-out test? | **YES**: 5th percentile of copy F1 among the 4845 four-condition test sets, 60th of text similarity |
| 9. Is each condition one answer? | **NO, by design in the puzzles**: 40 cases are coded outside their condition's ICD-10 category, about half of them mimics with another disease as the answer; 173 turn-0 prompts named their own diagnosis, fixed in 113 cases (`b5da9971`) |
| 10. Are cases within a condition diverse? | **NOT ALWAYS**: FND has 2 distinct required sets in 30 cases, NPH 3; the within-condition median distance of required tools is 0 |

## 1. Design

**Unit and groups.** The case is the observation; the condition (20 groups of 30) is the factor. Families
(neuromuscular, cognitive, movement, acute vascular, CNS inflammatory, paroxysmal, infectious, neoplastic,
toxic-metabolic, functional) were written in the script before any distance was computed. They are a
neurologist's textbook grouping and need physician confirmation.

**Views** (one distance matrix each; all distances embed in Euclidean space, so PERMANOVA is valid):

| View | What it compares | Distance |
|---|---|---|
| narrative_tfidf | patient text (complaint, HPI, history, exam) | chord on TF-IDF |
| reports_tfidf | all tool reports of the case | chord on TF-IDF |
| narrative_style | function-word frequencies, sentence and word length, punctuation | chord |
| narrative_embedding, reports_embedding | meaning (embeddinggemma-300m, CERN-hosted, 400-word chunks averaged) | chord |
| required_tools | set of tools in required criteria | √(1 − Jaccard) |
| required_tokens | required criteria as tool + arguments | √(1 − Jaccard) |
| workup_tokens | required + recommended | √(1 − Jaccard) |
| avoided_tokens | waste, harm and contraindicated actions | √(1 − Jaccard) |
| order_pairs_tool, order_pairs_token | ordered pairs from the sequence constraints | √(1 − Jaccard), only the 462/465 cases with constraints |
| order_sequence | canonical order of required tools (topological sort of the constraints) | normalised edit distance |

**Tests per view.**
- PERMANOVA (pseudo-F, R²), also with permutations restricted within difficulty strata.
- PERMDISP: is a difference only in spread?
- Partial R² through Gower-centred matrices: difficulty, encounter type, condition given each.
- Leave-one-out 1-NN and 5-NN purity (chance 5%), silhouette and its share of negative cases, AUC of
  "a between-condition pair is farther than a within-condition pair".
- 190 pairwise PERMANOVAs with Holm and Benjamini–Hochberg, compared with a **sibling null**: the R² of
  two random halves of one condition, which is the size of "no difference" at n = 30.
- Negative control: the same statistics with shuffled labels (expected R² = 19/599 = 0.032, k-NN 5%).
- Families: within-family minus across-family distance between condition centroids, permuting whole
  conditions (n = 20 is the honest sample size here), and adjusted Rand index of a 10-cluster
  hierarchical clustering of conditions against the families.
- Mantel between views, between conditions (20×20) and within conditions (case pairs).

**Functional test (copy baseline).** For each case, retrieve the most similar narrative (TF-IDF or
embedding) under a restriction and copy its required work-up: from the same condition (siblings), from
any case (all_others), from a different condition (leave_condition_out), from a different family
(leave_family_out); plus random, oracle (best possible case in the pool) and popular (the most common
work-up in the pool). Scored with token F1, tool F1, ICD-10 category hit and the rate of copied actions
that the case's policy lists as avoided or harmful. Intervals: bootstrap over conditions (10,000).
Paired tests across the 20 conditions: Wilcoxon signed-rank.

## 2. Main table

R² from PERMANOVA. Pair R² min is the closest condition pair. Shuffled columns are the negative control.

| View | n | R² | R² cond. given encounter | R² difficulty | AUC | 1-NN | Silhouette | Pair R² min | Pairs under sibling p95 | Shuffled R² | Shuffled 1-NN | PERMDISP p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| narrative_tfidf | 0.128 | 0.114 | 0.115 | 0.95 | 0.95 | 0.04 | 0.04 | 0.047 | 0.032 | 0.040 | 0.79 | 0.78 |
| reports_tfidf | 0.322 | 0.284 | 0.284 | 1.00 | 0.99 | 0.15 | 0.15 | 0.103 | 0.031 | 0.058 | 0.77 | 0.72 |
| narrative_style | 0.147 | 0.129 | 0.129 | 0.84 | 0.59 | 0.03 | 0.03 | 0.048 | 0.032 | 0.050 | 0.89 | 0.96 |
| narrative_embedding | 0.270 | 0.229 | 0.230 | 0.68 | 0.71 | −0.03 | −0.03 | 0.055 | 0.035 | 0.050 | 0.77 | 0.78 |
| reports_embedding | 0.448 | 0.369 | 0.369 | 0.82 | 0.95 | 0.10 | 0.10 | 0.118 | 0.032 | 0.030 | 0.78 | 0.82 |
| required_tools | 0.744 | 0.600 | 0.600 | 0.96 | 0.83 | 0.39 | 0.39 | 0.016 | 0.024 | 0.042 | 0.78 | 0.74 |
| required_tokens | 0.597 | 0.515 | 0.515 | 0.97 | 0.98 | 0.42 | 0.42 | 0.139 | 0.033 | 0.060 | 0.77 | 0.78 |
| workup_tokens | 0.549 | 0.472 | 0.472 | 0.98 | 0.99 | 0.34 | 0.34 | 0.153 | 0.032 | 0.042 | 0.77 | 0.82 |
| avoided_tokens | 0.752 | 0.640 | 0.640 | 0.97 | 0.96 | 0.53 | 0.53 | 0.260 | 0.032 | 0.040 | 0.78 | 0.74 |
| order_pairs_tool | 0.765 | 0.679 | 0.679 | 0.95 | 0.84 | 0.49 | 0.49 | 0.037 | 0.036 | 0.039 | 0.79 | 0.84 |
| order_pairs_token | 0.614 | 0.540 | 0.540 | 0.91 | 0.93 | 0.55 | 0.55 | 0.050 | 0.039 | 0.043 | 0.78 | 0.86 |
| order_sequence | 0.852 | 0.652 | 0.652 | 0.97 | 0.82 | 0.40 | 0.40 | 0.037 | 0.032 | 0.057 | 0.77 | 0.80 |

PERMANOVA p is 1e-4 (the minimum with 9999 permutations) in every view, also with permutations
restricted within difficulty strata. Pairwise, after Holm over 190 pairs: 190 significant in the text
views, required tokens, work-up and avoided tokens; 189 in required tools and order sequence (not
AD/FTD); 167 and 171 in the two order-pair views, which cover fewer cases.

Reading:
- The negative controls sit where theory puts them (R² 0.024–0.039, k-NN 3–6%), so the pipeline has no
  built-in bias towards finding differences.
- Pairs "under sibling p95" are pairs whose R² is no larger than random halves of a single condition. In
  the policy views there are none for tools, arguments and avoided actions; a few in the order views,
  where most cases have only one or two constraints (median 1 per case, 135 cases with none).
- Encounter type is almost a copy of the condition (ALS 30/30 outpatient, for example): it explains
  0.08–0.20 alone and nothing once the condition is known (≤ 0.005). It is a confound to state, not an
  alternative explanation.

## 3. The work-up

- **Tools.** The 16 tools are shared, so a tool-level view is the hardest place to differ: still R² 0.74.
  The within-condition median distance is 0: two cases of the same condition usually require exactly
  the same tools.
- **Arguments.** 388 of the 438 distinct required tool+argument tokens occur in one condition only;
  51% of all required instances are condition-exclusive. The most shared are the generic ones
  (`analyze_brain_mri` in 11 conditions, `check_drug_interactions` in 9, `analyze_ecg` in 8).
- **Avoided actions** separate conditions the most among the content views (R² 0.75, silhouette 0.53):
  what not to order is very condition-specific.
- **Order.** 233 of 237 distinct precedence pairs belong to one condition. When two cases constrain the
  same pair of tools, cases of the same condition put them in the same order (17 reversals in 8237
  comparisons, 0.2%, all in bacterial meningitis: CT before or after the lumbar puncture, which depends
  on the case) and cases of different conditions reverse them 17.6% of the time, mostly MRI versus
  clinical assessment (NPH, migraine and FND put them in opposite orders). At the argument level no
  pair is ever reversed: different conditions constrain different studies. A pair ordered both ways
  inside one case is a repeated tool (the NPH tap test: assessment, CSF drainage, assessment) and is not
  counted.
- **Variety inside a condition** (`per_condition.csv`, distinct required token sets among 30 cases):
  FND 2, NPH 3, Parkinson's 7, FTD 7, up to SE 29 and HE 27. A model can learn FND's or NPH's
  work-up from a handful of cases; the stratified test cases of those conditions measure recall of a
  template more than reasoning.

## 4. The text

- **Vocabulary** makes conditions recognisable (narrative TF-IDF 1-NN 0.95) but each narrative is far
  from all others (R² 0.13, silhouette 0.04): many disease words, little shared structure.
- **Meaning** overlaps. With embeddings, a between-condition pair is farther than a within-condition
  pair only 68% of the time, and 62% of the cases have a negative silhouette (closer on average to
  another condition). This is the expected picture for neurology: headache, weakness, confusion and
  seizures appear across many diagnoses.
- **Style** is an authorial fingerprint: from function words, sentence length and punctuation alone,
  1-NN finds the condition 58% of the time (chance 5%, shuffled 5.3%). Each condition was generated by
  its own agent, so a model can learn "which author wrote this" as a shortcut to the diagnosis. The
  shortcut works on stratified test cases (their author is in training) and not on held-out conditions
  (their author never is).
- **Text and work-up are nearly independent between conditions**: the Mantel correlation between the
  narrative distance of two conditions and the distance of their required work-ups is 0.09 (p 0.32; 0.13,
  p 0.24, with embeddings). Conditions that read alike do not need the same tests, which is what a
  diagnostic benchmark wants. Tool reports do track the work-up (0.62, p 0.0009), as they must.

## 5. Families

Mean energy distance between conditions of the same family and of different families; p permutes
the family labels of the 20 conditions; ARI compares a 10-cluster average-linkage clustering of the
conditions with the families.

| View | Within family | Across | Gap p | ARI | ARI p |
|---|---|---|---|---|---|
| required_tools | 0.83 | 1.16 | 0.0004 | 0.24 | 0.010 |
| order_sequence | 0.99 | 1.29 | 0.003 | 0.22 | 0.013 |
| order_pairs_tool | 1.18 | 1.37 | 0.026 | 0.14 | 0.036 |
| required_tokens | 0.89 | 0.92 | 0.33 | 0.11 | 0.11 |
| workup_tokens | 0.72 | 0.77 | 0.20 | −0.04 | 0.82 |
| avoided_tokens | 1.05 | 1.13 | 0.15 | −0.06 | 0.92 |
| order_pairs_token | 1.06 | 1.06 | 0.51 | 0.07 | 0.20 |
| narrative_tfidf | 0.14 | 0.15 | 0.087 | 0.00 | 0.61 |
| narrative_style | 0.16 | 0.19 | 0.009 | 0.05 | 0.30 |
| narrative_embedding | 0.08 | 0.10 | 0.079 | −0.02 | 0.67 |
| reports_tfidf | 0.43 | 0.48 | 0.020 | −0.03 | 0.77 |
| reports_embedding | 0.10 | 0.11 | 0.046 | 0.18 | 0.027 |

Reading: at the level of **which tools** and **in which order**, conditions of the same family are
closer than conditions of different families; at the level of **arguments** (which MRI sequence, which
antibody panel) and of **what to avoid**, the family no longer matters. The narratives' meaning does not
follow the families either. The family structure is real but weak (ARI ≤ 0.24), and with 20 conditions
in 10 families the test has little power. It also depends on the taxonomy: with the nine groups of
Fig. 2b (ALS with neurodegeneration, MS with infection and inflammation, syncope and HE as systemic
mimics; `paper/figures/data/prepare_diversity.py`) only required tools keep a family effect (p 0.034;
order sequence 0.053, report meaning 0.003), and required studies go the other way (p 0.91). The
honest summary is that conditions are distinct one by one, not as families. The cognitive family is the least separated internally
(below). Style clusters by family a little (p 0.009), probably because related conditions were written
from similar sources.

## 6. Closest condition pairs

| Pair | Where they are close | Note |
|---|---|---|
| Alzheimer's / FTD | required tools R² 0.016, order 0.037; FTD cases copying an AD work-up get token F1 0.53 | Same tools (MRI, labs, neuropsych battery), different arguments: they separate at the token level |
| Ischaemic stroke / SAH | required tools 0.067, order 0.11 | Same acute pathway (CT first); differ in CTA/LP arguments |
| FND / migraine with aura | required tools 0.099, order 0.13 | Both have very short required sets (FND 1.2 items on average) |
| AE-NMDAR / SE, HE / SE | report embeddings 0.12–0.13 | EEG and labs reports read alike; work-ups differ |
| GBS / MG | report embeddings 0.13 | Neuromuscular reports; MG nearest-neighbour cases mostly GBS (17/30) |

The differential sections tell the same story from the authors' side: FTD cases name Alzheimer's in
100% of differentials, NPH names vascular dementia 100%, SAH names migraine 93%, FEPI names FND 73%.

## 7. Copy baseline

Token F1 of the required work-up, mean over cases (95% interval over conditions). TF-IDF retriever;
the embedding retriever gives the same picture.

| Pool | Token F1 | Tool F1 | Diagnosis (ICD-3) | Copied avoided action | Copied harmful action |
|---|---|---|---|---|---|
| Same condition, nearest | 0.78 (0.72–0.84) | 0.91 | 0.91 | 3% | 1% |
| Same condition, random | 0.70 | 0.87 | – | – | – |
| Any case, nearest | 0.75 | 0.89 | 0.88 | 4% | 1% |
| Other condition, nearest | 0.10 (0.05–0.16) | 0.42 | 0.06 | 28% | 2% |
| Other family, nearest | 0.06 (0.03–0.09) | 0.36 | 0.05 | 27% | 3% |
| Other condition, random | 0.04 | 0.33 | – | – | – |
| Other condition, most common work-up | 0.09 | 0.45 | – | – | – |
| Other condition, oracle (best case in pool) | 0.37 | 0.87 | – | – | – |

Wilcoxon over the 20 conditions: siblings > other condition p ≈ 1e-6; other condition nearest > random
p 0.003; nearest > most common work-up p 0.37 (embeddings 0.83).

Reading:
- Within a condition the cases are nearly interchangeable (0.78); across conditions nothing transfers at
  the argument level (0.10, no better than copying the most common work-up).
- The oracle shows the ceiling: even the best possible case from another condition covers only 37% of
  the required arguments, while it covers 87% of the tools. A model that has learned the tools can reach
  a new condition's tool set; it cannot reach the arguments without clinical knowledge of that condition.
- Copying from another condition puts an avoided action into 28% of work-ups: across conditions the
  policies disagree, which is the property that makes a held-out condition a real test.
- Exceptions (per condition, `copy` → `by_condition` in `summary.json`): FTD 0.53, vascular dementia
  0.27, NPH 0.22 when copying from other conditions. The cognitive conditions borrow from each other.

## 8. The proposed split

Test MG, HEP-ENC, BACT-MEN, GLIO-HG; validation MS-RR, SYNC-CARD. FND was the first validation choice and
left it on 3 Nov 2026: with 2 distinct required sets in 30 cases it cannot rank configurations. Its
replacement is the training condition with the lowest copy F1 (0.017) among those with at least 15
distinct required sets (cardiac syncope, 17), dataset criteria only. Among all C(20,4) = 4845 choices of four
test conditions, the proposed set sits at:
- the **60th percentile** of nearest-narrative similarity to the other conditions (range 0.115–0.177;
  proposed 0.149): an ordinary set, not a set picked for being textually remote;
- the **5th percentile** of copy F1 (range 0.002–0.293; proposed 0.025): one of the hardest sets to solve
  by copying a training work-up.

Many test cases share **no required study at all** with any case of another condition: glioma 27 of
30, myasthenia 19, against 0 for 13 of the 20 conditions (validation: cardiac syncope 0; train: FND 23,
migraine 18).
For these cases a model has to produce the work-up from clinical knowledge; nothing in training
contains it.

Per test condition: MG is the closest to training (tool F1 0.50 when copying, nearest cases GBS 17/30
and ALS 6/30), so its result partly measures neuromuscular transfer; HE's nearest cases are NPH (18/30)
but their work-ups share little (tool F1 0.20); BACT-MEN and GLIO-HG copy at tool F1 0.39 and 0.36.
Validation: MS copies at tool F1 0.22 (nearest cases now FND 13/30 and stroke 12/30); cardiac syncope at
0.06, although 22 of its 30 nearest narratives are FND (transient loss of consciousness reads alike, the
work-ups do not overlap).

This is a property of the dataset, not a choice made on model results, so it does not violate the rule
of not using the test conditions for configuration choices.

## 9. Answers and labels

- **ICD-10 categories.** Each condition's codes were taken as its most frequent categories until they
  cover 80% of its cases: one category per condition (G12, G30, … F01), five for cardiac syncope (I42,
  I44, I45, I47, I49). No two conditions share one. 24 of the 30 SE cases also carry G40, the epilepsy
  underlying the status, so "epilepsy" gets the category right for them; the scorer matches labels, not
  codes (`icd10_code` has weight 0), so this affects only the ICD-3 metric of this analysis.
- **40 cases fall outside their condition's categories** (`summary.json` → `answers`). About half are
  coding variants of the same disease (MCI due to AD as G31.84, meningococcal meningitis A39.0, spinal
  glioblastoma C72.0, cardiac syncope coded by its cause, CADASIL vascular dementia). The other half are
  diagnostic puzzles whose answer is a mimic: atypical parkinsonism in PD (MSA, DLB, PSP), TB and
  cryptococcal meningitis in BACT-MEN, CNS lymphoma in GLIO-HG, MELAS and CADASIL in migraine, toxic
  causes in SE. So the condition label is the **presentation**, not always the answer. This adds
  diversity inside a condition and is what the puzzle tier is for.
- Six mimics have **another NeuroBench condition** as the answer: SE-P02 and FEPI-TEMP-P03 (FND),
  SE-P07 (HE), HEP-ENC-P06 (SE), MIG-AURA-P07 and SE-P04 (ischaemic stroke); FEPI-TEMP-P02 (LGI1) is
  close to AE-NMDAR. With FND in training, the two that cross the split boundary (SE-P07, answer HE;
  HEP-ENC-P06, answer SE) are the proposed exclusion list; no case of another condition has cardiac
  syncope as its answer and no cardiac syncope case has another NeuroBench condition as its answer.
- **The narrative names its own diagnosis.** This analysis found 115 cases with labels of at least 6
  characters. The check on the turn-0 prompt with every accepted label, acronyms included, found 173:
  the filter missed acronyms ("No ALS family history" in 23 ALS cases; FTD, MG, HE, SE, FND, PD, MS) and
  medication indications ("Lactulose (HE prophylaxis)"). The negated family history naming exactly the
  target disease is an authoring tell. **Fixed at the class level on 3 Nov 2026 (commit `b5da9971`,
  not yet on master)**: 113 cases, 125 edits, of which 98 negated family histories (ALS 23, MS 23, PD 19,
  migraine 13, FTD 9, …), 7 negated personal histories, 4 patient worries and 3 referrals naming the
  answer. Known-disease scenarios, positive family histories with a clinical role and observed SE were
  kept. Decisions: `data/review/round-2026-10/plans/DX-NAMED-decisions.md`. The text views of this
  analysis were computed before the fix and must be rerun once it is merged.

## 10. Limits

- Statistically different is not clinically independent. The policies are drafts; the work-up
  distances measure what the authors wrote.
- The views are not independent (required tools and order sequence correlate 0.85 within conditions):
  they are 12 descriptions of one dataset, not 12 confirmations.
- With n = 30 per condition every pair passes PERMANOVA; effect sizes (R², the sibling null, the copy
  baseline) are the informative part, not p-values.
- The family test has 20 units; families are a priori and need a neurologist's confirmation.
- Embeddings come from one small model (embeddinggemma-300m) on 400-word chunks. `e5-large-v2` on the
  gateway did not answer on 3 Nov 2026.
- Order views cover the 462 cases that have at least one constraint, with a median of one constraint.

## Figure and tables for the paper

Built like Figures 1–2 (HTML/CSS, `python3 paper/figures/build.py <name>` → PDF and PNG); numbers from
`paper/figures/data/diversity.json`, written by `paper/figures/data/prepare_diversity.py`, which reads
this analysis's outputs and recomputes the split enumeration, the family tests and the closest work-up.

- `paper/figures/fig_ed_diversity.{html,pdf,png}`: Extended Data figure, 180 × 161.8 mm.
- `paper/figures/tab_ed_views.{html,pdf,png}`: Extended Data table, one row per view.
- `paper/figures/tab_ed_conditions.{html,pdf,png}`: Extended Data table, one row per condition.

Draft legend of the figure:

> **Conditions differ in their work-up much more than in their text.** **a**, Share of variation
> between cases explained by the condition (PERMANOVA R², left) and share of cases whose nearest other
> case belongs to the same condition (1-NN, right), for five descriptions of the text and seven of the
> work-up (required tools; required studies, i.e. tool plus arguments; required and recommended;
> actions to avoid; order constraints as tool pairs, study pairs and full sequence). Open circles: the
> same statistic with condition labels shuffled. Tiles: specificity of the work-up vocabulary and the
> largest R² of case difficulty. **b**, Pairwise PERMANOVA R² between the 20 conditions, grouped as in
> Fig. 2b; upper triangle required studies, lower triangle narrative meaning (embedding). Orange: the R²
> of two random halves of one condition (95th percentile), the size of no difference. Test conditions of
> the proposed split in bold. **c**, Token F1 of the required studies (left) and tools (right) when a
> case copies the required work-up of another case: the most similar narrative within its condition,
> from another condition or from another family, against random, most common and best possible copies.
> Bars, 95% bootstrap intervals over conditions. **d**, All 4845 choices of four test conditions, by the
> narrative similarity of their cases to the nearest case of the remaining conditions and by the F1 of
> copying that case's work-up. Blue, the proposed test set. 600 cases; 9999 permutations; policies are
> drafts pending physician approval.

## What to do with this

1. Paper: report the main table (R², 1-NN, sibling null, shuffled control) for text and work-up, the copy
   baseline, and the split percentile. Say that conditions differ mainly in the work-up and that text
   style carries an authorial signal.
2. Dataset, at the class level: remove the target disease from negated family histories (MS, PD first);
   consider more within-condition variety for FND, NPH, PD and FTD before using their stratified cases
   as a test.
3. Interpretation of held-out results: report MG separately (it borrows from GBS/ALS); treat AD/FTD and
   stroke/SAH as near pairs if either is ever held out.
