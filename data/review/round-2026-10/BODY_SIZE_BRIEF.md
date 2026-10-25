# Brief: weight and height consistent with each case (25 Oct 2026)

Commit b5a46c7c added `patient.demographics.weight_kg` and `height_cm` to every case: a default
height (sex, ethnicity group, age band, deterministic offset) and the weight that reproduces the
stored `bmi` exactly. The agent's prompt now shows "height H cm, weight W kg, BMI B". Your job:
make the three numbers consistent with everything the case says, for dataset quality (decide,
apply, record why).

## Input
A table per case (path in your prompt): age, sex, ethnicity, bmi, the defaults, and every text
snippet (with its field path) that states a weight, height or BMI, describes body build (obese,
cachectic, underweight, emaciated), reports weight change, or gives a weight-based dose together
with an absolute amount. Open the case only to resolve a snippet.

## Rules
1. A current weight or height stated anywhere (HPI, exam, tool report such as an echo BSA, PFT or
   dosing line) is authoritative: set `weight_kg` / `height_cm` to it. Keep the stored BMI if a
   plausible height reproduces it; otherwise set `bmi = round(weight / height_m^2, 1)` and check no
   text cites the old BMI (if one does, fix that text, or keep the BMI and adjust height).
2. A BMI stated in text wins over the stored one.
3. Body-build words must agree with BMI (obese >= 30, overweight 25-29.9, underweight < 18.5,
   cachexia/emaciation usually < 20). If they disagree and no number is stated, change BMI (and
   weight) to fit the narrative. A weight loss ("lost 12 kg in 6 months") must leave a plausible
   current BMI.
4. Weight-based doses stated with an absolute amount ("levetiracetam 60 mg/kg, 4500 mg", "IVIG
   2 g/kg = 160 g") must match the weight within about 10% (allow documented caps such as
   levetiracetam 4500 mg or fosphenytoin maximums). If not, prefer changing the weight when nothing
   else states it; otherwise fix the absolute amount in the text.
5. Respiratory reports in mL/kg (GBS, MG: FVC, the 20/30/40 rule) must agree with the weight:
   FVC litres = mL/kg x weight / 1000. Where a GBS or MG case stores FVC in litres only, add the
   mL/kg figure in the report text if it is the decisive value; never change a value a criterion's
   expected_evidence cites without updating the evidence the same way.
6. Do not change anything else: no diagnosis, tiers, criteria or tool choice.

## Procedure
- Edit only through `data/review/round-2026-10/bin/case_io.py` (`load`/`save`); touch only your
  conditions' cases (another agent edits the others).
- Final consistency check (script in your scratchpad subfolder, run with `uv run python -I`):
  `round(weight_kg / (height_cm/100)^2, 1) == bmi` for every case you touched; 120 < height < 230.
- After editing each case run `uv run python data/review/round-2026-10/bin/perfect_agent.py CASE`.
- Append "## Weight and height (25 Oct 2026)" to each changed case log
  (`data/review/round-2026-10/logs/CASE.md`) saying what changed and why.
- Write `data/review/round-2026-10/plans/BODY-SIZE-<group>-decisions.md` (one line per changed
  case) with a short list of doubts for the physicians.
- Do not commit. Report under 150 words: cases changed by rule, text edits, doubts.
