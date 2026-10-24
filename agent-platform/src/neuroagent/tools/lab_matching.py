"""Which stored laboratory panels answer an `interpret_labs` order (24 Oct 2026).

A case stores its first-line laboratory results as one payload (`initial_tool_outputs.labs`),
named in free text: `"Complete blood count"`, `"Chemistry (CMP)"`, `"Baseline workup"`. The
MockServer used to serve the whole payload to the first order, whatever it named, so a
second-tier result stored there (MS-RR's AQP4/MOG-IgG) reached a basic-labs order, and an order for
an assay the case does not store got the first-line labs back. This module decides, panel by
panel, which stored panels answer which ordered assays.

An ordered assay is a vocabulary term (`normalize_analyte`). Its components are the row tests the
benchmark library reports for it (`FallbackLibrary.analyte_tests`: CBC is WBC, haemoglobin,
platelets, ...), plus the term itself. A stored panel answers the assay when

* one of its rows is a component of the assay (every informative token of the component appears
  in the row test), or
* its name is the assay (`"Thyroid function"` for `thyroid`, `"Complete blood count"` for `CBC`).

Assays whose components are specimen-specific (urinalysis, blood gas, BAL, protein
electrophoresis) are answered by name only: a serum glucose row is not the urine dipstick's.

Comparison is on tokens after spelling normalisation (`_PHRASES`): abbreviations and British
spellings (`Hb`, `haemoglobin`), and multi-word names that would otherwise collide on one word
(`lactate dehydrogenase` is LDH, not lactate; `creatine kinase` is CK, not creatinine).
"""

from __future__ import annotations

import re
from typing import Callable, Iterable

from .vocabulary import analyte_class_members, normalize_analyte

# Applied in order to the lower-cased text before tokenising.
_PHRASES: tuple[tuple[str, str], ...] = (
    (r"haem", "hem"), (r"\burinary\b", "urine"), (r"\b24[- ]?(?:hours?|hr|h)\b", "24h"), (r"oestr", "estr"), (r"leucocyt", "leukocyt"),
    (r"lactate dehydrogenase", "ldh"), (r"creatine (?:phospho)?kinase", "ck"), (r"\bcpk\b", "ck"),
    (r"c[- ]reactive protein", "crp"), (r"(?:erythrocyte )?sedimentation rate|\bsed rate", "esr"),
    (r"white (?:blood )?cells?(?: count)?|\bwbc count|\bleukocytes?\b", "wbc"),
    (r"red (?:blood )?cells?(?: count)?", "rbc"),
    (r"alkaline phosphatase", "alp"), (r"thyroid[- ]stimulating hormone|thyrotropin", "tsh"),
    (r"thyroid peroxidase|\btpo\b", "tpo"), (r"\bft4\b|free thyroxine|thyroxine,? free|t4,? free", "free t4"),
    (r"\bft3\b|free triiodothyronine|t3,? free", "free t3"),
    (r"partial thromboplastin(?: time)?|\bptt\b", "aptt"), (r"prothrombin time", "pt"),
    (r"international normali[sz]ed ratio", "inr"),
    (r"blood urea nitrogen|\burea\b", "bun"),
    (r"hemoglobin a1c|glycated hemoglobin|glycosylated hemoglobin|\bhba1c\b|\ba1c\b", "hba1c"),
    (r"vitamin b[- ]?12|cobalamin|\bb[- ]12\b", "b12"), (r"vitamin b[- ]?1\b|thiamine?", "thiamine"),
    (r"folic acid", "folate"), (r"\bhgb\b|\bhb\b", "hemoglobin"), (r"\bhct\b", "hematocrit"),
    (r"\bplts?\b|platelet count", "platelets"),
    (r"\bbicarb\b|\btotal co2\b|\bco2\b|\bhco3\b", "bicarbonate"),
    (r"\bna\b", "sodium"), (r"\bk\b", "potassium"), (r"\bcl\b", "chloride"), (r"\bmg\b", "magnesium"),
    (r"\bphos\b|phosphorus", "phosphate"), (r"\bcr\b|\bcreat\b", "creatinine"),
    (r"\bglu\b", "glucose"), (r"\balb\b", "albumin"), (r"\bt\.? ?bili\b", "bilirubin"),
    (r"\bsgot\b", "ast"), (r"\bsgpt\b", "alt"), (r"gamma[- ]?glutamyl ?transferase|\bggt\b", "ggt"),
    (r"(?:beta|b|β)[- ]?h?cg\b|\bhcg\b|human chorionic gonadotropin", "hcg"),
    (r"\bnmdar\b|\bglun1\b|nmda[- ]receptor|n-methyl-d-aspartate receptor", "nmda receptor"),
    (r"aquaporin[- ]?4|\baqp4\b", "aqp4"), (r"myelin oligodendrocyte glycoprotein", "mog"),
    (r"acetylcholine receptor|\bachr\b", "achr"), (r"\bammonium\b|\bnh3\b", "ammonia"),
    (r"methylmalonic acid", "mma"), (r"\bosmolarity\b", "osmolality"),
    (r"human immunodeficiency virus", "hiv"), (r"\btroponin [it]\b|\bhs-?tn[it]\b|\btn[it]\b", "troponin"),
    (r"procalcitonin|\bpct\b", "procalcitonin"), (r"lactic acid", "lactate"),
    (r"valproic acid", "valproate"), (r"(?:urine |serum )?(?:drug|toxicology) screen|\btoxicology\b", "tox"),
    (r"(?:blood|serum) alcohol|\balcohol level", "ethanol"), (r"ceruloplasmin|caeruloplasmin", "ceruloplasmin"),
)

