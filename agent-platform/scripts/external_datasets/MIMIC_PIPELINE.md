# MIMIC-neuro pipeline: the code that built the 100 MIMIC cases

The `mimic_*` scripts in this folder built the MIMIC-IV neurology cases (task 07, final 100 cases) on CERN
storage. The methods are in `docs/benchmark/mimic-neuro-methods.md`. The code is published because the
PhysioNet DUA asks that the code behind published results be open; the data are not. Every record-derived
input (reader manual files, selections, exclusion and override CSVs, extraction JSONs, the synonyms overlay)
lives in the credentialed workspace and never in this repository.

Before publication, every line of these files was screened by a credentialed session for identifiers, dates,
record text, values and small counts (26 Nov 2026): none carries record content. Two analysis scripts that
held episode-derived rule strings, and four superseded drafts, were left out.

The workspace paths (`/eos/user/a/aprotani/physionet/...`) are hard-coded defaults; change them to rebuild
elsewhere.

## Rebuild order

1. `mimic_pilot_v3.py`: tables (`03_tables.parquet`).
2. `mimic_pilot_v4.py`, then `mimic_pilot_v6.py`: labs, treatments, strict criteria, selection.
3. `mimic_build_case.py`: `extract` and `draft` stages for every case.
4. `mimic_compile4.py`, then `mimic_compile6.py`: case flags and exclusions from the reader decisions.
5. `mimic_manual_grid6.py`, then `mimic_manual_fix7.py`: exam grids and re-read corrections in the manual files.
6. `run06_build.sh`: the build chain (case builder, rejected labels, timing checks, perfect-agent check).
7. `mimic_export7.py`: `07_cases` and `07_selection.csv`.

After a rebuild on a newer master, rerun the perfect-agent check and
`scripts/validation/apply_diagnosis_synonyms.py --check`: `diagnosis_synonyms.yaml` and the prompt rendering
in `harness/context.py` have changed since the cases were built.

## Files

| Role | Files |
|---|---|
| Build | `run06_build.sh`, `mimic_case_build6.py`, `mimic_case_build3.py`, `mimic_case_build.py`, `mimic_case_assemble.py`, `mimic_case_review.py`, `mimic_pilot_v3.py`, `mimic_pilot_v4.py`, `mimic_pilot_v6.py`, `mimic_pilot_cohort.py`, `mimic_note_results.py`, `mimic_treat.py`, `mimic_build_case.py`, `mimic_compile4.py`, `mimic_compile6.py`, `mimic_manual_grid6.py`, `mimic_manual_fix7.py`, `mimic_rejected6.py`, `mimic_case_checks3.py`, `mimic_perfect6.py`, `mimic_export7.py`, `MIMIC_MANUAL_SPEC.md` (manual-file format) |
| Validation and reported numbers | `mimic_pilot_counts6.py` (flow and counts), `REREAD6_PROTOCOL.md`, `mimic_reread6_files.py`, `mimic_reread6_merge.py`, `mimic_reread3.py` (used by `reread6_files`), `mimic_blind_files.py`, `mimic_case_diff7.py`, `mimic_policy_align6.py` |
| Other analyses | `mimic_dx_audit5.py` (task-05 audit of model runs), `mimic_room8.py`, `mimic_room8_tables.py` (task-08 room count), `mimic_screen4.py` (terminal reading aid) |
| Utility | `mimic_access_check.py` (access and integrity of the downloaded files) |

Some scripts print record text to the terminal or write it to their outputs (`mimic_screen4.py`,
`mimic_reread3.py --show`, the reason columns echoed by the pilot scripts): run them
only inside the credentialed workspace.
