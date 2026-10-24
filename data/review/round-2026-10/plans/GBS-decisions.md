# GBS: decisions on the open questions (24 October 2026)

Andrea, 24 Oct 2026: resolve every open point "nel modo migliore per la qualità del dataset". Each
entry gives the question, the decision, the reason with its source, and what changed where.

Sources checked on 24 Oct 2026:
- EAN/PNS 2023 guideline, read in full text (Eur J Neurol 2023;30:3646-3674, version of record).
  Verified: no ganglioside testing in motor-sensory GBS, anti-GQ1b when MFS or MFS spectrum is
  suspected, not for subtyping (p. 3655); electrodiagnostic subtyping not advised; antecedent
  infection testing "generally not clinically useful"; HIV listed only among differential
  infections; FVC 3-6 times daily, a fall >30% alerts, elective ventilation at FVC <=20 mL/kg, SBC
  <20, "an MEP of <30 cmH2O or MIP <40 cmH2O" for elective ventilation, and FVC <60% predicted as a
  predictor of ventilation (OR 2.86; pp. 3657-3658); no mention of IgA screening; **no
  recommendation on MFS treatment** (the guideline states it is based on motor-sensory GBS
  studies).
- Leonhard 2019 (Nat Rev Neurol 15:671-683, PMC6821638): pure MFS "treatment is generally not
  recommended", close monitoring for overlap; 20/30/40 rule.
- ASCO 2021 irAE guideline (Schneider, JCO 39:4073-4126) as reproduced in the ASCO bundle:
  ICI-related GBS, methylprednisolone 2-4 mg/kg/day with slow taper; pulse 1 g/day for 5 days may be
  considered in grade 3-4 with IVIg or PE.
- LactMed, Immune Globulin (NBK501437): IgG a normal milk component; no special precautions.
- Wakerley 2014 (Nat Rev Neurol 10:537-544): incomplete MFS forms (acute ophthalmoparesis, acute
  ataxic neuropathy, acute ptosis) and the PCB and bifacial variants.

## Synonyms (CENTRAL 5) and labels (CENTRAL 6)

**Variant synonyms.** Decision: scope them per case. The single `G61.0` entry gave every case
"AIDP", "AMAN" and "miller fisher syndrome", so an MFS answer scored in AIDP cases and an AIDP answer
in the MFS, PCB, bifacial, ptosis and AMAN cases. Now `G61.0` carries only the generic GBS labels
(the four spellings/abbreviation); `G61.0+aidp` (all GBS cases except P01, RM12, RM15, RS11, RS15,
RP16, whose NCS is not that subtype or whose variant is not classic GBS; checked: RP11 and RS18 NCS
are demyelinating), `G61.0+aman` (RP16), `G61.0+mfs` (P01: miller fisher syndrome, fisher syndrome,
MFS), `G61.0+gq1b` (RM15: anti gq1b syndrome, incomplete miller fisher syndrome), `G61.0+pcb` (RM12,
RS15: pharyngeal cervical brachial), `G61.0+bifacial` (RS11). Generic GBS labels stay in the variant
cases: EAN/PNS and ICD-10 place MFS and the regional variants in the GBS spectrum. Residual limit: a
submitted ICD code G61.0 credits any GBS-spectrum answer (ICD-10 has no variant codes); not fixable
by labels. Applied with `--prune --conditions guillain_barre` (30 cases); `--check` clean.

