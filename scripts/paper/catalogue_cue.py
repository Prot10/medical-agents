"""How much the tool catalogue alone tells the model the diagnosis (paper evidence).

The policy loop advertises the same 16-tool catalogue in every case. Its enum terms and its prose
were written for the 20 NeuroBench conditions, so the catalogue could act as a menu of answers. This
script measures that cue: the model must submit on its first turn (no tool can be called), and only
what the request advertises changes between variants. The policy system prompt is the same in all
of them; the narrative profile, whose prompt says no tests exist, is the reference without either.

    # one variant × seed against a served model (engineering: draft policies)
    uv run python scripts/paper/catalogue_cue.py run --variant catalogue --seed 1 \
        --output outputs/paper/catalogue_cue/catalogue-s1 -- --all --concurrency 16 --allow-draft-policies
    # aggregate: per condition, paired over cases, mean over seeds, bootstrap 95% CI
    uv run python scripts/paper/catalogue_cue.py report outputs/paper/catalogue_cue \
        --compare catalogue:no-catalogue --compare no-prose:no-catalogue

Variants (all on the checked profile ``policy-<model>`` with ``max_turns`` 1, except ``narrative``):

- ``catalogue``: the catalogue as advertised;
- ``no-prose``: every description removed (tool and parameter), names, types and enums kept, so the
  difference to ``catalogue`` is the cue carried by the prose;
- ``no-catalogue``: only ``submit_assessment``;
- ``drop``: the catalogue with the enum members given by ``--drop`` removed (term ablation);
- ``narrative``: the ``narrative-<model>`` profile (no catalogue, its own system prompt).

``report`` reads every run directory below the root whose ``variant.json`` it finds. Each run is a
normal benchmark output (``rewards.jsonl``, ``summary.json``, ``episodes/``).
"""

from __future__ import annotations

import argparse
import copy
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

VARIANTS = ("catalogue", "no-prose", "no-catalogue", "drop", "narrative")


