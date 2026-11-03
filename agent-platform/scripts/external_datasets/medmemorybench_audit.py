"""Per-persona fit of MedMemoryBench to the NeuroBench case format.

For each of the 20 English personas, finds the diagnostic window (events before the
first treatment start), the diagnostic studies mentioned in it, and which NeuroBench
tool each study would map to. Writes one row per persona.

    uv run --no-project --with pandas --with pyarrow python -I \
        agent-platform/scripts/external_datasets/medmemorybench_audit.py \
        data/external/medmemorybench/data/en outputs/external_datasets/medmemorybench.csv
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

# Study keyword -> NeuroBench tool it would be served by.
STUDY_TOOLS = {
    r"\bMRI\b": "analyze_brain_mri",
    r"\bCT\b|computed tomography": "order_ct_scan",
    r"\bEEG\b": "analyze_eeg",
    r"\bECG\b|electrocardiogram|Holter": "analyze_ecg",
    r"cerebrospinal|\bCSF\b|lumbar puncture": "analyze_csf",
    r"DAT.?SPECT|\bPET\b|SPECT": "order_advanced_imaging",
    r"echocardiog": "order_echocardiogram",
    r"EMG|nerve conduction|polysomnograph|spirometr|FEV1|biopsy|genetic": "order_specialized_test",
    r"UPDRS|MMSE|MoCA|PHQ-9|GAD-7|neurological exam": "perform_clinical_assessment",
    r"HbA1c|eGFR|TSH|FT3|FT4|CRP|ESR|ALT|blood test|NT-proBNP|potassium|creatinine": "interpret_labs",
}
NEURO = {7, 8}
TREATMENT = re.compile(r"\b(start|initiat|prescrib)\w*[^.]{0,80}\b(mg|insulin|therapy|tablet|medication|regimen)\b", re.IGNORECASE)


def main(src: Path, out: Path) -> None:
    personas = pd.read_parquet(src / "personas.parquet")
    events = pd.read_parquet(src / "events.parquet")
    rows = []
    for _, p in personas.iterrows():
        ev = events[(events.persona_id == p.persona_id) & (events.type == "health")].sort_values(
            "event_date"
        )
        first_tx = next(
            (r.event_date for r in ev.itertuples() if TREATMENT.search(str(r.event))), None
        )
        window = ev[ev.event_date <= first_tx] if first_tx else ev.head(0)
        text = " ".join(window.event.astype(str))
        tools = sorted({t for pat, t in STUDY_TOOLS.items() if re.search(pat, text, re.IGNORECASE)})
        rows.append(
            {
                "persona_id": p.persona_id,
                "type_name": p.type_name,
                "neuro_primary": p.persona_id in NEURO,
                "diagnostic_window_events": len(window),
                "first_treatment": first_tx,
                "tools_in_window": ";".join(tools),
                "n_tools": len(tools),
            }
        )
    df = pd.DataFrame(rows)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(df.to_string(index=False, max_colwidth=60))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
