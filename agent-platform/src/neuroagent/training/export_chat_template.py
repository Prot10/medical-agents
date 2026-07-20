"""Write the think-preserving training chat template to disk, for the eval server.

Multi-turn GRPO renders with TRL's Qwen3.5 TRAINING chat template, because the shipped
(inference) template strips `<think>` from any assistant turn a user message follows — which
deletes the policy's own reasoning from its context and breaks append-only token
concatenation. Serving the trained policy under the shipped template would therefore evaluate
it on contexts it never saw during training.

    python -m neuroagent.training.export_chat_template --output results/qwen3_5_training.jinja
    CHAT_TEMPLATE=results/qwen3_5_training.jinja bash scripts/runtime/serve_model.sh qwen3.5-4b
"""

from __future__ import annotations

import argparse
import logging
import sys

from .train_grpo import export_training_chat_template


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="results/chat_templates/qwen3_5_think_training.jinja",
        help="Where to write the template (pass this file to vLLM via --chat-template)",
    )
    args = parser.parse_args()

    path = export_training_chat_template(args.output)
    if path is None:
        print(
            "No Qwen3.5 training chat template available in this TRL install — upgrade to "
            "trl>=1.8, or serve with the shipped template AND train with reflection disabled.",
            file=sys.stderr,
        )
        return 1
    print(f"\n  wrote {path}\n  serve with: CHAT_TEMPLATE={path} bash "
          f"agent-platform/scripts/runtime/serve_model.sh <model>\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
