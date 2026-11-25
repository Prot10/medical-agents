# Paper: decisions

Updated 18 Nov 2026. One line per decision, with its date. The block "Second critical review (18 Nov)" is the latest word on thesis, claims, measures, figures and tables: where an older line disagrees with it, that block holds. The manuscript plan (`manuscript/`) was brought in line with this file on 17 Nov: anything there that disagrees with it is a bug.

## Journal
- **Nature Machine Intelligence** (17 Nov). ICML dropped: the method alone was judged too weak.

## Content
- Two trained models compared (17 Nov):
  - A: rewarded for the right tests in the right order (final reward);
  - B: rewarded only for a correct diagnosis and a low cost.
- The discarded reward versions, with reasons and numbers (17 Nov):
  - 3 Nov: answering without tests scored ≥ a complete work-up in 225/600 cases → fixed;
  - 13 Nov: A ordered 5.8 useless tests per case → −0.03 for every useless test;
  - 18 Nov: with −0.03, A still orders 2.8 useless tests per case against 2.0 for the untrained model (seed 1, validation) → a stronger penalty is to be chosen on validation before seeds 2 and 3 (not launched).

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
  - [ ] 20–30 MIMIC-IV admissions solved by the physicians → physician vs agent comparison (Fig. 4c);
  - [ ] ~100 model work-ups on MIMIC-IV admissions rated blind → does our score agree with the physicians?
  - Both studies run on MIMIC-IV admissions (Andrea, 18 Nov): the physicians reviewed the synthetic cases and their policies, and have not seen the admissions. Needs personal PhysioNet access for each physician, a place to serve the cases that respects the data use agreement (not the public review site), and at least one neurologist who has not seen the policies.
- In the Methods: role and experience of the physicians, not their names.
- **25 Nov (Andrea): how to make the clinical part attack-proof.** Our two neurologists are not senior. The physicians matter most where they define what is right (the policies, then the blind rating), little where they check (the LLM translation). Decisions: guideline cited per policy; one senior neurologist audits a policy sample and rates blind; raters independent of the policies; physicians' level stated and claims worded to it. Ranking, comparison with 22 papers and action list: `paper/clinician-involvement.md` §4.

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
| Where the gain comes from: Qwen3.5-9B with the rules in the prompt, fine-tuned by imitation, run as a multi-agent panel; a larger untrained model; tokens per case (18 Nov, replaces "A vs larger models + cost and time") | Main (one figure) |
| Inter-physician agreement + re-checked sample | Main briefly + ED |
| Training on other models (Gemma, small Qwen, maybe Granite), 1 seed | ED |
| Per condition, with a clinical reading | ED + Discussion |
| Acute vs chronic (synthetic only) | ED |
| Controls: no-test and no-menu baselines | ED (one figure); the scripted agents moved to Fig. 3d and Supp Table 4 (18 Nov) |
| Second split: other conditions held out, one seed (18 Nov) | ED (one figure) |
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
| 7 | Controls (no test, no menu) |
| 8 | Robustness (weights, contradictory facts) |
| Table 1 | Main results: untrained, B, A on the NeuroBench test and on MIMIC, with the A − B difference |
| 9 | Second split: other conditions held out, one seed (18 Nov; the slot was free) |

Main figures (17 Nov; several experiments can share a figure, in different panels):

| Fig. | Content |
|---|---|
| 1 | Overview: cases, tests, score, physician review (+ inter-physician agreement) |
| 2 | Correct diagnosis with wrong or missing tests, untrained models (models only since 18 Nov) |
| 3 | A vs B vs base (the reward history moved to ED2 on 17 Nov) |
| 4 | The physicians, on MIMIC-IV admissions: (a) blind rating vs score, (b) blind rating of each agent, (c) physician vs agent on the same admissions |
| 5 | Real MIMIC neuro cases: the three models, and against the treating clinicians |
| 6 | Where the gain comes from: rules in the prompt, fine-tuning, multi-agent panel, a larger model (18 Nov) |

