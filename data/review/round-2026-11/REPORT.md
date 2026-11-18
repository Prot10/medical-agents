# November 2026 review round: report (17 Nov 2026)

**Base.** All 600 cases were byte-identical to the VPS snapshot (aggregate hash 88bd8dc0…fba3, 600/600 files). Baseline on pristine 06b74446: perfect agent 600/600, synonyms 0, pytest 6533 passed / 0 failed.

**Notes (ledger.jsonl, 963 rows).** FIXED 813, ALREADY-FIXED 33, CENTRAL 52, NO-ACTION 63, DECLINED 2, NEEDS-ANDREA 0. NO-ACTION is an extra status for approvals and empty verdicts.

| cond | F | AF | C | NA | D |
|---|---|---|---|---|---|
| FEPI-TEMP | 206 | 6 | | 1 | |
| MS-RR | 117 | | | | 1 |
| FTD | 102 | 6 | | | |
| ALZ-EARLY | 34 | | 44 | 7 | |
| VASC-DEM | 67 | 5 | 3 | | |
| FND | 72 | | | | 1 |
| MIG-AURA | 52 | 3 | | 8 | |
| PD | 46 | | | 1 | |
| MG | 31 | 1 | 4 | 4 | |
| NMDAR-ENC | 21 | 3 | | 11 | |
| SYNC-CARD | 40 | 3 | 1 | 16 | |
| NPH | 20 | 1 | | 15 | |
| GLIO-HG | 5 | 5 | | | |

DECLINED: MS-RR-S03 (the patient is African American, not East Asian); FND-RS02 (a note copied from RS01, about refeeding risk this patient does not have).

**Classes, before → after (all 600 cases).**
- Literature criteria: 353 → 0. Stored literature outputs: 416 → 0.
- Gadolinium MRIs with a null flag: 214 → 0, now plain/contrast pairs.
- Unlabelled served follow-ups: 2910 → 2417.
- Per-condition classes (biopsy harm, HLA-B*15:02, MG RNS/steroid/thymectomy, FND duplicates, percentile labels): counts in plans/<COND>-summary.md.

**Approved cases.** All 91 changed: 90 through the literature class and 40 through MRI pairs. Notes or classes also changed MG RM13, RM14, RM15, RS11; NMDAR-ENC P03 P07 P08 RM02 S01 S02 S03 S04 S06 S09 S10; SYNC-CARD P02 RM04 RP01 RS03 RS05 RS06 S01 S02 S04 S05 S06.

**Labels.** 51 `accepted[0]` wording changes, each ruled by a note (FEPI 9, FTD 5, VASC 7, FND 7, MIG 11, PD 4, MG 1, SYNC 6, NPH 1). `icd_codes[0]` changed only in FND RS02, S02, S03 and S04, rewritten as new phenotypes (R1: near-duplicates). Synonym entries are updated for FND, MG (G70.01), SYNC-CARD, NPH, FTD and VASC-DEM.

**CENTRAL** (CENTRAL.md). Fix the review-app display: null shows as "none", keys print alphabetically, on-request studies look like pathway steps (this display caused the 52 CENTRAL rulings). Vocabulary: swallow assessment, clustered MuSK, mammography. Also: a StopRule rationale field, criteria-pack updates, and a re-run of the guidance builder (its input is not here).

**For Andrea and the physicians.** Nothing blocks. R1 should pick one neuropsychology percentile convention (VASC-DEM uses AACN 2020; ALZ-EARLY keeps R1's own row-range flags). SE and GBS still serve unlabelled biopsy and TEE reports; they have no notes and were not changed.

**Checks (final).** Perfect agent 600/600. The 21 warnings are the 16 at base plus benign new ones: fallback-answered alternatives in MG and SYNC-CARD, and a CSF report shared in NMDAR-ENC-RS04. Synonyms --check 0. pytest 6533 passed / 0 failed, including tool_io schemas and review-app tests. Schemas 4 passed.

**Verification.** Every changed case ended on a pass with 0 material errors. Minor pre-existing defects were fixed when found; the remaining ones are not listed one by one.

**Models.** Every subagent (triage, MRI, leads, workers, verifiers, auditors, claims) ran on claude-opus-5-5: 435 transcripts checked. The 80 `<synthetic>` entries are spend-limit stubs from the dead batch-2 loop.

**Commits.** 393c547e LIT · 71517e55 MRI · c21886be · 4879db1d 75bc1c0a 7bc59591 61217e00 c443a564 (batch 1) · 9b4b311b 96bba603 a3ae950c e5b8515e b236cf1b (batch 2) · 5d0e547a d5590232 ae0ee949 6c176d54 943f867c 17d1a09e (batch 3) · 59b5efe4 synonyms · this report.

**Final cases hash:** 58c1d9051e901033df55fc84408230d50ac0d3fedaee748f9f1eb9e31303c122
