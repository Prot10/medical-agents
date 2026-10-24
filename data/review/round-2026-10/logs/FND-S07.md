# FND-S07
Reviewer status: R1 not reviewed, R2 not reviewed (no FND notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `initial_tool_outputs.mri` | Brain MRI report bundled cervical and thoracic cord sequences; the cord question (the real indication in acute paraplegia) had no criterion and no spine study (plan I). | FIXED: brain report now brain-only, non-contrast; new `initial_tool_outputs.body_imaging` (region spine, modality MRI, non-contrast): normal cervical and thoracic cord to the conus, no compression; new recommended criterion `action-spine-mri` (`order_body_imaging {study: spine_MRI}`). |
| A | major | `ground_truth.action_criteria` | Template tiers; brain MRI was the only imaging criterion; literature and drug check `recommended`; labels equal rationales. | FIXED (plan 3.2, S07): exam (required), `action-spine-mri` (recommended), brain MRI `action-4` (optional, `{contrast: false}`), new `action-neuropsych-battery` (optional), literature (optional), last. |
| A | major | `ground_truth.action_criteria[action-2-check-drug-interactions]`, `initial_tool_outputs.drug_interactions` | Drug check `recommended` in a patient with no medicines, with an output that had nothing to review. | FIXED: criterion and output deleted (plan 3.2 "delete S07"). The generation panel does not mark the drug check required, so no exemption is needed. |
| B | major | `followup_outputs[0]` (`family_meeting_fnd_education`) | A literature search disguising a family meeting (ruling 4), with PMID-style citations ("The FND challenge..." Lancet Neurol 2021) and outcome claims not in the plan's verified sources. | FIXED: deleted; family involvement is in M-COMM. |
| D | major | `initial_tool_outputs.literature_search` | Absent; the literature criterion was answered only by the disguised follow-up. | FIXED: canonical motor-only output (plan B, without the LaFrance and Goldstein rows). |
| A | minor | `ground_truth.sequence_constraints`, `stop_rule` | None; stop rule exam only. | FIXED: soft exam -> spine MRI; `required_before_assessment` exam; max 0. |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta `criteria_met` keys; em-dash fragment; impression leak "No further investigation is required...". | FIXED (plan H): library keys; 1 validated sign (bilateral Hoover); walking to the bathroom when unobserved listed as supportive; reflex, sensory and sphincter findings stated; canonical impression. |
| E | minor | `patient.neurological_exam.motor`, `.additional` | Em dashes and an unclear Hoover sentence. | FIXED: same findings, manoeuvre stated for each side; arm strength 5/5 stated (paraplegia with normal upper-limb coordination). |
| C | major | `ground_truth.assessment` | Template musts (neuropsychology "recommended tier", duplicates) and prohibitions citing Stone 2018. | FIXED (plan D): musts DX (both legs), COMM, PHYSIO, PSY (low mood and distress after the exam failure, after screening for depression); prohibitions P1, P2, P3, P7. |
| C | major | `ground_truth.differential` | Template MS, structural, neuropathy "(when obtained) EMG", autoimmune encephalitis and malingering rows; cord compression, myelitis and GBS (the mimics of acute paraplegia) missing. | FIXED (plan F, S07): spinal cord compression `low`, acute transverse myelitis including NMOSD/MOGAD `low`, GBS `low`; added hypokalemic periodic paralysis `low` (waking with weakness after rest is the classic history; reflexes preserved, arms spared, normal involuntary power). Template rows deleted. |
| D | major | `ground_truth.key_clinical_evidence` | Seven template items with the composition leak and Stone 2018 claims. | FIXED: five case-specific items. |
| C | minor | `ground_truth.red_herrings` | One generic stressor row. | FIXED: the exam failure and family pressure (specific), and the abrupt overnight onset (new). |
| C | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`, generic rationales. | FIXED (plan L): same 7 waste ids, `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales. |
| D | minor | `fallback_tool_outputs.specialized_test` | "Minor non-specific finding" served for any specialized test (plan G). | FIXED: nulled with the advanced-imaging and drug fallbacks; removed from `metadata.fallback_tool_kinds`; echo fallback `echo_type: TTE`. |
| C | minor | `metadata.notes` | "Anti-AQP4 and MOG-IgG critical to check given demographics" contradicted the policy: with a normal cord on MRI, no sensory level and normal sphincters there is no myelitis to test for. | FIXED: neutral case summary. |
| E | minor | `metadata.difficulty_rationale`, `revision_reason` | Template ("normal MRI and supportive normal labs"). | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
Acute complete paraplegia is now worked up as the plan sets it: the examination is required and shows a bilateral Hoover sign (each hip extends at full strength during attempted flexion of the other) with preserved reflexes, flexor plantars, intact sensation without a level and normal sphincters; walking to the bathroom when unobserved is supportive only. One spine MRI is recommended for the cord question and is reported on its own (normal cervical and thoracic cord to the conus, no compression); the brain MRI is now brain-only, non-contrast and optional. The drug-check criterion is gone (she takes no medicines), and so is the literature follow-up that stood in for a family meeting. The differential now names the mimics of acute paraplegia (cord compression, transverse myelitis including NMOSD and MOGAD, GBS, and hypokalemic periodic paralysis given the waking onset), all `low` with case reasons. Musts: positive diagnosis, explanation including the family, FND physiotherapy, psychological therapy for her low mood and distress after screening for depression; prohibitions P1-P3 and P7. The metadata note recommending AQP4 and MOG antibodies was removed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.2): this motor-only case still accepts "psychogenic non-epileptic seizures", "PNES", "functional seizures" and F44.5.

## Open questions for Andrea (judgment calls you could not settle)
- None. Hypokalemic periodic paralysis was added to the differential beyond the plan because the history (waking unable to move the legs after a long study session) is its classic presentation; it is `low` on examination grounds and no potassium criterion was added, so the tiers are unchanged.

## Checks
- `perfect_agent.py FND-S07 -v`: ok; the exam receives the stored clinical assessment and `order_body_imaging {study: spine_MRI}` receives the stored spine MRI (a `spine_CT` order gets the library CT, not the MRI; verified through the environment).
- `case_io.py check FND-S07`: schema and synonym guard OK; no failure names FND-S07.
- `test_case_guards.py -k FND-S07`: pass; discriminator guard (not yet enabled for FND) also clean.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan (section 4 S07) and PATTERNS.md.
- Confirmed: spine MRI split into `initial_tool_outputs.body_imaging` (region spine, modality MRI) and served to `order_body_imaging {study: spine_MRI}`; brain MRI brain-only and optional; drug check removed (no medicines; the panel does not require it); disguised family-meeting follow-up gone; bilateral Hoover wording correct; GBS row backed by the HPI (no illness, no sensory symptoms or pain); CSF avoided action and fallback were already absent at HEAD; diagnosis unchanged.
- Found and fixed: the added hypokalemic periodic paralysis row argued "the arms are spared without fluctuation", which does not count against a periodic paralysis (attacks are often leg-predominant); now it rests on preserved reflexes, full involuntary hip extension on Hoover testing and normal walking when unobserved. The transverse myelitis row stated as a rule that myelitis "would give a sensory level and bladder involvement within 24 hours"; softened to "a myelitis severe enough to cause paraplegia is expected to give...".
- Checks after my edits: `perfect_agent.py -v` ok (each required and recommended call served by the case's own stored report, not a fallback; the "<- ?" source label is a dump-format artefact, confirmed by executing the calls through the environment); `case_io.py check` schema and synonym guard OK, no test failure names the case; `test_case_guards.py -k` pass; discriminator guard (FND not yet enabled) run by hand: clean.
