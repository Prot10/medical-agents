# Body size, group B: decisions (25 Oct 2026)

Conditions: SE, GLIO-HG, MS-RR, MIG-AURA, NPH, FEPI-TEMP, HEP-ENC, NMDAR-ENC, PD, SAH (300 cases;
127 with a body-size mention). Brief: `BODY_SIZE_BRIEF.md`. Only `patient.demographics` changed; no text edits.

## Changed cases

- FEPI-TEMP-P03 (rule 3): "Mild obesity" vs BMI 28.2 -> BMI 31.0, weight 76.4 kg, height 157 cm.
- FEPI-TEMP-S03 (rule 3): "Mild obesity" vs BMI 28.1 -> BMI 31.0, weight 101.6 kg, height 181 cm.
- HEP-ENC-M01 (rule 3): "Obesity" vs BMI 29.3 -> BMI 31.5, weight 96.5 kg, height 175 cm.
- MIG-AURA-P08 (rules 1-2): stated height 150 cm and BMI 18.8 -> height 150 cm, weight 42.3 kg.
- SE-S05 (rule 3): "malnourished appearance" vs BMI 28.8 -> BMI 19.6, weight 62.8 kg, height 179 cm.
- SAH-P07 (rule 3): "Obesity BMI was higher, lost weight" vs BMI 21.8 -> BMI 27.6, weight 73.3 kg, height 163 cm.

## Checked and kept

- Integer BMIs in text match the stored value when rounded: FEPI-TEMP-RS04 (30 vs 30.2), MIG-AURA-P02
  (29 vs 29.1), MIG-AURA-P07 (26 vs 25.7), NPH-M07 (32 vs 32.1), HEP-ENC-S10 (31 vs 31.2).
- Exact BMIs in text match: FEPI-TEMP-RP05, HEP-ENC-M04, HEP-ENC-M07, MIG-AURA-M03, MIG-AURA-S03,
  MIG-AURA-S05, MS-RR-RS04, NPH-S07 ("mild obesity", 30.1).
- Weight-based doses: every one is stated per kg with a cap only (levetiracetam 60 mg/kg max 4500 mg,
  lorazepam 0.1 mg/kg max 4 mg, PCC 35 units/kg max 3500, albumin 1 g/kg up to 100 g); none states a
  computed absolute amount. SE-M08 pyrimethamine "75 mg (50 mg if under 60 kg)" fits 71.9 kg.
- Weight losses (2-8 kg, 15 lb) all leave a normal or overweight current BMI.

## Doubts for the physicians

- SE-P01 (BMI 26.5) and HEP-ENC-S06 (BMI 31.8) are called "malnourished heavy drinker" only in
  ground-truth reasoning; the patient text gives no body-build word. Kept: malnutrition in alcohol use
  does not require a low BMI, and HEP-ENC-S06 has massive tense ascites inflating the weight.
- SAH-P07: 27.6 was chosen as an overweight BMI after weight loss in IIH; the PMH line itself is
  ungrammatical and does not state the current weight. Confirm or give the intended figure.
- SE-S05: 19.6 is a judgement for "malnourished appearance"; any value 18.5-20 fits equally.
- HEP-ENC-M01, FEPI-TEMP-P03, FEPI-TEMP-S03: class I values (31-31.5) chosen for "obesity"/"mild obesity".
