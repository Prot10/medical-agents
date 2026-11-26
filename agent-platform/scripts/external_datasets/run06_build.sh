#!/bin/bash
# Task 06 build pipeline: build the selected cases, expand labels (decision 40), add template rejected labels, timing checks.
set -e
W=/eos/user/a/aprotani/physionet/work/mimic-neuro; export TMPDIR=$W/tmp; export PYTHONHASHSEED=0; cd ~/projects/ma-mimic
S=agent-platform/scripts/external_datasets; P="nice -n 10 $HOME/projects/medical-agents/.venv/bin/python -I"
$P $S/mimic_case_build6.py --out $W/out --selection 06_selection.csv "$@" 2>&1 | grep -v "build errors 0; perfect agent ok" || true
$P agent-platform/scripts/validation/apply_diagnosis_synonyms.py --cases-dir $W/out/06_cases --overlay $W/out/07_synonyms_overlay.yaml --prune | tail -1
uv run -q --no-project --with pandas python -I $S/mimic_rejected6.py --out $W/out
$P agent-platform/scripts/validation/apply_diagnosis_synonyms.py --cases-dir $W/out/06_cases --overlay $W/out/07_synonyms_overlay.yaml --prune --check | head -3
$P $S/mimic_case_checks3.py --out $W/out --tag 06 2>&1 | tail -3
$P $S/mimic_perfect6.py --out $W/out
