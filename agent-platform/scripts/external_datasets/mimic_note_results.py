"""Detector version 2 (7 Nov 2026). Does a MIMIC discharge summary report the *result* of a study that has no structured table?

Studies: EEG, EMG/NCS, echocardiogram, ECG, telemetry, LP narrative (and its opening pressure),
bedside respiratory function (NIF / FVC). The scope is the note after the presentation:
``Pertinent Results`` and ``Brief Hospital Course`` (``note_scope``); the HPI, exam and plan
sections are not read.

A study is *reported* when some clause names it (``KEYWORD``) and carries a result: a finding
verb or a study-specific finding term (``RESULT``), and is not only a plan, an order or a
pending study (``PLAN_ONLY`` with no specific finding). A clause is the text between sentence
boundaries around the keyword, capped at ``SPAN`` characters each side. Pasted reports that do
not repeat the study name (echo: "LVEF ...") are caught by ``STANDALONE``.

``passages`` returns the text around a broad keyword set, for a human reader to label; it is
used only to write a check sample under the PhysioNet workspace, never printed.

No record content in this file (PhysioNet DUA).
"""

from __future__ import annotations

import re

SPAN = 220
I = re.IGNORECASE

KEYWORD = {
    "eeg": r"\b(?:v|cv|c|LTM[- ]?|video[- ]?)?EEGs?\b|electroenceph|\bLTM\b|long[- ]term (?:video )?monitoring",
    "emg": r"\bEMGs?\b|\bNCSs?\b|nerve conduction|electrodiagnos|\bEMG/NCS\b",
    "echo": r"\bTTE\b|\bTEE\b|echocardiog|\becho\b|bubble study",
    "ecg": r"\bEKGs?\b|\bECGs?\b|electrocardiog",
    "telemetry": r"\btele(?:metry)?\b|\bholter\b|event monitor|zio patch|ziopatch|\bziop?\b|cardiac monitor",
    "lp": r"\bLP\b|lumbar puncture|spinal tap|\bCSF\b",
    "resp_function": r"\bNIFs?\b|negative inspiratory|\bFVCs?\b|vital capacit|\bMIPs?\b|\bVCs?\b(?=[\s:]*[-\d])",
}
GENERIC_RESULT = (r"\bshow(?:ed|s|n|ing)?\b|reveal|demonstrat|notable for|significant for|consistent with|\bc/w\b|"
                  r"concerning for|suggestive of|no evidence|\bnegative\b|\bpositive\b|\bnormal\b|\babnormal\b|"
                  r"unremarkable|\bfound\b|\bfindings?\b|\bimpression\b|\bwithout\b|\bread as\b|\bresult(?:ed|s)?\b|"
                  r"\binterpret")
