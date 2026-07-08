"""Batch-generate gold trajectories for all NeuroBench cases.

Processes cases sequentially using Claude API via the Anthropic SDK.
Reads prompts from the prepared prompts directory, generates trajectories,
and saves raw outputs to raw_v2/.

Usage:
    # Defaults read $TRAINING_DATA_ROOT/gold_trajectories_v5/{prompts,raw_v2}
    # (TRAINING_DATA_ROOT defaults to /eos/.../NeuroAgent/training_data).
    uv run python scripts/training/batch_generate_trajectories.py \
        --styles minimal_efficient cost_conscious \
        --max-cases 200

    # Local override for fast iteration:
    TRAINING_DATA_ROOT=./training_data \
        uv run python scripts/training/batch_generate_trajectories.py ...
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import time
from pathlib import Path

import anthropic

logger = logging.getLogger(__name__)

# Where generated trajectory artefacts live. Defaults to EOS so a fresh clone
# can pull them via filesystem instead of git; override via env var for local
# iteration (TRAINING_DATA_ROOT=./training_data ...).
TRAINING_DATA_ROOT = os.environ.get(
    "TRAINING_DATA_ROOT",
    "/eos/project-d/diagbox/dvc/NeuroAgent/training_data",
)

BUDGET_INSTRUCTION = """CRITICAL CONSTRAINT: The total output must be SHORT — roughly 3000-4000 tokens (~12,000-16,000 characters). This is a hard budget.

Key rules:
- <think> blocks: 2-4 sentences MAX. State differential update + why this test + what you expect.
- <tool_response> blocks: ONLY abnormal/significant findings. Omit all normal values, null fields.
- Final assessment: 1-2 sentences per section. Be direct and clinical.
- 3-5 tool calls maximum.

Output ONLY the ReAct trace — no preamble, no commentary."""


def generate_trajectory(
    client: anthropic.Anthropic,
    prompt_path: Path,
    model: str = "claude-sonnet-4-20250514",
) -> str | None:
    """Generate a single trajectory using the Anthropic API."""
    prompt_text = prompt_path.read_text()

    try:
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt_text}\n\n{BUDGET_INSTRUCTION}",
                }
            ],
        )
        return response.content[0].text
    except anthropic.APIError as e:
        logger.error("API error for %s: %s", prompt_path.name, e)
        return None
    except Exception as e:
        logger.error("Error for %s: %s", prompt_path.name, e)
        return None


def main():
    parser = argparse.ArgumentParser(description="Batch generate gold trajectories")
    parser.add_argument(
        "--prompts-dir",
        default=f"{TRAINING_DATA_ROOT}/gold_trajectories_v5/prompts",
    )
    parser.add_argument(
        "--output-dir",
        default=f"{TRAINING_DATA_ROOT}/gold_trajectories_v5/raw_v2",
    )
    parser.add_argument("--styles", nargs="+", default=["minimal_efficient", "cost_conscious"])
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument("--model", default="claude-sonnet-4-20250514")
    parser.add_argument("--skip-existing", action="store_true", default=True)
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    prompts_dir = Path(args.prompts_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all prompts
    prompt_files = sorted(prompts_dir.glob("*.txt"))
    logger.info("Found %d prompt files", len(prompt_files))

    # Filter by style
    prompt_files = [
        f for f in prompt_files
        if any(f.stem.endswith(f"_{s}") for s in args.styles)
    ]
    logger.info("After style filter: %d prompts", len(prompt_files))

    # Skip existing
    if args.skip_existing:
        existing = {f.stem for f in output_dir.glob("*.txt")}
        prompt_files = [f for f in prompt_files if f.stem not in existing]
        logger.info("After skipping existing: %d prompts to generate", len(prompt_files))

    if args.max_cases:
        # Limit to max_cases unique case IDs
        seen_cases = set()
        filtered = []
        for f in prompt_files:
            # Extract case_id (everything before last _style)
            for style in args.styles:
                if f.stem.endswith(f"_{style}"):
                    case_id = f.stem[: -len(f"_{style}")]
                    break
            else:
                continue
            if case_id not in seen_cases or len(seen_cases) <= args.max_cases:
                seen_cases.add(case_id)
                if len(seen_cases) <= args.max_cases:
                    filtered.append(f)
        prompt_files = filtered
        logger.info("After max_cases=%d limit: %d prompts", args.max_cases, len(prompt_files))

    if args.dry_run:
        for f in prompt_files[:10]:
            print(f"  Would generate: {f.stem}")
        print(f"  ... and {len(prompt_files) - 10} more")
        return

    # Generate
    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var
    total = len(prompt_files)
    success = 0
    failed = 0

    for i, prompt_file in enumerate(prompt_files):
        logger.info("[%d/%d] Generating %s...", i + 1, total, prompt_file.stem)
        t0 = time.time()

        text = generate_trajectory(client, prompt_file, model=args.model)
        elapsed = time.time() - t0

        if text:
            output_path = output_dir / f"{prompt_file.stem}.txt"
            output_path.write_text(text)
            success += 1
            logger.info(
                "  OK: %d chars, %.1fs", len(text), elapsed,
            )
        else:
            failed += 1
            logger.warning("  FAILED")

        # Rate limiting — be gentle
        if elapsed < 2.0:
            time.sleep(2.0 - elapsed)

    logger.info("Done. %d/%d success, %d failed", success, total, failed)


if __name__ == "__main__":
    main()
