# Criteria pack: {CONDITION}

**ICD-10:** {code(s)}
**Condition enum:** `NeurologicalCondition.{NAME}`
**Case ID prefix:** `{prefix}`

---

## 1. Diagnostic criteria

{Canonical criteria — be specific enough that an agent can recognize the
condition from realistic tool outputs. Reference at least one citation tag
from the allow-list below.}

## 2. Standard workup hierarchy

These tier assignments are the **defaults** for a typical case. Cases with
atypical features may shift a tool up or down a tier (the authoring agent
decides per-case, citing why).

**Required (REQUIRED tier — must be called):**
- `tool_name` (`tool_parameters`) — rationale [cite]

**Recommended (RECOMMENDED tier — expected workup hygiene):**
- `tool_name` (`tool_parameters`) — rationale [cite]

**Optional (OPTIONAL tier — defensible if performed):**
- `tool_name` (`tool_parameters`) — rationale [cite]

## 3. Tools that are typically USELESS for this condition

Tools the agent should NOT call for a typical case of this condition (no
clinical justification + non-trivial cost). Per-case overrides allowed when
comorbidities create a separate indication.

- `tool_name` — why useless [cite]

## 4. Tools that are HARMFUL / contraindicated

Rare — populate only when there's a real safety concern (contrast in renal
failure, LP before imaging in mass effect, etc.).

- `tool_name` — why harmful [cite]

## 5. Sequence constraints

Only authored when ordering is clinically load-bearing.

- `before_tool` → `after_tool` (`hard`/`soft`): reason [cite]

## 6. Subtype variations (M/S/P/R)

Standard subtype suffixes: M=mild, S=standard, P=progressive/severe,
R=reverse (reversible mimic / red-herring case). Note tools that move
between tiers for each subtype.

- **M:** {deviation, if any}
- **S:** standard workup
- **P:** {deviation — usually adds tools or shifts to higher tier}
- **R:** {deviation — usually expands differential / adds rule-out tools}

## 7. Common red-herring categories

The kinds of distractors typically embedded in cases of this condition.
The fleet uses this when authoring `red_herrings[]` entries.

- **Category name:** description of how it misleads.

## 8. Allowed citations

The fleet may cite ONLY these references. Anything else is rejected by the
post-fleet validator.

- `[cite_tag_1]` — full citation
- `[cite_tag_2]` — full citation
- (3–8 entries per pack)
