# MIG-AURA-M05
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (structured ICHD-3 history required, MRI for red flags only, echo, EEG and monitoring removed), applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `assessment.prohibited_recommendations[0]`, `required_recommendations[3]`, `key_clinical_evidence[2]`, `action-2.expected_evidence`, `red_herrings[2]`, literature HRT block | HRT treated as prohibited or "contraindicated", and literature/red herring called transdermal oestrogen "WHO Category 3": WHO MEC classifies contraceptives, not HRT, and migraine with aura is not a contraindication (NICE NG23; plan class H). | FIXED: HRT prohibition and "avoid oestrogen-containing HRT" must deleted; canonical class H must added (she has hot flushes); key evidence and the HRT literature block rewritten (NICE NG23; MacGregor, Post Reprod Health 2018). |
| C | major | `followup_outputs` LDL block, `assessment`, `red_herrings[0]`, `action-2.expected_evidence` | "Borderline LDL 132" and a QRISK estimate appear only in a literature output and red herring; the case has no labs and the HPI says her health check was normal (class E). | FIXED: LDL literature follow-up, LDL must, LDL red herring and LDL text in expected evidence deleted. |
| B | minor | `ground_truth.red_herrings[2]` | "Elevated FSH and low oestradiol": no such results in the case. | FIXED: replaced by a red herring on the real data (hot flushes, combined pill stopped 18 years ago, HPI). |
| A | major | `initial_tool_outputs.drug_interactions.general`, `fallback_tool_outputs.drug_interactions.general` | Initial block was an empty shell whose summary was the expected text (guard leak); fallback said "agent not specified" (class C). Criterion `{"context": ...}` not sendable. | FIXED: both null (and `fallback_tool_kinds.drug_interactions` removed); criterion with ten HRT/oestradiol `{"drug": ...}` alternatives, recommended (plan: recommended because HRT is in the plan); follow-up `followup_outputs[0]` with real content (no contraindication from aura, HRT contraindications not present, transdermal preferred, progestogen for the uterus, aura review, HRT not contraception, non-hormonal alternatives). Leak guard now passes. |
| B | major | `initial_tool_outputs.clinical_assessment` | Template (class A): copied HPI sentences, `aura_accompanied_or_followed_within_sixty_minutes_by_headache: true` for attacks now without headache, generic red flags. | FIXED: structured assessment with her data (C6 false for current attacks; 4 of 6), homonymous aura persisting with either eye closed (the structured history distinguishes amaurosis), pattern-change red flag, GCA negatives, hormonal status; `all_criteria_for_typical_aura_without_headache_1_2_1_2_met` true; impression supports 1.2.1.2. |
| D | major | `initial_tool_outputs.mri.impression` | "Normal MRA, no posterior circulation stenosis, AVM, or aneurysm" in a brain MRI report (class K); "no ... enhancing lesion" on a study with no contrast parameter; `findings` empty while impression named four WMH. | FIXED: vessel and enhancement text removed; structured WMH finding; occipital, DWI and SWI negatives. No vessel study added (plan). |
| C | minor | `assessment.prohibited_recommendations[1]` | Ergot boilerplate (class I). | FIXED: deleted. Added the class G antiplatelet prohibition (she fears TIA) and the canonical combined-contraception prohibition (perimenopausal, still menstruating). |
| C | major | `assessment.required_recommendations` | "Confirm ICHD-3 1.2.1.2 criteria" restated the assessment; no contraception advice in a still-menstruating woman; no plan for follow-up. | FIXED: four musts: explanation (aura without headache, MRI normal); class H HRT must; contraception until menopause confirmed (combined methods UKMEC 4, LNG-IUS for both roles); no acute or preventive medicine needed, diary and review triggers. |
| A | major | `action-1-search-medical-literature`, literature follow-ups | Required step; queries as slugs; acephalic block claimed "Normal DWI, normal MRA ... provides strong diagnosis" and concluded for this patient. | FIXED: optional, `{}`, last; acephalic block rewritten (ICHD-3 1.2.1.2 comment; Fisher, Can J Neurol Sci 1980) and HRT block rewritten; both general. |
| C | minor | `ground_truth.differential` | Key features generic; GCA "consider ESR/CRP" with no labs in the case. | FIXED: TIA low (features, MRI), amaurosis very low (homonymous, positive, fundi normal), occipital seizure very low (phenomenology, MRI), GCA very low (no GCA symptoms, under 50). |
| D/E | minor | `key_clinical_evidence` | Engineering sentence (class D). | FIXED: three lines from this case. |
| B | minor | `ground_truth.red_herrings` | Empty `field_path` in all three entries. | FIXED: three entries with real paths (HPI twice, MRI finding). |
| C | minor | `avoided_actions` echo entry | Cited `[Charles_2017]` for PFO (class N). | FIXED: citation removed; rationale names PREMIUM, PRIMA, MIST. Dashes in two rationales replaced. |
| C | minor | `action-3`, `action-4` | Template labels; MRI arguments narrow; duplicate and free-text citations. | FIXED: case-specific; MRI `{}`, recommended (pattern change at 48). |
| C | major | `sequence_constraints`, `stop_rule` | None; literature required in stop rule, max 0. | FIXED: soft history-before-MRI; stop rule action-3 only (the only required criterion), max 1. Order: history, MRI, drug check, literature. |
| B | minor | `metadata.difficulty_description`, `difficulty_rationale` | "HRT ... Category 3", "HRT contraindication counselling". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 48-year-old perimenopausal woman with 20 years of migraine with typical visual aura now has the same aura 2-3 times a month without headache. The label (typical aura without headache, 1.2.1.2) is unchanged. The structured history shows the aura is her usual homonymous, positive, spreading aura (4 of 6 C characteristics, headache now absent) and flags the pattern change at 48. MRI (recommended) shows no infarct or occipital lesion and four non-specific WMH; the MRA text is gone. The case no longer forbids HRT: the must is the NICE NG23 approach (transdermal oestradiol at the lowest effective dose with a progestogen, review if the aura changes), and the drug check (recommended) is an HRT check with real content. A contraception must is added because she still menstruates. The invented LDL and FSH/oestradiol data are gone. TIA is low and antiplatelet therapy is prohibited.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `diagnosis_synonyms.yaml` G43.109 group: add "typical aura without headache", "acephalgic migraine", "migraine aura without headache" (plan 5.1, M05); drop "migraine aura".
- Criteria pack allow-list: `[NICE_NG23]`, `[UKMEC_2016]`, `[AHS_neuroimaging_2020]`, `[PREMIUM_2017]`, `[PRIMA_2016]`, `[MIST_2008]`.

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: removal of the HRT prohibition and every "category 3" or "contraindicated" HRT text, the class H must, the HRT drug output (contents, NICE NG23 statements), the removed LDL and FSH data, the null initial and fallback drug blocks, structured-history criteria versus the HPI (C6 false, 4 of 6), MRI report, literature sources (Fisher 1980, MacGregor 2018 exist), contraception must for a still-menstruating woman, differential, red-herring paths, sequence direction, stop rule (only required criterion). Every log claim holds. No reviewer notes exist for this case. Note: `metadata.case_body_concerns[0]` still says the drug check has "only fallback" (stale authoring note, now untrue); left unchanged because metadata notes are not edited this round.

Found and fixed:
- `assessment.prohibited_recommendations[0]`: the canonical class G text claimed "succession of symptoms"; her aura is visual only. Rewritten to her features (positive visual symptoms spreading over 20-30 minutes, identical to 20 years of previous auras).

`perfect_agent.py -v` ok, `case_io.py check` clean for the case, guard tests pass.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `metadata.case_body_concerns[0]`: stale authoring note "check_drug_interactions (only fallback)", untrue since the drug check now has its own stored output; removed, as P08, P09, RM11 and RS11 had already done (metadata only, not shown to the agent).

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x2, [ICHD_3] x3.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- synonyms "typical aura without headache" and "acephalgic migraine" added; "migraine aura without headache" declined (an answer "migraine without aura, tension-type headache" contains its tokens).
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.