**Labels (ruling 3, summary CENTRAL 6).** Decision: normalise, no diagnosis changes.
- M01, M02, RS17: "Guillain-Barre" -> "Guillain-Barré".
- P02: em dash removed: "Guillain-Barré syndrome, AIDP, HIV-associated, with CSF pleocytosis".
- P03: "areflexia" -> "mildly affected and ambulant" (trace patellar and brachioradialis reflexes:
  the auditor's flag was a real inaccuracy).
- RP11: "Guillain-Barré syndrome related to an immune checkpoint inhibitor (pembrolizumab)".
- RP15: speculative "(likely immune dysregulation)" removed: "Guillain-Barré syndrome, AIDP, after
  lung transplantation".
- RS18: em dash removed: "Guillain-Barré syndrome, severe AIDP, seronegative, with cranial nerve
  involvement and a cervicomedullary T2 MRI signal change".
Codes: all stay G61.0.

## Summary open questions 1-7

**Q1. RM15 and RS15 stay G61.0 by the edit route.** Confirmed. Wakerley 2014 lists acute ptosis as
an incomplete MFS form and defines PCB; RM15 has anti-GQ1b positive bilateral ptosis with global
areflexia, full eye movements and a negative MG work-up; RS15 has oropharyngeal, neck and arm
weakness with arm areflexia and spared legs. Relabelling as MG or MND would contradict their own
data (normal RNS and jitter, negative AChR/MuSK, areflexia). Synonyms scoped accordingly.

**Q2. FVC <60% predicted.** Confirmed as an ICU-level monitoring trigger, not an intubation
criterion. EAN/PNS 2023 reports FVC <60% predicted as a predictor of ventilation (with neck flexion
weakness and nadir <7 days, >85% ventilated); its elective-ventilation threshold is FVC <=20 mL/kg.
Pack section 5. Related finding (new): EAN/PNS writes "MEP <30 or MIP <40 cmH2O" where Lawn 2001
writes MIP <30 and MEP <40. Four monitored-bed cases sat in the discordant band (M03 MIP -35, RM11
-36, RM14 -36, RP15 -34): under the governing guideline they would need elective ventilation
considered. Decision: keep them as monitored-bed cases and move MIP out of the band (M03 -44, RM11
-44, RM14 -42 with the earlier value -44, RP15 -46; all still flagged L), and set the escalation
must in the eight monitored-bed cases that quote it (M03, P03, RM11, RM14, RP13, RP15, RS11, RS14)
to "MIP weaker than -40 cmH2O" (the earlier of the two thresholds). ICU cases already meet other
triggers; canonical a4 evidence (Lawn's ICU triggers) unchanged.

**Q3. IgA before IVIg.** Confirmed: no routine IgA screening; the prohibition is renal function
only. EAN/PNS 2023 (full text) and Leonhard 2019 do not require it; test only with a known IgA
deficiency or a previous reaction to blood products (none in the 30 cases; no case mentions IgA).
Pack section 4.

**Q4. RP11 doses.** Confirmed: the must's "IV methylprednisolone (2-4 mg/kg/day, or a 1 g/day pulse
for 5 days in severe disease) followed by a slow taper" with IVIg or PE matches ASCO 2021. Kept
(recommendations are unscored; doses let a physician check the must). No change.

**Q5. `[LactMed]` in RM14.** Confirmed: LactMed Immune Globulin (NBK501437) supports "IVIg is
compatible with breastfeeding; IgG is a normal component of breast milk". Full reference added to
the pack. No plasma exchange claim in the case. No change.

**Q6. HIV out of the required lab arguments.** Confirmed. EAN/PNS 2023 lists HIV only as a
differential infection, not a routine test; P02 (known HIV) keeps its viral load and CD4 criterion.
No change.

**Q7. Subtype words in labels only where the NCS meets them.** Confirmed (EAN/PNS: subtyping not
advised for routine decisions, so it must never be asserted beyond the data); the synonym scoping
above applies the same rule to scoring. S03 "with secondary axonal injury" kept (approved case; the
NCS impression itself reports secondary axonal features).

**Approved cases re-review.** The seven approved cases (RP16, RS12, S02, S03, S04, S01, RS18)
changed for class errors and go back to Reviewer 2 under the round's rule; nothing for Andrea to
decide.

## Auditor flags ("noted and deliberately left unchanged")

- P03 label "areflexia": fixed (above).
- RS18 HPI "left lower facial weakness" against forehead involvement: fixed to "left facial weakness
  in a lower motor neuron distribution, involving the forehead".
- Em dashes in `accepted[0]` of P02, RP11, RS18: removed (above).
- RM13 absent sural SNAPs with intact sensation: kept; subclinical sensory loss is common in a
  diabetic neuropathy background and does not affect the labels or criteria.
- S03 NCS without a needle EMG line: kept (approved case; the criterion does not need it).
- Older em dashes in unchanged exam prose: kept (no churn in approved prose).

## Further finding: MFS treatment citations

P01 and RM15 cited `[EAN_PNS_2023]` for "IVIg and PE are not routinely advised in Miller Fisher
syndrome"; EAN/PNS 2023 says nothing on MFS treatment. Re-cited to `[Leonhard_2019]` (RM15 must 1
`[Leonhard_2019, Wakerley_2014]`); the literature results' evidence_level is now "review". Pack
section 1 states which source governs MFS.