_STOP = frozenset({
    "serum", "plasma", "total", "level", "levels", "test", "tests", "assay", "cell", "based",
    "quantitative", "qualitative", "random", "fasting", "whole", "the", "of", "and", "or", "with",
    "antibody", "antibodies", "ab", "anti", "panel", "panels", "profile", "screen", "screening",
    "function", "studies", "study", "count", "concentration", "measurement", "value", "result",
    "results", "markers", "marker", "absolute", "calculated", "differential", "diff", "baseline",
    "workup", "venous", "arterial", "in", "on", "at", "for", "a", "an", "s", "ml", "dl", "l",
})

# Name-only assays: their component rows are specimen tests that a serum row would satisfy.
_SCOPED = frozenset({normalize_analyte(name) for name in (
    "urinalysis", "ABG", "BAL", "SPEP", "IFE", "peripheral smear",
)})

# Stored panel names that are the assay under another name (normalised assay -> name tokens).
_NAME_ALIASES: dict[str, tuple[frozenset[str], ...]] = {
    normalize_analyte(assay): tuple(frozenset(names.split()) for names in spellings)
    for assay, spellings in {
        "CBC": ("complete blood", "hematology", "full blood"),
        "CMP": ("comprehensive metabolic", "chemistry cmp"),
        "BMP": ("basic metabolic", "electrolytes", "renal"),
        "LFTs": ("liver", "hepatic", "lft", "lfts"),
        "coagulation": ("coagulation", "coag", "clotting"),
        "thyroid": ("thyroid",),
        "lipid_panel": ("lipid", "lipids"),
        "inflammatory_markers": ("inflammatory",),
        "tox_screen": ("toxicology", "tox"),
        "AED_levels": ("aed", "antiseizure", "antiepileptic", "anticonvulsant"),
        "urinalysis": ("urinalysis", "urine dipstick", "ua"),
        "IFE": ("immunofixation",),
        "SPEP": ("electrophoresis",),
        "ABG": ("abg", "blood gas"),
        "autoimmune_encephalitis_panel": ("autoimmune encephalitis",),
        "paraneoplastic_panel": ("paraneoplastic", "onconeural"),
        "dementia_workup": ("dementia", "reversible cause"),
    }.items()
}


def tokens(text: str) -> frozenset[str]:
    lowered = str(text).lower().replace("_", " ")
    for pattern, replacement in _PHRASES:
        lowered = re.sub(pattern, replacement, lowered)
    return frozenset(
        token for token in re.split(r"[^a-z0-9]+", lowered) if token and token not in _STOP
    )


def _like(a: str, b: str) -> bool:
    """Same token, a shared stem of four letters or more, or a numbered or plural form (IgG/IgG4)."""
    if a == b:
        return True
    short, long = sorted((a, b), key=len)
    if not long.startswith(short):
        return False
    return len(short) >= 4 or (len(short) >= 3 and re.fullmatch(r"\d+|s", long[len(short):]) is not None)


def _covers(container: frozenset[str], needed: frozenset[str]) -> bool:
    return bool(needed) and all(any(_like(n, c) for c in container) for n in needed)


def row_is(test: str, component: str) -> bool:
    """Is the stored row `test` the component `component` (or the other way round)?"""
    row, comp = tokens(test), tokens(component)
    return _covers(row, comp) or (len(row) >= 2 and _covers(comp, row))


class LabMatcher:
    """Panel-to-assay matching for one MockServer, with the library's components."""

    def __init__(self, components: Callable[[str], list[str]]):
        self._components = components

    def components(self, assay: str) -> list[str]:
        """The assay, its library row tests, and the members of a class term (`AED_levels`)."""
        return [str(assay), *self._components(str(assay)), *sorted(analyte_class_members(str(assay)))]

    def name_is(self, name: str, assay: str) -> bool:
        """The stored panel's name is the assay itself (or a recorded alias of it)."""
        name_tokens = tokens(name)
        if not name_tokens:
            return False
        own = tokens(assay)
        if own and _covers(own, name_tokens):
            return True
        return any(_covers(name_tokens, alias) for alias in _NAME_ALIASES.get(normalize_analyte(assay), ()))

    def panel_answers(self, name: str, rows: Iterable, assay: str) -> bool:
        if self.name_is(name, assay):
            return True
        if normalize_analyte(assay) in _SCOPED:
            return False
        components = self.components(assay)
        return any(row_is(row.test, component) for row in rows for component in components)


def mentions(text: str, test: str) -> bool:
    """Does free text name this row test (all of its informative tokens)?"""
    needed = tokens(test)
    return bool(needed) and _covers(tokens(text), needed)


def split_sentences(text: str) -> list[str]:
    return [part for part in re.split(r"(?<=[.;])\s+", text.strip()) if part]
