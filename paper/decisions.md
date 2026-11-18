# Paper: decisions

Updated 17 Nov 2026. One line per decision, with its date. The manuscript plan (`manuscript/`) was brought in line with this file on 17 Nov: anything there that disagrees with it is a bug.

## Journal
- **Nature Machine Intelligence** (17 Nov). ICML dropped: the method alone was judged too weak.

## Content
- Two trained models compared (17 Nov):
  - A: rewarded for the right tests in the right order (final reward);
  - B: rewarded only for a correct diagnosis and a low cost.
- The discarded reward versions, with reasons and numbers (17 Nov):
  - 3 Nov: answering without tests scored ≥ a complete work-up in 225/600 cases → fixed;
  - 13 Nov: A ordered 5.8 useless tests per case → −0.03 for every useless test.

## Agent reasoning (17 Nov)
- Qwen and Gemma currently run with thinking off (decided with vLLM 0.23 and 4,096 tokens: Qwen ran out of tokens without calling any test).
- To check whether it is still the best choice: "do not make it dumber than necessary".
- Test: untrained Qwen3.5-9B, thinking off vs on at 8k / 16k / 32k tokens, 60 validation cases × 3 seeds. No test case.
- If thinking wins: decide after seeing how much it wins and what retraining A and B costs.
- **Result (17 Nov): thinking loses at every budget → A and B stay without thinking, no retraining.**

  | Thinking | Score | Diagnosis | Tests | Invalid actions | Failed episodes |
  |---|---|---|---|---|---|
  | off | 0.41 | 0.88 | 3.6 | 29 | 1 |
  | 8k | 0.38 | 0.82 | 2.9 | 188 | 18 |
  | 16k | 0.39 | 0.84 | 2.7 | 183 | 16 |
  | 32k | 0.38 | 0.81 | 2.8 | 173 | 12 |

  Mean of 3 seeds over 180 episodes per row. The budget does not matter (~600 tokens per turn, 6k at most). With thinking, Qwen asks for several tests in the same turn (~120 times against 12) or answers without calling any test. Data: EOS `runs/thinking_val_20261117/`. Goes in ED as the reason for the choice.

## LaTeX template (17 Nov)
- NMI has no template of its own: it points to the Springer Nature template (option `sn-nature`, "Nature Portfolio journals"). Our `sn-jnl.cls` and `sn-nature.bst` are identical to the official December 2024 zip, the latest version.
- For the final version NMI wants a single .tex file, Computer Modern fonts, no non-standard packages or personal macros, the bibliography pasted from the .bbl.

## Clinical validation
- Status (meeting of 16 Nov): every case reviewed by two physicians, independently, one after the other, on the same account.
- To ask / asked:
  - [ ] one condition redone with two separate accounts → inter-physician agreement (kappa);
  - [ ] after the corrections: a sample of cases checked again;
  - [ ] 20–30 cases solved by the physicians → physician vs agent comparison (Fig. 4c);
  - [ ] ~100 model work-ups rated blind → does our score agree with the physicians?
- In the Methods: role and experience of the physicians, not their names.

## Where things go (17 Nov)
NMI: **Main** at most 6 figures/tables and ~3,500 words · **Extended Data (ED)** at most 10, inside the article · **Supplementary** no limit, separate PDF.

| Experiment | Where |
|---|---|
| A vs B vs base, synthetic test, 3 seeds | Main |
| Reward history (discarded versions) | ED (moved out of the Main on 17 Nov, see Figure 3) |
| Base models: correct diagnosis with wrong or missing tests (Qwen, Gemma, Granite, 2–3 large) | Main |
| Physicians rate ~100 work-ups blind: does the score agree? | Main |
| Physicians solve 20–30 cases: physician vs agent | Main |
| Transfer to 100 MIMIC neuro cases | Main |
| A (9B) vs larger models + cost and time on one GPU | Main (one figure) |
| Inter-physician agreement + re-checked sample | Main briefly + ED |
| Training on other models (Gemma, small Qwen, maybe Granite), 1 seed | ED |
| Per condition, with a clinical reading | ED + Discussion |
| Acute vs chronic (synthetic only) | ED |
| Controls: no-test and no-menu baselines + scripted agents (perfect, orders everything, no test) | ED (one figure) |
| Robustness: changed score weights + cases with contradictory facts | ED (one figure) |
| The dataset: what a case looks like, 20 conditions and splits, physician review (the old October Fig. 2) | ED |
| Non-neurological MIMIC, subset of ~100 cases | Trial; placement decided from the results |
| RL with MIMIC cases: 50 in training, 50 in test (with the current 100) | Exploratory; placement decided from the results |
| Reasons for the requests: every test ordered carries a reason written by the model; are they correct? (17 Nov) | To decide |

