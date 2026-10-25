# Body size, group A: decisions (25 Oct 2026)

Conditions: GBS, MG, ALZ-EARLY, ALS, ISCH-STR, VASC-DEM, BACT-MEN, SYNC-CARD, FND, FTD (174 cases with
a body-size mention). Brief: `BODY_SIZE_BRIEF.md`. 70 cases changed: 66 by rule 1 (a stated weight and height, FTD-P08 a stated weight only;
each keeps the stored BMI or moves it by 0.1, and no text cites the old value), 3 by rule 3 (BMI
changed to fit a body-build word) and 1 rule-3 text edit (ISCH-STR-RS05). Every
FVC mL/kg figure (GBS, MG) and every weight-based IVIg, hydroxychloroquine, Cockcroft-Gault or
apixaban/edoxaban statement was checked against the new weight: all agree within rounding, so no
text change was needed for rules 4-5. Final check: BMI = weight / height^2 (one decimal) and
120 < height < 230 in all 174 cases; `perfect_agent.py` 70/70.

## Changed cases

- BACT-MEN-RS04: w 41.9->44, h 156->160, BMI 17.2->17.2. rule 1: HPI states ward weight 44 kg, height 160 cm; BMI 17.2 as stored and as cited
- FND-M06: w 90->94.9, h 175->175, BMI 29.4->31. rule 3: past history 'Obesity' with stored BMI 29.4; BMI raised to 31.0 at the default height
- FTD-P08: w 57.7->64, h 157->165, BMI 23.4->23.5. rule 1: exam states 'Weight stable at 64 kg'; height 165 cm keeps BMI near the stored 23.4 (now 23.5); no text cites a BMI
- GBS-M01: w 78.1->67.5, h 172->160, BMI 26.4->26.4. rule 1: exam states weight 67.5 kg, height 160 cm
- GBS-M02: w 62.7->68.3, h 159->166, BMI 24.8->24.8. rule 1: exam states weight 68.3 kg, height 166 cm
- GBS-M03: w 82.4->72.3, h 174->163, BMI 27.2->27.2. rule 1: exam states weight 72.3 kg, height 163 cm
- GBS-P01: w 73.5->65.5, h 178->168, BMI 23.2->23.2. rule 1: exam states weight 65.5 kg, height 168 cm
- GBS-P02: w 51.8->53.8, h 152->155, BMI 22.4->22.4. rule 1: exam states weight 53.8 kg, height 155 cm
- GBS-P03: w 60.8->57.9, h 167->163, BMI 21.8->21.8. rule 1: exam states weight 57.9 kg, height 163 cm
- GBS-RM11: w 71.1->67, h 170->165, BMI 24.6->24.6. rule 1: exam states weight 67 kg, height 165 cm
- GBS-RM12: w 68.3->75, h 172->180, BMI 23.1->23.1. rule 1: exam states weight 75 kg, height 180 cm
- GBS-RM13: w 73.6->70, h 161->157, BMI 28.4->28.4. rule 1: exam states weight 70 kg, height 157 cm
- GBS-RM14: w 60.2->61, h 159->160, BMI 23.8->23.8. rule 1: exam states weight 61 kg, height 160 cm
- GBS-RM15: w 60.7->63, h 165->168, BMI 22.3->22.3. rule 1: exam states weight 63 kg, height 168 cm
- GBS-RM16: w 75->76, h 176->177, BMI 24.2->24.3. rule 1: exam states weight 76 kg, height 177 cm
- GBS-RP11: w 64.4->72, h 155->164, BMI 26.8->26.8. rule 1: exam states weight 72 kg, height 164 cm
- GBS-RP12: w 70.5->74, h 166->170, BMI 25.6->25.6. rule 1: exam states weight 74 kg, height 170 cm
- GBS-RP13: w 65.3->68, h 155->158, BMI 27.2->27.2. rule 1: exam states weight 68 kg, height 158 cm
- GBS-RP14: w 84.1->81, h 168->165, BMI 29.8->29.8. rule 1: exam states weight 81 kg, height 165 cm
- GBS-RP15: w 75.4->80, h 169->174, BMI 26.4->26.4. rule 1: exam states weight 80 kg, height 174 cm
- GBS-RP16: w 69.4->78, h 168->178, BMI 24.6->24.6. rule 1: exam states weight 78 kg, height 178 cm
- GBS-RS11: w 73.4->76, h 172->175, BMI 24.8->24.8. rule 1: exam states weight 76 kg, height 175 cm
- GBS-RS12: w 65.9->62, h 165->160, BMI 24.2->24.2. rule 1: exam states weight 62 kg, height 160 cm
- GBS-RS13: w 74.5->80, h 169->175, BMI 26.1->26.1. rule 1: exam states weight 80 kg, height 175 cm
- GBS-RS14: w 58.6->58, h 164->163, BMI 21.8->21.8. rule 1: exam states weight 58 kg, height 163 cm
- GBS-RS15: w 69.8->70.7, h 159->160, BMI 27.6->27.6. rule 1: exam states weight 70.7 kg, height 160 cm
- GBS-RS16: w 65.2->64.5, h 159->158, BMI 25.8->25.8. rule 1: exam states weight 64.5 kg, height 158 cm
- GBS-RS17: w 69.8->68, h 157->155, BMI 28.3->28.3. rule 1: exam states weight 68 kg, height 155 cm
- GBS-RS18: w 95.4->96.5, h 167->168, BMI 34.2->34.2. rule 1: exam states weight 96.5 kg, height 168 cm
- GBS-S01: w 73.3->82, h 174->184, BMI 24.2->24.2. rule 1: exam states weight 82 kg, height 184 cm
- GBS-S02: w 67.1->70.5, h 160->164, BMI 26.2->26.2. rule 1: exam states weight 70.5 kg, height 164 cm
- GBS-S03: w 73.1->71.5, h 179->177, BMI 22.8->22.8. rule 1: exam states weight 71.5 kg, height 177 cm
- GBS-S04: w 85.2->76.7, h 176->167, BMI 27.5->27.5. rule 1: exam states weight 76.7 kg, height 167 cm
- ISCH-STR-RS03: w 73->59, h 174->174, BMI 24.1->19.5. rule 3: exam 'Cachexia noted with recent 20-lb weight loss' with stored BMI 24.1; BMI lowered to 19.5 (59 kg, about 68 kg before the loss); the apixaban note 'at most one [criterion] can apply' still holds Lead: 61 kg, BMI 20.1 (clear of the apixaban 60 kg threshold).
- ISCH-STR-RS05: text only. rule 3 (stated BMI wins): past history 'Obesity (BMI 29.8)' relabelled 'Overweight (BMI 29.8)'; demographics unchanged
- ISCH-STR-S03: w 78.1->83, h 165->165, BMI 28.7->30.5. rule 3: past history 'Obesity' with stored BMI 28.7; BMI raised to 30.5 at the default height
- MG-M01: w 82->91, h 169->178, BMI 28.7->28.7. rule 1: exam states weight 91 kg, height 178 cm
- MG-M02: w 55.7->58.5, h 158->162, BMI 22.3->22.3. rule 1: exam states weight 58.5 kg, height 162 cm
- MG-M03: w 90.1->92, h 173->175, BMI 30.1->30. rule 1: exam states weight 92 kg, height 175 cm
- MG-M04: w 64.2->66, h 156->158, BMI 26.4->26.4. rule 1: exam states weight 66 kg, height 158 cm
- MG-P01: w 58.4->67, h 157->168, BMI 23.7->23.7. rule 1: exam states weight 67 kg, height 168 cm
- MG-P02: w 87.4->83.5, h 182->178, BMI 26.4->26.4. rule 1: exam states weight 83.5 kg, height 178 cm
- MG-P03: w 58.2->59.6, h 163->165, BMI 21.9->21.9. rule 1: exam states weight 59.6 kg, height 165 cm
- MG-P04: w 88.8->86.8, h 180->178, BMI 27.4->27.4. rule 1: exam states weight 86.8 kg, height 178 cm
- MG-RM11: w 67.8->68.6, h 171->172, BMI 23.2->23.2. rule 1: exam states weight 68.6 kg, height 172 cm
- MG-RM12: w 84.9->83, h 178->176, BMI 26.8->26.8. rule 1: exam states weight 83 kg, height 176 cm
- MG-RM13: w 58.1->63.5, h 155->162, BMI 24.2->24.2. rule 1: exam states weight 63.5 kg, height 162 cm
- MG-RM14: w 68->72.4, h 155->160, BMI 28.3->28.3. rule 1: exam states weight 72.4 kg, height 160 cm
- MG-RM15: w 73.4->70, h 172->168, BMI 24.8->24.8. rule 1: followup_outputs[0].output.findings[0].description states weight 70 kg, height 168 cm
- MG-RM16: w 48.8->57, h 151->163, BMI 21.4->21.5. rule 1: exam states weight 57 kg, height 163 cm
- MG-RP11: w 87.8->82, h 182->176, BMI 26.5->26.5. rule 1: exam states weight 82 kg, height 176 cm
- MG-RP12: w 56.6->66, h 165->178, BMI 20.8->20.8. rule 1: exam states weight 66 kg, height 178 cm
- MG-RP13: w 84.1->79, h 165->160, BMI 30.9->30.9. rule 1: exam states weight 79 kg, height 160 cm
- MG-RP14: w 59.9->67, h 156->165, BMI 24.6->24.6. rule 1: exam states weight 67 kg, height 165 cm
- MG-RS11: w 80->78, h 167->165, BMI 28.7->28.7. rule 1: exam states weight 78 kg, height 165 cm
- MG-RS12: w 70.4->72, h 172->174, BMI 23.8->23.8. rule 1: exam states weight 72 kg, height 174 cm
- MG-RS13: w 61.3->72, h 155->168, BMI 25.5->25.5. rule 1: exam states weight 72 kg, height 168 cm
- MG-RS14: w 68.9->69, h 168->168, BMI 24.4->24.4. rule 1: exam states weight 69 kg, height 168 cm
- MG-RS15: w 55.2->59, h 153->158, BMI 23.6->23.6. rule 1: exam states weight 59 kg, height 158 cm
- MG-RS16: w 88.8->84, h 179->174, BMI 27.7->27.7. rule 1: exam states weight 84 kg, height 174 cm
- MG-RS17: w 66.7->72, h 159->165, BMI 26.4->26.4. rule 1: followup_outputs[2].output.findings[0].description states weight 72 kg, height 165 cm
- MG-S01: w 60.9->62.4, h 166->168, BMI 22.1->22.1. rule 1: followup_outputs[3].output.findings[0].description states weight 62.4 kg, height 168 cm
- MG-S02: w 67->65.4, h 165->163, BMI 24.6->24.6. rule 1: followup_outputs[2].output.findings[0].description states weight 65.4 kg, height 163 cm
- MG-S04: w 56.2->54.8, h 162->160, BMI 21.4->21.4. rule 1: followup_outputs[2].output.findings[0].description states weight 54.8 kg, height 160 cm
- VASC-DEM-M08: w 75.2->71, h 177->172, BMI 24->24. rule 1: exam states weight 71 kg, height 172 cm
- VASC-DEM-M10: w 79.3->83, h 168->172, BMI 28.1->28.1. rule 1: exam states weight 83 kg, height 172 cm
- VASC-DEM-P04: w 56.2->57.7, h 156->158, BMI 23.1->23.1. rule 1: exam states weight 57.7 kg, height 158 cm
- VASC-DEM-S05: w 71.1->72, h 171->172, BMI 24.3->24.3. rule 1: exam states weight 72 kg, height 172 cm
- VASC-DEM-S06: w 79->82, h 171->174, BMI 27->27.1. rule 1: exam states weight 82 kg, height 174 cm
- VASC-DEM-S07: w 68->70, h 163->165, BMI 25.6->25.7. rule 1: exam states weight 70 kg, height 165 cm

