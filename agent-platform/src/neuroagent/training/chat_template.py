"""Derive a training chat template with `{% generation %}` markers.

Qwen3.5's shipped chat template renders assistant turns, tool calls and tool responses
correctly, but carries no `{% generation %}` markers. Without them
`apply_chat_template(..., return_assistant_tokens_mask=True)` returns an all-zero mask
and TRL's `assistant_only_loss` cannot isolate assistant tokens.

We patch the template *derived from the tokenizer* rather than vendoring a copy, so it
stays in sync with the model. The markers wrap exactly the assistant response body
(reasoning + content + tool calls + `<|im_end|>`) and exclude the `<|im_start|>assistant`
header, which is a prompt cue the model never generates.

Why this matters: the loss must be computed on the tokens the student generates —
thoughts and actions — never on tool observations. Training on observations teaches the
model to hallucinate lab values instead of calling tools
(Agent Distillation, arXiv:2505.17612; partial masking, arXiv:2505.20023).
"""

from __future__ import annotations

# The assistant-branch block we rewrite, verbatim from Qwen3.5's template. The
# `<|im_start|>assistant\n` header is emitted inside both arms of this if/else, so we
# hoist it out before opening `{% generation %}` — a generation block may not straddle
# an `{% else %}`.
_HEADER_IF = "        {%- if loop.index0 > ns.last_query_index %}"
_HEADER_WITH_THINK = (
    "            {{- '<|im_start|>' + message.role + '\\n<think>\\n' "
    "+ reasoning_content + '\\n</think>\\n\\n' + content }}"
)
_HEADER_ELSE = "        {%- else %}"
_HEADER_PLAIN = "            {{- '<|im_start|>' + message.role + '\\n' + content }}"
_HEADER_ENDIF = "        {%- endif %}"
_TURN_END = "        {{- '<|im_end|>\\n' }}"

_HEADER_BLOCK = [
    _HEADER_IF,
    _HEADER_WITH_THINK,
    _HEADER_ELSE,
    _HEADER_PLAIN,
    _HEADER_ENDIF,
]

_HEADER_BLOCK_PATCHED = [
    "        {{- '<|im_start|>' + message.role + '\\n' }}",
    "        {%- generation %}",
    _HEADER_IF,
    "            {{- '<think>\\n' + reasoning_content + '\\n</think>\\n\\n' + content }}",
    _HEADER_ELSE,
    "            {{- content }}",
    _HEADER_ENDIF,
]

_TURN_END_PATCHED = "        {{- '<|im_end|>' }}{%- endgeneration %}{{- '\\n' }}"


class ChatTemplatePatchError(RuntimeError):
    """Raised when the shipped template no longer matches what we expect to patch."""


def build_training_chat_template(base_template: str) -> str:
    """Insert `{% generation %}` markers around assistant response bodies.

    The `<|im_end|>\\n` emitted for a *tool* turn must not be touched, so we patch only
    inside the assistant branch, which we locate by its unique reasoning-content lines.
    """
    if "generation %}" in base_template.replace("add_generation_prompt", ""):
        if "{%- generation %}" in base_template or "{% generation %}" in base_template:
            return base_template

    lines = base_template.split("\n")

    start = next(
        (
            i
            for i in range(len(lines) - len(_HEADER_BLOCK) + 1)
            if lines[i : i + len(_HEADER_BLOCK)] == _HEADER_BLOCK
        ),
        None,
    )
    if start is None:  # pragma: no cover - guards against a model update
        raise ChatTemplatePatchError(
            "Qwen assistant-branch block not found; the chat template changed. "
            "Re-derive the patch against the new template before training."
        )

    lines[start : start + len(_HEADER_BLOCK)] = _HEADER_BLOCK_PATCHED

    # The assistant branch's own `<|im_end|>` is the first one after the patched header.
    end_idx = next(
        (i for i in range(start + len(_HEADER_BLOCK_PATCHED), len(lines)) if lines[i] == _TURN_END),
        None,
    )
    if end_idx is None:  # pragma: no cover
        raise ChatTemplatePatchError("Assistant-branch '<|im_end|>' emit line not found.")

    lines[end_idx] = _TURN_END_PATCHED

    return "\n".join(lines)


def apply_training_chat_template(tokenizer) -> str:
    """Patch `tokenizer.chat_template` in place and return the new template."""
    if tokenizer.chat_template is None:
        raise ChatTemplatePatchError("Tokenizer has no chat_template to patch.")
    patched = build_training_chat_template(tokenizer.chat_template)
    tokenizer.chat_template = patched
    return patched
