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
from functools import lru_cache
from typing import Callable, Iterable

from .vocabulary import analyte_class_members, normalize_analyte

# Applied in order to the lower-cased text before tokenising.
_PHRASES: tuple[tuple[str, str], ...] = (
    (r"haem", "hem"), (r"\burinary\b", "urine"), (r"\b24[- ]?(?:hours?|hr|h)\b", "24h"), (r"oestr", "estr"), (r"leucocyt", "leukocyt"),
    (r"lactate dehydrogenase", "ldh"), (r"creatine (?:phospho)?kinase", "ck"), (r"\bcpk\b", "ck"),
    (r"c[- ]reactive protein", "crp"), (r"(?:erythrocyte )?sedimentation rate|\bsed rate", "esr"),
    # The urine dipstick's leukocyte esterase is not the white cell count (25 Oct 2026).
    (r"\bleukocyte esterase\b", "leukesterase"),
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
    (r"\bna\b", "sodium"), (r"\bk\b", "potassium"), (r"\bcl\b", "chloride"),
    # `Mg` is magnesium, but `mg` after a number or before a slash is the unit (25 Oct 2026: every
    # "112 mg/dL" read as citing magnesium, LABS-EVIDENCE CENTRAL).
    (r"(?<![\d.])(?<![\d.] )\bmg\b(?!\s*(?:/|per\b))", "magnesium"),
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
    # `IGRA` (25 Oct 2026): the two commercial assays are the one term.
    (r"interferon[- ]gamma release assays?|quantiferon(?:[- ]tb)?(?: gold)?(?: plus)?|\bt[- ]?spot(?:[. ]?tb)?\b", "igra"),
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
    return _tokens(str(text))


@lru_cache(maxsize=65536)
def _tokens(text: str) -> frozenset[str]:
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


like = _like


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
        return any(
            row_is(row.test, component) and specimen_compatible(row.test, name, component, assay)
            for row in rows for component in components
        )


# Specimens other than blood, by the tokens that name them (25 Oct 2026). A urinalysis row `RBC`
# or `Urine WBC` is not the blood count's red or white cell count, and a spot `Urine sodium` is not
# the serum sodium of a metabolic panel (ISCH-STR-P03 received its urinalysis from a CBC order).
_SPECIMENS: dict[str, frozenset[str]] = {
    "urine": frozenset({"urine", "urinalysis", "ua", "dipstick"}),
    "csf": frozenset({"csf", "cerebrospinal"}),
}
_BLOOD = re.compile(r"\b(?:serum|plasma|blood|whole blood|venous|arterial)\b(?! \(dipstick\))")


def _specimens_named(text: str) -> frozenset[str]:
    found = tokens(text)
    return frozenset(key for key, markers in _SPECIMENS.items() if found & markers)


def row_specimens(test: str, panel_name: str) -> frozenset[str]:
    """The non-blood specimen a stored row measures: its own words, else its panel's name.

    A row that names serum, plasma or blood is a blood test whatever panel holds it (`Serum
    osmolality` beside the urine studies).
    """
    own = _specimens_named(test)
    if own:
        return own
    if _BLOOD.search(str(test).lower()):
        return frozenset()
    return _specimens_named(panel_name)


def specimen_compatible(test: str, panel_name: str, *ordered: str) -> bool:
    """Is a stored row of a non-blood specimen answering only an order that names that specimen?"""
    stored = row_specimens(test, panel_name)
    if not stored:
        return True
    named = frozenset().union(*(_specimens_named(text) for text in ordered))
    return stored <= named


def mentions(text: str, test: str) -> bool:
    """Does free text name this row test (all of its informative tokens)?"""
    needed = tokens(test)
    return bool(needed) and _covers(tokens(text), needed)


def split_sentences(text: str) -> list[str]:
    return [part for part in re.split(r"(?<=[.;])\s+", text.strip()) if part]


# --------------------------------------------------------------------------- prose of a cut payload
#
# 25 Oct 2026. The interpretation of a stored payload was filtered by sentence: a sentence naming a
# kept test was kept whole. Most interpretations are one list sentence ("Abnormal values: WBC 11.8
# (H), sodium 134 (L), CRP 45 (H), lactate 4.1 (H)."), so an order for the blood count read out
# the CRP and lactate of panels it never named (SE M02-M07, P03, S01, S07, S09; 262 criterion
# orders across the dataset). A sentence that names tests of both kept and dropped panels is now
# cut by list item: the items separated by commas, semicolons or "and" at the top level (never
# inside parentheses). An item naming only dropped tests goes; an item naming a kept test, or no
# test at all (a closing remark), stays. Findings and panel summaries count as naming their tests
# ("thrombocytopenia" the platelets, "renal function" the creatinine: `_IMPLIED`). A shared head ("Abnormal
# values:", "Elevated ...") moves to the first item kept, a shared tail ("... within reference
# ranges") to the last, and the final "and" is restored, so the sentence still reads as written.
# An item that still names both is cut once more at "with", then inside its parentheses. A head
# naming a specimen ("Urinalysis: ...") scopes its items to that specimen, and goes with them when
# the order kept no row of it.

TestRef = tuple[str, str]  # (row test, panel name)

_HEAD = re.compile(
    r"^(?:[^:\d()]{1,40}:\s+|(?:(?:mildly|markedly|slightly)\s+)?"
    r"(?:elevated|raised|high|low|abnormal|increased|decreased|reduced)\s+(?=\S))",
    re.IGNORECASE,
)
_TAIL = re.compile(
    r"\s+((?:(?:are|were|is|was|all|both|otherwise)\s+)?(?:(?:mildly|markedly|slightly|all)\s+)?"
    r"(?:within|elevated|raised|normal|negative|positive|unremarkable|not detected|in range|low|high)\b[^()]*)$",
    re.IGNORECASE,
)
_SEPARATOR = re.compile(r",\s+and\s+|;\s+|,\s+|\s+and\s+")
_WITH = re.compile(r"\s+with\s+")
_AND = re.compile(r"(?:,\s+)?and\s+|\s+and\s+")
_SPECIMEN_WORDS = frozenset().union(*_SPECIMENS.values())
_QUALIFIERS = frozenset({"complement", "measured", "intact"})

# Findings and panel summaries that name a result without naming its test: "pyuria" is the urine
# white cells, "thrombocytopenia" the platelets, "renal function" the creatinine. Read in prose
# only (never in panel matching), so "Proteinuria 2+ with microscopic hematuria" goes with the
# urinalysis an order did not name.
_IMPLIED: tuple[tuple[re.Pattern, str], ...] = tuple((re.compile(pattern, re.IGNORECASE), words) for pattern, words in (
    (r"\bproteinuria\b", "urine protein"), (r"\bha?ematuria\b", "urine rbc"), (r"\bpyuria\b", "urine wbc"),
    (r"\bleu[ck]ocyto(?:sis|penia)\b|\bneutrophilia\b|\bneutropenia\b", "wbc neutrophils"),
    (r"\blympho(?:penia|cytosis)\b", "lymphocytes"), (r"\bbanda?emia\b", "bands"),
    (r"\bana?emi(?:a|c)\b", "hemoglobin"), (r"\bthrombocyto(?:penia|sis)\b", "platelets"),
    (r"\bhyp(?:er|o)glyc(?:a)?emi(?:a|c)\b", "glucose"), (r"\bhyp(?:er|o)natr(?:a)?emi(?:a|c)\b", "sodium"),
    (r"\bhyp(?:er|o)kal(?:a)?emi(?:a|c)\b", "potassium"), (r"\bhyp(?:er|o)magnes(?:a)?emi(?:a|c)\b", "magnesium"),
    (r"\bhyp(?:er|o)calc(?:a)?emi(?:a|c)\b", "calcium"), (r"\bhyp(?:er|o)phosphat(?:a)?emi(?:a|c)\b", "phosphate"),
    (r"\bhyperammon(?:a)?emi(?:a|c)\b", "ammonia"), (r"\bhyperlactat(?:a)?emia\b|\blactic acidosis\b", "lactate"),
    (r"\bhypoalbumin(?:a)?emia\b", "albumin"), (r"\bhyperbilirubin(?:a)?emia\b", "bilirubin"),
    (r"\brenal (?:function|indices|tests)\b", "creatinine bun"),
    (r"\b(?:hepatic|liver) (?:function|tests|enzymes|indices|panel)\b|\btransaminases\b", "alt ast"),
    (r"\bthyroid function\b", "tsh"), (r"\binflammatory markers\b", "crp esr"),
    (r"\belectrolytes\b", "sodium potassium"), (r"\bcoagulation\b|\bclotting\b", "inr pt"),
    (r"\bblood count\b|\bcbc\b|\bfbc\b", "wbc hemoglobin platelets"),
    (r"\bmetabolic panel\b|\bbmp\b|\bcmp\b", "sodium creatinine glucose"),
    (r"\blipids?\b|\blipid (?:panel|profile)\b", "ldl"),
)
)


# "renal and hepatic function": two adjectives sharing one noun are one list item.
_ORGAN = r"(renal|kidney|hepatic|liver|thyroid|cardiac|pancreatic|adrenal|muscle|bone)"
_SHARED_NOUN = re.compile(
    rf"{_ORGAN} and {_ORGAN} (function|functions|indices|tests|panels?|enzymes|markers)\b", re.IGNORECASE)


def _merge_shared_nouns(items: list[tuple[str, str]]) -> list[tuple[str, str]]:
    merged: list[tuple[str, str]] = []
    for sep, item in items:
        if (merged and _AND.fullmatch(sep) and re.fullmatch(r"[A-Za-z]+", merged[-1][1].strip())
                and _SHARED_NOUN.match(f"{merged[-1][1].strip()} and {item.strip()}")):
            merged[-1] = (merged[-1][0], f"{merged[-1][1]}{sep}{item}")
            continue
        merged.append((sep, item))
    return merged


def _implied(text: str) -> str:
    text = _SHARED_NOUN.sub(lambda m: f"{m[1]} {m[3]} and {m[2]} {m[3]}", text)
    extra = [words for pattern, words in _IMPLIED if pattern.search(text)]
    return f"{text} {' '.join(extra)}" if extra else text


def _split_top(text: str, pattern: re.Pattern) -> list[tuple[str, str]]:
    """`[(separator, item), ...]` at parenthesis depth 0; the first separator is ``""``."""
    out: list[tuple[str, str]] = []
    depth, start, sep, i = 0, 0, "", 0
    while i < len(text):
        ch = text[i]
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        elif depth == 0 and i > start:
            match = pattern.match(text, i)
            if match and match.end() > match.start():
                out.append((sep, text[start:i]))
                sep, start, i = match.group(0), match.end(), match.end()
                continue
        i += 1
    out.append((sep, text[start:]))
    return [(s, item) for s, item in out if item.strip()] or [("", text)]


def _capitalise(text: str) -> str:
    first = re.match(r"[^\s,;:()]+", text)
    word = first.group(0) if first else ""
    return text[0].upper() + text[1:] if word.isalpha() and word.islower() else text


class _ProseCut:
    """Cuts the prose of one payload to the rows an order kept (see the block comment)."""

    def __init__(self, kept: list[TestRef], dropped: list[TestRef]):
        self.kept, self.dropped = list(kept), list(dropped)
        # Analytes measured in blood somewhere in the payload: an item naming no specimen ("sodium
        # 122") means the blood test, never the urine sodium; one with no blood namesake ("nitrite
        # positive") names the urine row by its analyte alone.
        self.blood = [tokens(t) for t, p in self.kept + self.dropped if not row_specimens(t, p)]

    def _analyte(self, test: str, panel: str) -> frozenset[str]:
        """The tokens prose uses for a row: its name without a parenthetical or a qualifier
        ("C3" for `Complement C3`, "prolactin" for `Prolactin (emergency department sample ...)`),
        and without its specimen word when no blood row shares the analyte."""
        full = tokens(test)
        core = tokens(re.sub(r"\([^()]*\)", " ", str(test))) - _QUALIFIERS or full
        if not row_specimens(test, panel):
            return core
        bare = core - _SPECIMEN_WORDS
        if not bare or any(_covers(blood, bare) for blood in self.blood):
            return full
        return bare

    def names(self, text: str, refs: list[TestRef], context: str = "") -> bool:
        """Does the text name one of these row tests, in the same specimen?

        Read item by item (and either side of "with"): an item that names a specimen (`urine osmolality 420`) names only that
        specimen's rows, so the serum osmolality of a kept panel does not make it a kept item, and
        "urinalysis" at the end of a list does not hide the serum tests before it. A specimen named
        in `context` (the list's head) holds for every item that names none. A text naming no
        specimen is also read whole, for a row test whose name spans several items ("Prolactin
        (sample 3 months ago, drawn 22 minutes after ...)").
        """
        outer = _specimens_named(context)
        parts = [part for _, item in _merge_shared_nouns(_split_top(text, _SEPARATOR))
                 for _, part in _split_top(item, _WITH)]
        for item in parts:
            item = _implied(item)
            named = _specimens_named(item) or outer
            found = tokens(item)
            for test, panel in refs:
                where = row_specimens(test, panel)
                if named and where != named:
                    continue
                if _covers(found, tokens(test)) or _covers(found, self._analyte(test, panel)):
                    return True
        if not (_specimens_named(text) or outer):
            return any(mentions(text, test) for test, _ in refs)
        return False

    def only_dropped(self, text: str, context: str = "") -> bool:
        return self.names(text, self.dropped, context) and not self.names(text, self.kept, context)

    def mixed(self, item: str, context: str) -> str:
        """One list item naming kept and dropped tests: cut at "with", then inside parentheses."""
        shared = _SHARED_NOUN.fullmatch(item)
        if shared:  # "renal and hepatic function": keep the halves the order kept
            first, second, noun = shared.groups()
            halves = [word for word in (first, second) if not self.only_dropped(f"{word} {noun}", context)]
            return " and ".join(halves) + f" {noun}" if halves else ""
        parts = _split_top(item, _WITH)
        if len(parts) >= 2:
            parts = [(sep, part) for sep, part in parts if not self.only_dropped(part, context)]
            if not parts:
                return ""
            item = parts[0][1] + "".join(sep + part for sep, part in parts[1:])
        if not self.names(item, self.dropped, context):
            return item

        def inside(match: re.Match) -> str:
            cut = self.items(match.group(1), context)
            return f" ({cut})" if cut else ""

        return re.sub(r"\s*\(([^()]*,[^()]*)\)", inside, item)

    def items(self, body: str, context: str = "") -> str:
        """The list items of `body` that do not name only dropped tests."""
        head = ""
        match = _HEAD.match(body)
        if match:
            head, body = match.group(0), body[match.end():]
            if ":" not in head and len(_split_top(body, _SEPARATOR)) < 2:
                head, body = "", head + body  # one item: "Low bicarbonate (20) with raised lactate (2.8)"
        context = f"{context} {head}".strip()
        specimen = _specimens_named(head)
        head_dropped = bool(head) and (self.only_dropped(head) or bool(specimen) and not any(
            row_specimens(t, p) == specimen for t, p in self.kept))
        items = _merge_shared_nouns(_split_top(body, _SEPARATOR))
        tail = ""
        # A tail is shared by a list joined with a final "and", or by a list of names without values
        # ("Electrolytes, renal and hepatic function, TSH normal"); otherwise it is its own item's.
        last = _TAIL.search(items[-1][1]) if len(items) >= 2 else None
        if last and (_AND.fullmatch(items[-1][0]) or not re.search(r"\d", body[: -len(last.group(0))])):
            tail = last.group(0)
            items[-1] = (items[-1][0], items[-1][1][: last.start()])
        keep: list[tuple[str, str]] = []
        changed = False
        for sep, item in items:
            has_kept = self.names(item, self.kept, context)
            has_dropped = self.names(item, self.dropped, context)
            if (has_dropped or head_dropped) and not has_kept:
                changed = True
                continue
            if has_dropped:
                cut = self.mixed(item, context)
                changed = changed or cut != item
                if not cut:
                    continue
                item = cut
            keep.append((sep, item))
        if not keep:
            return ""
        if not changed:
            return head + body
        if ((_AND.fullmatch(items[-1][0]) or _SHARED_NOUN.match(items[-1][1].strip())) and len(keep) >= 2 and keep[-1][1] != items[-1][1]
                and not _AND.fullmatch(keep[-1][0]) and " and " not in keep[-1][1]):
            keep[-1] = (" and ", keep[-1][1])  # the last item went: the new last one takes the "and"
        if len(keep) == 1 and " and " not in keep[0][1]:
            tail = re.sub(r"^(\s+)are\b", r"\1is", tail)  # "Troponin and TSH are normal" -> "TSH is normal"
        if len(keep) == 2 and re.fullmatch(r",\s+and\s+", keep[1][0]):
            keep[1] = (" and ", keep[1][1])  # two items left: no serial comma
        return head + keep[0][1] + "".join(sep + item for sep, item in keep[1:]) + tail


def cut_prose(text: str, kept: list[TestRef], dropped: list[TestRef]) -> str:
    """One sentence (or summary line) of a stored payload, cut to the tests the order kept.

    Unchanged when it names no dropped test; ``""`` when it names dropped tests and no kept one;
    otherwise cut by list item (see the block comment above).
    """
    cutter = _ProseCut(kept, dropped)
    stripped = text.rstrip()
    end = stripped[-1] if stripped and stripped[-1] in ".;" else ""
    body = stripped[:-1] if end else stripped
    if not cutter.names(body, cutter.dropped) and not _HEAD.match(body):
        return text
    if cutter.only_dropped(body):
        return ""
    cut = cutter.items(body).strip()
    if cut == body.strip():
        return text
    if not cut:
        return ""
    if body[:1].isupper():
        cut = _capitalise(cut)
    return cut + end
