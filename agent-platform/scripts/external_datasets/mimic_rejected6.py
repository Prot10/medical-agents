"""Task 06 (decision 40 follow-up): the repository's diagnosis_synonyms.yaml grants no `rejected`
labels for any code, so apply_diagnosis_synonyms adds none. Each NeuroBench template case writes its
own rejected labels. This adds to every selected MIMIC case the rejected labels that at least half of
its condition's NeuroBench cases carry, unless a label shares its token set with an accepted label
(either way) or any sentence of the case's own discharge note names it (all its words in one sentence,
or the abbreviation as a word): a label the record itself raises is never vetoed. Records the source
in metadata and recomputes the list from scratch (template-derived labels are replaced each run). Run AFTER apply_diagnosis_synonyms; idempotent.
No record content in this file.

    python -I mimic_rejected6.py --out $W/out --selection 06_selection.csv
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
COND = {"ischemic_stroke": "ISCH", "subarachnoid_hemorrhage": "SAH", "status_epilepticus": "SE", "guillain_barre": "GBS",
        "multiple_sclerosis": "MS", "focal_epilepsy_temporal": "FEPI", "hepatic_encephalopathy": "HEP",
        "functional_neurological_disorder": "FND", "bacterial_meningitis": "BACT", "syncope_cardiac": "SYNC", "brain_tumor_glioma": "GLIO"}
tok = lambda s: set(re.sub(r"[^a-z0-9]+", " ", s.lower()).split())


def template_rejected(cond: str, frac: float = 0.5) -> list[str]:
    files = sorted((ROOT / "data/neurobench/cases").glob(f"{cond}-*.json"))
    c = collections.Counter()
    for f in files:
        c.update({x.lower() for x in json.loads(f.read_text())["ground_truth"]["diagnosis"].get("rejected", [])})
    return sorted(k for k, v in c.items() if v >= len(files) * frac)


# Decision 48 (task 07): SE also rejects its main clinical mimics, with the label strings the repository already uses
# (diagnosis_synonyms.yaml functional-seizure entries; NeuroBench syncope labels).
REMOVALS: dict = {}
MIMICS = {"SE": ["psychogenic nonepileptic seizures", "PNES", "functional seizures", "dissociative seizures", "nonepileptic seizures",
                 "convulsive syncope", "vasovagal syncope", "reflex syncope"]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--selection", default="06_selection.csv")
    a = ap.parse_args()
    out = Path(a.out)
    sel = pd.read_csv(out / a.selection)
    sel = sel[sel.case_id.notna() & (sel.case_id != "") & (sel.exclusion.isna() | (sel.exclusion == ""))]
    rf = out / "07_rejected_removals.json"
    REMOVALS.update(json.loads(rf.read_text()) if rf.exists() else {})
    cache, n_add, n_skip, n_d48 = {}, collections.Counter(), collections.Counter(), collections.Counter()
    for cid in sel.case_id:
        p = out / "06_cases" / f"{cid}.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        cond = COND[d["condition"]]
        rej = cache.setdefault(cond, template_rejected(cond))
        dx = d["ground_truth"]["diagnosis"]
        acc = [tok(x) for x in dx["accepted"]]
        note = json.loads((out / "02_source" / f"{cid}.json").read_text())["discharge"][0]["text"]
        sents = [tok(x) for x in re.split(r"(?<=[.;:\n])\s+", note.lower()) if x.strip()]
        named = lambda r: any(tok(r) - {"disease", "syndrome"} <= s_ for s_ in sents)
        ok = lambda r: not any(tok(r) <= a_ or a_ <= tok(r) for a_ in acc) and not named(r)
        removals = {x.lower() for x in REMOVALS.get(cid, {}).get("labels", [])}  # task 07: case-level corrections from the re-read
        ok = lambda r, ok0=ok: ok0(r) and r.lower() not in removals
        keep = [r for r in rej if ok(r)]
        n_skip[cond] += len(rej) - len(keep)
        if not keep:  # decision 48: the 50 % rule gives none for this case -> one third of the templates, plus the condition's mimics
            keep = [r for r in template_rejected(cond, 1 / 3) if ok(r)]
            keep += [r for r in MIMICS.get(cond, []) if ok(r) and r.lower() not in {k.lower() for k in keep}]
            d["metadata"]["rejected_labels_rule"] = "decision 48: one third of the condition's templates, plus its main clinical mimics"
            n_d48[cond] += 1
        prev = d["metadata"].get("rejected_from_templates", [])
        base = [x for x in dx.get("rejected", []) if x not in prev]
        dx["rejected"] = base + keep
        d["metadata"]["rejected_from_templates"] = keep
        n_add[cond] += len(keep)
        d["metadata"]["rejected_labels_source"] = ("labels rejected in >= half of the condition's NeuroBench cases "
                                                   "(diagnosis_synonyms.yaml grants no rejected labels)")
        p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n")
    print("template rejected labels per condition:", {k: len(v) for k, v in cache.items()}, "| added (label x case):", dict(n_add),
          "| skipped because the case's note names them:", dict(n_skip), "| decision-48 cases:", dict(n_d48))
    no = [c for c in sel.case_id if (out / "06_cases" / f"{c}.json").exists()
          and not json.loads((out / "06_cases" / f"{c}.json").read_text())["ground_truth"]["diagnosis"].get("rejected")]
    print("cases without any rejected label:", len(no), collections.Counter(c.split("-")[1] for c in no))


if __name__ == "__main__":
    main()
