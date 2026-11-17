# Paper: decisions

Updated 17 Nov 2026. One line per decision, with its date.

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
  - [ ] 20–30 cases solved by the physicians → physician vs agent comparison (and the human reference in Fig. 2);
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

Extended Data (17 Nov): 9 items of 10, merged by topic because we were at 12. One slot is left for the rows still to decide (non-neurological MIMIC, reasons for the requests); if both are needed, the thinking test moves to the Supplementary.

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
| 9 | Thinking off vs on (why A and B do not use thinking) |

Main figures (17 Nov; several experiments can share a figure, in different panels):

| Fig. | Content |
|---|---|
| 1 | Overview: cases, tests, score, physician review (+ inter-physician agreement) |
| 2 | Correct diagnosis with wrong or missing tests, untrained models, with the neurologists as a human reference |
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
- In the PDF it prints as "Fig. 3": the old October dataset figure still takes the place of Fig. 2. To decide whether it moves to Extended Data.

Figure 3 (17 Nov), draft to settle the layout (`paper/figures/fig3_svg.py`, `fig3-new.pdf`, 180 × 131 mm, same rules as Fig. 2; every number is "xx"). Redone the same day after the research on what reviewers expect (`paper/nmi-notes.md`):
- Three models in every panel: untrained (grey), rewarded on diagnosis + cost (orange, "Outcome reward"), rewarded on the work-up (blue, "Policy reward").
- a: correct diagnoses and tests per case on validation over training, mean and range across seeds; open circle = chosen checkpoint. Not the policy score: for the orange model it would be circular.
- b: test, seven measures: the independent ones first (correct diagnoses, required tests ordered, cases with an unsafe action, cost), then both scores (outcome and policy): each model wins on its own, so B does not look like a weak opponent. P of the paired policy vs outcome comparison.
- c: per test condition (only 4: a reviewer will ask whether the effect comes from one of them).
- d: why the outcome reward loses diagnoses: cases the untrained model solves from the story alone against cases that need tests (split taken from the no-test run).
- Out of the Main: the reward history goes entirely to ED2 (in the Main it suggests "they changed the reward until it worked", and it rests on one seed and on validation); the single case leaves (the widget is already in Figs 1 and 2).
- The panel on unseen conditions from the R3 plan is not needed: the test set contains only conditions excluded from training.

Figure 2, changes of 17 Nov after the same research: one more class in the bars of c, "complete but with useless tests" (MIRA's reviewers, Nature 2026, asked for precision and a penalty for useless tests), and "n = xx" correct diagnoses next to each bar (Hager, Nat Med 2024). The same day, at Andrea's decision, the neurologists enter Fig. 2 as a human reference: a pink diamond in panel a and a row in the bars of c (Hager, MIRA and SDBench put clinicians beside the models). Needs the 20–30 cases solved by the physicians; in panel a the neurologists cover a subset of the cases, and the models on the same cases go to ED.

Notes:
- Weights of models trained on MIMIC: not freely publishable (PhysioNet agreement).
- Everything in the repository is written in English (Andrea, 17 Nov).
