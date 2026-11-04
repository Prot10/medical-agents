"""The catalogue's prose says what a study measures, never which disease it is for.

The policy loop advertises the same catalogue in every case, so its descriptions are read before
the first tool call of all 600 episodes. Until 4 Nov 2026 they had been written against the 20
NeuroBench conditions: the tap test of NPH, the teratoma of anti-NMDAR encephalitis, the glioma
molecular algorithm, the functional disorder, syncope. `scripts/paper/catalogue_cue.py` measured
the effect with the model forced to answer on its first turn: removing every description changed
the diagnosis rate of the NPH, glioma and FND cases, so the prose was a menu of answers
(docs/paper/catalogue-cue.md). The descriptions were rewritten to method, specimen and output.

This test keeps them that way. It scans every description the model receives — tool and parameter
— for the names of the benchmark's conditions and their defining associations. Enum members quoted
in the prose ('ms', 'dementia', `paraneoplastic_panel`) are names of orderable terms, not prose,
and are skipped: the vocabulary is the subject of the differential-completeness work, not of this
rule. Diseases outside the benchmark that name what a test reports (a type 1 Brugada pattern, long
QT genes) are allowed.
"""

from __future__ import annotations

import re

import pytest

from neuroagent.tools.tool_registry import ToolRegistry

# The 20 conditions, their usual abbreviations and the associations that point at one of them.
_CONDITION_TERMS = re.compile(
    r"amyotrophic|motor neuron|\bALS\b|alzheimer|dementia|meningit|meningococc|epilep|seizure|"
    r"functional (neurological )?disorder|frontotemporal|\bFTD\b|guillain|\bGBS\b|polyradicul|"
    r"gliom|glioblastom|tumou?r|neoplas|malignan|metasta|melanoma|lymphoma|hepatic|cirrho|"
    r"encephalopath|stroke|isch(a)?em|infarct|thromb(oly|ectomy)|migrain|\baura\b|"
    r"multiple sclerosis|\bMS\b|optic neuritis|demyelin|NMDAR|encephalitis|teratoma|"
    r"paraneoplastic|myasthen|\bMG\b|thym|hydroceph|\bNPH\b|tap test|parkinson|\bPD\b|\bMSA\b|"
    r"lewy|\bDBS\b|subarachnoid|aneurysm|vasospasm|ha?emorrhage|syncope|loss of consciousness|"
    r"small.vessel|prion|giant cell|arteritis|cryptogenic|aphasia|hyposmia|myelitis|"
    r"cord compression",
    re.IGNORECASE,
)
_QUOTED_TERM = re.compile(r"'[^']*'|`[^`]*`|\{[^}]*\}")


def _descriptions(node, path: str = ""):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "description" and isinstance(value, str):
                yield path or "<tool>", value
            else:
                yield from _descriptions(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for item in node:
            yield from _descriptions(item, path)


@pytest.fixture(scope="module")
def catalogue() -> list[dict]:
    return ToolRegistry.create_default_registry().get_all_definitions()


def test_no_description_names_a_benchmark_condition(catalogue):
    hits = []
    for tool in catalogue:
        function = tool["function"]
        for path, text in _descriptions(function):
            prose = _QUOTED_TERM.sub("", text)
            hits += [f"{function['name']} {path}: {match.group(0)!r}" for match in _CONDITION_TERMS.finditer(prose)]
    assert not hits, "\n".join(hits)


def test_the_scan_sees_the_old_prose():
    # The rule would pass vacuously if the pattern or the quote stripping were wrong.
    old = (
        "'gait_and_balance_timed': Timed Up and Go and timed walk; run before and after a CSF tap "
        "test in suspected NPH. 'mediastinum_CT'/'_MRI': thymic hyperplasia or thymoma in myasthenia"
    )
    found = {match.group(0).lower() for match in _CONDITION_TERMS.finditer(_QUOTED_TERM.sub("", old))}
    assert {"tap test", "nph", "thym", "myasthen"} <= found
    assert not _CONDITION_TERMS.search(_QUOTED_TERM.sub("", "'ms': sagittal FLAIR. 'dementia': volumetric."))
