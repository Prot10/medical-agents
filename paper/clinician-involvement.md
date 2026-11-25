# Clinician involvement in comparable papers (25 Nov 2026)

How many clinicians the close papers used, of what kind, and for which role. Read from the main texts (PDFs in
`docs/research/pdfs`, Nature/arXiv HTML for Hager, PsychFound, HealthBench, MedR-Bench, CRAFT-MD) and from the
published peer review files of MIRA, AMIE and PsychFound. Supplements were not read: "NR" = not reported in the main
text. AMIE and Med-PaLM were read in their arXiv v1; the Nature versions changed the rating design (see AMIE below).

Roles: **a** writes cases or data; **b** sets the reference (ground truth, rubric, policy); **c** reviews the dataset;
**d** rates model outputs; **e** human baseline; **f** validates an LLM judge or simulator.

## 1. Table

| Paper | Venue | Clinicians | Type and seniority | Roles | Raters per item / agreement |
|---|---|---|---|---|---|
| SDBench / MAI-DxO (Nori) | Science 2026 | 21 in the baseline + an in-house panel (NR) | 17 primary care + 4 hospital generalists, US/UK, median 12 y | b (rubric), c (508 gatekeeper answers), e (21: ~36 cases each, 56 test cases), f (judge κ 0.70) | no inter-physician agreement |
| MIRA (Ferber) | Nature 2026 | 10 in the baseline + 2 dataset reviewers + 1 blind rater | first 4 residents (0–5 y) + radiologist + haemato-oncologist; **reviewers asked for more senior ones** → 4 board-certified, 7–11 y, ED experience | c (600 cases × 2 physicians), d (1 blind physician, 56 patients), e (1 physician per case), f (several judges, 1 physician) | 1 per item; no inter-physician κ |
| Hager (MIMIC-CDM) | Nat Med 2024 | 5 (all co-authors) | 1 author made all medical decisions; 4 internal medicine/ED: 3 residents (2–4 y, Germany) + 1 US hospitalist (29 y) | a, b, d (one person); e (4 × 80 cases) | 1; no κ |
| DiagGym (Qiu) | arXiv 2025 | ≥12 | "senior physicians", >10 y; specialty NR | b (399 cases: 2 write rubrics, 1 reviews, 1 weights), c (1 per case), d (3 rate the simulator), f (12, 3 per item) | % agreement with majority; no κ |
| AgentClinic | arXiv 2025 | 3 + 3 | "MDs"; NR | d (realism), e (3 physicians) | NR |
| PsychFound (Wang) | **NMI 2026** | ≥90 (24 trial residents + 60 readers + small expert panels) | psychiatry, one hospital in Beijing; residents / attendings / seniors (20 each in the reader study); raters >20 y | all six roles, incl. a randomised trial | 2 blind raters, weighted κ 0.72–0.84; judge check κ 0.71/0.75 |
| AMIE (Tu) | Nature 2025 | 20 PCPs + 23 specialists + OSCE labs | PCPs 3–25 y; specialists matched to the case, 1–36 y | a (OSCE packs), b (rubric via focus groups), d (blind), e (20 PCPs) | **1 per case in the preprint; reviewer called it a "major weakness"** → 3 per case, κ >0.6 on 31/32 axes |
| AMIE DDx (McDuff) | Nature 2025 | 39 (paid via vendors) | 20 internal medicine (median 9 y) + 19 specialists (median 14 y; 3 neurologists) | b, d (1 specialist per case), e | 1; judge κ 0.63 |
| Med-PaLM (Singhal) | Nature 2023 | 9 raters + 5 for exemplars + panels NR | US/UK/India; primary care, surgery, internal medicine, paediatrics | a, b, d (blind, 1 per answer) | 1; NR |
| HealthBench | arXiv 2025 (OpenAI) | 262, paid | 26 specialties, 60 countries; 50% attendings | a, b (48k criteria, 1 author each), d/f | 55–75% agreement |
| MedHELM (Bedi) | arXiv 2025 | 29 (taxonomy) + 20 (raters) | 14 specialties, mostly Stanford | b, d/f | ≥2 per item, ICC 0.43 between clinicians |
| MedR-Bench (Qiu) | Nat Commun 2025 | 6 (not authors) | ~5 y, one Shanghai hospital; specialty NR | c (100 cases × 3), e, f | majority vote, % only |
| CRAFT-MD (Johri) | Nat Med 2025 | 5 dermatologists (co-authors) | board-certified, US | a (100 vignettes), d (⅓ double-rated), e (2), f (1) | raw counts; 15–16 h total |
| Ferber oncology agent | Nat Cancer 2025 | 4 + 1 radiologist (co-authors) | oncology | b, d (4 per item, majority) | NR |
| Barrit neurology | Brain Sci 2025 | 15 | 13 neurologists (8 board-certified, 5 senior residents) + 2 senior academic raters | d (blind), e | ICC 0.77 |
| MedAgentBench | NEJM AI 2025 | 2 (co-authors) | internal medicine | a | — |
| MDAgents | NeurIPS 2024 | 3 | 2 PGY-2 internal medicine + 1 GP | f | ICC 0.27 |
| Med-RLVR, MedAgentGym, MedAgents, TxAgent | various | 0 identified | — | — | — |

## 2. Patterns