Extended Data (17 Nov): 9 items of 10, merged by topic because we were at 12: eight figures and Extended Data Table 1 (main results). The thinking test moved to Supplementary Table 11, so one slot stays free for a row still to decide (non-neurological MIMIC, reasons for the requests).

| ED | Content |
|---|---|
| 1 | The dataset |
| 2 | Reward history |
| 3 | Inter-physician agreement + re-checked sample |
| 4 | Training on other models |
| 5 | Per condition |
| 6 | Acute vs chronic |
| 7 | Controls (no test, no menu, scripted agents) |
| 8 | Robustness (weights, contradictory facts) |
| Table 1 | Main results: untrained, B, A on the NeuroBench test and on MIMIC, with the A − B difference |
| (free) | Non-neurological MIMIC or reasons for the requests, decided from the results |

Main figures (17 Nov; several experiments can share a figure, in different panels):

| Fig. | Content |
|---|---|
| 1 | Overview: cases, tests, score, physician review (+ inter-physician agreement) |
| 2 | Correct diagnosis with wrong or missing tests, untrained models (models only since 18 Nov) |
| 3 | A vs B vs base (the reward history moved to ED2 on 17 Nov) |
| 4 | The physicians: (a) blind rating vs score, (b) physician vs agent on the same cases |
| 5 | Real MIMIC neuro cases |
| 6 | A vs larger models, and cost on one GPU |

Palette (17 Nov), the same in every figure — Okabe-Ito, colour-blind safe (Wong, Nat Methods 2011):

| Role | Colour |
|---|---|
| Model A (rewarded on the work-up) | blue `#0072B2` |
| Model B (rewarded on diagnosis + cost) | orange `#E69F00` |
| Base (untrained) | grey `#999999` |
| Physicians / policy | pink `#CC79A7` |
| Correct ✓ | green `#009E73` |
| Error ✗ | vermilion `#D55E00` |

Approval (18 Nov): Andrea approved Figures 1–5 as drawn here. For Figs. 2–5 this approves the layout; the marks sit on invented data and every number stays "xx" until the runs and the physician studies exist (Fig. 5 prints only the fixed cohort counts 12 and 88).

