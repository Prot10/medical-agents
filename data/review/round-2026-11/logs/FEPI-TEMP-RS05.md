# FEPI-TEMP-RS05

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-4-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: no change. The only stored brain MRI (initial_tool_outputs.mri) is a non-contrast 3T epilepsy protocol whose technique line states 'no gadolinium'; it has no post-contrast sequence, signal key or enhancement finding, so it is not a gadolinium study (mri_probe flags gad_text only on that negative phrase). It stays contrast_used null (decision 4: false would send a contrast order to the library normal; plain and contrast orders both receive the case study, never the library). Criterion action-3-analyze-brain-mri stays plain ({protocol: epilepsy}, no contrast argument): ILAE 2019 HARNESS-MRI does not need gadolinium for hippocampal sclerosis (FEPI-TEMP criteria pack: no gadolinium in HS reports); expected_evidence already matches the report. No case fallback MRI, no body-imaging MRI.
- MRI-CONTRAST verified: checked the only stored brain MRI (initial, contrast_used null, no post-contrast sequence, key, finding or impression clause), the null case fallback MRI, no body-imaging MRI, criterion action-3-analyze-brain-mri plain per ILAE 2019 with expected_evidence received by the case report, plain and contrast orders answered by the case study (never the library), nothing else changed since 393c547e; perfect_agent ok. Changed: removed the technique clause '; no gadolinium' from initial_tool_outputs.mri.additional_observations[0], because decision 4 says a null report answers both orders and says nothing about gadolinium (a contrast order received a report stating none was given), the FEPI-TEMP criteria pack allows no gadolinium line in HS, FCD or MRI-negative reports, and FEPI-TEMP-RP02 was handled the same way; the probe now shows gad_text=n.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 29fada5d-c985-4e9d-aea0-75096f5d8f27 | FIXED | class LIT, commit 393c547e; no literature output or criterion left (checked) |
| 4a631479-293f-49da-811d-3bb474324856 | FIXED | class LIT, commit 393c547e; no literature output or criterion left (checked) |
| 5479d55f-3dd3-440e-81aa-8c42bb62bf19 | FIXED (HLA D6) | deleted required_recommendations[1] (HLA must); new prohibited_recommendations[3] with HLA-A*31:01 clause; key_clinical_evidence[4] 'before carbamazepine or oxcarbazepine' |
| f5970455-ca97-446c-84d0-b6b44079ca4c | FIXED (BIOPSY D3) | ground_truth.avoided_actions[4] stereotactic, [5] open (harm, [ILAE_MRI_2019]), [6] avoid-harm-resection ([Kwan_2010], treatment-naive) |
| de44b8b5-592a-4bdf-ba72-503f2acde8e1 | FIXED (BIOPSY D3) | note misfiled on the TEE step; same biopsy avoided actions |
| 85512f5e-58e2-4679-9239-1285d2226e5e | FIXED (TEE D5) | new ground_truth.avoided_actions[7] avoid-waste-tee (order_echocardiogram {echo_type: TEE}, waste, [NICE_NG217_2025]) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | patient.history_present_illness | Class LAT (D10): right-hand picking automatism with a left temporal focus (template error); flipped to the left hand (the only mention) | FIXED |
| C | minor | ground_truth.assessment.prohibited_recommendations (valproate) | Class VPA (D7): UK MHRA 'under 55' procedure in the valproate prohibition; replaced by the jurisdiction-neutral text for men | FIXED |
| A | minor | followup_outputs order | The drug-interaction check came before the video-EEG; reordered to video-EEG, drug interactions, then the off-pathway biopsies and TEE | FIXED |
| B | minor | ground_truth.avoided_actions[avoid-waste-tee].rationale, avoided_actions[avoid-waste-2-order-echocardiogram].rationale | Both echo rationales asserted 'no murmur', but the case documents no cardiac examination (no physical exam block); now 'no known heart disease' (verifier pass 3) | FIXED |

## Changes
Literature steps were removed by the class change (commit 393c547e). The unconditional HLA-B*15:02 must is replaced by a prohibition: do not start carbamazepine or oxcarbazepine without first testing HLA-B*15:02 given his South Asian ancestry, with HLA-A*31:01 tested at the same time. Standalone stereotactic and open hippocampal biopsies and a resection are avoided actions (harm), since he is treatment-naive and the MRI and EEG establish the diagnosis; the stored transesophageal echocardiogram is a waste avoided action. The picking automatism is now in the left hand, on the side of the left temporal focus, and the valproate prohibition uses the jurisdiction-neutral wording. The pathway lists the video-EEG before the drug-interaction check.

## Verification
Pass 1: 0 errors found
- Checked: all 6 notes ruled, rulings match plan D3, D5, D6 and LIT; HLA must removed and prohibition present once with the HLA-A*31:01 clause; KCE[4] consistent; LAT flip complete (only mention in the HPI); TEE waste and the existing TTE waste do not overlap any criterion; biopsies and resection labelled harm. perfect_agent -v passes and each required and recommended criterion receives the report carrying its evidence; test_case_guards -k passes; case_io check shows only the centrally maintained test_guidance_claims counts; no em dashes in new text.

Pass 2: 0 errors found
- Checked without change: all 6 notes ruled and rulings correct against plan D3, D5, D6 and LIT; HLA prohibition once, with the HLA-A*31:01 clause, and KCE[4] consistent; TEE waste and TTE waste match no criterion; biopsies and resection harm (treatment-naive); left-hand picking matches the left focus, tongue-bite side unchanged; valproate prohibition uses the text for men; perfect_agent -v passes; test_case_guards -k passes.
Pass 3: 1 error found
- B minor, ground_truth.avoided_actions (avoid-waste-tee, new this round, copied from avoid-waste-2-order-echocardiogram): the rationales said he has 'no murmur', a finding the case never records (patient has no physical exam, only the neurological exam and vitals); both now say 'no known heart disease', which the history supports. Ruling 85512f5e text updated.
- Checked without change: all 6 notes ruled and rulings correct (D3, D5, D6, D7, LIT); ruling field paths resolve (stereotactic [4], open [5], resection [6], TEE [7]); HLA prohibition once with the HLA-A*31:01 clause; left-hand picking matches the left focus, no other hand mention; perfect_agent -v passes; test_case_guards -k passes; case_io check fails only on the centrally maintained test_guidance_claims counts.
Pass 4: 0 errors found
- Checked without change: all 6 notes ruled and rulings correct (D3, D5, D6, D7, D10, LIT); ruling field paths resolve (prohibition [3]; avoided actions stereotactic [4], open [5], resection [6], TEE [7]); HLA prohibition once with the HLA-A*31:01 clause and KCE[4] consistent; the single HLA must removed and must [1] on sodium is conditional; left-hand picking (the only hand mention) matches the left focus, tongue-bite side unchanged; TEE and TTE waste rationales ('no known heart disease') agree with the history; labs criterion served sodium, glucose 138 and calcium and the red-herring path resolves to the glucose row; drug-interaction report agrees with the sulfonamide allergy and ancestry; perfect_agent -v passes; test_case_guards -k passes (54 for the six cases); no em dash in added text; rulings file and note table cover every note id.