1. **Scale follows the group, not the venue.** Hundreds of clinicians (HealthBench, Google's AMIE) come from industry
   budgets with paid vendors. Academic agent papers in Nature-family journals work with **4–12 clinicians**: Hager 5,
   MIRA ~13, CRAFT-MD 5, DiagGym ≥12, SDBench 21 in the baseline.
2. **Many published papers have one clinician per item and no inter-rater agreement** (Hager, MIRA, AMIE DDx,
   Med-PaLM, SDBench). Reviewers let it pass when it was not the headline result, and attacked it when it was
   (AMIE: single specialist rating the main outcome → triplicated).
3. **What reviewers attacked was the kind and independence of the clinicians, not the count.**
   - MIRA: 6 clinicians of mixed seniority, 4 of them residents → "too small and unrepresentative", "benchmark against
     more experienced and specialist clinicians". Answer: 4 board-certified physicians added.
   - AMIE: number of specialists not stated, no double coding, no reliability testing → "major weakness".
   - PsychFound (NMI): clustering by physician, blinding of the adjudicator, human check of the LLM judge.
   - SDBench states its generalist-only baseline as a limitation.
4. **Specialty match counts.** AMIE DDx matched raters to the case specialty; MIRA's reviewers wanted emergency
   physicians for emergency cases. For a neurology benchmark, neurologists are the right raters.
5. **Clinicians as co-authors are common** (Hager, CRAFT-MD, MedAgentBench, Ferber, Goodell) and accepted, provided
   the role of each is stated in the Methods and the contributions.
6. **The reference built by the same clinicians who then rate is rarely addressed**, but reviewers raise the
   equivalent concern (PsychFound: adjudicator blinding; MIRA: an independent panel for the ground truth).

## 3. Where NeuroAgent stands

- Reference policies: 2 neurologists, each case reviewed twice but one after the other under one account, so no
  agreement can be computed yet; a third reviewer never logged in. Seniority and years of experience are not
  recorded in the repo.
- Planned (decisions.md): one condition redone with two accounts (κ); 20–30 MIMIC-IV admissions solved by physicians;
  ~100 work-ups rated blind; at least one neurologist who has not seen the policies.

Compared with the table: the policy review (600 cases, per-case process references) is a larger clinician effort per
case than most papers. The weak points are those reviewers attacked elsewhere: **only two people**, **the same two
for the reference, the ratings and the baseline**, **seniority not stated**, **no agreement measure yet**.

## 4. Decisions (Andrea, 25 Nov 2026)

Our two neurologists are not senior (exact level and years still to be recorded). The physicians are not the story of
the paper, which is a machine learning paper about the reward; they are the foundation the story stands on: the thesis
says the model learns "the work-up physicians ask for", so a doubt on the physicians is a doubt on the thesis. The
clinical part must become **more solid, not more central in the narrative**. Goal: leave no opening for the attacks
listed in section 2 (too few, too junior, not independent, no agreement, circularity).

### Where the physicians matter, ranked

| # | Where | Weight | Is a junior neurologist enough? | What closes the attack |
|---|---|---|---|---|
| 1 | Case policies = the reference, the reward and the metric | Highest | Not alone | Each policy cites its guideline (the reference is the guideline, checked by physicians, not two opinions); **one senior neurologist** (board-certified, >10 y) audits a sample (e.g. 2 cases per condition = 40) and we report agreement with the two reviewers; κ between the two reviewers on ≥1 condition reviewed with separate accounts |
| 2 | Blind rating of model work-ups (Fig. 4a–b, claim C3) | High | Yes, if independent | At least one rater who never saw the policies (ideally the same senior of row 1); 2–3 raters per item; κ |
| 3 | Physicians solve cases like the agent (Fig. 4c) | Medium | Yes, if stated | State their level ("neurologists in training" if so); the claim "orders about as many tests as physicians" is weaker with trainees, who tend to order more, so lean on Fig. 5 (tests recorded by the treating clinicians in MIMIC-IV), which does not depend on our physicians |
| 4 | Checking the LLM that translates free-text requests (GLM-5.3) and the LLM-judge row of Fig. 4a | Low | Yes | A sample of 100–200 translations checked by a physician, % agreement reported. Our main score is deterministic, not an LLM judge: say so as a strength |

### Actions

- [ ] Record for each physician: specialty, training level, years of experience, country, role, blinding, payment,
      co-authorship. Goes in the Methods (no names).
- [ ] Find one senior neurologist (supervisors' network) for a limited number of hours: policy audit (row 1) and blind
      rating (row 2).
- [ ] Policies: every rule traceable to a cited guideline; list the guideline per condition in the Supplementary.
- [ ] κ between the two current reviewers (one condition, separate accounts), already planned in `decisions.md`.
- [ ] Blind rating: raters who wrote the policies reported apart from the independent ones.
- [ ] Physicians solving cases: wording matched to their level; the two policy reviewers reported apart.
- [ ] Translation check on a sample (row 4).
- [ ] Claims: never "as physicians do" without the level; never "outperforms physicians".

Target size: about 3–4 neurologists with clear roles (the 2 current + 1 senior, + 1 independent if possible). Beyond
~8 the gain with reviewers is small: independence, seniority on the reference and measured agreement matter more than
the headcount.
