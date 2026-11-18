# MG-P02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed initial literature_search outputs: Lambert-Eaton myasthenic syndrome diagnosis tumor screening treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R2 needs_changes (NB-87MF-FBTV-TPWE) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:MG-P02:policy_verdict | FIXED | Waste labels: ground_truth.avoided_actions[2] avoid-waste-sfemg {test_type: emg_single_fiber}, [3] avoid-waste-levodopa-challenge, [4] avoid-waste-gait-and-balance-timed, [5] avoid-waste-speech-language-evaluation (waste, [Titulaer_2011]); their follow-ups (followup_outputs[1]-[4]) already sit after the optional autonomic testing. Stop rule: ALREADY-FIXED (action-2-order-specialized-test is test_type repetitive_nerve_stimulation; display CENTRAL.md item 3). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.avoided_actions[6] | Case fallback chest X-ray served unlabelled in a tumour search that needs CT then PET (D10 class) | FIXED: avoid-waste-chest-xray {study: chest_xray}, [EFNS_paraneoplastic_2011] |
| C clinical | - | ground_truth (tiers, musts) | LEMS: RNS and ECG already required; the MG steroid, screening, severity and thymectomy classes do not apply (plan C13) | No change |
| E language | minor | metadata.last_revised, metadata.revision_reason | Described the August edit | FIXED |
| A schema | minor | ground_truth.avoided_actions (avoid-waste-sfemg).citations | Rationale cites Oh 2005 in text without its key (found in verification pass 1) | FIXED: [Oh_2005] added |

## Changes
The stored reports that answered orders the policy neither asked for nor labelled are now labelled waste: the levodopa challenge (no parkinsonian signs; his gait is explained by proximal weakness and the sensory neuropathy), the timed gait and balance battery, the single-fibre EMG after a repetitive stimulation study that is already diagnostic (low CMAPs, 142-152% facilitation) with positive P/Q-type VGCC antibodies, the speech and language battery, and a chest X-ray, which cannot replace the CT and FDG-PET of the tumour search. Their reports stay, so those orders are not answered by a contradicting library normal. The stop rule already required the repetitive stimulation study itself (not any specialized test), so autonomic testing or SFEMG cannot satisfy it; the app displays only the tool name (CENTRAL). Nothing else changed: the LEMS work-up, tiers and management are as before. Checks: perfect_agent.py -v ok; test_case_guards.py for MG-P02 passed. No MRI edited. Not an approved case. Literature (class LIT): none left (checked).

## Verification
Pass 1: 0 errors found
Checked the note ruling; the final case read in full. The five waste labels match stored reports that no criterion uses; the stop rule keys on the RNS criterion; LEMS tiers and musts unchanged as the plan says.
Cosmetic (not counted): avoid-waste-sfemg rationale cites Oh 2005 in text without the key; [Oh_2005] (pack allow-list) added.
Checks after pass 1: perfect_agent.py -v ok; test_case_guards.py -k for this id passed.
Pass 2: 0 errors found
Verified the pass-1 addition of [Oh_2005] to avoid-waste-sfemg citations: the key is on the MG pack allow-list (Oh 2005, electrodiagnostic criteria of LEMS, RNS increment) and supports the rationale that RNS is already diagnostic. No change.
Checks: perfect_agent.py -v ok; test_case_guards.py -k (all six pass-2 ids) passed.
