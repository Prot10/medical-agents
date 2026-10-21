"""Export completed benchmark episodes as typed episode records.

Records are labeled ``candidate_not_gold`` by default; only the review process may relabel a
record ``physician_approved``.

    uv run python -m neuroagent.training.data.export_episodes \\
        --runs outputs/smoke/policy-qwen outputs/smoke/react-qwen \\
        --output training_data/candidate_episodes.jsonl
"""

from __future__ import annotations

import argparse
from pathlib import Path

from neuroagent_schemas import ClinicalEpisode, RunCompleted, RunStarted

from .episodes import EpisodeRecord


def export(run_dirs: list[Path], output: Path) -> int:
    lines = []
    for run_dir in run_dirs:
        for path in sorted((run_dir / "episodes").glob("*.json")):
            episode = ClinicalEpisode.model_validate_json(path.read_text())
            if not isinstance(episode.events[-1], RunCompleted):
                continue
            started = next(event for event in episode.events if isinstance(event, RunStarted))
            record = EpisodeRecord(
                candidate_id=f"{run_dir.name}/{path.stem}",
                case_id=started.case_id,
                label="candidate_not_gold",
                provenance={"profile_id": started.profile_id, "model_id": started.model_id, "run_dir": str(run_dir)},
                episode=episode,
            )
            lines.append(record.model_dump_json())
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(line + "\n" for line in lines))
    return len(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", nargs="+", required=True, type=Path, help="benchmark output directories")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(f"exported {export(args.runs, args.output)} candidate episodes to {args.output}")


if __name__ == "__main__":
    main()