def strip_prose(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The catalogue without any description: names, types, enums and required fields remain."""

    def walk(node: Any) -> Any:
        if isinstance(node, dict):
            return {key: walk(value) for key, value in node.items() if key not in ("description", "title")}
        if isinstance(node, list):
            return [walk(item) for item in node]
        return node

    return [
        {**tool, "function": {key: walk(value) for key, value in tool["function"].items() if key != "description"}}
        for tool in tools
    ]


def drop_terms(tools: list[dict[str, Any]], terms: set[str]) -> list[dict[str, Any]]:
    """The catalogue with the given enum members removed; the prose is left as it is."""
    tools = copy.deepcopy(tools)

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("enum"), list):
                node["enum"] = [value for value in node["enum"] if value not in terms]
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(tools)
    return tools


def run(args: argparse.Namespace, benchmark_args: list[str]) -> None:
    import neuroagent.evaluation.benchmark as bench
    from neuroagent.harness import loops

    if args.variant == "narrative":
        profile = f"narrative-{args.model}"
    else:
        profile = f"policy-{args.model}"
        load = bench.load_profiles
        bench.load_profiles = lambda directory: {
            key: value.model_copy(update={"max_turns": 1}) for key, value in load(directory).items()
        }
        terms = set(args.drop)
        if args.variant == "drop" and not terms:
            raise SystemExit("--variant drop needs --drop TERM ...")

        def catalogue(context) -> list[dict[str, Any]]:
            tools = context.environment.tool_definitions()
            if args.variant == "no-catalogue":
                return []
            if args.variant == "no-prose":
                return strip_prose(tools)
            if args.variant == "drop":
                return drop_terms(tools, terms)
            return tools

        loops.ClinicalPolicyLoop._catalogue = staticmethod(catalogue)

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "variant.json").write_text(
        json.dumps({"variant": args.variant, "seed": args.seed, "model": args.model, "drop": sorted(args.drop),
                    "profile": profile}, indent=2)
    )
    bench.main(["--profile", profile, "--output", str(args.output), "--seed", str(args.seed), *benchmark_args])


def load_runs(root: Path) -> dict[str, dict[int, dict[str, dict]]]:
    """variant label -> seed -> case_id -> reward row."""
    runs: dict[str, dict[int, dict[str, dict]]] = defaultdict(dict)
    for meta_path in sorted(root.rglob("variant.json")):
        meta = json.loads(meta_path.read_text())
        rewards = meta_path.parent / "rewards.jsonl"
        if not rewards.exists():
            continue
        label = meta["variant"] + ("[" + ",".join(meta["drop"]) + "]" if meta.get("drop") else "")
        rows = [json.loads(line) for line in rewards.read_text().splitlines() if line.strip()]
        runs[label][meta["seed"]] = {row["case_id"]: row for row in rows}
    return runs


def per_case(seeds: dict[int, dict[str, dict]], metric: str) -> dict[str, float]:
    """Mean of the metric over the seeds of one variant, per case; a failed episode scores 0."""
    values: dict[str, list[float]] = defaultdict(list)
    for rows in seeds.values():
        for case_id, row in rows.items():
            values[case_id].append(float((row.get("reward") or {}).get(metric, 0.0)))
    return {case_id: statistics.mean(v) for case_id, v in values.items()}


def bootstrap(diffs: list[float], rng: random.Random, draws: int = 4000) -> tuple[float, float]:
    means = sorted(statistics.mean(rng.choices(diffs, k=len(diffs))) for _ in range(draws))
    return means[int(0.025 * draws)], means[int(0.975 * draws) - 1]


def report(args: argparse.Namespace) -> None:
    runs = load_runs(args.root)
    if not runs:
        raise SystemExit(f"no run with a variant.json below {args.root}")
    print("runs: " + "; ".join(f"{label} seeds {sorted(seeds)}" for label, seeds in sorted(runs.items())))
    condition: dict[str, str] = {}
    for seeds in runs.values():
        for rows in seeds.values():
            condition.update({case_id: row["condition"] for case_id, row in rows.items()})
    means = {label: per_case(seeds, args.metric) for label, seeds in runs.items()}
    rng = random.Random(0)
    summary: dict[str, Any] = {"metric": args.metric, "variants": {}, "comparisons": {}}
    for label, values in means.items():
        by_condition: dict[str, list[float]] = defaultdict(list)
        for case_id, value in values.items():
            by_condition[condition[case_id]].append(value)
        summary["variants"][label] = {
            "seeds": sorted(runs[label]),
            "overall": statistics.mean(values.values()),
            "by_condition": {c: statistics.mean(v) for c, v in sorted(by_condition.items())},
        }
    for spec in args.compare:
        a, b = spec.split(":")
        if a not in means or b not in means:
            print(f"skip {spec}: missing variant")
            continue
        shared = sorted(set(means[a]) & set(means[b]))
        diffs: dict[str, list[float]] = defaultdict(list)
        for case_id in shared:
            diffs[condition[case_id]].append(means[a][case_id] - means[b][case_id])
        everything = [d for values in diffs.values() for d in values]
        rows = {
            c: {"n": len(v), "a": statistics.mean(means[a][i] for i in shared if condition[i] == c),
                "b": statistics.mean(means[b][i] for i in shared if condition[i] == c),
                "diff": statistics.mean(v), "ci95": bootstrap(v, rng)}
            for c, v in diffs.items()
        }
        overall = {"n": len(everything), "diff": statistics.mean(everything), "ci95": bootstrap(everything, rng)}
        summary["comparisons"][spec] = {"overall": overall, "by_condition": rows}
        print(f"\n{a} - {b}  ({args.metric}, {len(shared)} cases, mean over seeds per case, bootstrap 95% CI)")
        print(f"{'condition':34} {'n':>3} {a[:10]:>10} {b[:10]:>10} {'diff':>7}  95% CI")
        for c, r in sorted(rows.items(), key=lambda item: -item[1]["diff"]):
            lo, hi = r["ci95"]
            flag = " *" if lo > 0 or hi < 0 else ""
            print(f"{c:34} {r['n']:>3} {r['a']:>10.3f} {r['b']:>10.3f} {r['diff']:>+7.3f}  [{lo:+.3f}, {hi:+.3f}]{flag}")
        lo, hi = overall["ci95"]
        print(f"{'all':34} {overall['n']:>3} {'':>10} {'':>10} {overall['diff']:>+7.3f}  [{lo:+.3f}, {hi:+.3f}]")
    if args.json:
        args.json.write_text(json.dumps(summary, indent=2))


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    benchmark_args: list[str] = []
    if "--" in argv:
        split = argv.index("--")
        argv, benchmark_args = argv[:split], argv[split + 1 :]
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run", help="one variant and seed; benchmark arguments follow --")
    run_parser.add_argument("--variant", choices=VARIANTS, required=True)
    run_parser.add_argument("--seed", type=int, required=True)
    run_parser.add_argument("--model", default="qwen3.5-9b")
    run_parser.add_argument("--drop", nargs="*", default=[], help="enum members removed by --variant drop")
    run_parser.add_argument("--output", type=Path, required=True)
    report_parser = sub.add_parser("report", help="aggregate the runs below a directory")
    report_parser.add_argument("root", type=Path)
    report_parser.add_argument("--metric", default="diagnosis")
    report_parser.add_argument("--compare", action="append", default=[], metavar="A:B")
    report_parser.add_argument("--json", type=Path)
    args = parser.parse_args(argv)
    if args.command == "run":
        run(args, benchmark_args)
    else:
        report(args)


if __name__ == "__main__":
    main()