Figure 1 (17 Nov):
- From scratch, simpler than the 26 Oct version; SVG file, then PDF.
- Laid out like NMI Fig. 1s: 180 × 133 mm, one row from left to right: a (cases, narrow) → b (episode, wide in the centre) → c (policy, narrow), same height. Changed on 17 Nov: a and c stacked on the left did not read in order.
- "Same diagnosis, different tests" moves to Fig. 2; "data in the hospital" to Fig. 6.
- A single real case as a comic strip, laid out like SDBench Fig. 1 (requests on the left, results on the right, thinking in a box, outcome at the bottom).
- Shows our method, not the base model: a real episode of model A (trained Qwen, checkpoint chosen on validation) on SYNC-CARD-RS03, a validation case never seen in training (the stroke case was a training case). Changed on 17 Nov.
- Every request shows the reason the model actually writes (the `clinical_context` field of the call), quoted with ellipses only.
- ✓/✗ for each policy item on the same case + the case score (0.96: the CT after the fall is missing); no overall number. Also (17 Nov), from the same episode: no useless test, stops when done, test cost $524.
- Panel a: two boxes of numbers (NeuroBench 600 → 419 / 60 / 119; MIMIC 100 admissions, 9 conditions, test only).
- Rounded boxes with a pale background, like the October figure.
- Panel b: all 5 tests, one numbered row per turn along a vertical line; on the left NeuroAgent's request (blue: test + reason), on the right, on the same row, the simulated hospital's answer (arrows both ways). Request and answer are widgets of the same shape: a coloured header (test / report name) and text below (reason / result). The drug-interaction check has no reason: it says so in grey. Then the final assessment. No thinking box and no summary block.
- In the manuscript since 17 Nov (`sections/02-results.tex`, file `fig1-new.pdf`), at its true width of 180 mm: shrunk to the template column (~130 mm) the text dropped to 5 pt.
- One name for the score, "policy score", in figures and legends (17 Nov): the Fig. 1 box said "Case score". Legend re-checked with the style skill: a positive title, b in two sentences, green ✓ and orange ✗ described in words as NMI asks.
- Legend (17 Nov), 139 words: says what each panel shows and what is needed to read it; numbers and the case story are in the figure and are not repeated (like the Fig. 1s of NMI, AMIE, AgentClinic).
- Measured fonts (17 Nov): published NMI has body text at 8.2 pt, legends at 7 pt, figures at 5.5–6.5 pt. Ours: figure 7 pt, legend 8 pt, template text 10 pt.
- NMI/Nature rules applied (17 Nov; NMI "AIP and formatting" page and the Nature figure guide): at most 180 mm wide, at most 170 mm high (we are at 129), sans-serif text 5–7 pt, letters 8 pt; all text black (no coloured text), no decorative icons (colour stays in backgrounds, borders and ✓/✗); PDF with editable TrueType fonts, no Type 3 → PDF printed with Chrome (`paper/figures/fig1_pdf.sh`).
- Text: all at 7 pt, panel letters 8 pt bold lower case (Nature guide: text 5–7 pt, 7 at most); no large numbers, no italics (the letters overlapped in the PDF), no arrows between panels.

Figure 2 (17 Nov), draft to settle the layout (`paper/figures/fig2_svg.py`, `fig2-new.pdf`, 180 × 129 mm, same palette and NMI rules as Fig. 1):
- Forms taken from similar papers: accuracy against another measure, one point per model (SDBench, npj Digit. Med. 2026); two rankings compared (AgentClinic); 100% bars for the outcomes (npj Digit. Med. 2026).
- Two rows: a | b on top, c | d below.
- a: accuracy against policy score, one point per model with 95% CI, name just past the interval; grey circle = open models up to 9B, black square = larger models.
- b: ranking by accuracy against ranking by score, crossing lines, Kendall's tau below.
- c: what lies behind the correct diagnoses, 100% bars: complete work-up / required test missed / unsafe action.
- d: the same correct diagnosis, three work-ups; model name above, tests as pills (required in order, not needed, out of order), cost and score on the right.
- No "fake values" labels: every printed number is "xx" until the real runs exist; the names of the large models are placeholders.
- Legend in the manuscript (17 Nov, 202 words, "xx" where data are missing): a title that states the result, then per panel what is drawn, on which data, what symbols and error bars mean, and a single sentence of reading. As in NMI, AMIE and Ferber (Nature Cancer 2025): a brief comment on the results, no method detail.
- The old October dataset figure moved to Extended Data Fig. 1 (17 Nov), as a draft to redo in the house style.

Figure 3 (17 Nov), draft to settle the layout (`paper/figures/fig3_svg.py`, `fig3-new.pdf`, 180 × 131 mm, same rules as Fig. 2; every number is "xx"). Redone the same day after the research on what reviewers expect (`paper/nmi-notes.md`):
- Three models in every panel: untrained (grey), rewarded on diagnosis + cost (orange, "Outcome reward"), rewarded on the work-up (blue, "Policy reward").
- a: correct diagnoses and tests per case on validation over training, mean and range across seeds; open circle = chosen checkpoint. Not the policy score: for the orange model it would be circular.
- b: test, seven measures: the independent ones first (correct diagnoses, required tests ordered, cases with an unsafe action, cost), then both scores (outcome and policy): each model wins on its own, so B does not look like a weak opponent. P of the paired policy vs outcome comparison.
- c: per test condition (only 4: a reviewer will ask whether the effect comes from one of them).
- d: why the outcome reward loses diagnoses: cases the untrained model solves from the story alone against cases that need tests (split taken from the no-test run).
- Out of the Main: the reward history goes entirely to ED2 (in the Main it suggests "they changed the reward until it worked", and it rests on one seed and on validation); the single case leaves (the widget is already in Figs 1 and 2).
- The panel on unseen conditions from the R3 plan is not needed: the test set contains only conditions excluded from training.