## Checked and kept

- Weight gain or loss with a plausible current BMI: FTD-M09, FTD-S01, FTD-S05, FTD-S07, FTD-S09 (14-22 lb gain),
  ALZ-EARLY-S04 (5 lb), BACT-MEN-P02 (4 kg), BACT-MEN-RS03 (7 kg), FND-RM03 (4 kg), FND-RS01 (15 kg, from BMI
  about 20.6 to 14.8), ISCH-STR-P03 (8 kg), MG-M03 (4 lb).
- Stated BMI equal to the stored one: ALS-M07, ALS-P02, ALZ-EARLY-RS03, ALZ-EARLY-RS04, ALZ-EARLY-RS06, FND-RP01,
  FND-RP02, FND-RS01, ISCH-STR-M03, ISCH-STR-S04, SYNC-CARD-P02, SYNC-CARD-RM04, VASC-DEM-S02; MG-S03 and
  VASC-DEM-P08 already stored the stated weight and height.
- Apixaban dose-reduction notes (ISCH-STR, SYNC-CARD, VASC-DEM) agree with the stored weights (above 60 kg where
  the text says no criterion applies; ISCH-STR-S04 at 55.9 kg is the case whose text names the weight criterion).

## Doubts for the physicians

1. ISCH-STR-S03 (South Asian man): "Obesity" at BMI 28.7 is obese under the WHO Asian cut-off (27.5) but not
   the general one; BMI was raised to 30.5 so it reads as obese under either. Revert if the Asian cut-off was meant.
2. ISCH-STR-RS03: "Cachexia" now BMI 19.5 (59 kg) puts him just under the apixaban 60 kg threshold; the text Lead: 61 kg, BMI 20.1 (clear of the apixaban 60 kg threshold).
   already allows one criterion and asks for a current weight, so the standard dose still holds. Confirm.
3. ISCH-STR-RS05: the label was changed from "Obesity" to "Overweight" because the text states BMI 29.8.
   If obesity as a vascular risk factor matters to the case, raise the BMI to 30 or more instead.
4. BACT-MEN-P03 (advanced HIV, 10 kg loss, "generalized wasting", mildly reduced muscle bulk) kept at BMI 20.8:
   the loss meets the wasting-syndrome definition (over 10%), but rule 3's "cachexia usually below 20" would
   lower it to about 19.5.
5. Stated weights that read as "thin" or "wasted" at a normal BMI were kept: MG-RM11 ("Thin", BMI 23.2),
   MG-RM16 ("Thin", BMI 21.5), MG-RP12 ("moderately wasted", stated BMI 20.8 after an 11 kg loss).
6. FND-M06 "Obesity" raised from BMI 29.4 to 31.0 (94.9 kg) at the default height; any value of 30 or more fits.