RESULT = {
    "eeg": r"epileptiform|discharge|slowing|\bsharp|spike|\bPLEDs?\b|\bLPDs?\b|\bGPDs?\b|\bLRDA\b|\bGRDA\b|"
           r"burst|electrographic|non-?convulsive|\bNCSE\b|background|encephalopath|triphasic|"
           r"(?:no|any|further) (?:\w+ )?(?:seizures?|events?)|seizures? (?:were|was) (?:captured|seen|noted|recorded)|"
           r"captured|status epilepticus|ictal|periodic|rhythmic|suppress|improv|worsen",
    "emg": r"demyelinat|axonal|polyneuropath|polyradicul|conduction block|F[- ]waves?|latenc|amplitude|\bCMAP|\bSNAP|"
           r"\bAIDP\b|\bCIDP\b|guillain|\bGBS\b|myopath|neuropath|radiculopath|plexopath|denervat|fibrillation",
    "echo": r"\bL?V?EF\b|ejection fraction|\bPFO\b|foramen ovale|thromb|vegetation|shunt|septal|\bASD\b|left ventric|"
            r"left atri|\bLV\b|\bLA\b|hypokines|akines|wall motion|valv|regurg|stenosis|dilat|bubble|saline|"
            r"systolic function|diastolic|\d+ ?%",
    "ecg": r"sinus|\bNSR\b|\bSR\b|atrial fib|\bafib\b|\bA[- ]?fib\b|\bAF\b|flutter|\bQTc?\b|\bPR\b|\bST\b|"
           r"T[- ]?waves?|\bTWI|bundle branch|\b[LR]BBB\b|\baxis\b|\bLVH\b|block|brady|tachy|paced|"
           r"\bischemic changes|\bacute changes|\bQRS\b|\bectopy|\bPVCs?\b|\bPACs?\b|\d+ ?bpm|\bST[ED]s?\b|"
           r"\bQ[- ]?waves?|STEMI|infarct|isch[ae]mi|tracing|artifact|repolari|hyperkal|voltage",
    "telemetry": r"(?:no|any|without) (?:\w+ ){0,3}(?:events?|arrhythmias?|ectopy|afib|a[- ]?fib|atrial fib\w*|alarms?|pauses?|abnormalit\w*)|"
                 r"sinus|\bNSR\b|atrial fib|\bafib\b|\bA[- ]?fib\b|brady|tachy|pauses?|ectopy|\bPVCs?\b|\bNSVT\b|"
                 r"\bSVT\b|arrhythm|flutter|\bAF\b|\bPAF\b|runs? of",
    "lp": r"opening pressure|\bOP\b|\bWBCs?\b|\bcells?\b|nucleated|protein|glucose|xanthochrom|\bRBCs?\b|pleocyt|"
          r"albuminocytolog|cyto-?albumin|gram stain|cultures? (?:grew|positive|negative|no growth)|no growth|"
          r"elevated|lymphocyt|neutrophil|polys|oligoclonal|\bHSV\b|\bPCR\b|cytology|clear|cloudy|turbid|bloody",
    "resp_function": r"-?\d+(?:\.\d+)? ?(?:cm ?H2O|cmH2O|cc|ml|mL|L\b|liters?)|"
                     r"(?:NIFs?|FVCs?|vital capacit\w*|MIPs?|VCs?)\s*(?:of|was|were|is|are|remained|:|=|>|<|-)?\s*-?\d|"
                     r"(?:stable|declin\w*|improv\w*|worsen\w*|reduced|poor|adequate|normal|good|excellent) (?:NIFs?|FVCs?)|"
                     r"(?:NIFs?|FVCs?)(?:/(?:NIFs?|FVCs?))? (?:were|was|remained) (?:stable|normal|good|adequate|reassuring|wnl)|"
                     r"\bremained\b|\bimproved\b|\bstable\b|\bnormal\b|appropriate|unremarkable|deteriorat|declin(?:ed|ing)|"
                     r"reassuring|adequate|-\d{2,3}\b",
}
# The sentence only plans, orders or waits for the study.
PLAN_ONLY = (r"pending|will (?:be|need|have|obtain|follow|get|undergo)|to be (?:done|scheduled|obtained|followed|arranged)|"
             r"schedul|recommend|outpatient|\bplan\b|planned|should|consider|\bf/u\b|follow[- ]?up|to obtain|"
             r"was ordered|were ordered|order(?:ed)? for|placed on|hooked up|connected to|discontinued|was removed|"
             r"\bq\s?\d+\s?h|\bq\d|every \d+ hours|checks?\b|monitor(?:ing)? of|was (?:not|never) (?:done|performed|obtained)|"
             r"deferred|declined|refused|could not be|unable to|not performed")
# The clause reports a result from another admission, or a strip that is not the study.
NOT_THIS_STUDY = (r"at that time|previous admission|prior admission|last admission|during (?:a|her|his) prior|"
                  r"single[- ]channel|single lead|\bno (?:\w+ ){0,2}(?:was )?(?:performed|done|obtained)\b")
# Pasted results without the study name in the clause.
STANDALONE = {
    "echo": r"\bLVEF\b\s*(?:[:=]|was|is|of)?\s*[<>]?\s*\d|ejection fraction\s*(?:[:=]|was|is|of|estimated)?\s*[<>]?\s*\d|"
            r"left ventricular (?:systolic )?function is",
}
BROAD = {
    "eeg": KEYWORD["eeg"] + r"|epileptiform|electrographic|\bspikes?\b|\bsharp waves?\b",
    "emg": KEYWORD["emg"] + r"|electrophysiolog|\bF[- ]waves?|conduction block",
    "echo": KEYWORD["echo"] + r"|\bLVEF\b|ejection fraction|\bPFO\b|left ventricular",
    "ecg": KEYWORD["ecg"] + r"|\bQTc\b|\bNSR\b|normal sinus",
    "telemetry": KEYWORD["telemetry"] + r"|\bmonitor(?:ed|ing)? (?:on|for) (?:arrhythm|afib|a[- ]?fib)",
    "lp": KEYWORD["lp"] + r"|opening pressure|xanthochrom|pleocyt|albuminocytolog",
    "resp_function": KEYWORD["resp_function"] + r"|respiratory (?:function|mechanics|status)|spirometr|\bPFTs?\b",
}
BROAD = {k: re.compile(v, I) for k, v in BROAD.items()}

# Derived detectors: a refinement of a reported study.
EEG_CONTINUOUS = re.compile(r"\bcv?EEG\b|\bLTM\b|continuous|video|long[- ]term|overnight|\b24[- ]?h|\b\d+ ?hours?|"
                            r"\bv-?EEG\b|monitoring", I)