Figure 2, changes of 17 Nov after the same research: one more class in the bars of c, "complete but with useless tests" (MIRA's reviewers, Nature 2026, asked for precision and a penalty for useless tests), and "n = xx" correct diagnoses next to each bar (Hager, Nat Med 2024). The same day, at Andrea's decision, the neurologists enter Fig. 2 as a human reference: a pink diamond in panel a and a row in the bars of c (Hager, MIRA and SDBench put clinicians beside the models). Needs the 20–30 cases solved by the physicians; in panel a the neurologists cover a subset of the cases, and the models on the same cases go to ED. **Reversed on 18 Nov (Andrea):** the neurologists left Fig. 2 (pink diamond in a, row in c, legend key) because they solve only 20–30 cases while the models solve all 119, and Fig. 4c already compares them with the models on the same cases; Supplementary Table 2 lost its neurologist block, now Supplementary Table 12.

Figure 4 (18 Nov), layout (`paper/figures/fig4_svg.py`, `fig4-new.pdf`, 180 × 100 mm, same rules as Figs. 2–3; every number is "xx"). Figures and tables are drafts until Andrea approves each one (18 Nov). Redone the same day at Andrea's request: shorter texts, better use of space, no overlap with the other figures.
- One question per row. Top: does the policy score measure what neurologists value (blind rating)? Bottom: how close is each model to neurologists who solve the same cases?
- a: Spearman correlation of each score with the blind ratings (policy score, outcome score, diagnosis alone, LLM judge), with the agreement between two neurologists as a band, the most a score can reach. The LLM-judge row needs a new, cheap run; it answers the most frequent reviewer request (validate automatic judges against clinicians).
- b: ratings of correct diagnoses by the four work-up classes of Fig. 2c: uses no score, so it also answers circularity.
- c: the three models read against the neurologist of each case (agrees on the diagnosis, the neurologist's tests ordered), plus required coverage and tests per case for everyone, which show how far the neurologists follow the policy. No P values: 20–30 cases, and the paper claims nothing about beating physicians.
- Dropped: the text panel with the study design (it repeated the legend); measures already in Fig. 3b (unsafe actions on the full test set).
- Every row is a horizontal dot plot with labels on the left, so no label wraps.
- Overlap resolved (18 Nov, Andrea): the neurologists left Fig. 2; physicians appear only in Fig. 4, compared with the models on the same cases. Numbers in Supplementary Table 12. The only other human reference is Fig. 5c, the tests the MIMIC-IV clinicians recorded for real patients, which is a different source (record, not a study).

Figure 5 (18 Nov), layout approved by Andrea the same day (`paper/figures/fig5_svg.py`, `fig5-new.pdf`, 180 × 100 mm, same rules as Figs. 2–4; every number is "xx" except the fixed cohort counts 12 and 88). One question per panel, checked against Figs. 1–4:
- a: policy reward minus outcome reward, paired by case, for correct diagnoses, required tests ordered and cases with an unsafe action, NeuroBench test and MIMIC-IV side by side: does the direction hold on real records? Fig. 3b shows the NeuroBench levels; the NeuroBench differences are repeated here only as the anchor of the comparison.
- b: MIMIC-IV split as Supplementary Table 1 (12 kept out of training, 88 seen in training or validation), laid out like Fig. 3c: is the result carried by conditions the models trained on?
- c: the three models against the tests the clinicians recorded for the same patients (tests the clinicians also did, clinicians' tests ordered, tests per case), laid out like Fig. 4c so the two human references read the same way. Numbers in Supplementary Table 13.
- Left out: the cohort flow (an Extended Data CONSORT diagram) and the policy score (in ED Table 1; the MIMIC-IV policies are still drafts).

Captions (18 Nov), all four re-checked against the current drawings, at most 250 words each (Fig. 1 ~190, Fig. 2 ~245, Fig. 3 ~215, Fig. 4 ~225):
- Fig. 1: the drug check takes no reason; the score also checks useless tests and stopping ("Also scored" in c); test cost at Medicare prices.
- Fig. 2: no neurologists; "points are means"; n counted over all seeds; the colours of d said in words (green, grey, orange), as NMI asks.
- Fig. 3: one opening sentence names the three models; error bars, CIs and the paired, corrected test stated once for b–d (c and d had none); the test itself is left to Methods until the choice between Wilcoxon and McNemar is made.
- Fig. 4: written for the redesigned figure; the pink line is the agreement between two neurologists and the band its CI.
- Style pass (18 Nov, skill scientific-paper-style, approved by Andrea): "work-up" defined in the Fig. 1 caption; reading sentences about results not yet measured removed; long sentences split.

Names (18 Nov), one per measure in captions, figure labels, tables and plan text: "Correct diagnoses (%)" (never "accuracy" or "correct diagnosis"), "Required tests ordered (%)", "Cases with an unsafe action (%)", "Cost per case ($)", "Tests per case", "Useless tests per case", "policy score", "outcome score". The ingredients of the outcome reward are "diagnosis and cost". "Accuracy" stays only where another paper's figure is cited and in the reward component "tool accuracy".

Notes:
- Weights of models trained on MIMIC: not freely publishable (PhysioNet agreement).
- Everything in the repository is written in English (Andrea, 17 Nov).

## Tables (17 Nov)
File `manuscript/sections/08-tables.tex`. Values are `xx ± xx` (mean ± s.d. across 3 seeds) and `xx (xx to xx)` (95% CI, bootstrap over cases, paired by case) until the runs exist; known facts are filled in.

| Table | Content |
|---|---|
| ED Table 1 | Main results, two blocks (NeuroBench test 119, MIMIC 100): untrained, outcome reward, policy reward, policy − outcome difference with CI, P (Wilcoxon or McNemar, Benjamini–Hochberg per block). Rows: correct diagnosis, required, recommended, unsafe, useless tests, tests, cost, outcome score, policy score |
| Supp 1 | MIMIC split: conditions kept out of training (HEP 10 + BACT 2) vs seen in training or validation (88) |
| Supp 2 | Untrained models (numbers behind Fig. 2) with ranks |
| Supp 3 | Per test condition (numbers behind Fig. 3c) |
| Supp 4 | Controls and ablations: scripted (perfect, order everything), untrained (no test, no menu, rules in the prompt), trained (SFT, outcome without cost, policy without penalty) |
| Supp 5 | The two rewards, weights filled in from `policy_reward.py` |
| Supp 6 | Datasets per split |
| Supp 7 | Models and inference settings |
| Supp 8 | Training and compute |
| Supp 9 | Physician agreement (kappa per dimension, blind rating vs score) |
| Supp 10 | Cost of running an episode |
| Supp 11 | Thinking off vs on (values filled in; check whether invalid actions and failed episodes are totals or per seed) |
| Supp 12 | Models against neurologists on the same cases (numbers behind Fig. 4c; added 18 Nov) |
| Supp 13 | Models against the MIMIC-IV clinicians who treated the same patients (numbers behind Fig. 5c; added 18 Nov) |

## Which test set carries the main claim (17 Nov, proposed, to confirm with Andrea)
Both, with different roles.
- **NeuroBench test = primary endpoint of the A vs B comparison.** Four conditions never seen in training, 119 cases × 3 seeds, case-specific policies reviewed by physicians, releasable.
- **MIMIC = external validation on real records; it must show the same direction.** Reported in the same table, never pooled with the synthetic test. Limits to state: 88 of 100 admissions come from conditions seen in training or validation (MS chose the checkpoint), only 12 from held-out conditions; policies are carried over from the templates of the same condition and are still draft; the strict pool keeps admissions with a complete recorded work-up (selection); a test never done answers "not available" (censoring); n = 100 is underpowered for diagnosis differences; the data cannot be released.
- MIMIC becomes a stronger second primary if two physicians approve its 100 policies and the held-out-condition block grows beyond 12 cases.