Palette (17 Nov), the same in every figure — Okabe-Ito, colour-blind safe (Wong, Nat Methods 2011):

| Role | Colour |
|---|---|
| Model A (rewarded on the work-up) | blue `#0072B2` |
| Model B (rewarded on diagnosis + cost) | orange `#E69F00` |
| Base (untrained) | grey `#999999` |
| Physicians / policy | pink `#CC79A7` |
| Correct ✓ | green `#009E73` |
| Error ✗ | vermilion `#D55E00` |

Approval (18 Nov): Andrea approved Figures 1–6 as drawn here; the critical review of the same day (below) revised all six, so each waits again for approval. For Figs. 2–6 this approves the layout; the marks sit on invented data and every number stays "xx" until the runs and the physician studies exist (Fig. 5 prints only the fixed cohort counts 12 and 88).

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

Figure 5 (18 Nov), layout approved by Andrea the same day, then revised by the critical review (below) (`paper/figures/fig5_svg.py`, `fig5-new.pdf`, 180 × 100 mm, same rules as Figs. 2–4; every number is "xx" except the fixed cohort counts 12 and 88). One question per panel, checked against Figs. 1–4:
- a: policy reward minus outcome reward, paired by case, for correct diagnoses, required tests ordered and cases with an unsafe action, NeuroBench test and MIMIC-IV side by side: does the direction hold on real records? Fig. 3b shows the NeuroBench levels; the NeuroBench differences are repeated here only as the anchor of the comparison.
- b: MIMIC-IV split as Supplementary Table 1 (12 kept out of training, 88 seen in training or validation), laid out like Fig. 3c: is the result carried by conditions the models trained on?
- c: the three models against the tests the clinicians recorded for the same patients (tests the clinicians also did, clinicians' tests ordered, tests per case), laid out like Fig. 4c so the two human references read the same way. Numbers in Supplementary Table 13.
- Left out: the cohort flow (an Extended Data CONSORT diagram) and the policy score (in ED Table 1; the MIMIC-IV policies are still drafts).

Figure 6 (18 Nov), layout approved by Andrea the same day, then redrawn by the critical review (below) (`paper/figures/fig6_svg.py`, `fig6-new.pdf`, 180 × 110 mm, same rules as Figs. 2–5; every number is "xx", model sizes are placeholders). The plan's placeholder put the trained model on the plane of Fig. 2a (correct diagnoses × policy score); redesigned to avoid repeating that figure:
- a: policy score and correct diagnoses against model size (log scale), untrained panel of Fig. 2 plus the two trained models of Fig. 3, arrows from the untrained Qwen3.5-9B (PsychFound, NMI 2026, Fig. 3). Size is what is new: Fig. 2 has no size and no trained models, Fig. 3 no larger models. Names only in the left plot; the x position is the same in both.
- b: what it takes to run one case (peak GPU memory, completion tokens per case, time per case) for the trained model and the larger ones, dashed line at the 40 GB of one A100; GLM-5.3 runs only through an API, so tokens only. Laid out like Figs. 4c and 5c. The cost of the tests stays in Fig. 3b; numbers in Supplementary Table 10, sizes in Supplementary Table 7.
- Open: total or active parameters for the mixture-of-experts models (drafted as total); the GPU the runtime is measured on (A100 40 GB fits only models up to about 20B).

Captions (18 Nov), all four re-checked against the current drawings, at most 250 words each (Fig. 1 ~190, Fig. 2 ~245, Fig. 3 ~215, Fig. 4 ~225):
- Fig. 1: the drug check takes no reason; the score also checks useless tests and stopping ("Also scored" in c); test cost at Medicare prices.
- Fig. 2: no neurologists; "points are means"; n counted over all seeds; the colours of d said in words (green, grey, orange), as NMI asks.
- Fig. 3: one opening sentence names the three models; error bars, CIs and the paired, corrected test stated once for b–d (c and d had none); the test itself is left to Methods until the choice between Wilcoxon and McNemar is made.
- Fig. 4: written for the redesigned figure; the pink line is the agreement between two neurologists and the band its CI.
- Style pass (18 Nov, skill scientific-paper-style, approved by Andrea): "work-up" defined in the Fig. 1 caption; reading sentences about results not yet measured removed; long sentences split.

Names (18 Nov), one per measure in captions, figure labels, tables and plan text: "Correct diagnoses (%)" (never "accuracy" or "correct diagnosis"), "Required tests ordered (%)", "Cases with an unsafe action (%)", "Cost per case ($)", "Tests per case", "Useless tests per case", "policy score", "outcome score". The ingredients of the outcome reward are "diagnosis and cost". "Accuracy" stays only where another paper's figure is cited and in the reward component "tool accuracy".

Goal of the paper (18 Nov, chosen by Andrea between two drafts), in the abstract plan and at the top of `plan.tex`:
> To support physicians in hospitals, a diagnostic agent must reach the diagnosis through the work-up that clinical practice asks for. Rewarding a small open model for following physician-reviewed case policies, rather than for a correct diagnosis at low cost, teaches it that work-up, on conditions and real admissions it never trained on, whereas the outcome reward teaches it to skip tests.

Andrea asked that the sentence say the agent must follow clinical practice, since the aim is to support physicians in hospitals. Supporting physicians is written as the goal, not as a result: there is no study in a hospital, and what the paper measures is the alignment with clinical practice (physician-reviewed policies, blind ratings, the clinicians' recorded tests).

Critical review (18 Nov), asked by Andrea after approving Figures 1–6: is every figure needed for the narrative, does any repeat another, is anything missing? Applied the same day; every figure waits again for approval.
- Narrative, one figure per step: Fig. 1 setup → Fig. 2 the problem (a correct diagnosis hides the work-up) → Fig. 3 the fix (policy reward against outcome reward) → Fig. 4 validity (neurologists) → Fig. 5 real admissions → Fig. 6 a small model is enough.
- Colour: orange is kept for the outcome reward in every figure. Fig. 1 misses are slate grey; Fig. 1c adds the outcome score of the same episode (orange bar) beside the policy score, so the reader sees from the start that the outcome score ignores the work-up.
- One agent name: "the agent" (Qwen3.5-9B trained on the policy reward); "NeuroAgent" no longer appears in figures or captions.
- Fig. 2: the y axis of a is required tests ordered (was the policy score: a reviewer reads a policy score as circular before the reward is introduced); the ranking panel is gone, Kendall's tau between the two rankings is one line under a; the bars become b and the single case c. Legend says "Up to 9B parameters" and "Larger models".
- Fig. 3: b adds the control trained on the outcome reward without the cost term (open orange circle), which separates "the cost term teaches skipping tests" from "any outcome reward does", and two measures, useless tests per case and cost per case. Fig. 3c (per condition) stays; Extended Data Fig. 5, which repeated it, now holds the ratings by work-up class.
- Fig. 4: b is the blind rating of each model (untrained, outcome reward, policy reward), P paired by case between the two trained models: the main effect tested with no score at all. The ratings by work-up class move to Extended Data Fig. 5; numbers of both in the new Supplementary Table 14.
- Fig. 5: in a, cases with an unsafe action sit in their own block ("lower is better"), so a point right of zero is not read as a gain. Claim C4 now includes the concordance with the treating clinicians (Fig. 5c), with its refutation.
- Fig. 6: one measure, the policy score, against size (a) and against wall time per case (b), sharing the y axis. The trained models sit exactly at 9B with vertical arrows (the 9B offset misplaced them); the correct-diagnoses plot (in Figs. 2a and 3b) and the memory and token rows (in Supplementary Table 10, which now names every model) are gone. GLM-5.3 runs only through an API and is left out of b. Claim C5 reads "in a fraction of their time".
- Risks to state in the paper: the physician studies of Fig. 4 are not designed yet; only 4 held-out conditions on NeuroBench and 12 held-out admissions on MIMIC-IV; one trained base model; the no-cost control needs a new training run.

Second critical review (18 Nov), asked by Andrea after the first real results; applied the same day to the plan, the tables and all six figures. Every figure and table waits again for approval.

First real numbers (seed 1 of each model; 60 validation cases × 3 inference seeds; draft policies; EOS `runs/e1_qwen3.5-9b/` and `runs/e1_qwen3.5-9b-policy-v3/`, `seed-1/val/`):

| | Untrained | Outcome reward, kept checkpoint (step 50) | Policy reward v3, kept checkpoint (step 300) |
|---|---|---|---|
| Correct diagnoses | 90% | 90% | 93% |
| Required tests ordered | 42% | 31% | 82% |
| Tests per case | 3.7 | 2.0 | 7.3 |
| Useless tests per case | 2.0 | not read | 2.8 |
| Ordered tests the policy asks for | 46% | not read | 61% |
| Cost of the tests per case | $2,361 | $947 | $2,269 |
| Policy score | 0.42 | not read | 0.64 |

- The checkpoint of each model is chosen on validation by its own reward (Andrea, 18 Nov), so what a model does later in training is not part of the story. The outcome-reward model kept by that rule orders about half the tests and keeps the diagnoses; only later checkpoints stop ordering tests and lose diagnoses (58% at step 100).
- Three things the invented-data figures drew are not supported and were removed: an outcome-reward model that loses diagnoses; a drop in unsafe actions (about 2% of cases for the untrained model, 12 of 600 episodes, unchanged by training); fewer useless tests for the policy-reward model (it orders more).
- Why the outcome reward has little reason to test: in most conditions the diagnosis can be read from the history (validation: MS 0.80 without tests against 0.77 with; test: only glioma needs tests, 0.07 against 0.87). Stated as a limitation.

Goal of the paper, new sentence (Andrea, 18 Nov: the model spends where it is needed, and its number of tests must be close to the physicians', since what counts is ordering the right ones). In the abstract plan and at the top of `plan.tex`; it replaces the sentence quoted above:
> To support physicians in hospitals, a diagnostic agent must reach the diagnosis through the work-up that clinical practice asks for. Rewarding a small open model for following physician-reviewed case policies teaches it to order the tests physicians ask for and few others, on conditions and real admissions it never trained on: it orders about as many tests as physicians do and spends where the case needs it. Rewarding the same model for a correct diagnosis at low cost keeps the diagnoses and saves by leaving required tests out.

- Title: "Executable clinical policies teach small open models the diagnostic work-up" (was "... the safe diagnostic work-up"). "Safe" is not a result of this paper and is in the list of words to avoid.
- Claims (abstract plan): C1 a correct diagnosis can hide an incomplete work-up; C2 the policy reward teaches the required tests without losing diagnoses, the outcome reward teaches to order fewer; C3 neurologists, blind, agree with the policy score and rate the policy-reward model highest, and the number of tests alone does not explain their rating; C4 the gain over the untrained model holds on 100 MIMIC-IV admissions, with tests close to those of the treating clinicians; C5 the gain comes from the reward, not from the prompt, imitation or a panel of agents. Each has a refutation criterion.
- Names, one per measure (they replace the list of 18 Nov above where they differ): "Correct diagnoses (%)", "Required tests ordered (%)", "Ordered tests the policy asks for (%)" (share of a model's tests that match a required or recommended item), "Tests per case" (read against the number the policies ask for and against physicians), "Cost relative to the required work-up" (1 = the cost of the required tests of the case), "Tokens per case (thousands)". "Cases with an unsafe action (%)", "Useless tests per case" and "Cost per case ($)" stay in ED Table 1 and the Supplementary tables only. Baselines: "Rules in the prompt", "Supervised fine-tuning", "Multi-agent panel" (in the style of MAI-DxO, never called MAI-DxO: it is our rebuild on a 9B model).
- Positioning: DiagGym (Qiu 2025) already trains with a reward on diagnosis plus the overlap with the tests recorded in the health record, and compares it with a diagnosis-only reward. Our delta is the reference (a physician-reviewed policy per case, not the recorded orders), conditions never seen in training and blind physician ratings. SDBench defines no reward: the 0.85 / 0.15 weights of the outcome reward are our choice and the text says so.
- Introduction example: meningitis named without lumbar puncture and blood cultures (a test left out, on which guidelines agree). The order of head CT and lumbar puncture is no longer used: WHO and NICE differ on it.

Figures after the second review (all "revised, awaiting approval"; invented data near the numbers above, every printed number "xx"):
- Fig. 1 (180 × 129 mm): the outcome-score bar left panel c; the box shows the policy score and the cost of the tests.
- Fig. 2 (180 × 127 mm): Kendall's tau line removed; b has three classes (complete / complete with useless tests / required test missed), no unsafe class; c marks tests only as required or not needed, without the head CT.
- Fig. 3 (180 × 131 mm): a, curves with the kept checkpoints (outcome reward at step 50). b, seven measures: correct diagnoses, required tests ordered, ordered tests the policy asks for, tests per case, cost relative to the required work-up, outcome score, policy score; pink dashed lines mark what the case policies ask for; the no-cost control stays. c, per condition. d, new: required tests ordered against tests per case, with a scripted agent that orders the same k tests in every case (k = 0 to 11) and the required work-up as a pink diamond: it separates "the right tests" from "more tests". The old d (cases solved from the history against cases that need tests) is gone: with the kept outcome-reward model the diagnoses do not drop.
- Fig. 4 (180 × 106 mm): both studies on MIMIC-IV admissions. a adds the row "Number of tests ordered" (the rival explanation "physicians just like more tests"). b rates four agents: untrained, multi-agent panel, outcome reward, policy reward. c, models against the neurologists on the same admissions; tests per case is read against theirs.
- Fig. 5 (180 × 97 mm): two full-width panels. a, the three models on the 100 admissions (correct diagnoses, required tests ordered, ordered tests the policy asks for, cost relative to the required work-up), P for policy reward against untrained. b, models against the treating clinicians (the old c). Removed: the paired differences on both test sets and the split 12 / 88 (in Supp Table 1). The caption states the selection: admissions were kept because their record holds the core tests of the policy.
- Fig. 6 (180 × 101 mm), redrawn: a, Qwen3.5-9B used in five ways (untrained, rules in the prompt, supervised fine-tuning, multi-agent panel, policy reward); b, a larger untrained model alone, with the rules, as a panel (Qwen3.8-27B is a placeholder). Columns: correct diagnoses, required tests ordered, ordered tests the policy asks for, tokens per case. The old figure (policy score against size and wall time) plotted the reward the model was trained on and did not answer "why not a better prompt or a panel of agents".
- Extended Data: 10 of 10 used. ED2 adds the choice of the penalty; ED7 keeps no test and no menu; ED Fig. 9 is new, a second split that holds other conditions out (one seed), since four test conditions are few.
- Tables: ED Table 1 has both differences (policy − outcome, policy − untrained), each with CI and P, and two new rows (ordered tests the policy asks for, cost relative to the required work-up); the no-cost control moved to Supp Table 4, which now holds controls, baselines and scripted agents with a tokens column; Supp 2 lost its rank column; Supp 10 counts model calls and tokens, panel included; Supp 12 is on MIMIC-IV admissions; Supp 14 rates four agents.

Runs this plan needs and that do not exist yet (none launched on 18 Nov):
- [ ] a stronger penalty for useless tests, chosen on validation, before seeds 2 and 3 of the policy reward;
- [ ] seeds 2 and 3 of both models;
- [ ] the outcome reward without its cost term (Fig. 3b);
- [ ] the scripted agent with the same k tests in every case, k = 0 to 11 (Fig. 3d; no GPU);
- [ ] rules in the prompt, supervised fine-tuning, multi-agent panel on Qwen3.5-9B; the larger model alone, with the rules and as a panel (Fig. 6), with token counts;
- [ ] the second split (ED Fig. 9), one seed;
- [ ] the share of ordered tests the policy asks for and the cost relative to the required work-up, as reported measures in the benchmark summary.

Baselines (Andrea, 25 Nov):
- Run on the NeuroBench test split now (119 cases × 3 seeds), not on validation first: these agents choose no checkpoint, so opening the test for them biases nothing. A and B still open the test only once their adapters are fixed.
- Supervised fine-tuning imitates the scripted perfect agent (required then recommended criteria of the policy, in an order that respects the sequence constraints, then the accepted diagnosis) on the 419 training cases: `training_data/sft_reference_episodes.jsonl`, scalar 0.99, 5.3 tests per case. Assessment urgency follows the encounter type (emergency → emergent, inpatient → urgent, outpatient → routine), since policies state none and the score does not use it.
- The larger model of Fig. 6b is Qwen3.8-27B (same family, chat template and sampling as Qwen3.5-9B; registered as evaluation-only).
- Rules in the prompt: `RULES_ADDENDUM` in `harness/context.py`, appended to the policy prompt (loop `loop.rules`); it says what the policy score checks with nothing specific to a case. Awaits Andrea's reading of the text.
- Multi-agent panel: `harness/panel.py`, loop `loop.panel`. Five roles (hypothesis, test chooser, challenger, stewardship, checklist), each a text-only call of at most 400 tokens that hears the earlier roles of the same step; the model as chair then makes one typed call, with the discussion as one-off feedback (never replayed, never in SFT). Tokens per case include every role.
- Smoke on the CERN gateway (Qwen3.8-27B, training case SE-M02): both loops complete; rules 4 tests, 57k tokens; panel 2 tests, 85k tokens.
- Runner: `agent-platform/scripts/training/baselines_rtx.sh` (RTX pod), results in EOS `runs/baselines_test_20261125/`, SFT adapter in `checkpoints/sft-reference/qwen3.5-9b`. Also runs no test (narrative) and Gemma / Granite untrained for Fig. 2. No test menu (free order) is not in it: it needs the gateway inside the pod.

First test results of the baselines (25 Nov, Qwen3.5-9B, 119 test cases × 3 seeds, draft policies): required tests ordered 32% untrained, 36% rules in the prompt, 33% SFT, 40% multi-agent panel (156k tokens per case against 57k); Qwen3.8-27B 43% untrained, 52% rules, 53% panel. Numbers in EOS `runs/baselines_test_20261125/`.
- Stronger SFT (Andrea, 25 Nov): the first SFT (2 epochs, lr 1e-4, LoRA r16; loss 1.2 → 0.3) left the work-up unchanged on test. Two more adapters on the same episodes, 4 epochs at lr 2e-4 with r16 and r64; the three, and the untrained model, are run on validation (60 × 3 seeds) and on 60 training cases (does it imitate?); the highest validation policy score is chosen, as for model A, and only that one goes to test. Runner `agent-platform/scripts/training/sft_tune_rtx.sh`, results in EOS `runs/sft_tune_20261125/`.

Open points for Andrea:
- PhysioNet access for each physician and where the MIMIC-IV cases are served for the two studies.
- One neurologist who has not seen the policies, as a third rater.
- Protocol of the two studies (sample, scale, blinding, analysis) written before any rating.
- What exactly "rules in the prompt" contains (proposed: what the policy score checks, in words, with nothing specific to a case).
- Which larger model goes in Fig. 6b, and whether the panel on that model is worth its cost.
- Whether R5 (MIMIC-IV results) should come before R4 (physicians on MIMIC-IV admissions), now that both use the same admissions; the order is unchanged for now.
- Check what the public SDBench repository contains before describing the panel in Methods.

Notes:
- Weights of models trained on MIMIC: not freely publishable (PhysioNet agreement).
- Everything in the repository is written in English (Andrea, 17 Nov).

## Tables (17 Nov)
File `manuscript/sections/08-tables.tex`. Values are `xx ± xx` (mean ± s.d. across 3 seeds) and `xx (xx to xx)` (95% CI, bootstrap over cases, paired by case) until the runs exist; known facts are filled in.

| Table | Content |
|---|---|
| ED Table 1 | Main results, two blocks (NeuroBench test 119, MIMIC 100): untrained, outcome reward, policy reward, then policy − outcome and policy − untrained, each with CI and P (Wilcoxon or McNemar, Benjamini–Hochberg per block). Rows: correct diagnoses, required, recommended, ordered tests the policy asks for, tests, useless tests, cost, cost relative to the required work-up, unsafe, outcome score, policy score (18 Nov, second review) |
| Supp 1 | MIMIC split: conditions kept out of training (HEP 10 + BACT 2) vs seen in training or validation (88) |
| Supp 2 | Untrained models (numbers behind Fig. 2), no rank column since 18 Nov |
| Supp 3 | Per test condition (numbers behind Fig. 3c) |
| Supp 4 | Controls, baselines and scripted agents (numbers behind Figs. 3b, 3d and 6): scripted (required work-up, every test, the same k tests); Qwen3.5-9B without RL (no test, no menu, rules in the prompt, SFT, multi-agent panel); trained (outcome without cost, policy without penalty); the larger model; with tokens per case |
| Supp 5 | The two rewards, weights filled in from `policy_reward.py` |
| Supp 6 | Datasets per split |
| Supp 7 | Models and inference settings, with parameter counts |
| Supp 8 | Training and compute |
| Supp 9 | Physician agreement (kappa per dimension, blind rating vs score) |
| Supp 10 | What it takes to run an episode: model calls, tokens, wall time, peak GPU memory, panel rows included (numbers behind Fig. 6; 18 Nov) |
| Supp 11 | Thinking off vs on (values filled in; check whether invalid actions and failed episodes are totals or per seed) |
| Supp 12 | Models against neurologists on the same MIMIC-IV admissions (numbers behind Fig. 4c; added 18 Nov) |
| Supp 13 | Models against the MIMIC-IV clinicians who treated the same patients (numbers behind Fig. 5b; added 18 Nov) |
| Supp 14 | Blind ratings: four agents (untrained, multi-agent panel, outcome reward, policy reward) and work-up classes (numbers behind Fig. 4b and ED Fig. 5) |

## Which test set carries the main claim (17 Nov, proposed, to confirm with Andrea)
Both, with different roles.
- **NeuroBench test = primary endpoint of the A vs B comparison.** Four conditions never seen in training, 119 cases × 3 seeds, case-specific policies reviewed by physicians, releasable.
- **MIMIC = external validation on real records; it must show the same direction.** Reported in the same table, never pooled with the synthetic test. Limits to state: 88 of 100 admissions come from conditions seen in training or validation (MS chose the checkpoint), only 12 from held-out conditions; policies are carried over from the templates of the same condition and are still draft; the strict pool keeps admissions with a complete recorded work-up (selection); a test never done answers "not available" (censoring); n = 100 is underpowered for diagnosis differences; the data cannot be released.
- MIMIC becomes a stronger second primary if two physicians approve its 100 policies and the held-out-condition block grows beyond 12 cases.