## Criteria pack, generator, guidance

- `dataset-generation/criteria_packs/GBS.md` rewritten to the plan: EAN/PNS 2023 governing, source
  map, canonical criteria order and tiers, conditional DDI, optional literature, ganglioside rule,
  no antecedent serology, respiratory rules with the discordant band, sequence constraints, stop
  rule, treatment statements, pitfalls; allow-list with full references for all 11 keys the cases
  cite; Asbury_1990, Hadden_1998 marked superseded, Sharshar_2003, Yuki_2012, van_den_Berg_2014 as
  background or secondary.
- `conditions.yaml` guillain_barre: removed `request_repeat_ncs` (future NCS results, C12); the
  respiratory follow-up under `order_specialized_test` with the canonical format; the ganglioside
  follow-up renamed `request_anti_gq1b_gt1a_ganglioside_panel` and restricted to MFS-spectrum/PCB;
  spine MRI under `order_body_imaging` with red-flag-only description; telemetry first 24 h, findings
  only. Key findings: no leukocytosis template, no Campylobacter/CMV/EBV/Mycoplasma serology, no
  anti-GM1; CSF cells <5 (not <10), protein may be normal in the first week; AMAN/AMSAN corrected
  (AMSAN is not "axonal with normal velocities" alone); pacing removed from the ECG finding.
  Presentations no longer contain scored results (CSF dissociation, respiratory function, LP protein,
  "anti-GQ1b pending") or an asserted Campylobacter trigger. Differential: acute-onset CIDP wording,
  botulism features, MG added.
- Review-app guidance: GBS brain MRI, spine MRI and CSF responses rewritten to the current counts
  (brain MRI recommended 7 required 1; spine MRI recommended 6 optional 2; CSF required 29
  recommended 1); YAML regenerated with `--write`; claim table updated; GBS claims pass (remaining
  failures are ALZ-EARLY, GLIO-HG and SAH claims).

## Cases changed

All 30 (synonym expansion). Content edits: M01, M02, RS17, P02, P03, RP11, RP15, RS18 (labels; RS18
HPI), P01, RM15 (citations), M03, RM11, RM14, RP15 (MIP values), M03, P03, RM11, RM14, RP13, RP15,
RS11, RS14 (escalation must). Each log has "## Close-out (24 Oct 2026)". Checks: perfect_agent
30/30; `case_io.py check` on all 30 clean (schema, synonym guard, no failure names a GBS case);
`test_case_guards -k GBS-` 60 passed; synonym `--check --conditions guillain_barre` clean.

## Still needing Andrea

Nothing that needs information only Andrea has.

## CENTRAL (vocabulary and code; not done here)

1. `interpret_labs`: `anti_GQ1b_IgG` and `anti_GT1a_IgG` (or one `anti_ganglioside_panel` with
   GQ1b/GT1a IgG), whose tokens reach trigger `request_anti_gq1b_gt1a_ganglioside_panel`. Cases: P01
   (MFS, GQ1b positive), RM15 (GQ1b positive), RM12 and RS15 (PCB, GT1a), RS11 and RS18 (negative).
   Then a recommended criterion in P01, RM12, RM15, RS15 and an optional one in RS11, RS18.
2. `analyze_csf` special test `CMV_PCR`: P02 (must asks for it), and the stored CSF reports of
   RM16, RP15, RS18 that already carry a CMV PCR result.
3. `interpret_labs` or `order_microbiology` `botulinum_toxin_assay` (serum/stool): RM12, RS15 (botulism
   lowered on clinical grounds until then).
4. Schema: `weight_kg`, `height_cm` in demographics (weight now in `physical_exam.general`, all 30).
5. Fallback library: `respiratory_function` normal report with FVC L, % predicted, mL/kg, MIP, MEP.
6. Tests: guard for respiratory outputs "within normal limits" with FVC <80% or low values flagged
   "(H)"; guard for the leaky clinical_significance sentence, "(agent not specified on this case's
   pathway)" and the a7 template text in other conditions.