OPENING_PRESSURE = re.compile(r"(?:opening pressure|\bOP\b)[^.\n]{0,40}?\d", I)

STUDIES_BY_CONDITION = {
    "ISCH": ["ecg", "echo", "telemetry"],
    "SAH": ["ecg", "lp"],
    "SE": ["eeg", "ecg", "lp"],
    "BACT": ["lp", "eeg"],
    "GBS": ["emg", "lp", "telemetry", "resp_function"],
}
VERSION = 2
DETECTORS = ["eeg", "eeg_continuous", "emg", "echo", "ecg", "telemetry", "lp", "lp_opening_pressure", "resp_function"]

_COMPILED = {k: (re.compile(KEYWORD[k], I), re.compile(RESULT[k] + "|" + GENERIC_RESULT, I), re.compile(RESULT[k], I))
             for k in KEYWORD}
_PLAN = re.compile(PLAN_ONLY, I)
_NOT_THIS = re.compile(NOT_THIS_STUDY, I)
_STANDALONE = {k: re.compile(v, I) for k, v in STANDALONE.items()}
_BOUNDARY = re.compile(r"(?<=[.;!?])\s|\n\s*\n|\n\s*(?=[-*#•]|\d+[.)]\s|[A-Z][A-Za-z /]{2,40}:)")

_RESULTS = re.compile(r"(?im)^\s*Pertinent Results\s*:")
_COURSE = re.compile(r"(?im)^\s*(?:Brief )?Hospital Course\s*:")
_END = re.compile(r"(?im)^\s*(?:Medications on Admission|Discharge Medications|Discharge Disposition|"
                  r"Discharge Diagnos[ie]s|Transitional Issues?)\s*:")


def note_scope(text: str) -> dict[str, str]:
    """``course``: Brief Hospital Course; ``results_course``: Pertinent Results + course."""
    text = text or ""
    r, c = _RESULTS.search(text), _COURSE.search(text)
    start_c = c.end() if c else None
    end = None
    if start_c is not None:
        e = _END.search(text, start_c)
        end = e.start() if e else len(text)
    course = text[start_c:end] if start_c is not None else ""
    start_r = r.end() if r else start_c
    results_course = text[start_r:end] if start_r is not None else ""
    return {"course": course, "results_course": results_course}


def clauses(rx: re.Pattern, text: str):
    """Clause around each match of ``rx``: from the previous boundary to the next one, capped."""
    for m in rx.finditer(text):
        lo = max(0, m.start() - SPAN)
        hi = min(len(text), m.end() + SPAN)
        left = text[lo:m.start()]
        bs = list(_BOUNDARY.finditer(left))
        a = lo + bs[-1].end() if bs else lo
        right = _BOUNDARY.search(text, m.end(), hi)
        b = right.start() if right else hi
        # A header ("ECHO (date):", "EEG ___ IMPRESSION:") leaves little after the keyword: take
        # the next clause too.
        if len(re.sub(r"[\W_]+|\b(?:IMPRESSION|FINDINGS|CONCLUSIONS?|Study Date of|Date)\b", "", text[m.end():b], flags=I)) < 25:
            nxt = _BOUNDARY.search(text, b + 1, min(len(text), b + 1 + SPAN))
            b = nxt.start() if nxt else min(len(text), b + SPAN)
        yield text[a:b], m


def reported(study: str, text: str) -> bool:
    kw, any_result, specific = _COMPILED[study]
    for clause, m in clauses(kw, text):
        # Result terms must appear in the clause, outside the keyword itself.
        rest = clause.replace(m.group(0), " ", 1)
        if not any_result.search(rest) or _NOT_THIS.search(clause):
            continue
        if _PLAN.search(rest) and not specific.search(rest):
            continue
        return True
    if study in _STANDALONE and _STANDALONE[study].search(text):
        return True
    return False


def detect(name: str, text: str) -> bool:
    if name == "eeg_continuous":
        kw = _COMPILED["eeg"][0]
        return reported("eeg", text) and any(EEG_CONTINUOUS.search(c) for c, _ in clauses(kw, text))
    if name == "lp_opening_pressure":
        return bool(OPENING_PRESSURE.search(text))
    return reported(name, text)


def passages(rx: re.Pattern, text: str, pad: int = 260, cap: int = 6) -> list[str]:
    """Merged windows around matches of ``rx`` (at most ``cap``), for a human reader."""
    spans = []
    for m in rx.finditer(text):
        a, b = max(0, m.start() - pad), min(len(text), m.end() + pad)
        if spans and a <= spans[-1][1]:
            spans[-1][1] = b
        else:
            spans.append([a, b])
    return [re.sub(r"\s+", " ", text[a:b]) for a, b in spans[:cap]]
