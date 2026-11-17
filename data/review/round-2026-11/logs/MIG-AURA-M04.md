# MIG-AURA-M04

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 9e6fc9af-a89d-4c21-b879-c2d1aeac7c89 | FIXED (class LIT, commit 393c547e) | Nothing left to remove: no search_medical_literature criterion, follow-up or stored output; fallback literature_search null. |
| 4ed3d3c1-f7c4-4720-bd89-696daae55326 | FIXED (plan D3) | ground_truth.assessment.required_recommendations[4] -> canonical must: "If topiramate is chosen, start it only under the topiramate pregnancy prevention programme with a contraceptive method unaffected by enzyme induction: a copper IUD, a levonorgestrel IUS, or medroxyprogesterone acetate injection used with condoms. Topiramate is treated as a potential enzyme inducer at any dose, so pills and the etonogestrel implant are not adequate." followup_outputs[0].output.warnings[1] and followup_outputs[2].output.interactions[1]: kept the 200 mg/day fact and added "FSRH (2022) advises treating topiramate as a potential enzyme inducer at any dose, so pills and the etonogestrel implant are not adequate contraception with it." |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.diagnosis.accepted[0] | "preventive therapy indicated": AHS 2021 lists brainstem aura under "consider", and three attacks in four months is below the offer threshold (class of note 1b2dc411, plan D8) | FIXED (label change: "preventive therapy to be considered"; matcher still accepts "migraine with brainstem aura") |
| C | major | ground_truth.assessment.required_recommendations[3] | "Offer migraine prevention because the brainstem aura recurs" overstated the indication (D8) | FIXED ("Discuss migraine prevention (AHS 2021 'consider' ...), weighing disability, preference and treatment risks; if she chooses it" + the same agents, doses and review) |

PATTERNS check: no TIA prohibition or antithrombotic must; the stored "Etonogestrel implant: UKMEC 2" in followup_outputs[0].output.alternatives and REQ0's switch list concern the aura, not topiramate, and stay (D3); triptan/ergot avoidance unchanged (no note); no leakage in the patient block; pathway order is clinical.

## Changes
Two changes. First, the topiramate must now follows FSRH 2022: if topiramate is chosen it is started only under the pregnancy prevention programme with a copper IUD, a levonorgestrel IUS or medroxyprogesterone acetate injection used with condoms, because topiramate is treated as a potential enzyme inducer at any dose and pills and the implant are not adequate; the contraceptive and preventive drug-check reports now carry the same any-dose caution next to the 200 mg/day fact. Second, prevention is now to be discussed rather than offered as indicated: the label ends "preventive therapy to be considered" and the must asks the agent to discuss prevention (AHS 2021 "consider" for brainstem aura; three attacks in four months) weighing disability, preference and risks, with the same amitriptyline and propranolol options and doses. The switch away from Rigevidon (implant included, which concerns the aura) is unchanged.

## Verification
perfect_agent.py -v: ok (every required and recommended criterion served by its own report). test_case_guards.py -k <case>: pass. case_io.py check: schema OK, synonym guard OK, no failure names this case (one unrelated failure names MIG-AURA-P05). DiagnosisCriterion.matches re-checked on a plain correct answer after any label edit: True; TIA / mimic answers: False.
Pass 1: 0 errors found
- Checked the D3 canonical must and the two report cautions, the D8 label and must (three attacks in four months matches the HPI and assessment; propranolol caveat consistent with her history), no literature step left, checks pass.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Checked: D3 canonical must and both report cautions (FU0 warnings[1], FU2 interactions[1]); D8 label and REQ3 (three attacks in four months matches HPI and assessment); the implant in REQ0 and FU0 alternatives concerns the aura (D3). Every note id has a ruling; no literature string left (fallback literature_search null); no new em dash; no answer leakage in the patient block or drug-check outputs.
Cosmetic (not counted): none (REQ1 'the MRI is normal' next to two non-specific hyperintensities left as patient-facing shorthand; the impression calls the posterior fossa normal).
Re-run at pass 2: perfect_agent.py -v ok (each required and recommended criterion receives the report carrying its expected evidence); test_case_guards -k for MIG-AURA-M01..M06: 48 passed; case_io.py check: schema OK, synonym guard OK, no failure names this case; mri_probe: no gadolinium text, no MRI pair needed; DiagnosisCriterion.matches: correct answer True, TIA / mimic False.
Condition audit (MIG-AURA auditor, 17 Nov 2026): 1 error found
- D/leak (own finding, TOOL_REPORT_STYLE_GUIDE check_drug_interactions: a drug check must not announce the patient's diagnosis): followup_outputs (check_drug_interactions, trigger check_sumatriptan_..._brainstem_aura).output.summary said 'Triptans and ergots are label-restricted in migraine with brainstem aura', applying the label restriction to this patient as if the diagnosis (migraine with brainstem aura, which the patient block does not name) were already made. FIXED: '... label-restricted in migraine with brainstem aura and hemiplegic migraine' (the two label exclusions, as in contraindications[0]). The interaction content and the criterion's expected evidence are unchanged; no ruling changes. perfect_agent passes.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Full re-verification: git diff 06b74446 read and the whole case read. The D3 canonical must is REQ4, and the any-dose FSRH caution is in FU0 warnings[1] and FU2 interactions[1]. REQ0 still lists the implant, which concerns the aura, not topiramate (D3). The D8 label "preventive therapy to be considered" agrees with REQ3 (discuss; AHS consider; three attacks in four months, as in the HPI and assessment) and with KCE[3]. The condition-audit triptan summary edit ("migraine with brainstem aura and hemiplegic migraine") is correct and matches contraindications[0]. The LIT removal is complete. The metadata.case_body_concerns deletion is clean. Unlogged edit found in the diff, correct and kept: differential[0] (Posterior circulation TIA) key_features "normal interictal examination and MRI" became "normal interictal examination; MRI shows no infarct (a normal DWI does not exclude TIA; the distinction is clinical)". This is the plan section 1 canonical fact (class TIA-CERT) and agrees with the MRI report. Rulings file matches the log.
- perfect_agent.py -v ok; test_case_guards -k (M01..M08) 64 passed.
Cosmetic (not counted): REQ1 says "the MRI is normal" although the MRI shows two non-specific hyperintensities (already noted at pass 2). Not counted, because no note asks for it and the plan kept it: MRI stays recommended for a red flag (recent-onset brainstem aura) that the stop rule does not require (lead decision D7).
